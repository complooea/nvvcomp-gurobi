"""Private, solver-independent interpretation of the declared MVP grammar."""

import math
import re
from dataclasses import dataclass

import numpy as np
import onnx
from onnx import TensorProto, numpy_helper

_COMPARISON = re.compile(r"\( (<=|>=) ([^\s()]+) ([^\s()]+) \)")
_ASSERTION = re.compile(rf"\( assert {_COMPARISON.pattern} \)")
_CONJUNCTION = re.compile(rf"\( and (?:{_COMPARISON.pattern} )+\)")
_DISJUNCTION = re.compile(rf"\( assert \( or (?:{_CONJUNCTION.pattern} )+\) \)")


class Unsupported(ValueError):
    pass


def uses_native_construction(model) -> bool:
    return any(n.op_type in ("Sigmoid", "Reshape") for n in model.graph.node)


def network_formulation(model) -> str:
    if uses_native_construction(model):
        return "native Gurobi affine/max/logistic (FuncNonlinear=1); C-order reshape; constant-objective feasibility"
    return "gurobi-machinelearning ONNX; constant-objective feasibility"


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
    disjunctions: list[list[list[Comparison]]]
    replay_text: str


def interpret_property(text: str, num_inputs: int, num_outputs: int) -> Property:
    # Complete statements, not a permissive search for recognizable fragments.
    text = re.sub(r";[^\n]*", "", text)
    declarations: set[str] = set()
    comparisons = []
    disjunctions = []
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
        assertion = _ASSERTION.fullmatch(statement)
        if depth != 0:
            raise Unsupported("Unbalanced VNN-LIB parentheses")
        if declaration:
            name = declaration[1]
            if name not in expected or name in declarations:
                raise Unsupported(f"Duplicate or out-of-range declaration: {name}")
            declarations.add(name)
            replay_statements.append(f"(declare-const {name} Real)")
        elif assertion or _DISJUNCTION.fullmatch(statement):
            # Replay accepts this same narrow DNF grammar. Keep the original
            # assertion order and scalar spellings, normalizing whitespace only.
            replay_statements.append(statement.replace("( ", "(").replace(" )", ")"))
            if assertion:
                clauses = [[assertion.groups()]]
            else:
                clauses = [
                    _COMPARISON.findall(clause.group(0))
                    for clause in _CONJUNCTION.finditer(statement)
                ]
            alternatives = []
            for clause in clauses:
                branch = []
                for operator, left, right in clause:
                    comparison = _interpret_comparison(
                        operator, left, right, declarations
                    )
                    if left.startswith("X_"):
                        if not assertion:
                            raise Unsupported(
                                "Disjunctions support output comparisons only"
                            )
                        value = comparison.right
                        assert isinstance(value, float)
                        variable = int(left[2:])
                        if operator == ">=":
                            lower[variable] = max(lower[variable], value)
                        else:
                            upper[variable] = min(upper[variable], value)
                    else:
                        branch.append(comparison)
                alternatives.append(branch)
            if assertion:
                comparisons.extend(alternatives[0])
            else:
                disjunctions.append(alternatives)
        else:
            raise Unsupported(f"Unsupported VNN-LIB statement: {statement}")
    if declarations != expected:
        raise Unsupported("Declare exactly the model's contiguous X and Y variables")
    if not all(math.isfinite(v) for v in lower + upper):
        raise Unsupported("Every input requires finite lower and upper box bounds")
    if not comparisons and not disjunctions:
        raise Unsupported("At least one asserted output comparison is required")
    return Property(
        lower, upper, comparisons, disjunctions, "\n".join(replay_statements) + "\n"
    )


def _interpret_comparison(operator, left, right, declarations) -> Comparison:
    if left not in declarations:
        raise Unsupported(f"Undeclared variable or unsupported operand: {left}")
    if right in declarations:
        if not left.startswith("Y_") or not right.startswith("Y_") or left == right:
            raise Unsupported("Only distinct output-variable comparisons are supported")
        value: str | float = right
    else:
        if not re.fullmatch(
            r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", right
        ):
            raise Unsupported(f"Unsupported scalar: {right}")
        value = float(right)
        if not math.isfinite(value) or abs(value) >= 1e100:
            raise Unsupported("Scalar must be finite and smaller than Gurobi infinity")
    return Comparison(left, operator, value)


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
        not model.opset_import
        or any(
            op.domain not in ("", "ai.onnx")
            or op.version not in (9, 11, *range(13, 22))
            for op in model.opset_import
        )
        or len({op.version for op in model.opset_import}) != 1
    ):
        raise Unsupported(
            "Expected compatible default-domain opsets: 9, 11, or 13 through 21"
        )
    sizes = []
    for value in [graph.input[0], graph.output[0]]:
        tensor = value.type.tensor_type
        shape = [dim.dim_value for dim in tensor.shape.dim]
        if (
            tensor.elem_type != TensorProto.FLOAT
            or len(shape) < 2
            or shape[0] != 1
            or any(d < 1 for d in shape)
        ):
            raise Unsupported("Expected static FLOAT32 tensors with batch size one")
        sizes.append(math.prod(shape))
    constants = {}
    for initializer in graph.initializer:
        if (
            initializer.data_location == TensorProto.EXTERNAL
            or initializer.external_data
        ):
            raise Unsupported("External ONNX tensor data is not supported")
        if initializer.name in constants or initializer.data_type not in (
            TensorProto.FLOAT,
            TensorProto.INT64,
        ):
            raise Unsupported("Expected unique FLOAT32 or INT64 initializers")
        array = numpy_helper.to_array(initializer)
        if not np.isfinite(array).all():
            raise Unsupported("Non-finite network constants")
        constants[initializer.name] = array
    previous, width = graph.input[0].name, sizes[0]
    shape = tuple(d.dim_value for d in graph.input[0].type.tensor_type.shape.dim)
    seen = set(constants) | {previous}
    last_op = None
    last_computation = None
    for node in graph.node:
        if (
            node.domain not in ("", "ai.onnx")
            or len(node.output) != 1
            or node.output[0] in seen
        ):
            raise Unsupported(
                "Expected a standard sequential graph with unique tensors"
            )
        attributes = {
            a.name: onnx.helper.get_attribute_value(a) for a in node.attribute
        }
        if len(attributes) != len(node.attribute):
            raise Unsupported("Duplicate ONNX attributes")
        if node.op_type == "Constant":
            value = attributes.get("value")
            if (
                node.input
                or set(attributes) != {"value"}
                or not isinstance(value, onnx.TensorProto)
                or value.data_type != TensorProto.INT64
                or value.external_data
                or value.data_location == TensorProto.EXTERNAL
            ):
                raise Unsupported(
                    "Constant supports inline INT64 reshape metadata only"
                )
            constants[node.output[0]] = numpy_helper.to_array(value)
            seen.add(node.output[0])
            continue
        if not node.input or node.input[0] != previous:
            raise Unsupported("Non-sequential or disconnected ONNX graph")
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
            if (
                shape != (1, width)
                or weights.dtype != np.float32
                or bias.dtype != np.float32
            ):
                raise Unsupported("Gemm requires rank-two data and FLOAT32 parameters")
            if attributes.get("transB", 0):
                weights = weights.T
            if weights.ndim != 2 or weights.shape[0] != width or weights.shape[1] < 1:
                raise Unsupported(
                    "Gemm weight dimensions do not match the sequential tensor"
                )
            width = weights.shape[1]
            if bias.shape not in ((width,), (1, width)):
                raise Unsupported("Gemm bias must have shape [width] or [1, width]")
            shape = (1, width)
        elif node.op_type in ("Relu", "Sigmoid"):
            if last_op != "Gemm" or len(node.input) != 1 or attributes:
                raise Unsupported(
                    "Activation must immediately follow a Gemm without attributes"
                )
        elif node.op_type == "Reshape":
            if len(node.input) != 2 or attributes or node.input[1] not in constants:
                raise Unsupported(
                    "Reshape requires constant integer shape without attributes"
                )
            target = constants[node.input[1]]
            if target.dtype != np.int64 or target.ndim != 1 or not target.size:
                raise Unsupported("Reshape shape must be a nonempty INT64 vector")
            dims = [int(d) for d in target]
            if dims.count(-1) > 1 or any(d < -1 for d in dims):
                raise Unsupported("Invalid inferred reshape dimensions")
            for i, dim in enumerate(dims):
                if dim == 0:
                    if i >= len(shape):
                        raise Unsupported("Reshape zero dimension outside input rank")
                    dims[i] = shape[i]
            known = math.prod(d for d in dims if d != -1)
            if -1 in dims:
                if known == 0 or width % known:
                    raise Unsupported("Reshape element count differs")
                dims[dims.index(-1)] = width // known
            if math.prod(dims) != width or any(d < 1 for d in dims):
                raise Unsupported("Reshape element count differs")
            shape = tuple(dims)
        else:
            raise Unsupported(f"Unsupported ONNX operation: {node.op_type}")
        last_op = node.op_type
        if node.op_type != "Reshape":
            last_computation = node.op_type
        previous = node.output[0]
        seen.add(previous)
    if (
        last_computation != "Gemm"
        or previous != graph.output[0].name
        or shape
        != tuple(d.dim_value for d in graph.output[0].type.tensor_type.shape.dim)
    ):
        raise Unsupported("Sequential network must end in its declared affine output")
    onnx.checker.check_model(model, full_check=True)
    return model, sizes[0], sizes[1]
