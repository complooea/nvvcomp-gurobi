"""Private, solver-independent interpretation of the declared verification grammar."""

import math
import re
from dataclasses import dataclass

import onnx
from onnx import TensorProto

from ._tensor_dag import Unsupported, lower

_COMPARISON = re.compile(r"\( (<=|>=) ([^\s()]+) ([^\s()]+) \)")
_ASSERTION = re.compile(rf"\( assert {_COMPARISON.pattern} \)")
_CONJUNCTION = re.compile(rf"\( and (?:{_COMPARISON.pattern} )+\)")
_DISJUNCTION = re.compile(rf"\( assert \( or (?:{_CONJUNCTION.pattern} )+\) \)")


def uses_native_construction(model) -> bool:
    previous = model.graph.input[0].name
    last = None
    for node in model.graph.node:
        if (
            node.op_type not in ("Gemm", "Relu")
            or not node.input
            or node.input[0] != previous
            or (node.op_type == "Relu" and last != "Gemm")
        ):
            return True
        previous, last = node.output[0], node.op_type
    return last != "Gemm" or previous != model.graph.output[0].name


def network_formulation(model) -> str:
    if uses_native_construction(model):
        operations = sorted({r.operation for r in lower(model).relations})
        nonlinear = (
            "; nonlinear functions FuncNonlinear=1"
            if set(operations) & {"Sigmoid", "Sin", "Cos"}
            else ""
        )
        return (
            f"native Gurobi shared tensor DAG; relations: {', '.join(operations)}"
            f"{nonlinear}; quadratic squares/products; radians; C-order static tensor views; "
            "constant-only shape/Boolean folding; constant-objective feasibility"
        )
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
        raise Unsupported("Expected one dense input/output tensor DAG")
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
    onnx.checker.check_model(model, full_check=True)
    try:
        lower(model)
    except (ValueError, IndexError, TypeError, OverflowError) as exc:
        raise Unsupported(str(exc)) from exc
    return model, sizes[0], sizes[1]
