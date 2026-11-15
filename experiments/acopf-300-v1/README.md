# Original IEEE-300 ACOPF 1.0 Gurobi experiment

Issue [#21](https://github.com/complooea/nvvcomp-gurobi/issues/21).
All **four selected queries have records**: **one numerical UNSAT and three
unknown/timeouts**, with no accepted SAT, exclusions, missing or corrupt records.
Numerical UNSAT is not an independently certified exact-real proof.

## Selection and eligibility

Pinned benchmark revision `303f2327a8e8411efc4457da03d2016ce42733cf`,
category `ml4acopf_2024`, version `1.0`, exact original model
`300_ieee_ml4acopf.onnx`; properties **3, 105, 2, 4** in source order.
The full source manifest and exact selection are retained here. All four
original pairs passed the [pre-solve semantic audit](#graph-and-property-audit)
before either population was executed. Variants and smoke rows are excluded
from selection, not excluded because of outcomes. Compressed/decompressed hashes
and acquisition URLs are retained; original gzip bytes live in ignored
`.benchmarks/`.

The complete graph is represented for every query with existing ACOPF encoding
semantics. Input/output shapes are `[1,402]` / `[1,3804]`; the graph has 168 tensor
nodes, 680,014 stored initializer elements, and the scalar relations listed
below. These are not interchangeable size/difficulty metrics.

## Graph and property audit

All four original graph/property pairs are eligible under the existing
interpreter; no unsupported semantics, interpreter expansion or approximation
was needed. Both complete IEEE-118/300 populations were audited before execution.
The [shared audit procedure](../../docs/experiments.md#acopf-semantic-audit-procedure)
documents tensor attributes, finite input boxes, supported operator semantics,
whole-graph lowering and the pinned original property generator.

The opset-14 graph has one static FLOAT32 input/output tensor. Slice/Gather
indices and shape scaffolding are constant; Equal/Where are not data-dependent
branches. Every property represents the complete graph, with shared scalar
relations, quadratic squares/products and global nonlinear Sigmoid/Sin/Cos
relations (`FuncNonlinear=1`, angles in radians), not fixed piecewise
approximations or property-dependent output-cone pruning.

| Graph descriptor | Count |
| --- | ---: |
| Tensor nodes | 168 |
| Stored initializer elements | 680,014 |
| Scalar affine relations | 13,538 |
| Scalar ReLUs | 1,024 |
| Scalar sigmoids | 438 |
| Scalar squares | 2,766 |
| Scalar variable products | 1,233 |
| Scalar sines | 411 |
| Scalar cosines | 411 |

These source-graph descriptors are distinct from measured pre-presolve
variables and constraints, reported separately below and in each record.

Classification follows original output definitions, not comments or published
verdicts. This model has `G=69` generators, `N=300` buses and `E=411` branches.
Generation occupies the first `2*G` outputs; voltage magnitude occupies the next
`N`. Property 4 uses voltage `vmax/vmin ± 1e-6`, despite its generation-bounds
comment. Property 3 uses active/reactive generation limits with `1e-6` offsets.
Thermal and active-power residual blocks start at `outputs - 2*N - 2*E` and
`outputs - 2*N` respectively.

| Property | Class | Meaning | Asserted output indices (inclusive) | Comparisons |
| --- | --- | --- | --- | ---: |
| 3 | structural output bound | active/reactive generation bounds | 0–137 | 276 |
| 105 | physical residual | active power balance residual | 3244 | 2 |
| 2 | physical residual | thermal-limit residual | 2382 | 1 |
| 4 | structural output bound | voltage magnitude bounds | 138–437 | 600 |

All original scalar thresholds and finite input bounds are preserved, not
regenerated from the generator or replaced with physical assumptions. Structural
output bounds have physical meaning too; the classification does not distinguish
physical versus nonphysical graphs or partial versus complete encodings.

## Outcomes and inventory

| ID | Property | Kind | Outcome | Whole-run seconds |
| --- | ---: | --- | --- | ---: |
| 0000 | 3 | generation bounds | unknown: timeout | 600.022791 |
| 0001 | 105 | power-balance residual | numerical UNSAT | 19.578616 |
| 0002 | 2 | thermal-limit residual | unknown: timeout | 600.036884 |
| 0003 | 4 | voltage bounds | unknown: timeout | 600.017557 |

Physical residuals: 2 listed, 1 numerical UNSAT, 1 timeout.
Structural output bounds: 2 listed, both timeout. Property 4 concerns voltage
magnitude bounds regardless of its misleading generation-bounds comment.
No SAT candidate was accepted; no timeout or other failure was retried.

## Timings and formulation sizes

Whole-run time sums to **1,819.655848 seconds across all four queries**;
invocation wall time sums to **1,819.656566 seconds**. Property 105's numerical
UNSAT took 19.578616 whole-run seconds. The three timeouts retain actual observed
wall times, not imputed 600-second runtimes; supervision/cleanup explains small
deadline overshoots, not extra solve credit.

All four construction timings are available: 0.667062–3.077533 seconds
(9.771845 summed). Solve-stage timings are available only for properties 105
and 2 (14.687895 and 595.188969 seconds respectively). Properties 3 and 4 lack
a completed solve-stage checkpoint at whole-run termination; those timings are
**unavailable, not zero or inferred by subtraction**. No validation stage was
recorded. Unavailable stages remain absent in the raw records.

Acquisition took 18.359537 seconds and the final archive audit 1.871125 seconds,
separately. Preparation performed no analysis (0 seconds).
Measured pre-presolve sizes for all four constructions:

| Metric | Minimum | Maximum |
| --- | ---: | ---: |
| Variables | 24,027 | 24,627 |
| Explicit binaries (property selectors) | 0 | 600 |
| Linear constraints | 17,343 | 17,343 |
| General constraints | 2,284 | 2,884 |
| Quadratic constraints | 3,999 | 3,999 |
| Linear nonzeros | 716,010 | 716,609 |

These measured optimization-encoding sizes are distinct from tensor-node counts,
initializer counts and scalar operation counts; they are not post-presolve sizes.

## Environment and execution contract

Measured source commit: `9b954b35a438d9f549760db95fe6196fd42155ed`.
The audit retains exact maintained-source/lockfile hashes and reference pins.
Apple M4, 10 physical/logical CPUs, 16 GiB RAM, macOS 26.6.2 arm64;
Python 3.12.16, Gurobi/gurobipy 13.0.1, gurobi-machinelearning 1.7.0,
ONNX 1.21.0, NumPy 2.2.6, ONNX Runtime 1.26.0, cachier 2.2.2.
Each record retains actual package and effective solver settings.

These four invocations ran sequentially after the IEEE-118 population, with
original **600-second whole-run deadlines**, **Gurobi Threads=1**, unchanged
numerical defaults and replay settings, no memory cap or tuning. Replay retains
**12 intra/inter-op CPU threads**; “one solver thread” does not describe a
single-threaded process. This is a local study policy, not a competition rule.
Startup, reads/decompression, interpretation, construction, optimization and
replay all remain inside the whole-run budget. Only remaining time is supplied
to Gurobi. Preparation is separate and does no analysis; audit is not reused as
cached verification work. No startup subtraction or late-result credit.

Before measurement, 107 focused experiment/verifier/tiny real-Gurobi/runner tests
and lint/format/type checks passed. No tests ran concurrently with measurement.
See the [revision-scoped review](../reviews/larger-acopf-experiment-review.md)
for final checks and independent review. Historical archives are unchanged;
published ABC verdicts are not local correctness oracles.

## Reproduction and handoff

Follow [experiment instructions](../../docs/experiments.md#original-ieee-118300-acopf-10)
with fresh paths for new measurement. Nine selected IEEE-118/300 budgets total
**90 minutes maximum run budget plus overhead**. Keep the populations separate
and queries sequential. Existing resume behavior skips every retained outcome,
including timeouts; do not delete failures to repeat them.

Run `uv run --locked python -m nvvcomp_gurobi.experiment report experiments/acopf-300-v1`
to regenerate `summary.json` and `report.md` from saved records, without original
artifacts, solver execution or a license. Copy `experiment.json` and `records/`
to a fresh directory and run `report` there for byte-identical regeneration under
the pinned reporter source.

- `source-instances.csv`, `instances.csv`: full source inventory/exact selection.
- `experiment.json`: complete eligibility/classification audit, graph descriptors,
  artifact hashes/acquisition URLs, hardware, execution policy and revisions.
- `records/0000.json`–`0003.json`: all outcomes, available timings, diagnostics,
  measured construction sizes, settings and provenance.
- `summary.json`, `report.md`: deterministic solver-free experiment reports.

The dependent comparison must retain all four rows; timeouts remain outside
common-proof timing. This exploratory extension does not establish matched
hardware, a controlled scaling law, or a causal graph-type effect.
