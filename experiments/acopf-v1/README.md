# IEEE-14 ACOPF 1.0 Gurobi experiment

Issue #10, implementing the power-system arithmetic slice of #7. All 14 original
queries were attempted through the existing `verify(Instance, ExecutionLimits)`
workflow, with original artifacts, one Gurobi thread, unchanged numerical defaults,
and independent FLOAT32 original-ONNX witness replay. Numerical UNSAT is not an
independently certified exact-real proof. Benchmark runs are experiments, not tests.

## Selection and graph audit

Benchmark revision: `303f2327a8e8411efc4457da03d2016ce42733cf`, category
`ml4acopf_2024`, version `1.0`, exactly `14_ieee_ml4acopf.onnx`. The category's
full source manifest contains linear/residual aliases and other models; none of
those are included in this selection. Acquisition retains its original bytes as
`source-instances.csv` and derives a 14-row `instances.csv` by exact model path,
preserving source row order. Properties 1–14 occur exactly once, all with
600-second deadlines. The inventory contains the source manifest, derived
manifest, one original compressed ONNX and 14 original compressed properties,
with URLs, stored-byte SHA256, and the documented selection. Audit and records
also retain decompressed artifact hashes. Original compressed artifacts live in
ignored `.benchmarks/`, not duplicated in this archive.

All 14 original graphs/properties were audited as eligible before solving. Input
shape is `[1,22]`, output shape `[1,186]`. The opset-14 graph includes shared
intermediates, slicing/gathering, concatenation, transpose, broadcasting, sparse
constant-weight matrix multiplication and constant-only Equal/Where/Expand shape
scaffolding. Lowering retains 693 affine relations, 96 ReLUs, 24 sigmoids,
134 squares, 60 variable products, 20 sine and 20 cosine relations. Sparse zero
weights and identity views are simplified without pruning any output cone.

The complete model is represented for every property, including property 2.
Squares/products use native quadratic equalities; sigmoid/sine/cosine use native
global Gurobi function relations with `FuncNonlinear=1`, not fixed piecewise
approximations. Angles use radians. Intermediate intervals derive conservatively
from the original input box and mathematical ranges, with outward-rounded
arithmetic; no absent physical limits or heuristic restrictions are imposed.
Data-dependent Equal/Where, variable division and general exponents remain
unsupported. Existing sequential affine/ReLU networks retain their applicable
gurobi-machinelearning construction path under the shared interpretation.

## Recorded outcomes

All **14** queries have records: **13 numerical UNSAT, one unknown**, no accepted
SAT, no timeouts, exclusions, missing records or corrupt records.

| Property class | Queries | Numerical UNSAT | Unknown |
| --- | ---: | ---: | ---: |
| Physical residuals (all except 3/4) | 12 | 12 | 0 |
| Structural output bounds (3/4) | 2 | 1 | 1 |

The unresolved query is property **3**, manifest ID `0010`. Gurobi returned status
2 and a candidate, but original-ONNX replay did not satisfy any original output
alternative, under either strict or tolerated input bounds. Its classification
is `invalid`, reason `validation_failed`; the candidate and replay diagnostics
are retained. The property's zero-output alternatives use thresholds of magnitude
`1e-6`, the same scale as the unchanged feasibility tolerance. This numerical
context does not establish the cause of the rejected candidate or turn it into
SAT/UNSAT. No tolerance tuning, hidden retry or outcome replacement was performed.

Every formulation completed construction in **0.0246–0.0258 seconds** per query
(0.3502 seconds summed). Pre-presolve sizes are 1,255–1,311 variables, 880 linear
constraints, 160–216 general constraints, 194 quadratic constraints, and
5,862–5,917 linear nonzeros. Property selectors account for 0–56 explicit binaries;
the network itself has none explicitly. These are measured construction sizes,
not estimates or post-presolve sizes. All 14 solve-stage timings are available,
summing to 0.6883 seconds. No construction or license failures occurred.

Summed whole-run time is **2.5975 seconds**; summed invocation wall time is
**2.5982 seconds**. Individual whole-run times are 0.1403–0.3224 seconds. Acquisition
took 50.8712 seconds and audit 0.1709 seconds, separately measured. Preparation
performed no analysis. Every query retained its original 600-second deadline;
early completion, not a reduced budget, accounts for the short elapsed time.
The first query was measured with `--stop-after 1`, inspected, and the remaining
13 were resumed in the same archive without rerunning that first query.

Measured implementation commit: `54444759a50f54df94be2763689ffc51b351f0ba`.
The audit records exact source and lockfile hashes. All 143 tests, including tiny
real-Gurobi and runner integration cases, passed before execution; typechecking
and lint passed. No tests ran concurrently with the experiment. Independent
GPT-6 Astra medium reviews and the addressed finding are in `review.md`.

## Published comparison context

`published-abc.json` retains all 14 matching raw rows from the pinned ABC result
CSV, source URL/revision and full-source SHA256. Matching uses the exact
version-1.0 model/property paths, not aliases. All 14 published rows report UNSAT;
they are neither independent certificates nor test oracles. This is source-name
and version matching, **not execution-bound ABC artifact hashing**. The source
CSV can be retrieved from the URL in that file and checked against `source_sha256`;
select its rows by the exact model path recorded there.

This set has 13/14 numerical UNSAT completion, with its one unresolved case due
to rejected replay rather than timeout. In contrast to the MVP's coverage/runtime
trade-off, these selected physical-residual queries all completed numerically;
that observation does not establish general ACOPF tractability, bound tightness,
or solver superiority. Structural bounds remain separately identified rather
than being treated as physical-residual proofs. Paired comparative statistics
belong to the shared comparison; these unmatched environments and timing policies
do not justify a hardware-independent speed claim.

## Reproduce

Install the locked solver extra and use a suitable Gurobi license. Use a fresh
output directory for new measurements; do not overwrite this archive or retry its
unresolved query within it.

```sh
uv sync --locked --extra solver
uv run --locked python -m nvvcomp_gurobi.experiment acquire .benchmarks/acopf-v1 --category ml4acopf_2024
uv run --locked python -m nvvcomp_gurobi.experiment audit .benchmarks/acopf-v1/instances.csv experiments/acopf-v1
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/acopf-v1/instances.csv experiments/acopf-v1 --stop-after 1
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/acopf-v1/instances.csv experiments/acopf-v1
uv run --locked python -m nvvcomp_gurobi.experiment report experiments/acopf-v1
```

The whole-run deadline includes startup, reads/decompression, interpretation,
construction, solving and replay. Only remaining time is supplied to Gurobi;
late results get no solved credit. Invocation time also includes supervision and
cleanup. Acquisition/audit are separate, not cached per-query solving work.
Execution used an Apple M4, 10 logical CPUs and 16 GiB RAM on macOS, with one
Gurobi thread and no memory cap or performance/numerical tuning. Pinned replay
uses 12 intra/inter-op CPU threads separately. Competition timing/accounting
differences remain explicit; this is not a matched-hardware comparison.

## Record inventory

- `instances.csv`: the 14 selected source rows in original order.
- `experiment.json`: complete audit, property classes, tensor/operation/scalar
  descriptors, acquisition inventory and hashes, hardware/resources, versions,
  measured commit and exact source/lockfile hashes.
- `records/0000.json` through `records/0013.json`: original identities and limits,
  all outcomes, raw statuses, whole-run and stage timings, actual formulation
  sizes and solver defaults, and witness/replay evidence where available.
- `summary.json`, `report.md`: solver-free machine-calculated reports.
- `published-abc.json`: selected published source rows with provenance limitations.
- `review.md`: independent Standards/Spec implementation reviews and disposition.
