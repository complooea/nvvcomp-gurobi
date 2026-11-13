"""Native global construction of the interpreted scalar relations.

The worker still owns the environment, deadline, optimization and replay.
Bounds are conservative mathematical ranges, never extra physical restrictions.
"""

import math

import gurobipy as gp
from gurobi_ml import add_predictor_constr

from ._interpretation import uses_native_construction
from ._tensor_dag import Ref, Unsupported, lower


def _outward(value, direction):
    return math.nextafter(value, direction)


def _bounds(relation, intervals):
    args = [
        intervals[a.index] if isinstance(a, Ref) else (float(a), float(a))
        for a in relation.arguments
    ]
    op = relation.operation
    if op == "Affine":
        lo = hi = relation.bias
        for (a, b), c in zip(args, relation.coefficients, strict=True):
            left, right = (a, b) if c >= 0 else (b, a)
            lo = _outward(lo + _outward(c * left, -math.inf), -math.inf)
            hi = _outward(hi + _outward(c * right, math.inf), math.inf)
        return lo, hi
    if op in ("Sin", "Cos"):
        return -1.0, 1.0
    if op == "Sigmoid":
        return 0.0, 1.0
    if any(not math.isfinite(v) for pair in args for v in pair):
        return -math.inf, math.inf
    a, b = args[0]
    if op == "Relu":
        return max(0, a), max(0, b)
    if op == "Square":
        return (
            0.0 if a <= 0 <= b else max(0, _outward(min(a * a, b * b), -math.inf)),
            _outward(max(a * a, b * b), math.inf),
        )
    if op == "Mul":
        c, d = args[1]
        products = (a * c, a * d, b * c, b * d)
        return _outward(min(products), -math.inf), _outward(max(products), math.inf)
    raise Unsupported(f"No interval semantics for relation: {op}")


def construct(optimization, model, inputs, outputs):
    if not uses_native_construction(model):
        add_predictor_constr(optimization, model, inputs, outputs)
        return
    dag = lower(model)
    optimization.update()
    variables = list(inputs.reshape(-1).tolist())
    intervals = [(v.LB, v.UB) for v in variables]
    for relation in dag.relations:
        interval = _bounds(relation, intervals)
        lo, hi = interval
        # Overflow or enormous interval estimates must not restrict the model.
        if (
            not math.isfinite(lo)
            or not math.isfinite(hi)
            or abs(lo) >= 1e100
            or abs(hi) >= 1e100
        ):
            lo, hi = -gp.GRB.INFINITY, gp.GRB.INFINITY
        y = optimization.addVar(lb=lo, ub=hi)
        args = [
            variables[a.index] if isinstance(a, Ref) else float(a)
            for a in relation.arguments
        ]
        op = relation.operation
        if op == "Affine":
            optimization.addConstr(
                y
                == gp.quicksum(
                    c * x for c, x in zip(relation.coefficients, args, strict=True)
                )
                + relation.bias
            )
        elif op in ("Mul", "Square"):
            optimization.addConstr(
                y == args[0] * (args[0] if op == "Square" else args[1])
            )
        else:
            x = args[0]
            if not isinstance(x, gp.Var):
                x = optimization.addVar(lb=x, ub=x)
            if op == "Relu":
                optimization.addGenConstrMax(y, [x], constant=0)
            else:
                function = {
                    "Sigmoid": optimization.addGenConstrLogistic,
                    "Sin": optimization.addGenConstrSin,
                    "Cos": optimization.addGenConstrCos,
                }[op]
                function(x, y, options="FuncNonlinear=1")
        variables.append(y)
        intervals.append(interval)
    for y, value in zip(outputs.reshape(-1).tolist(), dag.output.flat, strict=True):
        optimization.addConstr(
            y == (variables[value.index] if isinstance(value, Ref) else float(value))
        )
