# Experiment reports and evidence

Start with the [comprehensive Gurobi–ABC comparison](proof-comparison-analysis.md).
It covers the shallow-ReLU MVP originating in #2 and the three expanded studies
in #7. Each workload retains its own population, deadlines and runtime denominators;
there is no pooled score or speed ratio.

| Study | Gurobi measurements and formulation | Published-ABC comparison evidence |
| --- | --- | --- |
| Shallow-ReLU MVP (#2) | [experiment](sat-relu-v1/README.md) | [evidence](sat-relu-v1-comparison/evidence.json), [all pairs](sat-relu-v1-comparison/instances.md), [source inventory](sat-relu-v1-comparison/published/source.json) |
| ReLUSplitter | [experiment](relusplitter-v1/README.md) | [statistics and inputs](relusplitter-v1-comparison/README.md) |
| Internal-sigmoid MNIST | [experiment](mnist-sigmoid-v1/README.md) | [statistics and inputs](mnist-sigmoid-v1-comparison/README.md) |
| IEEE-14 ACOPF | [experiment](acopf-v1/README.md) | [statistics and inputs](acopf-v1-comparison/README.md) |

The former MVP comparison narrative has been incorporated into the comprehensive
report and deleted; its original text remains in Git history. Measurement records,
generated comparison files and published inputs remain unchanged.

Reviews are supporting process records, not alternative research reports:

- [MVP comparison review](reviews/sat-relu-comparison-review.md): historical checks
  and review of the original MVP comparison.
- [Statistics implementation review](reviews/proof-comparison-statistics-review.md):
  #11's shared calculation implementation.
- [Analysis review](reviews/proof-comparison-analysis-review.md): #12's original
  three-study narrative; its reviewed revision is explicitly recorded.

See [comparison instructions](../docs/comparisons.md) for solver-free reproduction.
