# Sigmoid MNIST published-ABC comparison inputs and statistics

See the shared [implementation review](../proof-comparison-review.md) for both review axes and final checks.

Issue #11, part of #7. This is comparison evidence, not interpretation. All **72**
version-1.0 `dist_shift_2023` / `mnist_concat` manifest queries, 300 seconds each,
have unique pinned-source hash matches. The appended `test_nano` result remains
unmatched, outside every selected denominator. No other model/version aliases
are selected. Gurobi/ABC numerical UNSAT counts are **42/64**; common-UNSAT timing
n is **42**. Accepted SAT counts are **6/8**; there are no accepted-answer
disagreements. Generated `statistics.md` separately retains the **64 published
UNSAT** and **eight published SAT** cohorts, including all unresolved queries.
Published cohorts are claims, not independently established truth labels.

## Regenerate without solver or network

```sh
uv run --locked python -m nvvcomp_gurobi.comparison experiments/mnist-sigmoid-v1 experiments/mnist-sigmoid-v1-comparison/published experiments/mnist-sigmoid-v1-comparison --category dist_shift_2023 --version 1.0
```

Reacquire inputs into a new directory (no ABC execution):

```sh
uv run --locked python scripts/acquire_comparison.py .benchmarks/mnist-sigmoid-v1 new-mnist-published --category dist_shift_2023
```

See [the measured archive](../mnist-sigmoid-v1/README.md) for benchmark acquisition,
actual formulation, implementation, hardware/resources, and accounting. Inputs
pin benchmark `303f2327a8e8411efc4457da03d2016ce42733cf` and published results
`eea564f5d0a8751d8321a409214db14d03f452b8`. Acquisition verifies original artifact
and manifest Git blobs; `published/source.json` retains source URLs/hashes,
selection and limitations. Full category CSV, source/selected manifests, scoring
reference snapshots, and published SAT witness/check caches are archived. Check
correspondence is authenticated, but comparison does not freshly replay witnesses.

`evidence.json` retains per-query identities and measurements, raw outcomes,
validation/unresolved states, proof/cohort IDs and timings, and input/calculation
hashes with measured experiment context. `instances.md` is per-query evidence;
`statistics.md` is generated calculation data, not causal analysis.

Every ABC match is **source-verified, execution-unbound**. Numerical UNSAT is
not an exact-real certificate. Gurobi whole-run timing includes startup,
interpretation, construction, solving and validation; acquisition and audit are
separate and per-query preparation is zero. Published ABC preparation and run
fields are separate: no automatic combined ratios, overhead subtraction, or
timeout imputation. Ratios use only common-UNSAT runs with known times and a
positive Gurobi denominator, not matched hardware. ABC execution resources and
tool environment are absent. This population stays separate from ReLUSplitter,
ACOPF and the [MVP](../sat-relu-v1-comparison/README.md), supplying inputs rather
than a pooled claim for the subsequent analysis relating to #2.
