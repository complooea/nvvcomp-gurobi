"""Thin VNN-COMP v1 executable adapter; no analysis in preparation."""

import argparse
import json
import signal
import time
from dataclasses import asdict
from pathlib import Path

from . import _INVOCATION_STARTED
from ._format import witness_text
from .verification import ExecutionLimits, Instance, VerificationResult, verify


def main():
    # External competition timeout must also reap our new-session worker.
    signal.signal(signal.SIGTERM, _terminated)
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ["prepare", "run"]:
        subparser = commands.add_parser(command)
        subparser.add_argument("version", choices=["v1"])
        subparser.add_argument("category")
        subparser.add_argument("onnx", type=Path)
        subparser.add_argument("vnnlib", type=Path)
        if command == "run":
            subparser.add_argument("output", type=Path)
            subparser.add_argument("timeout", type=float)
    args = parser.parse_args()
    if args.command == "prepare":
        print(
            json.dumps(
                {
                    "preparation_seconds": time.monotonic() - _INVOCATION_STARTED,
                    "analysis_performed": False,
                }
            )
        )
        return
    try:
        limits = ExecutionLimits(args.timeout)
    except ValueError as exc:
        parser.error(str(exc))
    remaining = limits.timeout_seconds - (time.monotonic() - _INVOCATION_STARTED)
    if remaining <= 0:
        result = VerificationResult(
            reason="timeout", diagnostic="Deadline exhausted before verification"
        )
    else:
        result = verify(Instance(args.onnx, args.vnnlib), ExecutionLimits(remaining))
    result.provenance["category"] = args.category
    result.provenance["invocation_timeout_seconds"] = args.timeout
    result.timings["invocation"] = time.monotonic() - _INVOCATION_STARTED
    if result.timings["invocation"] > args.timeout:
        result.outcome, result.reason = "unknown", "timeout"
        result.diagnostic = "Whole invocation deadline exceeded"
    word = result.outcome
    if word == "unknown":
        if result.reason in ("timeout", "solver_timeout"):
            word = "timeout"
        elif result.reason in (
            "error",
            "worker_error",
            "prerequisite_error",
            "input_error",
        ):
            word = "error"
    text = word + "\n"
    if result.outcome == "sat":
        assert result.witness is not None
        text += witness_text(result.witness)
    args.output.write_text(text)
    args.output.with_suffix(args.output.suffix + ".json").write_text(
        json.dumps(asdict(result), indent=2) + "\n"
    )


def _terminated(signum, frame):
    raise SystemExit(128 + signum)


if __name__ == "__main__":
    main()
