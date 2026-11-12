"""Construction for the interpreted sequential smooth-network subset only.

Environment ownership, optimization and witness acceptance stay in the worker.
All tensors are flattened in ONNX C order; Reshape preserves that order.
"""

import gurobipy as gp
from gurobi_ml import add_predictor_constr
from onnx import helper, numpy_helper


def construct(optimization, model, inputs, outputs):
    if not any(n.op_type in ("Sigmoid", "Reshape") for n in model.graph.node):
        add_predictor_constr(optimization, model, inputs, outputs)
        return
    constants = {t.name: numpy_helper.to_array(t) for t in model.graph.initializer}
    current = inputs.reshape(-1)
    for node in model.graph.node:
        if node.op_type in ("Constant", "Reshape"):
            continue
        if node.op_type == "Gemm":
            weights, bias = (constants[n] for n in node.input[1:])
            attributes = {a.name: helper.get_attribute_value(a) for a in node.attribute}
            if attributes.get("transB", 0):
                weights = weights.T
            following = optimization.addMVar(weights.shape[1], lb=-gp.GRB.INFINITY)
            optimization.addConstr(following == current @ weights + bias.reshape(-1))
        else:
            following = optimization.addMVar(
                current.size,
                lb=0,
                ub=1 if node.op_type == "Sigmoid" else gp.GRB.INFINITY,
            )
            for x, y in zip(current.tolist(), following.tolist(), strict=True):
                if node.op_type == "Sigmoid":
                    optimization.addGenConstrLogistic(x, y, options="FuncNonlinear=1")
                else:
                    optimization.addGenConstrMax(y, [x], constant=0)
        current = following
    optimization.addConstr(outputs.reshape(-1) == current)
