import gzip
import os
import signal
import subprocess
import time
from pathlib import Path

import pytest

from nvvcomp_gurobi.verification import ExecutionLimits, Instance, verify


def test_missing_original_artifact_returns_diagnostic(tmp_path: Path):
    result = verify(
        Instance(tmp_path / "missing.onnx", tmp_path / "missing.vnnlib"),
        ExecutionLimits(timeout_seconds=10),
    )
    assert result.outcome == "unknown"
    assert result.reason == "input_error"
    assert "missing.onnx" in result.diagnostic
    assert result.solver_status is None
    assert 0 <= result.timings["total"] < 10


def test_malformed_onnx_is_explicitly_unsupported(instance_factory):
    instance = instance_factory("(assert (>= Y_0 0))")
    instance.onnx_path.write_bytes(b"not an ONNX model")
    result = verify(instance, ExecutionLimits(10))
    assert result.outcome == "unknown"
    assert result.reason == "unsupported", result.diagnostic
    assert result.solver_status is None


def test_manifest_references_resolve_compressed_artifacts_without_mutating_them(
    instance_factory,
):
    instance = instance_factory("(assert (or (>= Y_0 0) (<= Y_0 -1)))")
    for path in [instance.onnx_path, instance.vnnlib_path]:
        path.with_suffix(path.suffix + ".gz").write_bytes(
            gzip.compress(path.read_bytes())
        )
        path.unlink()
    result = verify(instance, ExecutionLimits(10))
    assert result.reason == "unsupported", result.diagnostic
    assert "Unsupported VNN-LIB" in result.diagnostic
    assert result.provenance["artifacts"]["onnx"]["path"].endswith(".onnx.gz")
    assert not instance.onnx_path.exists()
    assert not instance.vnnlib_path.exists()


def test_failed_process_launch_is_a_structured_failure(instance_factory, monkeypatch):
    def unavailable(*args, **kwargs):
        raise OSError("process resources unavailable")

    monkeypatch.setattr(subprocess, "Popen", unavailable)
    result = verify(instance_factory("(assert (>= Y_0 0))"), ExecutionLimits(10))
    assert result.outcome == "unknown"
    assert result.reason == "worker_error"
    assert "resources unavailable" in result.diagnostic


def test_deadline_kills_blocking_startup_without_waiting_for_solver(
    instance_factory, worker_startup
):
    worker_startup("import time\ntime.sleep(60)\n")
    result = verify(instance_factory("(assert (>= Y_0 0))"), ExecutionLimits(5))
    assert result.outcome == "unknown"
    assert result.reason == "timeout"
    assert result.solver_status is None
    assert 5 <= result.timings["total"] < 20


@pytest.mark.solver
def test_late_results_are_rejected_without_a_timing_race(instance_factory, monkeypatch):
    original_wait, original_clock = subprocess.Popen.wait, time.monotonic
    elapsed = 0

    def wait(*args, **kwargs):
        nonlocal elapsed
        response = original_wait(*args, **kwargs)
        elapsed = 100
        return response

    monkeypatch.setattr(subprocess.Popen, "wait", wait)
    monkeypatch.setattr(time, "monotonic", lambda: original_clock() + elapsed)
    result = verify(instance_factory("(assert (>= Y_0 0))"), ExecutionLimits(30))
    assert result.outcome == "unknown"
    assert result.reason == "timeout"
    assert "late results" in result.diagnostic
    assert result.solver_status == 2
    assert result.validation == "strict"


@pytest.mark.parametrize(
    "assertion",
    [
        "(assert (> Y_0 0))",
        "(assert (= Y_0 0))",
        "(assert (<= (+ Y_0 Y_1) 0))",
        "(assert (or (<= Y_0 0) (>= Y_1 1)))",
        "(assert (or (and (<= Y_0 0)) (and (>= X_0 0))))",
        "(assert (or (and (<= Y_0 0)) (and)))",
        "(assert (or (and (<= Y_0 0)) (and (> Y_1 1))))",
        "(assert (or (and (<= Y_0 0)) (and (<= Y_2 1))))",
        "(assert (or (and (<= Y_0 Y_0))))",
        "(assert (or (and (<= Y_0 0)) garbage))",
        "(assert (<= Y_2 0))",
        "(assert (<= Y_0 NaN))",
        "(assert (<= X_0 X_1))",
        "(push 1)",
        "(assert (>= Y_0 0)) garbage",
        "(assert (>= Y_0 0)) )",
    ],
)
def test_unsupported_property_is_not_silently_approximated(instance_factory, assertion):
    result = verify(instance_factory(assertion), ExecutionLimits(10))
    assert result.outcome == "unknown"
    assert result.reason == "unsupported", result.diagnostic
    assert result.solver_status is None


@pytest.mark.parametrize("options", [{"op": "Sigmoid"}, {"trans_a": 1}])
def test_unsupported_network_operations_and_attributes(instance_factory, options):
    result = verify(
        instance_factory("(assert (>= Y_0 0))", **options), ExecutionLimits(10)
    )
    assert result.reason == "unsupported", result.diagnostic
    assert result.solver_status is None


@pytest.mark.parametrize("timeout", [0, -1, float("nan"), float("inf")])
def test_invalid_execution_limits_are_caller_errors(timeout):
    with pytest.raises(ValueError, match="positive and finite"):
        ExecutionLimits(timeout)


def test_caller_interruption_reaps_the_isolated_process(instance_factory, monkeypatch):
    original_wait = subprocess.Popen.wait
    interrupted = []

    def interrupt_once(process, *args, **kwargs):
        if not interrupted:
            interrupted.append(process.pid)
            raise KeyboardInterrupt
        return original_wait(process, *args, **kwargs)

    monkeypatch.setattr(subprocess.Popen, "wait", interrupt_once)
    try:
        with pytest.raises(KeyboardInterrupt):
            verify(instance_factory("(assert (>= Y_0 0))"), ExecutionLimits(30))
        with pytest.raises(ProcessLookupError):
            os.kill(interrupted[0], 0)
    finally:
        # Clean up even on RED, when the implementation still leaks the worker.
        try:
            os.killpg(interrupted[0], signal.SIGKILL)
            os.waitpid(interrupted[0], 0)
        except ProcessLookupError:
            pass
