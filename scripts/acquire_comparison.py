"""Acquire pinned published evidence; never execute a verifier or validator.

Requires the original category files acquired by nvvcomp_gurobi.experiment.
Writes a new directory so existing evidence cannot be silently overwritten.
"""

import argparse
import csv
import gzip
import hashlib
import io
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen

RESULTS = "eea564f5d0a8751d8321a409214db14d03f452b8"
BENCHMARK = "303f2327a8e8411efc4457da03d2016ce42733cf"
BASE = f"https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/{RESULTS}/"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("benchmark", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument(
        "--category",
        default="sat_relu",
        choices=["sat_relu", "relusplitter_2026", "dist_shift_2023", "ml4acopf_2024"],
    )
    args = parser.parse_args()
    args.destination.mkdir(parents=True, exist_ok=False)
    category_path = f"alpha_beta_crown/2026_{args.category}/"

    def download(path):
        with urlopen(BASE + path, timeout=120) as response:
            data = response.read()
        # These are reference snapshots, not executable project Python modules.
        target = (
            args.destination / "raw" / (path + ".txt" if path.endswith(".py") else path)
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return {
            "path": str(target.relative_to(args.destination)),
            "url": BASE + path,
            "sha256": hashlib.sha256(data).hexdigest(),
        }

    paths = [
        "LICENSE",
        "README.md",
        "SCORING/process_results.py",
        "SCORING/settings.py",
        "SCORING/cex_checks.py",
        category_path + "results.csv",
    ]
    inventory = [download(p) for p in paths]
    rows = list(
        csv.reader(
            io.StringIO(
                (args.destination / "raw" / category_path / "results.csv").read_text()
            )
        )
    )
    witness_paths = []
    for row in rows:
        if row[4] == "sat":
            stem = f"{Path(row[1]).stem}_{Path(row[2]).stem}.counterexample"
            witness_paths.extend(
                [category_path + stem + ".gz", category_path + stem + ".check.json"]
            )
    with ThreadPoolExecutor(max_workers=8) as pool:
        inventory.extend(pool.map(download, witness_paths))

    # Verify local original bytes against the public pinned Git blobs, independently
    # of the experiment's hash inventory. This does not bind ABC execution to them.
    tree_url = f"https://api.github.com/repos/VNN-COMP/vnncomp2026_benchmarks/git/trees/{BENCHMARK}?recursive=1"
    with urlopen(tree_url, timeout=120) as response:
        tree_bytes = response.read()
    tree = json.loads(tree_bytes)
    if tree.get("truncated"):
        raise ValueError("Incomplete benchmark tree")
    blobs = {e["path"]: e["sha"] for e in tree["tree"]}
    artifacts = {}
    manifest = args.benchmark / "instances.csv"
    for row in csv.reader(io.StringIO(manifest.read_text())):
        for relative in row[:2]:
            path = args.benchmark / relative
            if not path.exists():
                path = Path(str(path) + ".gz")
            data = path.read_bytes()
            source_path = f"benchmarks/{args.category}/1.0/" + str(
                path.relative_to(args.benchmark)
            )
            blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
            if blobs[source_path] != blob:
                raise ValueError(f"Pinned Git blob mismatch: {source_path}")
            raw = gzip.decompress(data) if path.suffix == ".gz" else data
            artifacts[str(Path(relative))] = {
                "sha256": hashlib.sha256(raw).hexdigest(),
                "stored_sha256": hashlib.sha256(data).hexdigest(),
                "git_blob": blob,
                "source_path": source_path,
            }
    source_manifest = f"benchmarks/{args.category}/1.0/instances.csv"
    original_manifest = args.benchmark / "source-instances.csv"
    data = (original_manifest if original_manifest.exists() else manifest).read_bytes()
    if (
        hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        != blobs[source_manifest]
    ):
        raise ValueError("Manifest differs from pinned source")
    source_rows = list(csv.reader(io.StringIO(data.decode())))
    selected_rows = list(csv.reader(io.StringIO(manifest.read_text())))
    expected_rows = (
        [r for r in source_rows if r[0] == "./onnx/14_ieee_ml4acopf.onnx"]
        if args.category == "ml4acopf_2024"
        else source_rows
    )
    if selected_rows != expected_rows:
        raise ValueError("Selected manifest differs from pinned selection")
    for name, content in (
        ("source-instances.csv", data),
        ("instances.csv", manifest.read_bytes()),
    ):
        target = args.destination / name
        target.write_bytes(content)
        inventory.append({"path": name, "sha256": hashlib.sha256(content).hexdigest()})
    # Retain only the relevant tree entries, with their API URL, rather than the
    # entire unrelated benchmark inventory.
    source = {
        "results_revision": RESULTS,
        "benchmark_revision": BENCHMARK,
        "category": args.category,
        "version": "1.0",
        "results_csv": "raw/" + category_path + "results.csv",
        "benchmark_tree_url": tree_url,
        "benchmark_tree_sha256": hashlib.sha256(tree_bytes).hexdigest(),
        "manifest_sha256": hashlib.sha256(data).hexdigest(),
        "selected_manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "selection": "exact ./onnx/14_ieee_ml4acopf.onnx"
        if args.category == "ml4acopf_2024"
        else "entire version-1.0 manifest",
        "acquisition_source_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "artifacts": artifacts,
        "files": inventory,
        "execution_artifact_binding": False,
        "limitations": [
            "Published CSV and check caches do not pin execution benchmark bytes or commit",
            "ABC execution hardware, resources, tool revision and environment are absent from this result folder",
        ],
    }
    (args.destination / "source.json").write_text(json.dumps(source, indent=2) + "\n")


if __name__ == "__main__":
    main()
