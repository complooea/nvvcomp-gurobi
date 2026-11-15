# Original IEEE-300 ACOPF: saved Gurobi–ABC comparison

Issue [#22](https://github.com/complooea/nvvcomp-gurobi/issues/22), part of #20.
All **four** selected original queries (properties **3, 105, 2, 4**, source order)
have records and unique source-hash ABC matches. No exclusions or missing/corrupt
records. Gurobi/ABC numerical UNSAT counts are **1/3**, accepted SAT **0/1**,
unresolved **3/0**. Local properties 3, 2 and 4 timed out; no timeout receives
proof timing. There are **zero accepted-answer disagreements**, not a correctness
certificate or a reason to relabel local outcomes.

[Statistics](statistics.md), [exact pair table](instances.md) and
[evidence JSON](evidence.json) retain all identities, cross-tabs, unresolved
reasons and exact paired timing populations. The **two physical-residual**
queries have 1/1 Gurobi/ABC UNSAT and 0/1 accepted SAT; both **structural-output-bound**
queries are unresolved locally and published UNSAT. Property 4 checks voltage
magnitude, not generation. Every query encodes the complete graph.

## Common-proof runtime, not completion

The only common proof is physical power-balance **property 105, local ID 0001**:
Gurobi **19.578616 s**, ABC **7.985156 s**; ratio of sums and median individual
ABC/Gurobi ratio are both **0.407851** (n=1). ABC has lower observed time on
this pair. The structural common-proof population is empty: IDs `[]`, n=0,
timing sums/ratios **unavailable**, not zero runtime or an inferred speedup.
The published SAT thermal check is falsification evidence, not proof runtime.
See the [size-progression analysis](../proof-comparison-analysis.md#larger-acopf-size-progression).

## Sources, SAT cache and accounting

The [experiment](../acopf-300-v1/README.md) retains semantics, actual formulation
sizes, environment, settings and measurement commit, unchanged by comparison.
Published rows **66–69** of the full 70-row category CSV match exact original
network/property paths. **66 unselected rows** (other models, linear/residual
variants and the appended smoke row) remain in `unmatched_abc`, outside selected
denominators.

`published/source.json` pins benchmark
`303f2327a8e8411efc4457da03d2016ce42733cf` and published-results
`eea564f5d0a8751d8321a409214db14d03f452b8`. Acquisition verifies the entire source
manifest, exact selected manifest and original compressed artifacts against pinned
Git blobs; stored/decompressed hashes are retained. The full CSV, manifests,
reference scoring snapshots and category SAT witness/check caches remain available.

Selected **property 2 / row 68** claims SAT in **6.210085 s**. Its retained
`300_ieee_ml4acopf_300_ieee_prop2.counterexample.check.json` reports strict
acceptance on the CPU provider (`vnncomp2026-cex-1`); normalized CSV-row hash,
witness hash, benchmark/version identity, checker and provider correspond.
This is **cached acceptance, not fresh local replay**. Validator dependencies
Python 3.12.13 / ONNX 1.21.0 / ONNX Runtime 1.26.0 are not ABC execution settings.
Cache correspondence does not prove cache correctness or bind historical ABC
execution to exact model/property bytes. All four source matches are
**execution-unbound**, ABC resources remain unknown, and numerical UNSAT is not
an independently checked certificate.

All-selected G/ABC run sums are **1,819.655848/56.033594 s**; preparation sums
are **0/80.269484 s**, separately. These totals include local unresolved effort,
not equal-coverage proof timing. Raw **600-second** deadlines apply; observed
timeout overshoots remain recorded without solve credit or imputed runtimes.
Startup, reading, interpretation, construction, solving and replay stay in local
run time; acquisition/audit stay separate. No startup subtraction or unapproved
combined preparation/run ratio is used.

## Regenerate without solver or network

```sh
uv run --locked python -m nvvcomp_gurobi.comparison experiments/acopf-300-v1 experiments/acopf-300-v1-comparison/published fresh-300-comparison --category ml4acopf_2024 --version 1.0
```

Compare the three generated files with this archive. No solver/license,
benchmark files, network, or new measurements/replays are needed. Optional
reacquisition into new paths:

```sh
uv run --locked python -m nvvcomp_gurobi.experiment acquire .benchmarks/acopf-300-v1 --category ml4acopf_2024 --acopf-model 300
uv run --locked python scripts/acquire_comparison.py .benchmarks/acopf-300-v1 new-300-published --category ml4acopf_2024 --acopf-model 300
```

See [reproduction guidance](../../docs/comparisons.md#larger-acopf-follow-up-22)
and the [revision-scoped review](../reviews/larger-acopf-comparison-review.md).
