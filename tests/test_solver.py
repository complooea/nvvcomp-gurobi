import pytest

from nvvcomp_gurobi.verification import ExecutionLimits, verify

pytestmark = pytest.mark.solver


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
