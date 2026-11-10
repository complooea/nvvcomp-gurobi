"""Private, solver-independent interpretation of the declared MVP grammar."""

import math
import re
from dataclasses import dataclass

import numpy as np
import onnx
from onnx import TensorProto, numpy_helper


class Unsupported(ValueError):
    pass


@dataclass(frozen=True)
class Comparison:
    left: str
    operator: str
    right: str | float


@dataclass
class Property:
    lower: list[float]
    upper: list[float]
    comparisons: list[Comparison]
    replay_text: str


def interpret_property(text: str, num_inputs: int, num_outputs: int) -> Property:
    # Complete statements, not a permissive search for recognizable fragments.
    text = re.sub(r";[^\n]*", "", text)
    declarations: set[str] = set()
    comparisons = []
    replay_statements = []
    lower, upper = [-math.inf] * num_inputs, [math.inf] * num_inputs
    expected = {f"X_{i}" for i in range(num_inputs)} | {
        f"Y_{i}" for i in range(num_outputs)
    }
    tokens = re.findall(r"\(|\)|[^\s()]+", text)
    index = 0
    while index < len(tokens):
        start, depth = index, 0
        while index < len(tokens):
            token = tokens[index]
            depth += (token == "(") - (token == ")")
            index += 1
            if depth <= 0:
                break
        statement = " ".join(tokens[start:index])
        declaration = re.fullmatch(
            r"\( declare-const ([XY]_(?:0|[1-9][0-9]*)) Real \)", statement
        )
        assertion = re.fullmatch(r"\( assert \( (<=|>=) (\S+) (\S+) \) \)", statement)
        if depth != 0:
            raise Unsupported("Unbalanced VNN-LIB parentheses")
        if declaration:
            name = declaration[1]
            if name not in expected or name in declarations:
                raise Unsupported(f"Duplicate or out-of-range declaration: {name}")
            declarations.add(name)
            replay_statements.append(f"(declare-const {name} Real)")
        elif assertion:
            operator, left, right = assertion.groups()
            if left not in declarations:
                raise Unsupported(f"Undeclared variable or unsupported operand: {left}")
            if right in declarations:
                if (
                    not left.startswith("Y_")
                    or not right.startswith("Y_")
                    or left == right
                ):
                    raise Unsupported(
                        "Only distinct output-variable comparisons are supported"
                    )
                value: str | float = right
            else:
                if not re.fullmatch(
                    r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", right
                ):
                    raise Unsupported(f"Unsupported scalar: {right}")
                value = float(right)
                if not math.isfinite(value) or abs(value) >= 1e100:
                    raise Unsupported(
                        "Scalar must be finite and smaller than Gurobi infinity"
                    )
            if left.startswith("X_"):
                assert isinstance(value, float)
                variable = int(left[2:])
                if operator == ">=":
                    lower[variable] = max(lower[variable], value)
                else:
                    upper[variable] = min(upper[variable], value)
            else:
                comparisons.append(Comparison(left, operator, value))
            replay_statements.append(f"(assert ({operator} {left} {right}))")
        else:
            raise Unsupported(f"Unsupported VNN-LIB statement: {statement}")
    if declarations != expected:
        raise Unsupported("Declare exactly the model's contiguous X and Y variables")
    if not all(math.isfinite(v) for v in lower + upper):
        raise Unsupported("Every input requires finite lower and upper box bounds")
    if not comparisons:
        raise Unsupported("At least one asserted output comparison is required")
    return Property(lower, upper, comparisons, "\n".join(replay_statements) + "\n")


def interpret_network(content: bytes) -> tuple[onnx.ModelProto, int, int]:
    model = onnx.load_model_from_string(content)
    graph = model.graph
    if (
        model.functions
        or graph.sparse_initializer
        or len(graph.input) != 1
        or len(graph.output) != 1
    ):
        raise Unsupported("Expected one dense sequential input/output graph")
    if (
        len(model.opset_import) != 1
        or model.opset_import[0].domain not in ("", "ai.onnx")
        or model.opset_import[0].version not in (9, *range(13, 22))
    ):
        raise Unsupported("Supported ONNX default opsets are 9 and 13 through 21")
    sizes = []
    for value in [graph.input[0], graph.output[0]]:
        tensor = value.type.tensor_type
        shape = [dim.dim_value for dim in tensor.shape.dim]
        if (
            tensor.elem_type != TensorProto.FLOAT
            or len(shape) != 2
            or shape[0] != 1
            or shape[1] < 1
        ):
            raise Unsupported("Expected FLOAT32 tensors of static shape [1, width]")
        sizes.append(shape[1])
    constants = {}
    for initializer in graph.initializer:
        if (
            initializer.data_location == TensorProto.EXTERNAL
            or initializer.external_data
        ):
            raise Unsupported("External ONNX tensor data is not supported")
        if initializer.name in constants or initializer.data_type != TensorProto.FLOAT:
            raise Unsupported("Expected unique FLOAT32 initializers")
        array = numpy_helper.to_array(initializer)
        if not np.isfinite(array).all():
            raise Unsupported("Non-finite network constants")
        constants[initializer.name] = array
    previous, width = graph.input[0].name, sizes[0]
    seen = set(constants) | {previous}
    last_op = None
    for node in graph.node:
        if (
            node.domain not in ("", "ai.onnx")
            or len(node.output) != 1
            or node.output[0] in seen
        ):
            raise Unsupported(
                "Expected a standard sequential graph with unique tensors"
            )
        if not node.input or node.input[0] != previous:
            raise Unsupported("Non-sequential or disconnected ONNX graph")
        attributes = {
            a.name: onnx.helper.get_attribute_value(a) for a in node.attribute
        }
        if len(attributes) != len(node.attribute):
            raise Unsupported("Duplicate ONNX attributes")
        if node.op_type == "Gemm":
            if (
                set(attributes) - {"alpha", "beta", "transA", "transB"}
                or attributes.get("alpha", 1) != 1
                or attributes.get("beta", 1) != 1
                or attributes.get("transA", 0) != 0
                or attributes.get("transB", 0) not in (0, 1)
            ):
                raise Unsupported(
                    "Gemm requires alpha=beta=1, transA=0 and transB in {0,1}"
                )
            if len(node.input) != 3 or any(
                name not in constants for name in node.input[1:]
            ):
                raise Unsupported("Gemm requires initializer weights and bias")
            weights, bias = (constants[name] for name in node.input[1:])
            if attributes.get("transB", 0):
                weights = weights.T
            if weights.ndim != 2 or weights.shape[0] != width or weights.shape[1] < 1:
                raise Unsupported(
                    "Gemm weight dimensions do not match the sequential tensor"
                )
            width = weights.shape[1]
            if bias.shape not in ((width,), (1, width)):
                raise Unsupported("Gemm bias must have shape [width] or [1, width]")
        elif node.op_type == "Relu":
            if last_op != "Gemm" or len(node.input) != 1 or attributes:
                raise Unsupported(
                    "Relu must immediately follow a Gemm without attributes"
                )
        else:
            raise Unsupported(f"Unsupported ONNX operation: {node.op_type}")
        last_op = node.op_type
        previous = node.output[0]
        seen.add(previous)
    if last_op != "Gemm" or previous != graph.output[0].name or width != sizes[1]:
        raise Unsupported("Sequential network must end in its declared affine output")
    onnx.checker.check_model(model, full_check=True)
    return model, sizes[0], sizes[1]
