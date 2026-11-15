# Original IEEE-118/300 ACOPF semantic audit

Issue [#21](https://github.com/complooea/nvvcomp-gurobi/issues/21), under
[#20](https://github.com/complooea/nvvcomp-gurobi/issues/20). This is an
eligibility/interpretation audit, not a comparison with published ABC outcomes.
Both complete populations passed preflight before either was executed.

## Sources and selection

- Benchmark revision: `303f2327a8e8411efc4457da03d2016ce42733cf`,
  category `ml4acopf_2024`, version `1.0`.
- Exact original networks: `118_ieee_ml4acopf.onnx` and
  `300_ieee_ml4acopf.onnx`. No linear/residual variants or smoke rows.
- Source order: IEEE-118 properties **2, 4, 3, 5, 6**; IEEE-300 properties
  **3, 105, 2, 4**. Five plus four queries, all with 600-second deadlines.
- Each archive retains the full `source-instances.csv`, selected `instances.csv`,
  and acquisition inventory in `experiment.json`. Original gzip bytes remain
  in ignored `.benchmarks/`; acquisition URLs, byte counts, compressed SHA256 and
  decompressed SHA256 are retained for reproducible retrieval.
- [Original property generator](https://github.com/AI4OPT/ml4acopf_benchmark/blob/cdbde645123927ec95a3c01b66ec934077725e19/generate_properties.py):
  revision `cdbde645123927ec95a3c01b66ec934077725e19`.

## Graph semantics

The existing `run_experiment(..., audit_only=True)` reads every original graph
and property through the same interpreter as verification. All nine are
eligible. Missing/corrupt bytes abort preflight, not become denominator
exclusions. Neither model required an interpreter expansion or approximation.

Both graphs use opset 14 with one static FLOAT32 input and output. The audit
checks finite constants and finite input boxes, contiguous declarations,
complete supported assertions, tensor shapes, and attributes through whole-graph
lowering. Attributes include Gemm `alpha/beta/transB`, Constant and
ConstantOfShape tensor `value`, Concat/Gather `axis`, and Transpose `perm`.
Slice indices/steps, Gather indices and Expand/shape scaffolding are constant.
Equal/Where only operate on constant shape scaffolding, not data-dependent
branches. Broadcasting, static views and sparse constant-weight MatMul preserve
the existing semantics. Pow uses supported squares; Sin/Cos use radians.

Native Gurobi scalar relations encode all outputs for every query, including
generation and voltage bound properties. Quadratic equalities represent
squares/products; Sigmoid/Sin/Cos use global nonlinear function relations
(`FuncNonlinear=1`), not fixed piecewise approximations. Shared intermediates
are represented once. Zero coefficients, identity views and constant shape
scaffolding are folded; there is no property-dependent output-cone pruning.
Intermediate bounds follow the existing conservative interval policy, not
additional assumed physical constraints. Data-dependent Boolean operations,
variable division and general powers remain unsupported.

| Descriptor | IEEE-118 | IEEE-300 |
| --- | ---: | ---: |
| Input shape | `[1,198]` | `[1,402]` |
| Output shape | `[1,1696]` | `[1,3804]` |
| Tensor nodes | 168 | 168 |
| Stored initializer elements | 163,868 | 680,014 |
| Scalar affine relations | 6,436 | 13,538 |
| Scalar ReLUs | 512 | 1,024 |
| Scalar sigmoids | 226 | 438 |
| Scalar squares | 1,234 | 2,766 |
| Scalar variable products | 558 | 1,233 |
| Scalar sines | 186 | 411 |
| Scalar cosines | 186 | 411 |

These are different descriptors, not interchangeable measures of verification
difficulty. Measured pre-presolve variables, binaries, linear/general/quadratic
constraints and linear nonzeros belong to each completed construction's
`result.provenance.formulation_size`, not this source-graph table.
Unavailable construction measurements must remain unavailable.

## Property semantics

Classification follows original output definitions and the generator's indexing,
not property comments or published verdicts. There are **four structural output
bound** and **five physical residual** checks. Structural bounds have physical
meaning too; this distinction does not mean physical versus nonphysical graphs.

| Grid | Property | Class | Meaning | Asserted output indices (inclusive) | Comparisons |
| --- | ---: | --- | --- | --- | ---: |
| 118 | 2 | physical residual | thermal-limit residual | 1189 | 1 |
| 118 | 4 | structural output bound | voltage magnitude bounds | 108–225 | 236 |
| 118 | 3 | structural output bound | active/reactive generation bounds | 0–107 | 216 |
| 118 | 5 | physical residual | active power balance residual | 1464 | 2 |
| 118 | 6 | physical residual | active power balance residual | 1518 | 2 |
| 300 | 3 | structural output bound | active/reactive generation bounds | 0–137 | 276 |
| 300 | 105 | physical residual | active power balance residual | 3244 | 2 |
| 300 | 2 | physical residual | thermal-limit residual | 2382 | 1 |
| 300 | 4 | structural output bound | voltage magnitude bounds | 138–437 | 600 |

The generator places generation in the first `2*G` outputs and voltage magnitude
in the next `N`. Property 4 compares `Y_(i+2*G)` against `vmax/vmin ± 1e-6`;
its “generation bounds” comment is wrong. Property 3 uses `pmax/pmin` and
`qmax/qmin ± 1e-6`. IEEE-118 has `G=54,N=118,E=186`; IEEE-300 has
`G=69,N=300,E=411`. Property 2 selects a thermal residual from the block starting
at `outputs - 2*N - 2*E`. Properties 5/6/105 select signed alternatives on one
active-power residual from the block starting at `outputs - 2*N`.
All original scalar thresholds and finite input bounds are preserved, not
regenerated from the generator or replaced with physical assumptions.

## Execution and handoff

See the separate [IEEE-118 archive](acopf-118-v1/README.md) and
[IEEE-300 archive](acopf-300-v1/README.md) for every outcome, including unresolved
records, stage availability, measured sizes, hardware and effective settings.
[Reproduction instructions](../docs/experiments.md#original-ieee-118300-acopf-10)
use the existing acquisition, audit, run and solver-free report interfaces.
The nine original budgets total 90 minutes plus overhead. Numerical UNSAT is
not an independently checked exact-real certificate. Any SAT candidate requires
the existing original-ONNX FLOAT32 replay before acceptance.

No historical IEEE-14 or other archived measurements are changed. Published ABC
outcomes are not correctness oracles; pairing and broader interpretation belong
to the dependent comparison ticket. This audit does not establish matched
hardware, a controlled scaling law, or a causal graph-type effect.
