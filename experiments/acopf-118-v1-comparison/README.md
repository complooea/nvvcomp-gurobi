# Original IEEE-118 ACOPF: saved Gurobi–ABC comparison

Issue [#22](https://github.com/complooea/nvvcomp-gurobi/issues/22), part of #20.
All **five** selected original queries (properties **2, 4, 3, 5, 6**, source order)
have records and unique source-hash ABC matches. No exclusions or missing/corrupt
records. Gurobi/ABC numerical UNSAT counts are **3/5**, accepted SAT **0/0**,
unresolved **2/0**: local thermal property 2 timed out and generation property 3
failed original-ONNX replay. Neither is proof or accepted SAT. There are **zero
accepted-answer disagreements**, not independent correctness confirmation.

[Statistics](statistics.md), [exact pair table](instances.md), and
[evidence JSON](evidence.json) retain all identities, cross-tabs, unresolved
reasons and exact paired timing populations. The **three physical-residual**
queries have 2/3 Gurobi/ABC UNSAT; the **two structural-output-bound** queries
have 1/2. Property 4 is voltage magnitude, despite its misleading upstream comment.
Every query encoded the complete graph; structural checks also have physical meaning.

## Common-proof runtime, not completion

| Population | Exact local IDs | n | G run sum s | ABC run sum s | ABC/G sum ratio | Median individual ratio |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| All classes | 0001, 0003, 0004 | 3 | 100.428847 | 25.494154 | 0.253853 | 1.382788 |
| Physical residual | 0003, 0004 | 2 | 8.954166 | 15.875329 | 1.772954 | 1.925519 |
| Structural output bound | 0001 | 1 | 91.474681 | 9.618826 | 0.105153 | 0.105153 |

Ratios are observed ABC/Gurobi whole-run seconds, not hardware-normalized
speedups. Both residual pairs favor Gurobi, but the structural voltage check
favors ABC and dominates the all-class sum ratio; that sum and the individual
median point in different directions. The unresolved thermal query is not a
paired proof. See the [size-progression analysis](../proof-comparison-analysis.md#larger-acopf-size-progression)
for interpretation alongside separate IEEE-14 and IEEE-300 populations.

## Sources and accounting

The [experiment](../acopf-118-v1/README.md) documents semantics, actual formulation
sizes, effective settings, environment and measurement commits. Its saved bytes
are unchanged. Published rows **15–19** of the full 70-row category CSV match the
exact original network/property paths. **65 unselected rows**, including other
models, linear/residual variants and the appended smoke row, remain outside this
denominator in `unmatched_abc`.

`published/source.json` pins benchmark
`303f2327a8e8411efc4457da03d2016ce42733cf` and published-results
`eea564f5d0a8751d8321a409214db14d03f452b8`. Acquisition verifies the entire source
manifest, exact selected manifest and original compressed artifacts against pinned
Git blobs; stored/decompressed hashes are retained. The full CSV, source/selected
manifests, reference scoring snapshots and all category SAT witness/check caches
are retained, including unselected context. No selected IEEE-118 row claims SAT.
No ABC execution or fresh replay occurred; cache correspondence is not cache
correctness or proof that historical ABC execution used the matched bytes.
All five source matches are **execution-unbound**; ABC resources are unknown.
Numerical UNSAT is not an independently checked certificate.

All-selected G/ABC run sums are **710.583275/154.464708 s**; preparation sums are
**0/99.270815 s**, separately. These all-run costs include unresolved local work,
not equal-coverage proof timing. Original raw **600-second** deadlines apply;
startup, interpretation, construction, solving and replay remain inside Gurobi
run time. Acquisition/audit are separate. No startup subtraction, timeout
imputation, late-completion credit or combined preparation/run ratio is used.

## Regenerate without solver or network

```sh
uv run --locked python -m nvvcomp_gurobi.comparison experiments/acopf-118-v1 experiments/acopf-118-v1-comparison/published fresh-118-comparison --category ml4acopf_2024 --version 1.0
```

Compare the three generated files with this archive. Only saved audit/records and
published snapshots are needed, not original models, a solver/license, or new
measurements. Reacquisition, not required for regeneration:

```sh
uv run --locked python -m nvvcomp_gurobi.experiment acquire .benchmarks/acopf-118-v1 --category ml4acopf_2024 --acopf-model 118
uv run --locked python scripts/acquire_comparison.py .benchmarks/acopf-118-v1 new-118-published --category ml4acopf_2024 --acopf-model 118
```

See [reproduction guidance](../../docs/comparisons.md#larger-acopf-follow-up-22)
and the [revision-scoped review](../reviews/larger-acopf-comparison-review.md).
