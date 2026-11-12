"""Manifest-driven, sequential experiments and solver-independent reporting."""

import argparse
import csv
import gzip
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import statistics
import subprocess
import time
import urllib.error
import urllib.request
from collections import Counter
from collections.abc import Callable
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from ._interpretation import (
    Unsupported,
    interpret_network,
    interpret_property,
    network_formulation,
)
from ._worker import TOOLING
from .verification import ExecutionLimits, Instance, VerificationResult, verify

Verification = Callable[[Instance, ExecutionLimits], VerificationResult]
BENCHMARK_URL = (
    "https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_benchmarks/"
    f"{TOOLING['benchmark']}/benchmarks/sat_relu/1.0"
)


def acquire_category(destination: Path, *, category: str = "sat_relu") -> Path:
    """Acquire the immutable category, retaining original compressed artifact bytes.

    Existing files must match the acquisition inventory; no silent overwrite.
    Downloads are not solver preparation and have their own elapsed time.
    """
    selections = {
        "sat_relu": (100, 100),
        "relusplitter_2026": (120, 180),
        "dist_shift_2023": (72, 300),
    }
    if category not in selections:
        raise ValueError(f"Unsupported pinned category: {category}")
    expected_rows, expected_budget = selections[category]
    benchmark_url = BENCHMARK_URL.replace("/sat_relu/", f"/{category}/")
    destination = destination.resolve()
    inventory = destination / "acquisition.json"
    if inventory.exists():
        saved = json.loads(inventory.read_text())
        if saved["benchmark_url"] != benchmark_url:
            raise ValueError("Acquisition source differs")
        for name, identity in saved["files"].items():
            if (
                hashlib.sha256((destination / name).read_bytes()).hexdigest()
                != identity["sha256"]
            ):
                raise ValueError(f"Acquired file changed: {name}")
        return destination / "instances.csv"
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("Use an empty acquisition directory")
    destination.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    files = {}

    def download(name: str) -> bytes:
        path = destination / name
        if not path.resolve().is_relative_to(destination):
            raise ValueError("Remote manifest path escapes category")
        url = f"{benchmark_url}/{name}"
        with urllib.request.urlopen(url, timeout=60) as response:
            content = response.read()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        files[name] = {
            "url": url,
            "sha256": hashlib.sha256(content).hexdigest(),
            "bytes": len(content),
        }
        return content

    manifest = download("instances.csv")
    rows = list(csv.reader(manifest.decode().splitlines()))
    if len(rows) != expected_rows or any(
        len(row) != 3 or float(row[2]) != expected_budget for row in rows
    ):
        raise ValueError(
            f"Pinned category must have {expected_rows} rows with {expected_budget}-second budgets"
        )
    for row in rows:
        if category == "dist_shift_2023" and row[0] != "./onnx/mnist_concat.onnx":
            raise ValueError("Pinned smooth selection requires mnist_concat only")
        for name in row[:2]:
            if name in files or name + ".gz" in files:
                continue
            try:
                download(name)
            except urllib.error.HTTPError as exc:
                if exc.code != 404:
                    raise
                download(name + ".gz")
    _save(
        inventory,
        {
            "benchmark_url": benchmark_url,
            "benchmark_revision": TOOLING["benchmark"],
            "acquisition_seconds": time.monotonic() - started,
            "files": files,
        },
    )
    return destination / "instances.csv"


def _save(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    with temporary.open("w") as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)
    descriptor = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _artifact(path: Path) -> tuple[bytes, dict]:
    if not path.exists():
        path = Path(str(path) + ".gz")
    original = path.read_bytes()
    content = gzip.decompress(original) if path.suffix == ".gz" else original
    return content, {
        "path": str(path),
        "sha256": hashlib.sha256(original).hexdigest(),
        "uncompressed_sha256": hashlib.sha256(content).hexdigest(),
        "bytes": len(original),
    }


def _revision() -> dict:
    root = Path(__file__).resolve().parents[2]
    source_hashes = {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((root / "src").rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts
    }
    source_hashes["uv.lock"] = hashlib.sha256(
        (root / "uv.lock").read_bytes()
    ).hexdigest()
    return {
        "git_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        "source_sha256": source_hashes,
    }


def _audit(manifest: Path, threads: int) -> dict:
    started = time.monotonic()
    entries = []
    with manifest.open(newline="") as stream:
        for index, row in enumerate(csv.reader(stream)):
            if len(row) != 3:
                raise ValueError(f"Manifest row {index + 1}: expected three fields")
            network, prop, budget = row
            limits = ExecutionLimits(float(budget), threads)
            paths = []
            for name in (network, prop):
                path = (manifest.parent / name).resolve()
                if not path.is_relative_to(manifest.parent):
                    raise ValueError(f"Manifest path escapes category: {name}")
                paths.append(path)
            content, artifacts = {}, {}
            # Missing/corrupt artifacts abort the preflight, never become exclusions.
            for kind, path in zip(("onnx", "vnnlib"), paths, strict=True):
                content[kind], artifacts[kind] = _artifact(path)
            entry = {
                "id": f"{index:04d}",
                "network": network,
                "property": prop,
                "timeout_seconds": limits.timeout_seconds,
                "artifacts": artifacts,
                "eligible": True,
                "exclusion_reason": None,
            }
            try:
                model, inputs, outputs = interpret_network(content["onnx"])
                property_ = interpret_property(
                    content["vnnlib"].decode(), inputs, outputs
                )
                entry["architecture"] = {
                    "formulation": network_formulation(model),
                    "input_shape": [
                        d.dim_value
                        for d in model.graph.input[0].type.tensor_type.shape.dim
                    ],
                    "output_shape": [
                        d.dim_value
                        for d in model.graph.output[0].type.tensor_type.shape.dim
                    ],
                    "inputs": inputs,
                    "outputs": outputs,
                    "operations": [node.op_type for node in model.graph.node],
                    "hidden_relu_layers": sum(
                        node.op_type == "Relu" for node in model.graph.node
                    ),
                    # A source-name grouping, not a claim of functional equivalence.
                    "original_model_group": Path(network)
                    .name.split("~", 1)[0]
                    .removesuffix(".gz")
                    .removesuffix(".onnx"),
                    "hidden_widths": [
                        next(
                            t.dims[-1]
                            for t in model.graph.initializer
                            if t.name == node.input[2]
                        )
                        for node in model.graph.node[:-1]
                        if node.op_type == "Gemm"
                    ],
                    "initializer_elements": sum(
                        math.prod(t.dims) for t in model.graph.initializer
                    ),
                    "output_comparisons": len(property_.comparisons)
                    + sum(
                        len(branch)
                        for alternatives in property_.disjunctions
                        for branch in alternatives
                    ),
                    "output_disjunction_alternatives": [
                        len(alternatives) for alternatives in property_.disjunctions
                    ],
                }
            except Unsupported as exc:
                entry["eligible"] = False
                entry["exclusion_reason"] = str(exc)
            entries.append(entry)
    if not entries:
        raise ValueError("Empty manifest")
    hardware = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "logical_cpus": os.cpu_count(),
    }
    if platform.system() == "Darwin":
        for key in ("hw.memsize", "hw.physicalcpu", "machdep.cpu.brand_string"):
            hardware[key] = subprocess.check_output(
                ["sysctl", "-n", key], text=True
            ).strip()
    acquisition = manifest.parent / "acquisition.json"
    return {
        "schema_version": 1,
        "created_utc": datetime.now(UTC).isoformat(),
        "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "manifest_path": str(manifest),
        "instances": entries,
        "audit_seconds": time.monotonic() - started,
        "support_policy": "Verification contract grammar; unsupported semantics only. No filename verdicts or outcome-based exclusions.",
        "execution": {
            "threads": threads,
            "sequential": True,
            "preparation_analysis": False,
        },
        "hardware": hardware,
        "acquisition": json.loads(acquisition.read_text())
        if acquisition.exists()
        else None,
        "python": platform.python_version(),
        "revision": _revision(),
        "packages": {
            name: importlib.metadata.version(name)
            for name in ("onnx", "numpy", "onnxruntime")
        },
        "reference_revisions": TOOLING,
    }


def run_experiment(
    manifest: Path,
    output: Path,
    *,
    threads: int = 1,
    verification: Verification = verify,
    stop_after: int | None = None,
    audit_only: bool = False,
) -> dict:
    """Audit all entries before solving; resume without overwriting saved records.

    ``verification`` permits controlled outcomes at the agreed experiment test seam.
    ``stop_after`` limits newly executed eligible instances, not their deadlines.
    Audit is separately measured selection work, never cached solver preparation.
    """
    manifest, output = manifest.resolve(), output.resolve()
    ExecutionLimits(1, threads)
    if stop_after is not None and stop_after < 1:
        raise ValueError("stop_after must be positive")
    output.mkdir(parents=True, exist_ok=True)
    lock = output / ".running"
    with lock.open("x") as stream:
        stream.write(str(os.getpid()))
    try:
        audit_path = output / "experiment.json"
        if audit_path.exists():
            audit = json.loads(audit_path.read_text())
            if (
                audit["manifest_sha256"]
                != hashlib.sha256(manifest.read_bytes()).hexdigest()
                or audit["manifest_path"] != str(manifest)
                or audit["execution"]["threads"] != threads
                or audit["revision"]["source_sha256"] != _revision()["source_sha256"]
            ):
                raise ValueError(
                    "Manifest, source, or execution settings changed; use a new output directory"
                )
            for entry in audit["instances"]:
                for artifact in entry["artifacts"].values():
                    if _artifact(Path(artifact["path"]))[1] != artifact:
                        raise ValueError("Artifact changed since audit")
        else:
            audit = _audit(manifest, threads)
            _save(audit_path, audit)
            (output / "instances.csv").write_bytes(manifest.read_bytes())
        if audit_only:
            return audit
        completed = 0
        for entry in audit["instances"]:
            path = output / "records" / f"{entry['id']}.json"
            if path.exists():
                continue
            record = {
                **entry,
                "preparation_seconds": 0.0,
                "preparation_analysis": False,
            }
            if entry["eligible"]:
                record.update(
                    {
                        "started_utc": datetime.now(UTC).isoformat(),
                        "invocation_seconds": None,
                        "result": asdict(
                            VerificationResult(
                                reason="interrupted",
                                diagnostic="Invocation started but no completed result was persisted; not automatically retried.",
                            )
                        ),
                    }
                )
                _save(path, record)
                started = time.monotonic()
                try:
                    result = verification(
                        Instance(
                            manifest.parent / entry["network"],
                            manifest.parent / entry["property"],
                        ),
                        ExecutionLimits(entry["timeout_seconds"], threads),
                    )
                except Exception as exc:  # noqa: BLE001 -- experiment retains unexpected eligible execution failures
                    result = VerificationResult(
                        reason="execution_error",
                        diagnostic=f"{type(exc).__name__}: {exc}",
                    )
                record["invocation_seconds"] = time.monotonic() - started
                record["result"] = asdict(result)
                completed += 1
            else:
                record["result"] = None
            _save(path, record)
            if stop_after is not None and completed >= stop_after:
                break
        return audit
    finally:
        lock.unlink()


def _statistics(values: list[float]) -> dict:
    if not values:
        return {"count": 0, "sum": 0, "min": None, "median": None, "max": None}
    return {
        "count": len(values),
        "sum": sum(values),
        "min": min(values),
        "median": statistics.median(values),
        "max": max(values),
    }


def report_experiment(output: Path) -> dict:
    """Regenerate JSON/Markdown from saved records alone; never invokes verification."""
    audit = json.loads((output / "experiment.json").read_text())
    outcomes, validation, reasons, exclusions = (
        Counter(),
        Counter(),
        Counter(),
        Counter(),
    )
    runtimes, solved_times, invocation_times, preparation_times = [], [], [], []
    missing, corrupt = [], []
    rows = []
    for entry in audit["instances"]:
        if not entry["eligible"]:
            exclusions[entry["exclusion_reason"]] += 1
            rows.append(
                f"| {entry['id']} | excluded | {entry['exclusion_reason']} | — | — |"
            )
            continue
        path = output / "records" / f"{entry['id']}.json"
        if not path.exists():
            missing.append(entry["id"])
            rows.append(f"| {entry['id']} | missing | not recorded | — | — |")
            continue
        try:
            record = json.loads(path.read_text())
            if any(record[k] != entry[k] for k in entry):
                raise ValueError("Record identity differs from audit")
            result = record["result"]
            if result["outcome"] not in ("sat", "unsat", "unknown"):
                raise ValueError("Invalid outcome")
            if result["validation"] not in (
                None,
                "strict",
                "tolerance_only",
                "invalid",
            ):
                raise ValueError("Invalid validation classification")
            if result["outcome"] == "sat" and result["validation"] not in (
                "strict",
                "tolerance_only",
            ):
                raise ValueError("SAT without accepted validation")
            if not isinstance(result["timings"], dict):
                raise ValueError("Invalid timings object")
            if not isinstance(result["reason"], str):
                raise ValueError("Invalid reason")
            runtime = result["timings"].get("total")
            if runtime is not None and (not math.isfinite(runtime) or runtime < 0):
                raise ValueError("Invalid runtime")
            for name in ("preparation_seconds", "invocation_seconds"):
                value = record[name]
                if value is not None and (not math.isfinite(value) or value < 0):
                    raise ValueError(f"Invalid {name}")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            corrupt.append({"id": entry["id"], "diagnostic": str(exc)})
            rows.append(f"| {entry['id']} | corrupt | invalid saved record | — | — |")
            continue
        outcomes[result["outcome"]] += 1
        validation[result["validation"] or "none"] += 1
        if record["invocation_seconds"] is not None:
            invocation_times.append(record["invocation_seconds"])
        if record["preparation_seconds"] is not None:
            preparation_times.append(record["preparation_seconds"])
        if runtime is not None:
            runtimes.append(runtime)
        if result["outcome"] != "unknown":
            if runtime is not None:
                solved_times.append(runtime)
        else:
            reasons[result["reason"]] += 1
        rows.append(
            f"| {entry['id']} | {result['outcome']} | {result['reason']} | "
            f"{result['validation'] or '—'} | {runtime if runtime is not None else 'unavailable'} |"
        )
    eligible = sum(entry["eligible"] for entry in audit["instances"])
    summary = {
        "reporter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "listed": len(audit["instances"]),
        "eligible": eligible,
        "excluded": sum(exclusions.values()),
        "exclusion_reasons": dict(exclusions),
        "recorded": sum(outcomes.values()),
        "missing": len(missing),
        "missing_ids": missing,
        "corrupt": corrupt,
        "solved_reported": outcomes["sat"] + outcomes["unsat"],
        "outcomes": dict(outcomes),
        "validation": dict(validation),
        "unresolved_reasons": dict(reasons),
        "runtime_seconds": {
            "all": _statistics(runtimes),
            "solved": _statistics(solved_times),
        },
        "invocation_seconds": _statistics(invocation_times),
        "preparation_seconds": _statistics(preparation_times),
        "audit_seconds": audit["audit_seconds"],
        "scoring": {
            "points": None,
            "accepted_sat_subset_points": 10 * outcomes["sat"],
            "accepted_sat_subset_instances": outcomes["sat"],
            "reference_revision": audit["reference_revisions"]["validator_scoring"],
            "missing_inputs": [
                "Artifact-matched other-tool outcomes and strict witness checks needed to assess conflicts and UNSAT correctness",
                "Complete participating-tool context for category normalization; cross-tool caches do not bind benchmark artifact hashes",
            ],
            "policy": "Pinned get_score awards 10 per accepted solve; time bonus disabled. Strict witnesses can refute UNSAT; tolerance-only witnesses earn SAT credit but cannot refute UNSAT. No score inferred from our own verdicts or filenames.",
        },
    }
    _save(output / "summary.json", summary)
    text = [
        "# Verification experiment report",
        "",
        f"Listed: {summary['listed']}; eligible: {eligible}; excluded: {summary['excluded']}.",
        f"Recorded eligible results: {summary['recorded']}; Missing records: {len(missing)}; corrupt records: {len(corrupt)}.",
        f"Solver-reported, accepted solves: {summary['solved_reported']}. Outcomes: {dict(outcomes)}.",
        f"Validation: {dict(validation)}. Unresolved reasons: {dict(reasons)}.",
        "",
        "## Interpretation",
        "",
        "SAT is accepted only after pinned FLOAT32 ONNX replay. Strict and tolerance-only classifications are separate; tolerance-only SAT does not refute an UNSAT claim. Numerical UNSAT is not an independently certified UNSAT or an exact-real proof. Solver outcomes are not independent ground truth. Filename labels never determine verdicts.",
        "",
        "## Timings and resources",
        "",
        "Whole-run time includes subprocess startup, reads/decompression, interpretation, encoding, solving, and validation. No startup overhead is subtracted; no kill-grace result gets solve credit. Invocation wall time additionally includes supervising/cleanup overhead. Preparation is a no-op (0 seconds); category eligibility audit is separately measured, not hidden preparation or cached solving analysis.",
        "",
        f"Runtime seconds: `{summary['runtime_seconds']}`.",
        f"Invocation seconds: `{summary['invocation_seconds']}`.",
        f"Audit seconds: {audit['audit_seconds']:.6f}.",
        f"Resources: `{audit['hardware']}`; execution: `{audit['execution']}`.",
        "Pinned replay uses 12 intra/inter-op CPU threads separately from the Gurobi Threads limit. No memory cap, performance tuning, or numerical tolerance tuning is applied.",
        "",
        "## Architecture and numerical scope",
        "",
        "Eligibility uses the verification contract's sequential FLOAT32 affine/ReLU/sigmoid/constant-reshape and supported conjunctive/disjunctive property grammar, independently of solve outcomes. Each eligible row's architecture descriptor records the actual formulation, tensor shapes, audited operations, hidden widths and ReLU depth, input/output dimensions, initializer count, and output comparison/alternative counts. Original-model groups are source-name groups, not evidence of functional equivalence. Depth comparisons may also vary width and neuron stability; no causal depth effect is inferred.",
        "Gurobi numerical defaults are unchanged; effective settings, package versions, witnesses, and validation diagnostics are retained in individual records. These are floating-point results, not exact-arithmetic certification.",
        "",
        "## Competition scoring",
        "",
        "Subset score unavailable: "
        + "; ".join(summary["scoring"]["missing_inputs"])
        + ".",
        f"Accepted SAT-only subset contribution: {summary['scoring']['accepted_sat_subset_points']} points across {outcomes['sat']} instances (10 each under pinned get_score; not the full eligible/category score). Numerical UNSAT contributions remain unassessed without artifact-matched cross-tool strict-witness evidence.",
        summary["scoring"]["policy"],
        "No ABC speed ratio or hardware-independent performance claim is made without matching artifacts and execution resources.",
        "",
        "## Per-instance records",
        "",
        "Manifest order identifies rows; original names and artifact hashes are in experiment.json and records/<id>.json.",
        "",
        "| ID | Outcome | Reason | Validation | Whole-run seconds |",
        "| --- | --- | --- | --- | --- |",
        *rows,
        "",
        "## Reproduce",
        "",
        "See docs/experiments.md for acquisition, audit, sequential execution, and solver-free report commands. Pinned references and source hashes are in experiment.json. Raw records are the authoritative report inputs.",
    ]
    (output / "report.md").write_text("\n".join(text) + "\n")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    acquire = commands.add_parser("acquire")
    acquire.add_argument("destination", type=Path)
    acquire.add_argument(
        "--category",
        choices=["sat_relu", "relusplitter_2026", "dist_shift_2023"],
        default="sat_relu",
    )
    for operation in ("audit", "run"):
        command = commands.add_parser(operation)
        command.add_argument("manifest", type=Path)
        command.add_argument("output", type=Path)
        command.add_argument("--threads", type=int, default=1)
        if operation == "run":
            command.add_argument("--stop-after", type=int)
    report = commands.add_parser("report")
    report.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.command == "acquire":
        print(acquire_category(args.destination, category=args.category))
    elif args.command == "report":
        print(json.dumps(report_experiment(args.output), indent=2))
    else:
        audit = run_experiment(
            args.manifest,
            args.output,
            threads=args.threads,
            audit_only=args.command == "audit",
            stop_after=getattr(args, "stop_after", None),
        )
        print(
            json.dumps(
                {
                    "listed": len(audit["instances"]),
                    "eligible": sum(e["eligible"] for e in audit["instances"]),
                }
            )
        )


if __name__ == "__main__":
    main()
