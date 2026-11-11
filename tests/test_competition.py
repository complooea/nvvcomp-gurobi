import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_prepare_and_run_executable_contract_for_unsupported_query(
    instance_factory, tmp_path
):
    instance = instance_factory("(assert (> Y_0 0))")
    prepared = subprocess.run(
        [
            str(ROOT / "prepare_instance.sh"),
            "v1",
            "sat_relu",
            str(instance.onnx_path),
            str(instance.vnnlib_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(prepared.stdout)["preparation_seconds"] >= 0
    output = tmp_path / "result.txt"
    subprocess.run(
        [
            str(ROOT / "run_instance.sh"),
            "v1",
            "sat_relu",
            str(instance.onnx_path),
            str(instance.vnnlib_path),
            str(output),
            "10",
        ],
        check=True,
    )
    assert output.read_text() == "unknown\n"
    structured = json.loads(output.with_suffix(".txt.json").read_text())
    assert structured["outcome"] == "unknown"
    assert structured["reason"] == "unsupported"
    assert structured["provenance"]["category"] == "sat_relu"


@pytest.mark.solver
def test_unsat_executable_output_has_no_witness(instance_factory, tmp_path):
    instance = instance_factory("(assert (>= Y_0 2))")
    output = tmp_path / "result.txt"
    subprocess.run(
        [
            str(ROOT / "run_instance.sh"),
            "v1",
            "sat_relu",
            str(instance.onnx_path),
            str(instance.vnnlib_path),
            str(output),
            "30",
        ],
        check=True,
    )
    assert output.read_text() == "unsat\n"


def test_unsupported_protocol_version_is_not_accepted(tmp_path):
    completed = subprocess.run(
        [
            str(ROOT / "prepare_instance.sh"),
            "v2",
            "sat_relu",
            "unused.onnx",
            "unused.vnnlib",
        ],
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 2
    assert "invalid choice" in completed.stderr
