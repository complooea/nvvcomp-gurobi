# IEEE-14 ACOPF published-ABC comparison inputs and statistics

See the shared [implementation review](../proof-comparison-review.md) for both review axes and final checks.

Issue #11, part of #7. This archive contains comparison data, not interpretation.
All **14** original version-1.0 queries for exactly `14_ieee_ml4acopf.onnx`,
600 seconds each, have unique pinned-source hash matches. The full category CSV
is retained: **56 unselected alias/model rows** remain in `unmatched_abc`, outside
selected denominators. Gurobi/ABC numerical UNSAT counts are **13/14**, with
common-UNSAT timing n **13**, no accepted SAT or accepted-answer disagreements.
The rejected-replay Gurobi query stays unresolved, not a proof or timeout.
Generated `statistics.md` keeps **12 physical-residual** queries separate from
**two structural-output-bound** queries (properties 3/4), using audited classes.

## Regenerate without solver or network

```sh
uv run --locked python -m nvvcomp_gurobi.comparison experiments/acopf-v1 experiments/acopf-v1-comparison/published experiments/acopf-v1-comparison --category ml4acopf_2024 --version 1.0
```

Reacquire into a new directory (no ABC execution):

```sh
uv run --locked python scripts/acquire_comparison.py .benchmarks/acopf-v1 new-acopf-published --category ml4acopf_2024
```

See [the original experiment](../acopf-v1/README.md) for acquisition, actual
formulation, implementation, hardware/resources, timing and unresolved replay
evidence. Inputs pin benchmark `303f2327a8e8411efc4457da03d2016ce42733cf` and ABC
results `eea564f5d0a8751d8321a409214db14d03f452b8`. Acquisition checks original
artifact Git blobs and the complete source manifest before verifying the exact
14-query selection. `published/source.json` retains source URLs, hashes, and
limitations. The original full manifest and selected manifest, full category
CSV, scoring reference snapshots, and published SAT witness/check caches are
retained, including evidence for unselected rows. No fresh replay is performed.

`evidence.json` provides identities, outcomes, validation/unresolved states,
proof/cohort populations and exact timing-denominator IDs, with input/calculation
hashes and measured experiment context. `instances.md` is per-query evidence;
`statistics.md` is generated data and denominator guidance.

Every ABC identity is **source-verified, execution-unbound**. Numerical UNSAT
is not an independently checked exact-real certificate. Gurobi whole-run time
includes startup, interpretation, construction, solving and replay; acquisition
and audit remain separate, per-query preparation is zero. ABC preparation and
run times stay separate. No combined ratio, overhead subtraction, timeout
imputation or matched-hardware claim is made; ABC execution hardware/resources
and tool environment are unavailable. ACOPF is not pooled with MNIST,
ReLUSplitter, or the [MVP](../sat-relu-v1-comparison/README.md). These archives
supply inputs for subsequent analysis relating to #2, not ABC bound-tightness
claims or predictions about other solver populations.
