# ReLUSplitter published-ABC comparison inputs and statistics

Issue #11, part of #7. This is generated comparison evidence, not interpretation.
The shared [statistics implementation review](../reviews/proof-comparison-statistics-review.md) records both axes and final checks.
The selected population is all **120** version-1.0 original manifest queries,
180 seconds each. All 120 have unique pinned-source hash matches. The appended
`test_nano` row remains in `unmatched_abc`, outside every selected denominator.
No version aliases or extra queries are added. Gurobi/ABC numerical UNSAT counts
are **1/96**; common-UNSAT timing n is **1**. Accepted SAT counts are **2/24**,
retained separately. There are no accepted-answer disagreements. See generated
`statistics.md` for complete selected-population and cohort counts and timings.

## Regenerate without solver or network

```sh
uv run --locked python -m nvvcomp_gurobi.comparison experiments/relusplitter-v1 experiments/relusplitter-v1-comparison/published experiments/relusplitter-v1-comparison --category relusplitter_2026 --version 1.0
```

To reacquire inputs into a new directory (never reruns ABC):

```sh
uv run --locked python scripts/acquire_comparison.py .benchmarks/relusplitter-v1 new-relusplitter-published --category relusplitter_2026
```

Benchmark acquisition, measured hardware, resources, implementation, and timing
qualifications are in [the original archive](../relusplitter-v1/README.md).
Acquisition verifies manifest and original artifact Git blobs against benchmark
revision `303f2327a8e8411efc4457da03d2016ce42733cf`; ABC results/check caches are
from `eea564f5d0a8751d8321a409214db14d03f452b8`. `published/source.json` records
URLs, hashes, selection, and limitations. Full category CSV, source/selected
manifests, scoring reference snapshots, and published SAT witnesses/check caches
are retained. No fresh witness replay is performed by comparison code.

`evidence.json` contains per-query matches, raw outcomes, validation states,
unresolved reasons, proof/cohort populations and exact timing-denominator IDs,
plus input/calculation hashes and measured experiment context. `instances.md`
retains per-query evidence; `statistics.md` contains generated calculation data.
Depth and original-model groups use audit descriptors, not generator promises;
variants also change width/stability and are not a causal depth experiment.

All ABC matches are **source-verified, execution-unbound**. Numerical UNSAT is
not an independently checked exact-real certificate. Gurobi whole-run timing
includes startup, interpretation, construction, solving and replay; acquisition
and audit are separate, and per-query preparation is zero. ABC preparation and
run fields remain separate. No overhead subtraction, timeout imputation, combined
prepare/run ratio, or matched-hardware claim is made. ABC execution hardware,
resources and exact tool environment are unavailable in this folder. Do not pool
this study with MNIST, ACOPF, or the MVP. The [comprehensive report](../proof-comparison-analysis.md)
interprets each population separately and connects the findings to #2.
