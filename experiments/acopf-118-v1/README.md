# Original IEEE-118 ACOPF 1.0 Gurobi experiment

Issue [#21](https://github.com/complooea/nvvcomp-gurobi/issues/21).
All **five selected queries have records**: **three numerical UNSAT and two
unknown**, with no accepted SAT, exclusions, missing or corrupt records.
One query was interrupted by an orchestration error rather than receiving its
full deadline; it is retained, not retried or counted as a proof.
Numerical UNSAT is not an independently certified exact-real proof.

## Selection and eligibility

Pinned benchmark revision `303f2327a8e8411efc4457da03d2016ce42733cf`,
category `ml4acopf_2024`, version `1.0`, exact original model
`118_ieee_ml4acopf.onnx`; properties **2, 4, 3, 5, 6** in source order.
The full source manifest and exact selection are retained here. All five
original pairs passed the [pre-solve semantic audit](../acopf-larger-audit.md)
before execution; no variants or smoke rows enter the denominator.
Compressed/decompressed hashes and acquisition URLs are in `experiment.json`
and each record; original compressed bytes live in ignored `.benchmarks/`.

The complete graph is represented for every query with existing ACOPF encoding
semantics, not just the queried output cone. Input/output shapes are
`[1,198]` / `[1,1696]`; the graph has 168 tensor nodes, 163,868 stored initializer
elements, and scalar relations listed in the shared audit. These descriptors
are distinct from measured optimization-encoding sizes.

## Outcomes and inventory

| ID | Property | Kind | Outcome | Whole-run seconds |
| --- | ---: | --- | --- | ---: |
| 0000 | 2 | thermal-limit residual | unknown: interrupted | unavailable |
| 0001 | 4 | voltage bounds | numerical UNSAT | 91.474681 |
| 0002 | 3 | generation bounds | unknown: validation failed | 10.139917 |
| 0003 | 5 | power-balance residual | numerical UNSAT | 5.735618 |
| 0004 | 6 | power-balance residual | numerical UNSAT | 3.218548 |

Physical residuals: 3 listed, 2 numerical UNSAT, 1 interrupted.
Structural output bounds: 2 listed, 1 numerical UNSAT, 1 invalid replay.
Property 4 is voltage magnitude bounds, not generation bounds despite its
upstream comment. Structural output checks still have physical meaning.

Property 3 produced a Gurobi status-2 candidate, but independent FLOAT32 CPU
replay on the original ONNX did not satisfy the original property under either
strict or tolerated input bounds. The candidate and diagnostics are retained;
it is **not accepted SAT or numerical UNSAT**. Output thresholds include
`1e-6` offsets, the same scale as the default feasibility tolerance; this does
not establish the cause of replay rejection. No tolerance changes or retries.

Property 2's supervisor was accidentally launched with a **one-second external
shell-tool timeout**, despite the correctly configured 600-second verification
deadline. The start record remained `unknown/interrupted`. The orphaned worker
was explicitly stopped, its absence and the supervisor's absence confirmed,
and only the stale lock removed before resuming the four unattempted queries.
No result was recovered or credited after interruption, and the record was not
replaced. See `orchestration.json` for the incident. All its stage/invocation
timings, effective solver settings and measured construction sizes remain
unavailable; the configured deadline and audit are retained. This is a
complete outcome inventory, **not five uninterrupted 600-second trials**.

## Timings and formulation sizes

Known whole-run times sum to **110.568764 seconds across four queries**;
known invocation wall times sum to **110.569033 seconds across four queries**.
These are not five-query elapsed-time totals. No time is imputed for the
interrupted record. Acquisition took 20.482280 seconds; the final archive audit
took 0.656554 seconds, separately. Preparation performed no analysis (0 seconds).

For the four completed invocations, construction took 0.202557–0.208265 seconds
(0.822184 summed); all four solve-stage timings are available (108.745247 seconds
summed). The replay stage is recorded only for property 3 (0.152959 seconds).
Absent stages are not zeros.

Measured pre-presolve sizes for these four constructions:

| Metric | Minimum | Maximum |
| --- | ---: | ---: |
| Variables | 11,234 | 11,468 |
| Explicit binaries (property selectors) | 2 | 236 |
| Linear constraints | 8,133 | 8,133 |
| General constraints | 1,112 | 1,346 |
| Quadratic constraints | 1,792 | 1,792 |
| Linear nonzeros | 180,720 | 180,954 |

No measured size is claimed for interrupted property 2. All sizes are before
presolve, not counts of ONNX initializers or tensor nodes.

## Environment and execution contract

Measured source commit: `9b954b35a438d9f549760db95fe6196fd42155ed`.
The audit pins exact maintained-source/lockfile hashes and reference revisions.
Apple M4, 10 physical/logical CPUs, 16 GiB RAM, macOS 26.6.2 arm64;
Python 3.12.16, Gurobi/gurobipy 13.0.1, gurobi-machinelearning 1.7.0,
ONNX 1.21.0, NumPy 2.2.6, ONNX Runtime 1.26.0, cachier 2.2.2.
All noninterrupted invocations retain actual settings and package provenance.

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
not local correctness oracles; comparison belongs to the dependent ticket.

## Reproduction and handoff

Use the existing commands in
[experiment instructions](../../docs/experiments.md#original-ieee-118300-acopf-10),
with fresh paths for a new measurement. Five IEEE-118 and four IEEE-300 original
600-second budgets total **90 minutes maximum run budget plus overhead**.
Resume never overwrites saved outcomes, including this interruption and invalid
candidate. Do not remove records to retry within this archive.

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
- `orchestration.json`: explicit interruption cause and cleanup/retention policy.
- `summary.json`, `report.md`: deterministic solver-free reports.

All five rows remain available for dependent comparison, but interrupted and
invalid-replay outcomes must remain unresolved, outside common-proof timing.
