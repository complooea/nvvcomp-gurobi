"""Verify original artifacts under a whole-run deadline, in an isolated process."""

import json
import math
import os
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal


@dataclass(frozen=True)
class Instance:
    onnx_path: Path
    vnnlib_path: Path


@dataclass(frozen=True)
class ExecutionLimits:
    timeout_seconds: float
    threads: int = 1

    def __post_init__(self):
        if not math.isfinite(self.timeout_seconds) or self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive and finite")
        if (
            isinstance(self.threads, bool)
            or not isinstance(self.threads, int)
            or self.threads < 1
        ):
            raise ValueError("threads must be a positive integer")


@dataclass
class VerificationResult:
    outcome: Literal["sat", "unsat", "unknown"] = "unknown"
    reason: str = "error"
    diagnostic: str = ""
    solver_status: int | None = None
    witness: dict[str, list[float]] | None = None
    validation: str | None = None
    timings: dict[str, float] = field(default_factory=dict)
    provenance: dict = field(default_factory=dict)


def verify(instance: Instance, limits: ExecutionLimits) -> VerificationResult:
    """Return a numerical verdict; SAT requires pinned CPU replay acceptance.

    Startup, reads, decompression, encoding, solve and validation share the limit.
    No solver package is imported in the calling process. Worker process groups
    are killed at the deadline; cleanup time never grants additional solve time.
    """
    started = time.monotonic()
    deadline = started + limits.timeout_seconds
    try:
        with tempfile.TemporaryDirectory(prefix="nvvcomp-") as directory:
            request = {
                "onnx_path": str(Path(instance.onnx_path).resolve()),
                "vnnlib_path": str(Path(instance.vnnlib_path).resolve()),
                "deadline": deadline,
                "threads": limits.threads,
                "result_path": str(Path(directory) / "result.json"),
            }
            result = _run_process(request, directory)
    except (OSError, ValueError, TypeError) as exc:
        result = VerificationResult(reason="worker_error", diagnostic=str(exc))
    if time.monotonic() > deadline:
        result.outcome = "unknown"
        result.reason = "timeout"
        result.diagnostic = (
            "Whole-run deadline exceeded; late results are not accepted. "
            + result.diagnostic
        )
    result.timings["total"] = time.monotonic() - started
    result.provenance["limits"] = asdict(limits)
    result.provenance.setdefault(
        "requested_artifacts",
        {
            "onnx": str(instance.onnx_path),
            "vnnlib": str(instance.vnnlib_path),
        },
    )
    return result


def _run_process(request: dict, directory: str) -> VerificationResult:
    output = Path(request["result_path"])
    with (Path(directory) / "worker.log").open("w+") as log:
        process = subprocess.Popen(
            [sys.executable, "-m", "nvvcomp_gurobi._worker", json.dumps(request)],
            cwd=directory,
            stdout=log,
            stderr=log,
            start_new_session=True,
        )
        try:
            process.wait(timeout=max(0, request["deadline"] - time.monotonic()))
        except subprocess.TimeoutExpired:
            pass  # The finally block enforces the deadline, including cleanup.
        finally:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass  # The process/group may already have exited.
            process.wait()
        if output.exists():
            result = VerificationResult(**json.loads(output.read_text()))
            if process.returncode != 0:
                log.seek(0)
                result.outcome, result.reason = "unknown", "worker_error"
                result.diagnostic += (
                    f"; worker exit {process.returncode}: {log.read()[-4000:]}"
                )
            return result
        log.seek(0)
        return VerificationResult(
            reason="worker_error",
            diagnostic=f"Worker exit {process.returncode}: {log.read()[-4000:]}",
        )
