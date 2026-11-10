"""Exercise the generated upstream runner, not a parallel archive implementation."""

import gzip
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "tests/fixtures/runner/run_instances.sh"


def run_runner(tmp_path, instance, *, result=None):
    runner = tmp_path / "runner.sh"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/adapt_runner.py"),
            str(UPSTREAM),
            str(runner),
        ],
        check=True,
    )
    base = tmp_path / "node"
    ce_dir = base / "logs/counterexamples/sat_relu"
    ce_dir.mkdir(parents=True)
    (ce_dir / "network_property.counterexample").write_text("stale witness\n")
    bench = base / "benchmarks/sat_relu/1.0"
    bench.mkdir(parents=True)
    (bench / "network.onnx").write_bytes(instance.onnx_path.read_bytes())
    (bench / "property.vnnlib").write_bytes(instance.vnnlib_path.read_bytes())
    (bench / "instances.csv").write_text("network.onnx,property.vnnlib,30\n")
    toolkit = base / "toolkit"
    toolkit.mkdir()
    if result is None:
        (toolkit / "tool").symlink_to(ROOT, target_is_directory=True)
    else:
        tool = toolkit / "tool"
        tool.mkdir()
        (tool / "prepare_instance.sh").write_text("exit 0\n")
        run = tool / "run_instance.sh"
        run.write_text("#!/bin/bash\ncat > \"$5\" <<'RESULT'\n" + result + "RESULT\n")
        run.chmod(0o755)
    # Only infrastructure is substituted: no AWS callback or GNU utilities on macOS.
    helpers = tmp_path / "helpers.sh"
    helpers.write_text(
        "log_superstage() { :; }; log_stage() { :; }; log_info() { :; }; "
        "log_box_open() { :; }; log_box_note() { :; }; log_box_close() { :; }; "
        "log_wall() { cat; }; "
        'timeout() { shift; "$@"; }; '
        "date() { echo 100.00; }\n"
    )
    env = dict(
        os.environ,
        NVVCOMP_BASE_DIR=str(base),
        NVVCOMP_BENCH_REL="benchmarks/sat_relu/1.0",
        NVVCOMP_NO_REPORT="1",
        COMP_LOG_LIB=str(helpers),
        competition_year="2026",
        benchmark_name="sat_relu",
        vnnlib_version="1.0",
        script_dir="tool",
        run_as_root="false",
        run_networks="all",
        task_id="integration-test",
        ROOT_URL="unused",
        TMPDIR=str(tmp_path),
    )
    subprocess.run(["bash", str(runner)], env=env, check=True)
    return base, tmp_path / "result_integration-test.txt"


@pytest.mark.solver
def test_runner_archive_is_directly_accepted_by_pinned_validator(
    instance_factory, tmp_path, monkeypatch
):
    instance = instance_factory("(assert (>= Y_0 0.5))\n(assert (<= Y_1 0))")
    base, output = run_runner(tmp_path, instance)
    assert output.read_text().startswith("sat\n((X_0 ")
    archive = next((base / "logs/counterexamples/sat_relu").glob("*.counterexample"))
    # Exactly what check_results.sh and export_results.sh do, with no extraction.
    compressed = archive.with_suffix(".counterexample.gz")
    with gzip.open(compressed, "wb") as stream:
        stream.write(archive.read_bytes())
    monkeypatch.chdir(tmp_path)
    from nvvcomp_gurobi._vendor.counterexamples import get_ce_diff

    classification, _ = get_ce_diff(
        str(instance.onnx_path), str(instance.vnnlib_path), str(compressed), 1e-4, 0.0
    )
    assert classification == "correct"
    assert ",sat," in (base / "logs/results_sat_relu.csv").read_text()


@pytest.mark.parametrize(
    "result",
    [
        "sat\n",
        "sat\nnot a witness\n",
        "sat\n((X_0 nan))\n",
        "sat\n((X_0 1e999))\n",
        "sat\n((X_0 1) (X_0 0))\n",
        "sat\n((X_0 1))\nunsat\n",
    ],
)
def test_runner_rejects_malformed_sat_without_archiving(
    instance_factory, tmp_path, result
):
    instance = instance_factory("(assert (>= Y_0 0))")
    base, output = run_runner(tmp_path, instance, result=result)
    assert output.read_text() == result
    assert not list((base / "logs/counterexamples/sat_relu").glob("*.counterexample"))
    assert (
        ",error_invalid_counterexample,"
        in (base / "logs/results_sat_relu.csv").read_text()
    )


@pytest.mark.parametrize("result", ["unsat\n", "unknown\n", "timeout\n", "error\n"])
def test_runner_preserves_non_sat_results_without_counterexample(
    instance_factory, tmp_path, result
):
    instance = instance_factory("(assert (>= Y_0 0))")
    base, output = run_runner(tmp_path, instance, result=result)
    assert output.read_text() == result
    assert not list((base / "logs/counterexamples/sat_relu").glob("*.counterexample"))
    assert f",{result.strip()}," in (base / "logs/results_sat_relu.csv").read_text()


@pytest.mark.parametrize("header", ["sat\n", "sat\r\n", "violated\n"])
def test_runner_preserves_sat_file_and_archives_exact_witness_body(
    instance_factory, tmp_path, header
):
    instance = instance_factory("(assert (>= Y_0 0))")
    body = "((X_0 +1e0)\n (X_1 -0.5)\n (Y_0 1)\n (Y_1 0))\n"
    base, output = run_runner(tmp_path, instance, result=header + body)
    assert output.read_bytes() == (header + body).encode()
    archive = base / "logs/counterexamples/sat_relu/network_property.counterexample"
    assert archive.read_bytes() == body.encode()


def test_adapter_never_overwrites_existing_output(tmp_path):
    output = tmp_path / "runner.sh"
    output.write_text("user work\n")
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/adapt_runner.py"),
            str(UPSTREAM),
            str(output),
        ],
        capture_output=True,
    )
    assert completed.returncode != 0
    assert output.read_text() == "user work\n"


def test_adapter_refuses_drifted_runner_without_creating_output(tmp_path):
    source = tmp_path / "upstream.sh"
    source.write_bytes(UPSTREAM.read_bytes() + b"\n# changed\n")
    output = tmp_path / "runner.sh"
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/adapt_runner.py"),
            str(source),
            str(output),
        ],
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 2
    assert "does not match pinned revision" in completed.stderr
    assert not output.exists()
