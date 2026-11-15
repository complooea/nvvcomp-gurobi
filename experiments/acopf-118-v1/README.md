# Original IEEE-118 ACOPF 1.0 Gurobi experiment

Issue [#21](https://github.com/complooea/nvvcomp-gurobi/issues/21).
All **five selected queries have records**: **three numerical UNSAT and two
unknown**, with no accepted SAT, exclusions, missing or corrupt records.
Numerical UNSAT is not an independently certified exact-real proof.

## Selection and eligibility

Pinned benchmark revision `303f2327a8e8411efc4457da03d2016ce42733cf`,
category `ml4acopf_2024`, version `1.0`, exact original model
`118_ieee_ml4acopf.onnx`; properties **2, 4, 3, 5, 6** in source order.
The full source manifest and exact selection are retained here. All five
original pairs passed the [pre-solve semantic audit](#graph-and-property-audit)
before execution; no variants or smoke rows enter the denominator.
Compressed/decompressed hashes and acquisition URLs are in `experiment.json`
and each record; original compressed bytes live in ignored `.benchmarks/`.

The complete graph is represented for every query with existing ACOPF encoding
semantics, not just the queried output cone. Input/output shapes are
`[1,198]` / `[1,1696]`; the graph has 168 tensor nodes, 163,868 stored initializer
elements, and scalar relations listed below. These descriptors
are distinct from measured optimization-encoding sizes.

## Graph and property audit

All five original graph/property pairs are eligible under the existing
interpreter; no unsupported semantics, interpreter expansion or approximation
was needed. Both complete IEEE-118/300 populations were audited before execution.
The [shared audit procedure](../../docs/experiments.md#acopf-semantic-audit-procedure)
documents tensor attributes, finite input boxes, supported operator semantics,
whole-graph lowering and the pinned original property generator.

The opset-14 graph has one static FLOAT32 input/output tensor. Slice/Gather
indices and shape scaffolding are constant; Equal/Where are not data-dependent
branches. The complete graph is encoded for every property, with shared scalar
relations, quadratic squares/products and global nonlinear Sigmoid/Sin/Cos
relations (`FuncNonlinear=1`, angles in radians), not fixed piecewise
approximations or property-dependent output-cone pruning.

| Graph descriptor | Count |
| --- | ---: |
| Tensor nodes | 168 |
| Stored initializer elements | 163,868 |
| Scalar affine relations | 6,436 |
| Scalar ReLUs | 512 |
| Scalar sigmoids | 226 |
| Scalar squares | 1,234 |
| Scalar variable products | 558 |
| Scalar sines | 186 |
| Scalar cosines | 186 |

These source-graph descriptors are not interchangeable measures of difficulty
or measured optimization-encoding size. Pre-presolve formulation sizes are
reported separately below and in each record.

Classification follows original output definitions, not comments or published
verdicts. This model has `G=54` generators, `N=118` buses and `E=186` branches.
Generation occupies the first `2*G` outputs; voltage magnitude occupies the next
`N`. Property 4 uses voltage `vmax/vmin ± 1e-6`, despite its generation-bounds
comment. Property 3 uses active/reactive generation limits with `1e-6` offsets.
Thermal and active-power residual blocks start at `outputs - 2*N - 2*E` and
`outputs - 2*N` respectively.

| Property | Class | Meaning | Asserted output indices (inclusive) | Comparisons |
| --- | --- | --- | --- | ---: |
| 2 | physical residual | thermal-limit residual | 1189 | 1 |
| 4 | structural output bound | voltage magnitude bounds | 108–225 | 236 |
| 3 | structural output bound | active/reactive generation bounds | 0–107 | 216 |
| 5 | physical residual | active power balance residual | 1464 | 2 |
| 6 | physical residual | active power balance residual | 1518 | 2 |

All original scalar thresholds and finite input bounds are preserved, not
regenerated from the generator or replaced with physical assumptions. Structural
output bounds have physical meaning too; the classification does not distinguish
physical versus nonphysical graphs or partial versus complete encodings.

## Outcomes and inventory

| ID | Property | Kind | Outcome | Whole-run seconds |
| --- | ---: | --- | --- | ---: |
| 0000 | 2 | thermal-limit residual | unknown: timeout | 600.014511 |
| 0001 | 4 | voltage bounds | numerical UNSAT | 91.474681 |
| 0002 | 3 | generation bounds | unknown: validation failed | 10.139917 |
| 0003 | 5 | power-balance residual | numerical UNSAT | 5.735618 |
| 0004 | 6 | power-balance residual | numerical UNSAT | 3.218548 |

Physical residuals: 3 listed, 2 numerical UNSAT, 1 timeout.
Structural output bounds: 2 listed, 1 numerical UNSAT, 1 invalid replay.
Property 4 is voltage magnitude bounds, not generation bounds despite its
upstream comment. Structural output checks still have physical meaning.

Property 3 produced a Gurobi status-2 candidate, but independent FLOAT32 CPU
replay on the original ONNX did not satisfy the original property under either
strict or tolerated input bounds. The candidate and diagnostics are retained;
it is **not accepted SAT or numerical UNSAT**. Output thresholds include
`1e-6` offsets, the same scale as the default feasibility tolerance; this does
not establish the cause of replay rejection. No tolerance changes or retries.

## Timings and formulation sizes

Whole-run times sum to **710.583275 seconds across five selected queries**;
invocation wall times sum to **710.583718 seconds across five selected queries**.
These are sums of the retained per-query measurements, not total experiment
effort. Acquisition took 20.482280 seconds; the primary eligibility audit took
0.656554 seconds, and a supplementary property-2 audit took 0.144355 seconds,
separately. Preparation performed no analysis (0 seconds).

For the five active invocations, construction took 0.202557–0.208265 seconds
(1.024918 summed). Four solve-stage timings are available (108.745247 seconds
summed); property 2 has no completed solve-stage checkpoint or solver status,
not a zero solve time. The replay stage is recorded only for property 3
(0.152959 seconds). Absent stages are not zeros.

Measured pre-presolve sizes for all five active constructions:

| Metric | Minimum | Maximum |
| --- | ---: | ---: |
| Variables | 11,232 | 11,468 |
| Explicit binaries (property selectors) | 0 | 236 |
| Linear constraints | 8,133 | 8,133 |
| General constraints | 1,110 | 1,346 |
| Quadratic constraints | 1,792 | 1,792 |
| Linear nonzeros | 180,719 | 180,954 |

All sizes are before presolve, not counts of ONNX initializers or tensor nodes.

## Environment and execution contract

Measured commits: `f9dd28aa57279e435d07b8dc5e69bb2eb9b45c1c` for property 2,
`9b954b35a438d9f549760db95fe6196fd42155ed` for the other four properties.
`experiment.json` maps each record to its measurement commit and pins their
identical maintained-source/lockfile hashes and reference revisions.
Apple M4, 10 physical/logical CPUs, 16 GiB RAM, macOS 26.6.2 arm64;
Python 3.12.16, Gurobi/gurobipy 13.0.1, gurobi-machinelearning 1.7.0,
ONNX 1.21.0, NumPy 2.2.6, ONNX Runtime 1.26.0, cachier 2.2.2.
All active invocations retain actual settings and package provenance.

Sequential execution, **Gurobi Threads=1**, unchanged numerical defaults, no
memory cap or per-instance tuning. Replay keeps **12 intra/inter-op CPU threads**;
the whole process is not single-threaded. One solver thread is a local study
choice, not a VNN-COMP requirement. Whole-run timing includes startup, artifact
reads/decompression, interpretation, construction, solving and replay; only
remaining time is passed to Gurobi. No startup subtraction or late-result credit.
Acquisition/audit are separate, not cached per-query analysis.

Before measurement, 107 focused experiment/verifier/tiny real-Gurobi/runner tests
and repository lint/format/type checks passed. No tests ran concurrently with
measurement. Final review and validation are recorded in the
[revision-scoped review](../reviews/larger-acopf-experiment-review.md).
Historical IEEE-14 and other archives are unchanged. Published ABC verdicts are
not local correctness oracles. The subsequent [saved-result comparison](../acopf-118-v1-comparison/README.md)
and [size-progression analysis](../proof-comparison-analysis.md#coverage-and-size-progression-by-class)
retain all outcomes without changing these measurements.

## Reproduction and handoff

Use the existing commands in
[experiment instructions](../../docs/experiments.md#original-ieee-118300-acopf-10),
with fresh paths for a new measurement. Five IEEE-118 and four IEEE-300 original
600-second budgets total **90 minutes maximum run budget plus overhead**.
Automatic resume never overwrites saved outcomes, including timeouts and invalid
candidates. Use fresh output paths for new measurements.

Saved inputs for solver-free reporting are `experiment.json` and `records/`.
Run `uv run --locked python -m nvvcomp_gurobi.experiment report experiments/acopf-118-v1`
to regenerate `summary.json` and `report.md` without artifact reads, solver
execution or a license. To validate in a fresh directory, copy just those inputs
there and run the same `report` command on that directory; outputs are
byte-identical under the pinned reporter source.

- `source-instances.csv`, `instances.csv`: source inventory and exact selection.
- `experiment.json`: eligibility, classifications, graph descriptors, artifact
  identities, acquisition inventory, hardware, settings policy and source pins.
- `records/0000.json`–`0004.json`: all identities/outcomes, available timings,
  measured sizes, effective settings, provenance and candidate/replay evidence.
- `summary.json`, `report.md`: deterministic solver-free reports.

All five active rows remain available for dependent comparison, but timeout and
invalid-replay outcomes remain unresolved, outside common-proof timing.
