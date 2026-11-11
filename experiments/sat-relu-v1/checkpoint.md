# First-execution inspection

Issue: https://github.com/complooea/nvvcomp-gurobi/issues/4

## Before solving

- Acquired all original category artifacts from benchmark revision
  `303f2327a8e8411efc4457da03d2016ce42733cf`; acquisition took 362.255 seconds.
  Original compressed bytes remain in `.benchmarks/sat-relu-v1`; the full URL,
  byte-size, and SHA256 inventory is embedded in `experiment.json`.
- Initial semantic audit identified opset 9 on all 100 networks, outside the
  previous verifier's declared opset range. Completed opset-9 support before
  solving, after checking ONNX Gemm-9/Relu-6 FLOAT32 semantics against the already
  supported schemas and running tiny known-answer SAT/UNSAT tests. No benchmark
  artifact or property was converted, rewritten, or selected by filename label.
- Complete final pre-solve audit: 100 listed, 100 eligible, zero exclusions;
  0.068048458 seconds. Every network is Gemm/ReLU/Gemm with two outputs; inputs
  5–95, hidden widths 29–1,071, initializer elements 234–100,676. Every property
  has two supported conjunctive output comparisons and finite input box bounds.
- Execution source revision: `a8d7247`; complete source/lockfile SHA256 identities
  are in `experiment.json`. Hardware: Apple M4, 10 logical/physical CPUs,
  17,179,869,184 bytes RAM, macOS 26.6.2, arm64; Python 3.12.16.
- A separate local license-capacity preflight successfully optimized a trivial
  2,101-variable model, beyond pip-bundled license capacity, with Gurobi 13.0.1.
  No license contents, credentials, or environment dump were recorded.

## Inspected first execution, before continuing

```sh
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/sat-relu-v1/instances.csv experiments/sat-relu-v1 --stop-after 1
```

Inspected `records/0000.json` before launching the remaining instances:

- `sat`, `validated_witness`, raw Gurobi status 2, classification `strict`.
- Whole-run 0.205458291 seconds; invocation 0.205513583 seconds. Interpretation,
  construction, solve, and replay times are retained separately.
- Witness: 27 inputs in the asserted box; ONNX-replayed outputs `[1.0, 0.0]`.
  Pinned validator accepted zero-tolerance input and output checks.
- Original/decompressed ONNX and property hashes match the pre-solve audit.
- Gurobi 13.0.1, gurobi-machinelearning 1.7.0, pinned CPU validator; default
  numerical settings unchanged, Threads=1, remaining solver TimeLimit
  99.880536459 seconds. Original 100-second whole-run limit retained.
- No unsupported conversion, missing dependency, license error, or replay failure.

Then launched the same `run` command without `--stop-after`, resuming the remaining
99 entries sequentially without overwriting the inspected first record.

## Measurement context

This is a local workstation measurement, not a dedicated/isolated competition
node. Lightweight editing, review, and non-solver fixture checks occurred during
the background run. No competing full benchmark or solver test suite was launched
during measurement. No affinity, memory cap, or performance/tolerance tuning was
introduced. Cross-machine runtime comparisons cannot establish intrinsic solver
superiority. The final report must be generated from saved records, not reruns.

The running experiment uses the source captured at `a8d7247`. A subsequent
report-only correction handles unavailable preparation timings; it does not alter
verification, selection, or solver execution. `summary.json` records the reporter
source hash independently of the experiment's original source identities.
