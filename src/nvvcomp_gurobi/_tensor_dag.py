"""Solver-independent lowering of the selected static ONNX tensor DAG.

Tensor views keep scalar references, so a shared intermediate is encoded once.
Only numeric tensors are constants; symbolic values never participate in shape
or Boolean folding. This is deliberately not a general ONNX interpreter.
"""

import math
from dataclasses import dataclass

import numpy as np
from onnx import TensorProto, helper, numpy_helper


class Unsupported(ValueError):
    pass


@dataclass(frozen=True)
class Ref:
    index: int


@dataclass
class Relation:
    operation: str
    arguments: tuple
    coefficients: tuple = ()
    bias: float = 0.0


@dataclass
class TensorDAG:
    inputs: int
    relations: list[Relation]
    output: np.ndarray
    shapes: dict[str, tuple[int, ...]]


def _constant(array):
    return array.dtype != object


def _integer_vector(array):
    if not _constant(array) or array.dtype != np.int64 or array.ndim != 1:
        raise Unsupported("Expected a constant INT64 shape/index vector")
    return [int(x) for x in array]


def _axis(axis, rank):
    if not -rank <= axis < rank:
        raise Unsupported("Tensor axis outside rank")
    return axis % rank


def _array(tensor):
    if tensor.external_data or tensor.data_location == TensorProto.EXTERNAL:
        raise Unsupported("External ONNX tensor data is not supported")
    if tensor.data_type not in (TensorProto.FLOAT, TensorProto.INT64, TensorProto.BOOL):
        raise Unsupported("Expected FLOAT32, INT64, or BOOL constants")
    result = numpy_helper.to_array(tensor)
    if not np.isfinite(result).all():
        raise Unsupported("Non-finite network constants")
    return result


def lower(model) -> TensorDAG:
    """Validate and lower the whole graph, without output-cone pruning."""
    graph = model.graph
    shape = tuple(d.dim_value for d in graph.input[0].type.tensor_type.shape.dim)
    count = math.prod(shape)
    relations: list[Relation] = []

    def emit(operation, arguments, coefficients=(), bias=0.0):
        ref = Ref(count + len(relations))
        relations.append(
            Relation(operation, tuple(arguments), tuple(coefficients), bias)
        )
        return ref

    def affine(terms, bias=0.0):
        args, coefficients = [], []
        for coefficient, value in terms:
            coefficient = float(coefficient)
            if coefficient == 0:
                continue
            if isinstance(value, Ref):
                args.append(value)
                coefficients.append(coefficient)
            else:
                bias += coefficient * float(value)
        if not args:
            return float(bias)
        if len(args) == 1 and coefficients == [1.0] and bias == 0:
            return args[0]
        return emit("Affine", args, coefficients, bias)

    def elementwise(operation, arrays):
        if any(a.dtype not in (np.dtype("float32"), np.dtype("O")) for a in arrays):
            # Integer multiplication is needed by the constant shape scaffold.
            if not all(_constant(a) for a in arrays) or operation != "Mul":
                raise Unsupported("Arithmetic data must be FLOAT32")
        arrays = np.broadcast_arrays(*arrays)
        if all(_constant(a) for a in arrays):
            functions = {
                "Add": np.add,
                "Sub": np.subtract,
                "Mul": np.multiply,
                "Neg": np.negative,
                "Pow": np.power,
                "Sin": np.sin,
                "Cos": np.cos,
                "Relu": lambda x: np.maximum(x, 0),
                "Sigmoid": lambda x: 1 / (1 + np.exp(-x)),
            }
            return np.asarray(functions[operation](*arrays))
        result = np.empty(arrays[0].shape, dtype=object)
        for index in np.ndindex(result.shape):
            values = [a[index] for a in arrays]
            if operation in ("Add", "Sub"):
                value = affine(
                    zip((1, 1 if operation == "Add" else -1), values, strict=True)
                )
            elif operation == "Neg":
                value = affine([(-1, values[0])])
            elif operation == "Mul" and any(not isinstance(v, Ref) for v in values):
                a, b = values
                value = affine([(b, a)] if isinstance(a, Ref) else [(a, b)])
            elif operation == "Pow":
                value = emit("Square", [values[0]])
            else:
                value = emit(operation, values)
            result[index] = value
        return result

    def matmul(a, b, bias=None):
        if a.ndim != 2 or b.ndim != 2 or a.shape[1] != b.shape[0]:
            raise Unsupported("MatMul requires compatible rank-two tensors")
        if not _constant(a) and not _constant(b):
            raise Unsupported("MatMul requires constant weights")
        if any(v.dtype not in (np.dtype("float32"), np.dtype("O")) for v in (a, b)):
            raise Unsupported("MatMul requires FLOAT32 data and weights")
        output_shape = (a.shape[0], b.shape[1])
        if bias is not None:
            bias = np.broadcast_to(bias, output_shape)
        if _constant(a) and _constant(b):
            result = a @ b
            return result if bias is None else result + bias
        result = np.empty(output_shape, dtype=object)
        for i, j in np.ndindex(output_shape):
            if _constant(b):
                terms = ((b[k, j], a[i, k]) for k in np.flatnonzero(b[:, j]))
            else:
                terms = ((a[i, k], b[k, j]) for k in np.flatnonzero(a[i, :]))
            result[i, j] = affine(terms, 0.0 if bias is None else float(bias[i, j]))
        return result

    tensors = {
        graph.input[0].name: np.array([Ref(i) for i in range(count)], object).reshape(
            shape
        )
    }
    for tensor in graph.initializer:
        if tensor.name in tensors:
            raise Unsupported("Duplicate network tensor")
        tensors[tensor.name] = _array(tensor)
    for node in graph.node:
        if (
            node.domain not in ("", "ai.onnx")
            or len(node.output) != 1
            or not node.output[0]
            or node.output[0] in tensors
        ):
            raise Unsupported(
                "Expected default-domain nodes with unique single outputs"
            )
        if any(n not in tensors for n in node.input):
            raise Unsupported("Missing, optional, or non-topological tensor input")
        attrs = {a.name: helper.get_attribute_value(a) for a in node.attribute}
        if len(attrs) != len(node.attribute):
            raise Unsupported("Duplicate ONNX attributes")
        args = [tensors[n] for n in node.input]
        op = node.op_type
        allowed = {
            "Constant": {"value"},
            "ConstantOfShape": {"value"},
            "Gemm": {"alpha", "beta", "transA", "transB"},
            "Gather": {"axis"},
            "Concat": {"axis"},
            "Transpose": {"perm"},
        }.get(op, set())
        if set(attrs) - allowed:
            raise Unsupported(f"Unsupported {op} attributes")
        arities = {
            "Constant": (0,),
            "ConstantOfShape": (1,),
            "Gemm": (3,),
            "MatMul": (2,),
            "Gather": (2,),
            "Slice": (3, 4, 5),
            "Reshape": (2,),
            "Expand": (2,),
            "Equal": (2,),
            "Where": (3,),
            "Add": (2,),
            "Sub": (2,),
            "Mul": (2,),
            "Pow": (2,),
            "Neg": (1,),
            "Sin": (1,),
            "Cos": (1,),
            "Relu": (1,),
            "Sigmoid": (1,),
            "Transpose": (1,),
            "Shape": (1,),
        }
        if op != "Concat" and (op not in arities or len(args) not in arities[op]):
            raise Unsupported(f"Unsupported ONNX operation or arity: {op}")
        if op == "Constant":
            if set(attrs) != {"value"} or not isinstance(attrs["value"], TensorProto):
                raise Unsupported("Constant requires inline tensor value")
            result = _array(attrs["value"])
        elif op == "ConstantOfShape":
            dims = _integer_vector(args[0])
            value = (
                _array(attrs["value"])
                if "value" in attrs
                else np.array([0], np.float32)
            )
            if value.size != 1 or any(d < 0 for d in dims):
                raise Unsupported("Invalid ConstantOfShape")
            result = np.full(dims, value.item(), dtype=value.dtype)
        elif op == "Shape":
            result = np.array(args[0].shape, np.int64)
        elif op == "Reshape":
            dims = _integer_vector(args[1])
            if not dims or dims.count(-1) > 1 or any(d < -1 for d in dims):
                raise Unsupported("Invalid reshape dimensions")
            dims = [args[0].shape[i] if d == 0 else d for i, d in enumerate(dims)]
            result = args[0].reshape(dims)
        elif op == "Transpose":
            result = args[0].transpose(attrs.get("perm"))
        elif op == "Gather":
            if not _constant(args[1]) or args[1].dtype != np.int64:
                raise Unsupported("Gather requires constant INT64 indices")
            result = np.take(
                args[0], args[1], axis=_axis(attrs.get("axis", 0), args[0].ndim)
            )
        elif op == "Slice":
            starts, ends = (_integer_vector(a) for a in args[1:3])
            axes = (
                _integer_vector(args[3]) if len(args) > 3 else list(range(len(starts)))
            )
            steps = _integer_vector(args[4]) if len(args) > 4 else [1] * len(starts)
            if not len(starts) == len(ends) == len(axes) == len(steps) or any(
                s == 0 for s in steps
            ):
                raise Unsupported("Invalid Slice metadata")
            axes = [_axis(a, args[0].ndim) for a in axes]
            if len(set(axes)) != len(axes):
                raise Unsupported("Duplicate Slice axes")
            slices = [slice(None)] * args[0].ndim
            for start, end, axis, step in zip(starts, ends, axes, steps, strict=True):
                # ONNX uses INT_MIN as the open end of a reverse slice.
                slices[axis] = slice(
                    start, None if step < 0 and end <= -(2**63 - 1) else end, step
                )
            result = args[0][tuple(slices)]
        elif op == "Concat":
            if not args or "axis" not in attrs:
                raise Unsupported("Concat requires tensors and axis")
            result = np.concatenate(args, axis=_axis(attrs["axis"], args[0].ndim))
        elif op in ("Equal", "Where"):
            if not all(_constant(a) for a in args):
                raise Unsupported(
                    f"Data-dependent {op} is unsupported; constant scaffolding only"
                )
            if op == "Where" and args[0].dtype != np.bool_:
                raise Unsupported("Where condition must be BOOL")
            result = np.equal(*args) if op == "Equal" else np.where(*args)
        elif op == "Expand":
            dims = _integer_vector(args[1])
            if any(d < 0 for d in dims):
                raise Unsupported("Invalid Expand shape")
            result = np.broadcast_to(
                args[0], np.broadcast_shapes(args[0].shape, tuple(dims))
            )
        elif op == "Gemm":
            a, b, c = args
            if (
                attrs.get("alpha", 1) != 1
                or attrs.get("beta", 1) != 1
                or attrs.get("transA", 0) != 0
                or attrs.get("transB", 0) not in (0, 1)
                or not _constant(b)
                or not _constant(c)
                or c.dtype != np.float32
            ):
                raise Unsupported(
                    "Gemm requires constant FLOAT32 parameters, alpha=beta=1, transA=0"
                )
            result = matmul(a, b.T if attrs.get("transB", 0) else b, c)
        elif op == "MatMul":
            result = matmul(*args)
        else:
            if op == "Pow" and (not _constant(args[1]) or not np.all(args[1] == 2)):
                raise Unsupported("Only constant square exponents are supported")
            result = elementwise(op, args)
        result = np.asarray(result)
        if _constant(result) and not np.isfinite(result).all():
            raise Unsupported("Non-finite folded constant")
        tensors[node.output[0]] = result
    output = tensors.get(graph.output[0].name)
    declared = tuple(d.dim_value for d in graph.output[0].type.tensor_type.shape.dim)
    if output is None or output.shape != declared:
        raise Unsupported("Graph output differs from its declared shape")
    return TensorDAG(
        count, relations, output, {name: t.shape for name, t in tensors.items()}
    )
