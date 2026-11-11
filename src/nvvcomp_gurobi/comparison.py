"""Solver-free cross-tool evidence. Measurement identity is not inferred from names."""

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median


def _valid_time(value):
    return value is None or (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value >= 0
    )


def _statistics(values):
    return {
        "count": len(values),
        "sum": sum(values),
        "min": min(values) if values else None,
        "median": median(values) if values else None,
        "max": max(values) if values else None,
    }


def _local_measurement(entry: dict, record) -> dict | None:
    if not isinstance(record, dict) or any(
        record.get(k) != v for k, v in entry.items()
    ):
        return None
    result = record.get("result")
    if not isinstance(result, dict) or not isinstance(result.get("timings"), dict):
        return None
    if (
        result.get("outcome") not in ("sat", "unsat", "unknown")
        or "validation" not in result
        or result["validation"] not in (None, "strict", "tolerance_only", "invalid")
    ):
        return None
    measurement = {
        "outcome": result["outcome"],
        "validation": result["validation"],
        "reason": result.get("reason", "unavailable"),
        "run_seconds": result["timings"].get("total"),
        "preparation_seconds": record.get("preparation_seconds"),
    }
    return _measurement(measurement, entry["timeout_seconds"])


def _measurement(measurement: dict, timeout: float) -> dict | None:
    if measurement.get("outcome") not in (
        "sat",
        "unsat",
        "unknown",
        "error",
        "timeout",
    ) or not all(
        _valid_time(measurement.get(k)) for k in ("run_seconds", "preparation_seconds")
    ):
        return None
    accepted = measurement["outcome"] == "unsat" or (
        measurement["outcome"] == "sat"
        and measurement.get("validation") in ("strict", "tolerance_only")
    )
    runtime = measurement.get("run_seconds")
    return {
        **measurement,
        "solved": accepted and (runtime is None or runtime <= timeout),
    }


def _runtime_population(
    instances: list[dict], tool: str, population: str, field: str
) -> dict:
    rows = [
        r
        for r in instances
        if tool in r
        and r[tool].get(field) is not None
        and (population != "solved" or r[tool]["solved"])
    ]
    return {
        "ids": [r["id"] for r in rows],
        "seconds": _statistics([r[tool][field] for r in rows]),
    }


def compare(audit: dict, records: dict, published: dict) -> dict:
    """Compare an audited experiment with normalized published measurements.

    Inputs are saved JSON objects, not models or solver dependencies. Artifact hashes
    identify the pinned source; execution_artifact_binding additionally requires
    evidence that those exact bytes were used for the published measurement.
    """
    instances: list[dict] = []
    candidates, bound, paired = [], [], []
    sat_ids, unsat_ids = [], []
    sat_points = {"gurobi": 0, "abc": 0}
    used = set()
    for entry in audit["instances"]:
        ident = entry["id"]
        path_matches = [
            r
            for r in published["records"]
            if r["network"] == entry["network"] and r["property"] == entry["property"]
        ]
        matches = [
            r
            for r in path_matches
            if r["category"] == audit["category"] and r["version"] == audit["version"]
        ]
        row = {
            "id": ident,
            "network": entry["network"],
            "property": entry["property"],
            "architecture": entry["architecture"],
            "exclusion_reason": entry["exclusion_reason"],
            "match": "unmatched",
            "comparison": "not_comparable",
        }
        instances.append(row)
        if not entry["eligible"]:
            row["comparison"] = "excluded"
            continue
        local_measurement = _local_measurement(entry, records.get(ident))
        local_status = (
            "missing_gurobi"
            if ident not in records
            else "corrupt_gurobi"
            if local_measurement is None
            else None
        )
        if local_measurement is not None:
            row["gurobi"] = local_measurement
        if len(matches) != 1:
            row["comparison"] = "ambiguous_abc" if matches else "missing_abc"
            if not matches and path_matches:
                row["match"] = "version_mismatch"
                row["comparison"] = "not_comparable"
            continue
        used.update(i for i, r in enumerate(published["records"]) if r is matches[0])
        match = "unmatched"
        abc = matches[0] if len(matches) == 1 else None
        if abc is not None:
            abc_measurement = _measurement(abc, entry["timeout_seconds"])
            if abc_measurement is not None:
                row["abc"] = abc_measurement
            hashes = abc.get("artifact_sha256", {})
            if (
                abc["version"] != audit["version"]
                or abc["category"] != audit["category"]
            ):
                match = "version_mismatch"
            elif not all(hashes.get(k) for k in ("onnx", "vnnlib")):
                match = "identity_unverified"
            elif any(
                hashes[k] != entry["artifacts"][k]["uncompressed_sha256"]
                for k in hashes
            ):
                match = "artifact_mismatch"
            else:
                match = (
                    "execution_bound"
                    if abc["execution_artifact_binding"]
                    else "source_verified_execution_unbound"
                )
        if abc is None or match not in (
            "execution_bound",
            "source_verified_execution_unbound",
        ):
            row["match"] = match
            continue
        row["match"] = match
        candidates.append(ident)
        if abc["execution_artifact_binding"]:
            bound.append(ident)
        if local_status is not None:
            row["comparison"] = local_status
            continue
        local = records[ident]
        result = local["result"]
        if "abc" not in row:
            row["comparison"] = "corrupt_abc"
            continue
        gurobi_solved = row["gurobi"]["solved"]
        abc_solved = row["abc"]["solved"]
        gurobi_run = row["gurobi"]["run_seconds"]
        abc_run = row["abc"]["run_seconds"]
        same = gurobi_solved and abc_solved and result["outcome"] == abc["outcome"]
        comparison = (
            "both_same_answer"
            if same
            else "disagreement"
            if gurobi_solved and abc_solved
            else "gurobi_only"
            if gurobi_solved
            else "abc_only"
            if abc_solved
            else "neither"
        )
        conflict = "none"
        if {result["outcome"], abc["outcome"]} == {"sat", "unsat"}:
            witness = result if result["outcome"] == "sat" else abc
            conflict = (
                "strict_witness_refutes_unsat"
                if witness["validation"] == "strict"
                else "tolerance_only_does_not_refute_unsat"
                if witness["validation"] == "tolerance_only"
                else "unvalidated_witness_does_not_refute_unsat"
            )
        if same and gurobi_run is not None and gurobi_run > 0 and abc_run is not None:
            paired.append(ident)
        gurobi_prep, abc_prep = (
            local.get("preparation_seconds"),
            abc.get("preparation_seconds"),
        )
        ratio = abc_run / gurobi_run if ident in paired else None
        total_ratio = (
            (abc_run + abc_prep) / (gurobi_run + gurobi_prep)
            if ident in paired and abc_prep is not None and gurobi_prep is not None
            else None
        )
        row.update(
            {
                "id": ident,
                "network": entry["network"],
                "property": entry["property"],
                "architecture": entry["architecture"],
                "match": "execution_bound"
                if ident in bound
                else "source_verified_execution_unbound",
                "comparison": comparison,
                "conflict": conflict,
                "conflict_execution_bound": ident in bound,
                "abc_over_gurobi_run_ratio": ratio,
                "abc_over_gurobi_prepare_plus_run_ratio": total_ratio,
            }
        )
    sat_ids_by_tool = {"gurobi": [], "abc": []}
    for row in instances:
        for tool in ("gurobi", "abc"):
            measurement = row.get(tool)
            if measurement is None or (tool == "abc" and row["id"] not in candidates):
                continue
            if (
                measurement["solved"]
                and measurement["outcome"] == "sat"
                and measurement.get("run_seconds") is not None
            ):
                sat_points[tool] += 10
                sat_ids_by_tool[tool].append(row["id"])
                if row["id"] not in sat_ids:
                    sat_ids.append(row["id"])
            if (
                measurement["solved"]
                and measurement["outcome"] == "unsat"
                and row["id"] not in unsat_ids
            ):
                unsat_ids.append(row["id"])
    ratios = [
        r["abc_over_gurobi_run_ratio"]
        for r in instances
        if r.get("abc_over_gurobi_run_ratio") is not None
    ]
    shapes = defaultdict(list)
    for row in instances:
        a = row["architecture"]
        row["structural_width_group"] = None
        if all(k in a for k in ("inputs", "outputs", "operations", "hidden_widths")):
            shapes[
                (
                    a["inputs"],
                    a["outputs"],
                    tuple(a["operations"]),
                    len(a["hidden_widths"]),
                )
            ].append(row)
    groups = []
    for (inputs, outputs, operations, depth), rows in shapes.items():
        widths = sorted({tuple(r["architecture"]["hidden_widths"]) for r in rows})
        if len(widths) < 2:
            continue
        groups.append(
            {
                "ids": [r["id"] for r in rows],
                "inputs": inputs,
                "outputs": outputs,
                "operations": list(operations),
                "hidden_layer_count": depth,
                "hidden_widths": [list(w) for w in widths],
            }
        )
        for row in rows:
            row["structural_width_group"] = f"W{len(groups):02d}"
    pair_rows = [r for r in instances if r["id"] in paired]
    gurobi_paired_times = [r["gurobi"]["run_seconds"] for r in pair_rows]
    abc_paired_times = [r["abc"]["run_seconds"] for r in pair_rows]
    total_ratios = [
        r["abc_over_gurobi_prepare_plus_run_ratio"]
        for r in pair_rows
        if r["abc_over_gurobi_prepare_plus_run_ratio"] is not None
    ]
    return {
        "instances": instances,
        "structural_width_groups": groups,
        "unmatched_abc": [
            r for i, r in enumerate(published["records"]) if i not in used
        ],
        "populations": {
            "candidate_matched": candidates,
            "execution_bound": bound,
            **{
                status: [r["id"] for r in instances if r["comparison"] == status]
                for status in sorted({r["comparison"] for r in instances})
            },
        },
        "counts": dict(Counter(r["comparison"] for r in instances)),
        "outcomes": {
            tool: dict(Counter(r[tool]["outcome"] for r in instances if tool in r))
            for tool in ("gurobi", "abc")
        },
        "unresolved_reasons": {
            tool: dict(
                Counter(
                    r[tool].get("reason", r[tool]["outcome"])
                    for r in instances
                    if tool in r and not r[tool]["solved"]
                )
            )
            for tool in ("gurobi", "abc")
        },
        "scoring": {
            "accepted_sat_subset": {
                "ids": sat_ids,
                "gurobi_points": sat_points["gurobi"],
                "abc_points": sat_points["abc"],
                "ids_by_tool": sat_ids_by_tool,
                "abc_execution_binding_required": True,
            },
            "unassessed_unsat_ids": unsat_ids,
            "full_subset_points": None,
            "missing_inputs": [
                "Execution-bound benchmark identities for published measurements and checks",
                "Complete artifact-matched participating-tool conflict context for UNSAT and category normalization",
            ],
        },
        "runtime": {
            "per_tool": {
                tool: {
                    population: _runtime_population(instances, tool, population, field)
                    for population, field in (
                        ("all_recorded", "run_seconds"),
                        ("solved", "run_seconds"),
                        ("preparation", "preparation_seconds"),
                    )
                }
                for tool in ("gurobi", "abc")
            },
            "paired_same_answer": {
                "ids": paired,
                "gurobi_run_seconds": _statistics(gurobi_paired_times),
                "abc_run_seconds": _statistics(abc_paired_times),
                "abc_over_gurobi_ratio_of_sums": sum(abc_paired_times)
                / sum(gurobi_paired_times)
                if gurobi_paired_times
                else None,
                "median_abc_over_gurobi_run_ratio": median(ratios) if ratios else None,
                "prepare_plus_run_ratio_ids": [
                    r["id"]
                    for r in pair_rows
                    if r["abc_over_gurobi_prepare_plus_run_ratio"] is not None
                ],
                "median_abc_over_gurobi_prepare_plus_run_ratio": median(total_ratios)
                if total_ratios
                else None,
            },
        },
    }


def _published(directory: Path) -> dict:
    source = json.loads((directory / "source.json").read_text())
    for item in source["files"]:
        if (
            hashlib.sha256((directory / item["path"]).read_bytes()).hexdigest()
            != item["sha256"]
        ):
            raise ValueError(f"Published file hash mismatch: {item['path']}")
    path = directory / source["results_csv"]
    records = []
    with path.open() as stream:
        for number, raw in enumerate(csv.reader(stream), 1):
            if len(raw) != 6:
                raise ValueError(f"Expected six CSV fields at row {number}")
            category, network, prop, prep, outcome, run = raw

            # Require explicit version/category paths on both artifacts. Preserve
            # smoke rows and other categories as unmatched rather than dropping them.
            def split(value, kind):
                parts = Path(value).parts
                index = parts.index("benchmarks")
                if parts[index + 3] != kind:
                    raise ValueError(f"Unsupported artifact field: {value}")
                return parts[index + 1], parts[index + 2], "/".join(parts[index + 3 :])

            ncat, version, relative_network = split(network, "onnx")
            pcat, pversion, relative_property = split(prop, "vnnlib")
            valid_paths = category == ncat == pcat and version == pversion
            normalized = {
                "sat": "sat",
                "violated": "sat",
                "unsat": "unsat",
                "holds": "unsat",
                "timeout": "timeout",
                "timed-out": "timeout",
                "unknown": "unknown",
                "error": "error",
            }.get(outcome.lower(), "unknown")
            validation = None
            check_status = "not_applicable"
            if normalized == "sat":
                stem = f"{Path(network).stem}_{Path(prop).stem}.counterexample"
                check_path = path.parent / (stem + ".check.json")
                witness_path = path.parent / (stem + ".gz")
                check_status = "missing_check"
                if check_path.exists() and witness_path.exists():
                    check = json.loads(check_path.read_text())
                    row_for_check = [*raw[:4], "violated", raw[5]]
                    row_hash = hashlib.sha256(
                        json.dumps(
                            row_for_check, sort_keys=True, separators=(",", ":")
                        ).encode()
                    ).hexdigest()
                    expected = {
                        "category": "2026_" + category,
                        "version": version,
                        "network_field": Path(network).stem,
                        "property_field": Path(prop).stem,
                    }
                    if (
                        check.get("results_row_identity") == row_hash
                        and check.get("witness_sha256")
                        == hashlib.sha256(witness_path.read_bytes()).hexdigest()
                        and check.get("benchmark") == expected
                        and check.get("schema_version") == 1
                        and check.get("checker_version") == "vnncomp2026-cex-1"
                        and check.get("provider") == "CPUExecutionProvider"
                    ):
                        validation = {
                            "correct": "strict",
                            "correct_up_to_tolerance": "tolerance_only",
                            "unsupported": "unsupported",
                        }.get(check["result"], "invalid")
                        check_status = (
                            "published_cache_row_and_witness_verified_execution_unbound"
                        )
                    else:
                        check_status = "check_identity_mismatch"
            artifacts = source["artifacts"]
            hashes = {
                kind: artifacts[relative]["sha256"]
                for kind, relative in (
                    ("onnx", relative_network),
                    ("vnnlib", relative_property),
                )
                if valid_paths
                and version == source["version"]
                and category == source["category"]
                and relative in artifacts
            }
            records.append(
                {
                    "row": number,
                    "category": category if valid_paths else "inconsistent_paths",
                    "version": version,
                    "network": relative_network,
                    "property": relative_property,
                    "outcome": normalized,
                    "raw_outcome": outcome,
                    "validation": validation,
                    "check_status": check_status,
                    "run_seconds": float(run),
                    "preparation_seconds": float(prep),
                    "artifact_sha256": hashes,
                    "execution_artifact_binding": False,
                }
            )
    return {"source": source, "records": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    parser.add_argument("published", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--category", required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    audit_path = args.experiment / "experiment.json"
    audit = json.loads(audit_path.read_text())
    audit.update(category=args.category, version=args.version)
    records = {}
    for entry in audit["instances"]:
        path = args.experiment / "records" / f"{entry['id']}.json"
        if path.exists():
            try:
                records[entry["id"]] = json.loads(path.read_text())
            except (OSError, ValueError):
                records[entry["id"]] = {}
    published = _published(args.published)
    evidence = compare(audit, records, published)
    evidence["provenance"] = {
        "published": published["source"],
        "experiment_sha256": hashlib.sha256(audit_path.read_bytes()).hexdigest(),
        "comparison_source_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "published_source_sha256": hashlib.sha256(
            (args.published / "source.json").read_bytes()
        ).hexdigest(),
        "record_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted((args.experiment / "records").glob("*.json"))
        },
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "evidence.json").write_text(
        json.dumps(evidence, indent=2, allow_nan=False) + "\n"
    )
    lines = [
        "# Per-instance comparison evidence",
        "",
        "All comparisons are conditional where execution artifact binding is unavailable. Ratios are ABC/Gurobi measured time, not hardware-normalized speedups. W labels group structural descriptors only, not weights or properties.",
        "",
        "| ID | Network | Inputs | Hidden widths | Elements | Width group | Match | Gurobi (validation) | ABC (validation) | Gurobi run s | ABC run s | ABC prep s | Comparison | ABC/G run |",
        "| --- | --- | ---: | --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | --- | ---: |",
    ]
    for row in evidence["instances"]:
        a, g, abc = row["architecture"], row.get("gurobi", {}), row.get("abc", {})
        lines.append(
            f"| {row['id']} | {Path(row['network']).name} | {a.get('inputs')} | {a.get('hidden_widths')} | {a.get('initializer_elements')} | {row['structural_width_group'] or '—'} | {row['match']} | {g.get('outcome', '—')} ({g.get('validation') or '—'}) | {abc.get('outcome', '—')} ({abc.get('validation') or '—'}) | {g.get('run_seconds')} | {abc.get('run_seconds')} | {abc.get('preparation_seconds')} | {row['comparison']} | {row.get('abc_over_gurobi_run_ratio')} |"
        )
    lines.extend(
        [
            "",
            "## Unmatched published rows",
            "",
            "```json",
            json.dumps(evidence["unmatched_abc"], indent=2),
            "```",
        ]
    )
    (args.output / "instances.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
