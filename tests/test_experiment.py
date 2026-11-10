import gzip
import json

import pytest

from nvvcomp_gurobi.experiment import report_experiment, run_experiment
from nvvcomp_gurobi.verification import VerificationResult


def test_run_accounts_for_manifest_and_saves_before_next_instance(
    tmp_path, instance_factory
):
    instance = instance_factory("(assert (>= Y_0 0))")
    # Manifest references are relative to its directory, including .gz fallback.
    compressed = instance.onnx_path.with_suffix(".onnx.gz")
    compressed.write_bytes(gzip.compress(instance.onnx_path.read_bytes()))
    instance.onnx_path.unlink()
    manifest = tmp_path / "instances.csv"
    manifest.write_text(
        "network.onnx,property.vnnlib,100\nnetwork.onnx.gz,property.vnnlib,37\n"
    )
    output = tmp_path / "experiment"
    calls = []

    def verification(original, limits):
        audit = json.loads((output / "experiment.json").read_text())
        assert len(audit["instances"]) == 2  # Entire audit precedes solving.
        assert original.vnnlib_path == instance.vnnlib_path
        assert limits.threads == 1
        calls.append(limits.timeout_seconds)
        if len(calls) == 1:
            return VerificationResult(
                outcome="sat",
                reason="validated_witness",
                validation="strict",
                witness={"inputs": [0, 0], "outputs": [0, 0]},
                solver_status=2,
                timings={"total": 2.0},
            )
        previous = json.loads((output / "records/0000.json").read_text())
        assert previous["result"]["validation"] == "strict"
        raise RuntimeError("unexpected conversion failure")

    run_experiment(manifest, output, verification=verification)
    assert calls == [100, 37]
    first = json.loads((output / "records/0000.json").read_text())
    failed = json.loads((output / "records/0001.json").read_text())
    assert first["artifacts"]["onnx"]["path"].endswith("network.onnx.gz")
    assert first["artifacts"]["onnx"]["sha256"]
    assert first["preparation_seconds"] == 0
    assert failed["result"]["outcome"] == "unknown"
    assert failed["result"]["reason"] == "execution_error"
    assert "unexpected conversion failure" in failed["result"]["diagnostic"]
    assert failed["eligible"] is True


def test_run_excludes_only_unsupported_semantics_and_resumes(
    tmp_path, instance_factory
):
    instance = instance_factory("(assert (>= Y_0 0))")
    unsupported = tmp_path / "unsupported.vnnlib"
    unsupported.write_text("(assert (or (>= Y_0 0) (<= Y_0 -1)))")
    manifest = tmp_path / "instances.csv"
    manifest.write_text(
        "network.onnx,unsupported.vnnlib,100\n"
        "network.onnx,property.vnnlib,100\n"
        "network.onnx,property.vnnlib,100\n"
    )
    output = tmp_path / "experiment"
    calls = []

    def verification(original, limits):
        calls.append(original)
        return VerificationResult(reason="timeout", solver_status=9)

    audit = run_experiment(manifest, output, audit_only=True, verification=verification)
    assert calls == []
    assert [e["eligible"] for e in audit["instances"]] == [False, True, True]
    assert "Unsupported VNN-LIB" in audit["instances"][0]["exclusion_reason"]
    run_experiment(manifest, output, stop_after=1, verification=verification)
    assert len(calls) == 1
    excluded = json.loads((output / "records/0000.json").read_text())
    assert excluded["result"] is None
    saved = (output / "records/0001.json").read_bytes()
    run_experiment(manifest, output, verification=verification)
    assert len(calls) == 2
    assert (output / "records/0001.json").read_bytes() == saved
    assert (
        json.loads((output / "records/0002.json").read_text())["result"]["reason"]
        == "timeout"
    )
    instance.vnnlib_path.write_text("changed artifact")
    with pytest.raises(ValueError, match="Artifact changed"):
        run_experiment(manifest, output, verification=verification)


def test_report_uses_saved_records_and_distinguishes_validation_and_missing(
    tmp_path, instance_factory
):
    instance_factory("(assert (>= Y_0 0))")
    manifest = tmp_path / "instances.csv"
    manifest.write_text("network.onnx,property.vnnlib,100\n" * 7)
    output = tmp_path / "experiment"
    results = iter(
        [
            VerificationResult(
                outcome="sat", validation="strict", timings={"total": 2}
            ),
            VerificationResult(
                outcome="sat", validation="tolerance_only", timings={"total": 4}
            ),
            VerificationResult(
                outcome="unsat", reason="infeasible", timings={"total": 6}
            ),
            VerificationResult(
                reason="validation_failed", validation="invalid", timings={"total": 8}
            ),
            VerificationResult(reason="timeout", timings={"total": 100}),
            VerificationResult(
                reason="error", diagnostic="conversion failed", timings={"total": 1}
            ),
        ]
    )
    run_experiment(
        manifest, output, stop_after=6, verification=lambda *_: next(results)
    )
    # This operation must need neither original artifacts nor a working verifier.
    (tmp_path / "network.onnx").unlink()
    summary = report_experiment(output)
    assert summary["listed"] == 7
    assert summary["eligible"] == 7
    assert summary["missing"] == 1
    assert summary["solved_reported"] == 3
    assert summary["outcomes"] == {"sat": 2, "unsat": 1, "unknown": 3}
    assert summary["validation"] == {
        "strict": 1,
        "tolerance_only": 1,
        "invalid": 1,
        "none": 3,
    }
    assert summary["unresolved_reasons"] == {
        "validation_failed": 1,
        "timeout": 1,
        "error": 1,
    }
    assert summary["runtime_seconds"]["all"]["sum"] == 121
    assert summary["runtime_seconds"]["solved"]["median"] == 4
    assert summary["scoring"]["points"] is None
    assert summary["scoring"]["accepted_sat_subset_points"] == 20
    assert "other-tool" in " ".join(summary["scoring"]["missing_inputs"])
    text = (output / "report.md").read_text()
    assert "not an independently certified UNSAT" in text
    assert "tolerance-only" in text
    assert "Missing records: 1" in text


@pytest.mark.parametrize(
    "damage", ["interrupted JSON", "[]", '{"result": null}', "timings"]
)
def test_report_flags_corrupt_results_and_keeps_exclusions(
    tmp_path, instance_factory, damage
):
    instance_factory("(assert (>= Y_0 0))")
    (tmp_path / "unsupported.vnnlib").write_text("(assert (= Y_0 0))")
    manifest = tmp_path / "instances.csv"
    manifest.write_text(
        "network.onnx,unsupported.vnnlib,100\nnetwork.onnx,property.vnnlib,100\n"
    )
    output = tmp_path / "experiment"
    run_experiment(manifest, output, verification=lambda *_: VerificationResult())
    path = output / "records/0001.json"
    if damage == "timings":
        record = json.loads(path.read_text())
        record["result"]["timings"] = []
        damage = json.dumps(record)
    path.write_text(damage)
    summary = report_experiment(output)
    assert summary["listed"] == 2
    assert summary["excluded"] == 1
    assert summary["eligible"] == 1
    assert summary["recorded"] == 0
    assert summary["corrupt"][0]["id"] == "0001"
    assert sum(summary["exclusion_reasons"].values()) == 1


def test_interrupted_invocation_is_recorded_not_silently_retried(
    tmp_path, instance_factory
):
    instance_factory("(assert (>= Y_0 0))")
    manifest = tmp_path / "instances.csv"
    manifest.write_text("network.onnx,property.vnnlib,100\n")
    output = tmp_path / "experiment"

    def interrupted(*_):
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        run_experiment(manifest, output, verification=interrupted)
    record = json.loads((output / "records/0000.json").read_text())
    assert record["result"]["outcome"] == "unknown"
    assert record["result"]["reason"] == "interrupted"
    run_experiment(manifest, output, verification=interrupted)
    summary = report_experiment(output)
    assert summary["unresolved_reasons"] == {"interrupted": 1}
