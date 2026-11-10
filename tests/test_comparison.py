import copy
import csv
import hashlib
import json
import subprocess
import sys

import pytest

from nvvcomp_gurobi.comparison import compare


def saved_pair():
    entry = {
        "id": "0000",
        "network": "onnx/model.onnx",
        "property": "vnnlib/query.vnnlib",
        "eligible": True,
        "exclusion_reason": None,
        "timeout_seconds": 100,
        "artifacts": {
            kind: {"uncompressed_sha256": kind * 16} for kind in ("onnx", "vnnlib")
        },
        "architecture": {
            "inputs": 2,
            "outputs": 2,
            "operations": ["Gemm", "Relu", "Gemm"],
            "hidden_widths": [10],
            "initializer_elements": 52,
        },
    }
    audit = {
        "category": "family",
        "version": "1.0",
        "instances": [entry],
        "reference_revisions": {"benchmark": "benchmark-pin"},
    }
    record = {
        **copy.deepcopy(entry),
        "preparation_seconds": 0,
        "result": {
            "outcome": "sat",
            "validation": "strict",
            "reason": "validated_witness",
            "timings": {"total": 2},
        },
    }
    abc = {
        "category": "family",
        "version": "1.0",
        "network": entry["network"],
        "property": entry["property"],
        "outcome": "sat",
        "validation": "strict",
        "run_seconds": 8,
        "preparation_seconds": 20,
        "artifact_sha256": {
            k: v["uncompressed_sha256"] for k, v in entry["artifacts"].items()
        },
        "execution_artifact_binding": False,
    }
    published = {
        "category": "family",
        "version": "1.0",
        "source": {"revision": "results-pin"},
        "records": [abc],
    }
    return audit, {"0000": record}, published


def test_comparison_distinguishes_source_identity_from_execution_binding():
    audit, records, published = saved_pair()
    evidence = compare(audit, records, published)
    row = evidence["instances"][0]
    assert row["match"] == "source_verified_execution_unbound"
    assert row["comparison"] == "both_same_answer"
    assert row["abc_over_gurobi_run_ratio"] == 4
    assert row["abc_over_gurobi_prepare_plus_run_ratio"] == 14
    assert evidence["populations"]["execution_bound"] == []
    assert evidence["populations"]["candidate_matched"] == ["0000"]
    assert evidence["runtime"]["paired_same_answer"]["ids"] == ["0000"]


@pytest.mark.parametrize(
    "change, expected",
    [
        (
            {"artifact_sha256": {"onnx": "different", "vnnlib": "vnnlib" * 16}},
            "artifact_mismatch",
        ),
        ({"version": "2.0"}, "version_mismatch"),
        ({"artifact_sha256": {}}, "identity_unverified"),
        ({"network": "onnx/other.onnx"}, "unmatched"),
    ],
)
def test_identity_is_not_inferred_from_category_or_manifest_position(change, expected):
    audit, records, published = saved_pair()
    published["records"][0].update(change)
    evidence = compare(audit, records, published)
    assert evidence["instances"][0]["match"] == expected
    assert evidence["populations"]["candidate_matched"] == []
    assert evidence["runtime"]["paired_same_answer"]["ids"] == []


@pytest.mark.parametrize(
    "scenario,expected",
    [
        ("missing", "missing_gurobi"),
        ("corrupt", "corrupt_gurobi"),
        ("excluded", "excluded"),
        ("duplicate", "ambiguous_abc"),
    ],
)
def test_all_listed_instances_remain_visible(scenario, expected):
    audit, records, published = saved_pair()
    if scenario == "missing":
        records.clear()
    elif scenario == "corrupt":
        records["0000"]["artifacts"]["onnx"]["uncompressed_sha256"] = "wrong"
    elif scenario == "excluded":
        audit["instances"][0].update(
            eligible=False, exclusion_reason="unsupported operation"
        )
    else:
        published["records"].append(copy.deepcopy(published["records"][0]))
    evidence = compare(audit, records, published)
    assert len(evidence["instances"]) == 1
    assert evidence["instances"][0]["comparison"] == expected
    assert evidence["runtime"]["paired_same_answer"]["ids"] == []


def test_extra_published_rows_and_missing_abc_are_explicit():
    audit, records, published = saved_pair()
    published["records"][0]["network"] = "onnx/smoke.onnx"
    evidence = compare(audit, records, published)
    assert evidence["instances"][0]["comparison"] == "missing_abc"
    assert evidence["unmatched_abc"][0]["network"] == "onnx/smoke.onnx"


@pytest.mark.parametrize(
    "runtime,preparation,expected,ratio",
    [
        (101, 20, "gurobi_only", None),
        (100, 20, "both_same_answer", 50),
        (None, None, "both_same_answer", None),
        (0, None, "both_same_answer", 0),
    ],
)
def test_raw_deadlines_and_unavailable_timings(runtime, preparation, expected, ratio):
    audit, records, published = saved_pair()
    published["records"][0].update(run_seconds=runtime, preparation_seconds=preparation)
    evidence = compare(audit, records, published)
    row = evidence["instances"][0]
    assert row["comparison"] == expected
    assert row["abc_over_gurobi_run_ratio"] == ratio
    if preparation is None:
        assert row["abc_over_gurobi_prepare_plus_run_ratio"] is None


@pytest.mark.parametrize(
    "tool,value",
    [("gurobi", -1), ("gurobi", float("nan")), ("abc", float("inf")), ("abc", "bad")],
)
def test_invalid_timing_records_are_explicit_not_successes(tool, value):
    audit, records, published = saved_pair()
    if tool == "gurobi":
        records["0000"]["result"]["timings"]["total"] = value
    else:
        published["records"][0]["run_seconds"] = value
    evidence = compare(audit, records, published)
    assert evidence["instances"][0]["comparison"] == "corrupt_" + tool
    assert evidence["runtime"]["paired_same_answer"]["ids"] == []


def test_statistics_state_populations_and_preserve_outcome_and_failure_counts():
    audit, records, published = saved_pair()
    evidence = compare(audit, records, published)
    assert evidence["outcomes"]["gurobi"] == {"sat": 1}
    assert evidence["runtime"]["paired_same_answer"]["gurobi_run_seconds"]["sum"] == 2
    assert evidence["runtime"]["paired_same_answer"]["abc_run_seconds"]["sum"] == 8
    assert (
        evidence["runtime"]["paired_same_answer"]["abc_over_gurobi_ratio_of_sums"] == 4
    )
    assert (
        evidence["runtime"]["paired_same_answer"][
            "median_abc_over_gurobi_prepare_plus_run_ratio"
        ]
        == 14
    )
    records["0000"]["result"].update(
        outcome="unknown", validation=None, reason="solver_error"
    )
    evidence = compare(audit, records, published)
    assert evidence["unresolved_reasons"]["gurobi"] == {"solver_error": 1}
    assert evidence["populations"]["abc_only"] == ["0000"]
    assert evidence["runtime"]["per_tool"]["gurobi"]["solved"]["ids"] == []
    assert (
        evidence["runtime"]["per_tool"]["gurobi"]["all_recorded"]["seconds"]["sum"] == 2
    )


def test_scoring_separates_accepted_sat_from_unassessed_unsat():
    audit, records, published = saved_pair()
    evidence = compare(audit, records, published)
    assert evidence["scoring"]["accepted_sat_subset"]["gurobi_points"] == 10
    assert evidence["scoring"]["accepted_sat_subset"]["abc_points"] == 10
    assert evidence["scoring"]["full_subset_points"] is None
    records["0000"]["result"].update(outcome="unsat", validation=None)
    published["records"][0].update(outcome="unsat", validation=None)
    evidence = compare(audit, records, published)
    assert evidence["scoring"]["accepted_sat_subset"]["ids"] == []
    assert evidence["scoring"]["unassessed_unsat_ids"] == ["0000"]


def test_structural_width_groups_hold_other_dimensions_fixed_not_weights_or_properties():
    audit, records, published = saved_pair()
    for ident, inputs, widths in [
        ("0001", 2, [20]),
        ("0002", 3, [30]),
        ("0003", 2, [10, 10]),
    ]:
        entry = copy.deepcopy(audit["instances"][0])
        entry["id"] = ident
        entry["architecture"].update(inputs=inputs, hidden_widths=widths)
        audit["instances"].append(entry)
    evidence = compare(audit, records, published)
    assert evidence["structural_width_groups"] == [
        {
            "ids": ["0000", "0001"],
            "inputs": 2,
            "outputs": 2,
            "operations": ["Gemm", "Relu", "Gemm"],
            "hidden_layer_count": 1,
            "hidden_widths": [[10], [20]],
        }
    ]
    assert evidence["instances"][0]["structural_width_group"] == "W01"
    assert evidence["instances"][2]["structural_width_group"] is None


@pytest.mark.parametrize(
    "check_result,identity,classification,status",
    [
        ("correct", True, "strict", "both_same_answer"),
        ("correct_up_to_tolerance", True, "tolerance_only", "both_same_answer"),
        ("unsupported", True, "unsupported", "gurobi_only"),
        ("correct", False, None, "gurobi_only"),
    ],
)
def test_cli_regenerates_evidence_from_raw_saved_files_without_networks(
    tmp_path, check_result, identity, classification, status
):
    audit, records, published = saved_pair()
    experiment = tmp_path / "experiment"
    (experiment / "records").mkdir(parents=True)
    (experiment / "experiment.json").write_text(json.dumps(audit))
    (experiment / "records/0000.json").write_text(json.dumps(records["0000"]))
    source_dir = tmp_path / "published"
    source_dir.mkdir()
    csv_row = [
        "family",
        "repo/benchmarks/family/1.0/onnx/model.onnx",
        "repo/benchmarks/family/1.0/vnnlib/query.vnnlib",
        "20",
        "sat",
        "8",
    ]
    with (source_dir / "results.csv").open("w") as stream:
        csv.writer(stream).writerow(csv_row)
    witness = b"retained witness bytes"
    (source_dir / "model_query.counterexample.gz").write_bytes(witness)
    normalized_row = [*csv_row[:4], "violated", csv_row[5]]
    check = {
        "schema_version": 1,
        "checker_version": "vnncomp2026-cex-1",
        "benchmark": {
            "category": "2026_family",
            "version": "1.0",
            "network_field": "model",
            "property_field": "query",
        },
        "results_row_identity": hashlib.sha256(
            json.dumps(normalized_row, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "witness_sha256": hashlib.sha256(witness).hexdigest(),
        "result": "correct",
        "provider": "CPUExecutionProvider",
    }
    check["result"] = check_result
    if not identity:
        check["results_row_identity"] = "different row"
    (source_dir / "model_query.counterexample.check.json").write_text(json.dumps(check))
    files = [
        {"path": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in source_dir.iterdir()
    ]
    source = {
        "category": "family",
        "version": "1.0",
        "results_csv": "results.csv",
        "files": files,
        "artifacts": {
            audit["instances"][0][k]: {
                "sha256": published["records"][0]["artifact_sha256"][kind]
            }
            for k, kind in (("network", "onnx"), ("property", "vnnlib"))
        },
    }
    (source_dir / "source.json").write_text(json.dumps(source))
    output = tmp_path / "evidence"
    command = [
        sys.executable,
        "-m",
        "nvvcomp_gurobi.comparison",
        str(experiment),
        str(source_dir),
        str(output),
        "--category",
        "family",
        "--version",
        "1.0",
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)
    evidence = json.loads((output / "evidence.json").read_text())
    assert evidence["counts"] == {status: 1}
    assert evidence["instances"][0]["abc"]["validation"] == classification
    assert "0000" in (output / "instances.md").read_text()
    saved = (output / "evidence.json").read_bytes()
    subprocess.run(command, check=True, capture_output=True, text=True)
    assert (output / "evidence.json").read_bytes() == saved
    (source_dir / "results.csv").write_text("tampered")
    failure = subprocess.run(command, capture_output=True, text=True)
    assert failure.returncode != 0
    assert "hash mismatch" in failure.stderr


@pytest.mark.parametrize(
    "outcome,validation,abc_outcome,expected,conflict",
    [
        ("unknown", None, "unsat", "abc_only", "none"),
        ("sat", "strict", "unknown", "gurobi_only", "none"),
        ("unknown", None, "timeout", "neither", "none"),
        ("sat", "strict", "unsat", "disagreement", "strict_witness_refutes_unsat"),
        (
            "sat",
            "tolerance_only",
            "unsat",
            "disagreement",
            "tolerance_only_does_not_refute_unsat",
        ),
        ("sat", "invalid", "sat", "abc_only", "none"),
    ],
)
def test_outcome_comparison_never_uses_timeout_as_success(
    outcome, validation, abc_outcome, expected, conflict
):
    audit, records, published = saved_pair()
    records["0000"]["result"].update(
        outcome=outcome, validation=validation, reason="timeout"
    )
    published["records"][0]["outcome"] = abc_outcome
    evidence = compare(audit, records, published)
    row = evidence["instances"][0]
    assert row["comparison"] == expected
    assert row["conflict"] == conflict
    assert row["abc_over_gurobi_run_ratio"] is None
    assert evidence["runtime"]["paired_same_answer"]["ids"] == []
