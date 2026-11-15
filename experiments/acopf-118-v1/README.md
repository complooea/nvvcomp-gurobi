# Original IEEE-118 ACOPF 1.0 Gurobi experiment

Issue [#21](https://github.com/complooea/nvvcomp-gurobi/issues/21).
All **five selected queries have records**: **three numerical UNSAT and two
unknown**, with no accepted SAT, exclusions, missing or corrupt records.
The original property-2 invocation was interrupted by an orchestration error.
An explicitly user-authorized recovery invocation received its full deadline
and timed out; it now supplies the active record, with the interruption retained
in [history](history/README.md), not counted as a second query or proof.
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
| 0000 | 2 | thermal-limit residual | unknown: timeout (recovery invocation) | 600.014511 |
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

Property 2's supervisor was accidentally launched with a **one-second external
shell-tool timeout**, despite the correctly configured 600-second verification
deadline. The start record remained `unknown/interrupted`. The orphaned worker
was explicitly stopped, its absence and the supervisor's absence confirmed,
and only the stale lock removed before resuming the four unattempted queries.
No completed verdict was recovered or credited after interruption. A later
inspection recovered a partial worker checkpoint with interpretation/construction
timings, settings and formulation sizes, but no solve timing or completed status.
It is preserved separately, not merged into the interrupted record.

The user then explicitly requested a fresh invocation and replacement of the
interrupted active record. One separately audited recovery run used identical
original bytes, full-graph semantics, numerical defaults, 600-second deadline
and one solver thread. It timed out after 600.014511 whole-run seconds.
Its record now occupies `records/0000.json`; the interrupted bytes, pre-recovery
reports, recovery audit, checkpoint and complete recovery record remain in
[history](history/README.md). The [orchestration log](orchestration.json) binds
both records by SHA256. This is five active query outcomes from completed
invocations, **not five first-attempt uninterrupted trials**; the orchestration
failure and additional recovery attempt remain disclosed.

## Timings and formulation sizes

Active whole-run times sum to **710.583275 seconds across five queries**;
active invocation wall times sum to **710.583718 seconds across five queries**.
These totals exclude the superseded interrupted attempt; they are not total
experiment effort including recovery overhead. No time is imputed for that
historical interruption. Acquisition took 20.482280 seconds; the initial archive
audit took 0.656554 seconds, separately. The recovery audit is separately retained
in history. Preparation performed no analysis (0 seconds).

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

Property 2's active sizes come from the recovery invocation, not the historical
checkpoint. All sizes are before presolve, not counts of ONNX initializers or
tensor nodes.

## Environment and execution contract

Measured source commit: `9b954b35a438d9f549760db95fe6196fd42155ed`.
The audit pins exact maintained-source/lockfile hashes and reference revisions.
Property 2's replacement invocation was measured at `f9dd28a`; its separately
retained audit verifies identical maintained-source and lockfile hashes to the
initial experiment. No implementation or settings changed between attempts.
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
not local correctness oracles; comparison belongs to the dependent ticket.

## Reproduction and handoff

Use the existing commands in
[experiment instructions](../../docs/experiments.md#original-ieee-118300-acopf-10),
with fresh paths for a new measurement. Five IEEE-118 and four IEEE-300 original
600-second budgets total **90 minutes maximum run budget plus overhead**.
Automatic resume never overwrites saved outcomes, including timeouts and invalid
candidates. The explicit, user-authorized promotion described above is a recorded
exception, not changed resume behavior. Do not remove records to hide failures.

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
- [history/README.md](history/README.md): superseded interruption and recovery
  provenance; excluded from the five-query reporting denominator.
- `summary.json`, `report.md`: deterministic solver-free reports.

All five active rows remain available for dependent comparison, but timeout and
invalid-replay outcomes remain unresolved, outside common-proof timing.
