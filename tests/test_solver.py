import pytest

from nvvcomp_gurobi.verification import ExecutionLimits, verify

pytestmark = pytest.mark.solver


def test_shared_dag_sat_with_original_onnx_replay(dag_instance_factory):
    result = verify(
        dag_instance_factory(
            "(assert (>= Y_0 3.38))\n(assert (<= Y_0 3.39))", fixed=True
        ),
        ExecutionLimits(30),
    )
    assert result.outcome == "sat", result.diagnostic
    assert result.validation == "strict"
    assert result.witness is not None
    assert result.witness["inputs"] == [0, 0]
    assert result.witness["outputs"] == pytest.approx([3.3817733], abs=1e-6)


def test_shared_dag_output_below_independent_range_is_unsat(dag_instance_factory):
    # u_0 in [0,1], u_1 in [1,2] radians: squares sum >= 1,
    # products and sines >= 0, cos(u_0) > .5 and cos(u_1) >= -1.
    # Thus y > .5. The threshold lies inside the coarse propagated interval,
    # so this also requires actual trigonometric constraints, not just [-1,1].
    result = verify(dag_instance_factory("(assert (<= Y_0 0))"), ExecutionLimits(30))
    assert result.outcome == "unsat", result.diagnostic
    assert result.reason == "infeasible"
    assert result.solver_status == 3


def test_static_views_and_constant_scaffold_preserve_coordinates(tmp_path):
    import numpy as np
    import onnx
    from onnx import TensorProto, helper, numpy_helper

    from nvvcomp_gurobi.verification import Instance

    arrays = {
        "shape": np.array([2, 3], np.int64),
        "start": np.array([2], np.int64),
        "end": np.array([-(2**63)], np.int64),
        "axis": np.array([0], np.int64),
        "step": np.array([-1], np.int64),
        "indices": np.array([1, 0], np.int64),
        "weights": np.array([[1, 0, 2]], np.float32),
        "size": np.array([2], np.int64),
        "target": np.array([-1, 2], np.int64),
        "negative": np.array(-1, np.int64),
        "seven": np.array(7, np.float32),
    }
    nodes = [
        helper.make_node("Reshape", ["x", "shape"], ["matrix"]),
        helper.make_node("Transpose", ["matrix"], ["transposed"], perm=[1, 0]),
        helper.make_node(
            "Slice", ["transposed", "start", "end", "axis", "step"], ["reversed"]
        ),
        helper.make_node("Gather", ["reversed", "indices"], ["gathered"], axis=1),
        helper.make_node("MatMul", ["weights", "gathered"], ["weighted"]),
        helper.make_node(
            "ConstantOfShape",
            ["size"],
            ["ones"],
            value=numpy_helper.from_array(np.array([1], np.int64)),
        ),
        helper.make_node("Mul", ["ones", "negative"], ["minus_ones"]),
        helper.make_node("Equal", ["target", "minus_ones"], ["mask"]),
        helper.make_node("Where", ["mask", "ones", "target"], ["expanded_shape"]),
        helper.make_node("Expand", ["seven", "expanded_shape"], ["sevens"]),
        helper.make_node("Concat", ["weighted", "sevens"], ["y"], axis=1),
    ]
    graph = helper.make_graph(
        nodes,
        "views",
        [helper.make_tensor_value_info("x", TensorProto.FLOAT, [1, 6])],
        [helper.make_tensor_value_info("y", TensorProto.FLOAT, [1, 4])],
        [numpy_helper.from_array(a, n) for n, a in arrays.items()],
    )
    model = helper.make_model(
        graph, opset_imports=[helper.make_opsetid("", 14)], ir_version=8
    )
    network, prop = tmp_path / "views.onnx", tmp_path / "views.vnnlib"
    onnx.save(model, network)
    prop.write_text(
        "\n".join(
            [f"(declare-const X_{i} Real)" for i in range(6)]
            + [f"(declare-const Y_{i} Real)" for i in range(4)]
            + [f"(assert ({op} X_{i} {i}))" for i in range(6) for op in (">=", "<=")]
            + [
                f"(assert ({op} Y_{i} {v}))"
                for i, v in enumerate([11, 2, 7, 7])
                for op in (">=", "<=")
            ]
        )
    )
    result = verify(Instance(network, prop), ExecutionLimits(30))
    assert result.outcome == "sat", result.diagnostic
    assert result.validation == "strict"
    assert result.witness == {"inputs": [0, 1, 2, 3, 4, 5], "outputs": [11, 2, 7, 7]}


def test_smooth_reshape_sat_replays_original_tensor_order(smooth_instance_factory):
    instance = smooth_instance_factory(
        "(assert (>= Y_0 2.25))\n(assert (<= Y_0 2.27))\n"
        "(assert (>= Y_1 -0.51))\n(assert (<= Y_1 -0.49))"
    )
    original = instance.onnx_path.read_bytes()
    result = verify(instance, ExecutionLimits(30))
    assert result.outcome == "sat", result.diagnostic
    assert result.validation == "strict"
    assert result.witness is not None
    assert result.witness["inputs"] == [0, 1, 2, 3]
    assert result.witness["outputs"] == pytest.approx([2.261594, -0.5], abs=1e-6)
    assert instance.onnx_path.read_bytes() == original
    assert "native" in result.provenance["formulation"]


def test_smooth_output_above_analytic_range_is_unsat(smooth_instance_factory):
    # 0 < sigmoid(z) < 1 implies Y_0 = s_0 + 2*s_1 < 3, independently
    # of the affine input values. A missing/disconnected sigmoid cannot prove this.
    result = verify(
        smooth_instance_factory("(assert (>= Y_0 3.5))"), ExecutionLimits(30)
    )
    assert result.outcome == "unsat", result.diagnostic
    assert result.reason == "infeasible"
    assert result.solver_status == 3


def test_later_disjunct_is_reachable_with_accepted_replay(instance_factory):
    result = verify(
        instance_factory(
            "(assert (>= Y_0 0.5))\n"
            "(assert (or (and (<= Y_0 -2)) (and (>= Y_0 0.75) (>= Y_0 Y_1) (<= Y_1 0))))"
        ),
        ExecutionLimits(30),
    )
    assert result.outcome == "sat", result.diagnostic
    assert result.validation == "strict"
    assert result.witness is not None
    assert 0.75 <= result.witness["outputs"][0] <= 1
    assert result.witness["outputs"][1] == 0


def test_all_disjuncts_impossible_with_unconditional_conjunct(instance_factory):
    # Y_0=X_0 in [-1,1], Y_1=max(X_1,0) in [0,1]. The first
    # alternative contradicts the unconditional conjunct; the second is negative.
    result = verify(
        instance_factory(
            "(assert (or (and (>= Y_0 0.5)) (and (<= Y_1 -1))))\n(assert (<= Y_0 -0.5))"
        ),
        ExecutionLimits(30),
    )
    assert result.outcome == "unsat", result.diagnostic
    assert result.reason == "infeasible"
    assert result.solver_status == 3
    assert result.validation is None
    assert result.witness is None


@pytest.mark.parametrize("opset", [9, 17])
def test_relu_sat_with_independently_replayed_witness(instance_factory, opset):
    result = verify(
        instance_factory("(assert (>= Y_0 0.5))\n(assert (<= Y_1 0))", opset=opset),
        ExecutionLimits(30),
    )
    assert result.outcome == "sat", result.diagnostic
    assert result.validation == "strict"
    assert result.solver_status == 2
    assert result.witness is not None
    x, y = result.witness["inputs"], result.witness["outputs"]
    assert 0.5 <= x[0] <= 1
    assert -1 <= x[1] <= 0
    assert y == [x[0], 0.0]
    assert result.provenance["packages"]["gurobipy"] == "13.0.1"
    assert result.timings["solve"] >= 0
    assert result.timings["validation"] > 0


@pytest.mark.parametrize("assertion", ["(assert (<= Y_0 -2))", "(assert (>= Y_1 2))"])
@pytest.mark.parametrize("opset", [9, 17])
def test_unreachable_output_is_numerical_unsat(instance_factory, assertion, opset):
    result = verify(instance_factory(assertion, opset=opset), ExecutionLimits(30))
    assert result.outcome == "unsat", result.diagnostic
    assert result.reason == "infeasible"
    assert result.solver_status == 3
    assert result.validation is None
    assert result.witness is None


def test_every_asserted_conjunct_is_preserved(instance_factory):
    # Each output restriction alone is reachable, but both cannot hold together.
    result = verify(
        instance_factory("(assert (>= Y_0 0.5))\n(assert (<= Y_0 -0.5))"),
        ExecutionLimits(30),
    )
    assert result.outcome == "unsat", result.diagnostic


def test_non_strict_bounds_include_equality(instance_factory):
    result = verify(
        instance_factory(
            "(assert (>= Y_0 1))\n(assert (<= Y_0 1))\n(assert (>= Y_1 1))"
        ),
        ExecutionLimits(30),
    )
    assert result.outcome == "sat", result.diagnostic
    assert result.witness == {"inputs": [1.0, 1.0], "outputs": [1.0, 1.0]}


def test_output_variable_comparison_keeps_inequality_direction(instance_factory):
    result = verify(
        instance_factory("(assert (<= Y_0 -0.5))\n(assert (>= Y_0 Y_1))"),
        ExecutionLimits(30),
    )
    assert result.outcome == "unsat", result.diagnostic


def test_slight_input_violation_retains_tolerance_only_classification(
    instance_factory, worker_startup
):
    # A candidate slightly outside the encoded box can occur within numerical
    # tolerances. Supply one deterministically at the external SDK boundary.
    worker_startup("""
import gurobipy as gp
import numpy as np
original = gp.MVar.getAttr
def get_attr(self, name):
    if name == "X":
        return np.array([[1.00001, 0.0]])
    return original(self, name)
gp.MVar.getAttr = get_attr
""")
    result = verify(
        instance_factory("(assert (>= Y_0 1))"),
        ExecutionLimits(30),
    )
    assert result.outcome == "sat", result.diagnostic
    assert result.validation == "tolerance_only"


def test_feasible_encoding_with_invalid_replay_never_becomes_unsat(instance_factory):
    # Real affine arithmetic admits x=0.1. FLOAT32 replay rounds above the
    # zero-tolerance output upper bound, so it cannot establish SAT either.
    result = verify(
        instance_factory(
            "(assert (>= X_0 0.1))\n(assert (<= X_0 0.1))\n(assert (<= Y_0 0.1))"
        ),
        ExecutionLimits(30),
    )
    assert result.outcome == "unknown", result.diagnostic
    assert result.reason == "validation_failed"
    assert result.validation == "invalid"
    assert result.solver_status == 2


@pytest.mark.parametrize(
    ("status", "reason"),
    [
        (4, "ambiguous_status"),
        (5, "unexpected_unbounded"),
        (9, "solver_timeout"),
        (11, "solver_termination"),
        (12, "numerical_failure"),
        (13, "solver_termination"),
    ],
)
def test_nondefinitive_solver_statuses_remain_unresolved(
    instance_factory, worker_startup, status, reason
):
    worker_startup(f"""
import gurobipy as gp
original = gp.Model.getAttr
def get_attr(self, name, *args):
    if name == "Status":
        return {status}
    if name == "SolCount":
        return 0
    return original(self, name, *args)
gp.Model.getAttr = get_attr
""")
    result = verify(instance_factory("(assert (>= Y_0 0))"), ExecutionLimits(30))
    assert result.outcome == "unknown", result.diagnostic
    assert result.reason == reason
    assert result.solver_status == status
    assert result.validation is None


def test_numerical_defaults_are_not_tuned(instance_factory):
    result = verify(instance_factory("(assert (>= Y_0 0))"), ExecutionLimits(30))
    assert result.outcome == "sat", result.diagnostic
    settings = result.provenance["solver_settings"]
    assert settings["FeasibilityTol"] == 1e-6
    assert settings["IntFeasTol"] == 1e-5
    assert settings["OptimalityTol"] == 1e-6
    assert settings["NumericFocus"] == 0
    assert settings["Threads"] == 1
    assert 0 < settings["TimeLimit"] < 30


def test_negative_affine_outputs_remain_reachable(instance_factory):
    result = verify(instance_factory("(assert (<= Y_0 -0.75))"), ExecutionLimits(30))
    assert result.outcome == "sat", result.diagnostic
    assert result.witness is not None
    assert -1 <= result.witness["outputs"][0] <= -0.75


def test_deadline_during_validation_keeps_raw_solver_status(
    instance_factory, worker_startup
):
    worker_startup("""
import gurobipy as gp
import time
original_attr, original_clock = gp.MVar.getAttr, time.monotonic
def get_attr(self, name):
    if name == "X":
        time.monotonic = lambda: original_clock() + 100
    return original_attr(self, name)
gp.MVar.getAttr = get_attr
""")
    result = verify(instance_factory("(assert (>= Y_0 0))"), ExecutionLimits(30))
    assert result.outcome == "unknown", result.diagnostic
    assert result.reason == "timeout"
    assert result.solver_status == 2
    assert result.validation == "strict"
    assert "validation" in result.timings


@pytest.mark.parametrize("layout", ["single_line", "closing_whitespace"])
def test_accepted_whitespace_layout_replays_the_same_property(instance_factory, layout):
    instance = instance_factory("(assert (>= Y_0 0.5))\n(assert (<= Y_1 0))")
    original = instance.vnnlib_path.read_text()
    if layout == "single_line":
        original = original.replace("\n", " ")
    else:
        original = original.replace(")", " \t)")
    instance.vnnlib_path.write_text(original)
    result = verify(instance, ExecutionLimits(30))
    assert result.outcome == "sat", result.diagnostic
    assert result.validation == "strict"
    assert instance.vnnlib_path.read_text() == original
