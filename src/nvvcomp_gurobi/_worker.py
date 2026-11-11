"""Private subprocess entry point; all instance analysis happens here."""

import gzip
import hashlib
import importlib.metadata
import json
import os
import platform
import sys
import time
from dataclasses import asdict
from pathlib import Path

from .verification import VerificationResult

TOOLING = {
    "benchmark": "303f2327a8e8411efc4457da03d2016ce42733cf",
    "rules": "b0ec5ac3c8f39262f07a1c67919fbb89fa42a245",
    "validator_scoring": "eea564f5d0a8751d8321a409214db14d03f452b8",
    "runner": "3d5a8848169fc5f0cc03ab9722865235e9857f16",
}


def _checkpoint(request: dict, result: VerificationResult):
    path = Path(request["result_path"])
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(asdict(result), allow_nan=False))
    temporary.replace(path)


def _remaining(request: dict) -> float:
    remaining = request["deadline"] - time.monotonic()
    if remaining <= 0:
        raise TimeoutError("Whole-run deadline exhausted")
    return remaining


def run(request: dict) -> VerificationResult:
    result = VerificationResult()
    stage = "interpretation"
    stage_start = time.monotonic()
    try:
        result.provenance = {
            "tooling_revisions": TOOLING,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "logical_cpus": os.cpu_count(),
            "formulation": "gurobi-machinelearning ONNX; constant-objective feasibility",
            "artifacts": {},
            "packages": {},
            "replay_settings": {
                "provider": "CPUExecutionProvider",
                "intra_op_threads": 12,
                "inter_op_threads": 12,
                "input_dtype": "float32",
                "strict_input_tolerance": 0.0,
                "tolerant_input_tolerance": 1e-4,
                "output_tolerance": 0.0,
            },
        }
        contents = {}
        for kind in ["onnx", "vnnlib"]:
            path = Path(request[f"{kind}_path"])
            if not path.exists() and path.with_suffix(path.suffix + ".gz").is_file():
                path = path.with_suffix(path.suffix + ".gz")
            original = path.read_bytes()
            content = gzip.decompress(original) if path.suffix == ".gz" else original
            contents[kind] = content
            result.provenance["artifacts"][kind] = {
                "requested_path": request[f"{kind}_path"],
                "path": str(path),
                "sha256": hashlib.sha256(original).hexdigest(),
                "uncompressed_sha256": hashlib.sha256(content).hexdigest(),
            }
        import onnx
        from google.protobuf.message import DecodeError

        from ._interpretation import Unsupported, interpret_network, interpret_property

        try:
            model, num_inputs, num_outputs = interpret_network(contents["onnx"])
            prop = interpret_property(
                contents["vnnlib"].decode("utf-8"), num_inputs, num_outputs
            )
        except (
            ValueError,
            DecodeError,
            onnx.checker.ValidationError,
            onnx.shape_inference.InferenceError,
        ) as exc:
            raise Unsupported(str(exc)) from exc
        result.provenance["replay_property"] = {
            "normalization": "Whitespace/comments only; statement and operand order preserved",
            "sha256": hashlib.sha256(prop.replay_text.encode("utf-8")).hexdigest(),
        }
        result.timings[stage] = time.monotonic() - stage_start
        _checkpoint(request, result)
        _remaining(request)
        stage, stage_start = "construction", time.monotonic()
        try:
            import gurobipy as gp
            import numpy as np
            from gurobi_ml import add_predictor_constr
        except ImportError as exc:
            result.reason = "prerequisite_error"
            result.diagnostic = f"Install the pinned solver extra: uv sync --locked --extra solver ({exc})"
            return result
        for name in [
            "gurobipy",
            "gurobi-machinelearning",
            "onnx",
            "onnxruntime",
            "numpy",
            "cachier",
        ]:
            result.provenance["packages"][name] = importlib.metadata.version(name)
        with gp.Env(empty=True) as environment:
            environment.setParam("OutputFlag", 0)
            environment.start()
            with gp.Model(env=environment) as optimization:
                optimization.Params.Threads = request["threads"]
                numerical = [
                    "FeasibilityTol",
                    "IntFeasTol",
                    "OptimalityTol",
                    "NumericFocus",
                    "IntegralityFocus",
                    "ScaleFlag",
                    "MarkowitzTol",
                    "MIPGap",
                    "MIPGapAbs",
                    "DualReductions",
                ]
                result.provenance["solver_settings"] = {
                    name: optimization.getParamInfo(name)[2] for name in numerical
                }
                result.provenance["gurobi_version"] = list(gp.gurobi.version())
                inputs = optimization.addMVar(
                    (1, num_inputs),
                    lb=np.array([prop.lower]),
                    ub=np.array([prop.upper]),
                    name="X",
                )
                outputs = optimization.addMVar(
                    (1, num_outputs), lb=-gp.GRB.INFINITY, name="Y"
                )
                add_predictor_constr(optimization, model, inputs, outputs)
                for comparison in prop.comparisons:
                    left = outputs[0, int(comparison.left[2:])]
                    right = (
                        outputs[0, int(comparison.right[2:])]
                        if isinstance(comparison.right, str)
                        else comparison.right
                    )
                    optimization.addConstr(
                        left <= right if comparison.operator == "<=" else left >= right
                    )
                optimization.setObjective(0.0)
                result.timings[stage] = time.monotonic() - stage_start
                optimization.Params.TimeLimit = _remaining(request)
                result.provenance["solver_settings"].update(
                    {
                        "Threads": request["threads"],
                        "TimeLimit": optimization.Params.TimeLimit,
                        "OutputFlag": 0,
                    }
                )
                _checkpoint(request, result)
                stage, stage_start = "solve", time.monotonic()
                optimization.optimize()
                result.timings[stage] = time.monotonic() - stage_start
                status = int(optimization.Status)
                result.solver_status = status
                result.diagnostic = (
                    f"Gurobi status {status}, solutions {optimization.SolCount}"
                )
                _checkpoint(request, result)
                _remaining(request)
                if status == gp.GRB.INFEASIBLE:
                    result.outcome, result.reason = "unsat", "infeasible"
                elif status in (gp.GRB.NUMERIC, gp.GRB.INF_OR_UNBD, gp.GRB.UNBOUNDED):
                    result.reason = {
                        gp.GRB.NUMERIC: "numerical_failure",
                        gp.GRB.INF_OR_UNBD: "ambiguous_status",
                        gp.GRB.UNBOUNDED: "unexpected_unbounded",
                    }[status]
                elif optimization.SolCount > 0:
                    stage, stage_start = "validation", time.monotonic()
                    from ._format import witness_text
                    from ._vendor.counterexamples import (
                        get_ce_diff,
                        predict_with_onnxruntime,
                    )

                    network = Path("original.onnx")
                    property_file = Path("replay.vnnlib")
                    network.write_bytes(contents["onnx"])
                    property_file.write_text(prop.replay_text)
                    candidate = np.asarray(inputs.getAttr("X"), dtype=np.float32)
                    replay = predict_with_onnxruntime(str(network), candidate)
                    if (
                        not np.isfinite(candidate).all()
                        or not np.isfinite(replay).all()
                    ):
                        result.validation = "invalid"
                        result.reason = "validation_failed"
                        result.diagnostic += "; non-finite candidate or replay"
                    else:
                        result.witness = {
                            "inputs": candidate.ravel(order="C").tolist(),
                            "outputs": replay.ravel(order="C").tolist(),
                        }
                        witness = Path("candidate.txt")
                        witness.write_text(witness_text(result.witness))
                        classification, diagnostic = get_ce_diff(
                            str(network), str(property_file), str(witness), 1e-4, 0.0
                        )
                        result.validation = {
                            "correct": "strict",
                            "correct_up_to_tolerance": "tolerance_only",
                        }.get(classification, "invalid")
                        result.diagnostic += f"; {classification}: {diagnostic}"
                        if result.validation != "invalid":
                            result.outcome, result.reason = "sat", "validated_witness"
                        else:
                            result.reason = "validation_failed"
                    result.timings[stage] = time.monotonic() - stage_start
                    _remaining(request)
                else:
                    result.reason = (
                        "solver_timeout"
                        if status == gp.GRB.TIME_LIMIT
                        else "solver_termination"
                    )
    except TimeoutError as exc:
        result.outcome, result.reason = "unknown", "timeout"
        result.diagnostic = str(exc)
    except OSError as exc:
        result.outcome = "unknown"
        result.reason = "input_error"
        result.diagnostic = str(exc)
    except Exception as exc:  # noqa: BLE001 -- subprocess boundary reports unexpected failures as data
        # Process boundary: retain failures as data, never turn them into UNSAT.
        result.outcome = "unknown"
        result.reason = (
            "unsupported" if type(exc).__name__ == "Unsupported" else "error"
        )
        result.diagnostic = f"{stage}: {type(exc).__name__}: {exc}"
    finally:
        result.timings.setdefault(stage, time.monotonic() - stage_start)
    return result


if __name__ == "__main__":
    request = json.loads(sys.argv[1])
    _checkpoint(request, run(request))
