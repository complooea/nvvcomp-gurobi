# ReLUSplitter 1.0 Gurobi experiment

Issue #8, implementing the ReLU-depth slice of #7. This archive uses the existing
`verify(Instance, ExecutionLimits)` workflow with original artifacts, sequential
execution, one Gurobi thread, unchanged numerical defaults, and independent
FLOAT32 original-ONNX witness replay. Numerical UNSAT is not an independently
certified exact-real proof. Full benchmark execution is an experiment, not a test.

## Selection and graph audit

Benchmark revision: `303f2327a8e8411efc4457da03d2016ce42733cf`, category
`relusplitter_2026`, version `1.0`. All 120 original manifest rows have 180-second
deadlines. Acquisition preserves 125 files: the manifest, 104 distinct ONNX graphs,
and 20 distinct properties. Every selected graph/property was interpreted before
execution. All are eligible: static FLOAT32 sequential Gemm/ReLU graphs with
784 inputs, 10 outputs, and nine output-comparison alternatives per query.

The source-name groups below are audited, not inferred from generator promises:

| Original-model group | Original queries / hidden ReLU layers | Generated queries / hidden ReLU layers |
| --- | --- | --- |
| model_0_0 | 2 / 4 | 10 / 5 |
| model_1_1 | 8 / 5 | 40 / 6 |
| model_2_2 | 4 / 4 | 20 / 5 |
| model_3_3 | 6 / 5 | 30 / 6 |

Across queries, depths 4/5/6 occur 6/44/70 times. Four-layer originals have widths
`[128,256,256,256]`; five-layer originals have `[128,256,256,256,256]`. Generated
variants prepend a width-256 ReLU layer to those width sequences. Group names
associate files with their original-model filename prefix; they do **not** prove
functional equivalence. Width and neuron stability also vary, so this population
does not isolate a causal depth effect. Each row's complete operations, widths,
parameter count, group, and property alternatives are in `experiment.json`.

## Recorded outcomes

All 120 original queries were attempted, with no exclusions, missing records, or
corrupt records. Outcomes are **2 strict replay-accepted SAT, 1 numerical UNSAT,
and 117 unknown/timeout**. The accepted solves are manifest IDs `0066` (UNSAT,
22.284 seconds), `0074` (strict SAT, 60.266 seconds), and `0075` (strict SAT,
73.513 seconds). No tolerance-only witness was accepted.

All 120 formulations finished construction (0.075–0.399 seconds per query;
43.726 seconds summed). Pre-presolve formulations contain 2,595–3,619 variables,
nine explicit property-selector binaries, 907–1,419 linear constraints, and
905–1,417 general constraints. ReLU constraints can introduce additional internal
solver structure; these are not post-presolve size claims. There were no observed
construction or license failures, but solving rarely completed within the budget.

Summed whole-run time is 21,217.765 seconds (about 5h53m38s); summed invocation time
is 21,217.787 seconds. Acquisition took 346.263 seconds and the full-run audit
1.188 seconds, both separately measured. No analysis preparation was performed.
Of the 117 timeouts, 69 retain raw Gurobi status 9 and 48 have no completed-status
checkpoint before supervision killed the worker. Completed solve-stage timings
exist for 72 queries only; absent stage timings are unavailable, not zero.
Construction provenance and whole-run time remain present for every query.

Implementation commit: `2ba2eb4242bd55cda799867d41e82a6a96b237d2`; the audit records
the exact source and lockfile hashes. See `summary.json` for machine-calculated
denominators and timing summaries and `report.md` for all original-query outcomes.

## Reproduce

From the repository root, install the locked solver extra and use a suitable
Gurobi license. Use a fresh output path for a new experiment; do not overwrite this
archive or retry unresolved rows within it.

```sh
uv sync --locked --extra solver
uv run --locked python -m nvvcomp_gurobi.experiment acquire .benchmarks/relusplitter-v1 --category relusplitter_2026
uv run --locked python -m nvvcomp_gurobi.experiment audit .benchmarks/relusplitter-v1/instances.csv experiments/relusplitter-v1-full
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/relusplitter-v1/instances.csv experiments/relusplitter-v1-full
uv run --locked python -m nvvcomp_gurobi.experiment report experiments/relusplitter-v1-full
```

Acquisition and eligibility audit are measured separately; preparation does no
analysis. The whole-run query deadline includes startup, reads, interpretation,
construction, optimization, and replay. Gurobi receives only remaining time. The
supervisor rejects late solves. Invocation wall time additionally includes
cleanup. No memory cap or hardware tuning is applied; the pinned replay code uses
12 intra/inter-op CPU threads separately from the single Gurobi thread. These
local timings are not matched-hardware or identical-accounting ABC measurements.
The first query's initial approximately 16 seconds overlapped the repository's
final tiny test-suite check; no further test runs were scheduled during the full
experiment. The sequential experiment runner itself never overlaps its queries.

## Record inventory

- `instances.csv`: original 120-row manifest, byte-for-byte.
- `experiment.json`: full preflight, acquisition URLs and SHA256 hashes, graph and
  property descriptors, hardware, package versions, benchmark/tooling revisions,
  implementation commit and exact source/lockfile hashes. Original benchmark bytes
  are reproducibly downloaded into ignored `.benchmarks/`, not duplicated here.
- `records/0000.json` through `records/0119.json`: original-query identities,
  execution limits, invocation and stage timings, conservative outcomes, raw solver
  status, witness/replay evidence where available, actual formulation, model size
  after successful construction, effective numerical settings, and environment.
- `summary.json`, `report.md`: solver-free reports regenerated from those records.
- `review.md`: independent Standards/Spec reviews using GPT-6 Astra medium,
  including the reviewed baseline, findings, and disposition.

The separate `../relusplitter-v1/` directory retains the first pilot invocation and
its original audit. That audit exposed inconsistent group naming for originals
versus generated variants. The descriptor was corrected before this full run;
encoding, numerical settings, and deadlines did not change. The pilot is not an
extra competition query and is not merged into this 120-query population.

Published ABC pairing and interpretation belong to the shared comparison slice;
this archive supplies source identities without treating published verdicts as
correctness oracles or claiming execution-bound ABC artifact hashes.
