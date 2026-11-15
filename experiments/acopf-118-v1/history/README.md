# IEEE-118 property-2 interruption and recovery history

The active five-query inventory uses the new **unknown/timeout** record at
[`../records/0000.json`](../records/0000.json). It is a completed, separately
measured 600-second invocation, not a recovered proof or resumed solve.
The user explicitly requested recovery and then replacement of the interrupted
active record. No automatic retry behavior or solver setting changed.

## Superseded original attempt

- [Original interrupted record](before-recovery/records/0000.json), preserved
  byte-for-byte; SHA256
  `2dc328481fe7ee148e5365d69552af89c28886a696681ac69d6388621b3a9186`.
- Pre-recovery [summary](before-recovery/summary.json),
  [report](before-recovery/report.md), and
  [orchestration log](before-recovery/orchestration.json), retained unchanged.
- [Recovered worker checkpoint](property-2-recovery/interrupted-worker-checkpoint.json):
  contains interpretation/construction timings and measured formulation/settings,
  but **no completed verdict, solver status, solve/replay or whole-run timing**.
  Its default `unknown/error` fields are an in-progress checkpoint, not an
  additional measured failure verdict. No late result receives credit.

## One user-authorized recovery invocation

- [Audit/provenance](property-2-recovery/experiment.json):
  one exact property-2 selection, identical original ONNX/property hashes and
  architecture, finite-box eligibility, same maintained-source/lockfile hashes.
- [Selection](property-2-recovery/instances.csv) and
  [source manifest](property-2-recovery/source-instances.csv).
- [Recovery record](property-2-recovery/records/0000.json), copied byte-for-byte
  into the active inventory; SHA256
  `f3a1e6d946244ebab3f9c5e4607e9284b4a9b80b21638fa73610611848e9b995`.
- [Recovery metadata](property-2-recovery/recovery.json), including original
  archive fingerprints taken before recovery/promotion.
- Standalone [summary](property-2-recovery/summary.json) and
  [report](property-2-recovery/report.md), regenerable with the existing public
  `report` command on `experiments/acopf-118-v1/history/property-2-recovery`.

The recovery run retained the original 600-second whole-run budget, one Gurobi
solver thread, default numerical settings and original replay configuration.
It timed out at 600.014511 seconds (including supervisor cleanup), with measured
construction sizes/settings and no completed solve-stage checkpoint or raw
solver status. No accepted SAT or numerical UNSAT was obtained; no further
retry was performed. All 29 existing tiny solver tests passed beforehand, and
no tests ran concurrently with the recovery measurement.

The active report counts property 2 **once**. Files under this history directory
are not additional selected queries, and their timings must not be added to
canonical query sums. They preserve total process history rather than conceal
the initial orchestration error. Earlier revision-scoped review conclusions
remain historical; they do not review this explicit replacement.
