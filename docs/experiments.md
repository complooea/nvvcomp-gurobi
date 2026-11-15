# Manifest-driven experiments

Experiment execution owns selection, accounting, persistence, and reporting. It
calls the unchanged [verification interface](verification.md) with original
artifact references and prescribed execution limits. It never supplies parsed
models, cached encodings, or an alternative validation implementation.

## Reproduce locally

Use Python 3.12, uv 0.13.6, and an appropriate local Gurobi license. Do not put
license files, environment dumps, or credentials in experiment output. Routine CI
uses tiny fixtures; it never downloads or runs this category.

```sh
uv sync --locked --extra solver
uv run --locked python -m nvvcomp_gurobi.experiment acquire .benchmarks/sat-relu-v1
uv run --locked python -m nvvcomp_gurobi.experiment audit .benchmarks/sat-relu-v1/instances.csv experiments/sat-relu-v1
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/sat-relu-v1/instances.csv experiments/sat-relu-v1 --stop-after 1
# Inspect records/0000.json before continuing. This is the first real execution,
# not a separate benchmark test suite. A timeout is a legitimate measurement.
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/sat-relu-v1/instances.csv experiments/sat-relu-v1
uv run --locked python -m nvvcomp_gurobi.experiment report experiments/sat-relu-v1
```

Use a **fresh output directory** for a new experiment. Repeating `run` resumes
missing records, never overwrites existing results, and rejects changed source,
manifest, resource settings, or audited artifacts. A `.running` exclusive file
prevents concurrent writers. If a process was killed without cleanup, first verify
its PID is no longer running before removing that one lock file. Do not delete
records to hide failures or rerun difficult instances within the same experiment.

Acquisition downloads from benchmark revision
`303f2327a8e8411efc4457da03d2016ce42733cf`, preserves compressed bytes, and records
URLs and SHA256 identities. Manifest paths are relative to its directory;
uncompressed names fall back to `<name>.gz`. Acquisition requires an empty
directory, or a completed, hash-verified existing inventory. After an interrupted
download, use a new directory rather than trusting a partial cache.

## Accounting and timing

### Original IEEE-118/300 ACOPF 1.0

Use the existing acquisition interface with `--category ml4acopf_2024` and
`--acopf-model 118` or `--acopf-model 300` (the default remains 14).
Each acquisition retains the full source manifest, but selects only the exact
original model, never its linear/residual variants or smoke rows. Source order
is preserved: IEEE-118 properties **2, 4, 3, 5, 6** and IEEE-300 properties
**3, 105, 2, 4**. Missing, duplicate or wrong-budget selected rows abort acquisition.

```sh
uv run --locked python -m nvvcomp_gurobi.experiment acquire .benchmarks/acopf-118-v1 --category ml4acopf_2024 --acopf-model 118
uv run --locked python -m nvvcomp_gurobi.experiment acquire .benchmarks/acopf-300-v1 --category ml4acopf_2024 --acopf-model 300
uv run --locked python -m nvvcomp_gurobi.experiment audit .benchmarks/acopf-118-v1/instances.csv experiments/acopf-118-v1 --threads 1
uv run --locked python -m nvvcomp_gurobi.experiment audit .benchmarks/acopf-300-v1/instances.csv experiments/acopf-300-v1 --threads 1
# Inspect both complete audits before executing either population.
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/acopf-118-v1/instances.csv experiments/acopf-118-v1 --threads 1
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/acopf-300-v1/instances.csv experiments/acopf-300-v1 --threads 1
uv run --locked python -m nvvcomp_gurobi.experiment report experiments/acopf-118-v1
uv run --locked python -m nvvcomp_gurobi.experiment report experiments/acopf-300-v1
```

Use fresh acquisition/output paths for a new measurement; the paths above name
the retained archives, not permission to replace them. Complete repository checks
and tiny solver tests first. Run the populations sequentially, without concurrent
tests or other experiment workloads. All nine queries retain **600-second
whole-run deadlines: 90 minutes maximum run budget**, plus acquisition, audit,
supervision and persistence overhead. Preparation performs no analysis and is
separate; all per-query analysis remains inside the deadline. This is
competition-aligned timing/accounting, not an official distributed-runner run.
One Gurobi solver thread is a local study choice, not a competition rule.
Original-ONNX replay retains 12 intra/inter-op CPU threads; the whole process
is not single-threaded. Numerical defaults and replay tolerances are unchanged.

All four structural checks concern generation (property 3) or voltage magnitude
(property 4) bounds. The latter's upstream comment incorrectly says generation.
The five physical-residual checks concern thermal limits (property 2 on each
model) or power balance (IEEE-118 properties 5/6, IEEE-300 property 105).
The complete graph is represented even for structural checks. Interpret these
as distinct property populations, not partial versus complete graph encodings.
Missing/corrupt artifacts require repair before execution; genuine unsupported
semantics are blockers, not permission to shrink the nine-query population.
See the separate [IEEE-118](../experiments/acopf-118-v1/README.md) and
[IEEE-300](../experiments/acopf-300-v1/README.md) archives for audit and outcomes.
Historical IEEE-14 measurements are not rerun or overwritten.

#### ACOPF semantic audit procedure

Before execution, use the existing `run_experiment(..., audit_only=True)` public
interface (the `audit` CLI command). It reads every original graph/property pair
through the same interpreter as verification. Check finite constants and finite
input boxes, contiguous declarations, complete supported assertions, static
tensor shapes and attributes through whole-graph lowering. Missing/corrupt
inputs abort preflight for repair; genuine unsupported semantics are explicit
blockers, not permission to reduce the selected population.

The original IEEE-118/300 graphs use opset 14 and static FLOAT32 input/output
tensors. Relevant attributes include Gemm `alpha/beta/transB`, Constant and
ConstantOfShape tensor `value`, Concat/Gather `axis`, and Transpose `perm`.
Slice indices/steps, Gather indices and Expand/shape scaffolding must be
constant. Equal/Where are supported only on constant shape scaffolding, not
data-dependent branches. Broadcasting, static views and sparse constant-weight
MatMul follow the existing semantics; Pow uses supported squares and Sin/Cos
use radians.

Represent the complete graph for every query, including generation/voltage
bound checks. Shared intermediates are represented once; zero coefficients,
identity views and constant scaffolding are folded without property-dependent
output-cone pruning. Quadratic equalities represent squares/products;
Sigmoid/Sin/Cos use global nonlinear relations (`FuncNonlinear=1`), not fixed
piecewise approximations. Intermediate bounds use the existing conservative
interval policy, not additional physical assumptions. Data-dependent Boolean
operations, variable division and general powers remain unsupported.

Audit classifications against the
[original property generator](https://github.com/AI4OPT/ml4acopf_benchmark/blob/cdbde645123927ec95a3c01b66ec934077725e19/generate_properties.py)
at revision `cdbde645123927ec95a3c01b66ec934077725e19`, using original output
definitions rather than comments or published verdicts. Preserve the original
property bytes, scalar thresholds and input bounds; do not regenerate them.
The separate archive READMEs retain model-specific descriptor counts, output
indices and classifications: [IEEE-118](../experiments/acopf-118-v1/README.md#graph-and-property-audit)
and [IEEE-300](../experiments/acopf-300-v1/README.md#graph-and-property-audit).
Across these archives there are four structural-output-bound and five
physical-residual checks.

Keep initializer elements, tensor-node counts, scalar operation counts and
measured formulation sizes distinct. Pre-presolve variables, binaries,
linear/general/quadratic constraints and linear nonzeros are recorded in
`result.provenance.formulation_size`; unavailable measurements remain
unavailable. Audit eligibility establishes supported semantics, not numerical
correctness, matched hardware, a controlled scaling law or a causal graph-type
effect. Cross-tool interpretation belongs in the comparison analysis.

The completed archives now have separate solver-free
[IEEE-118](../experiments/acopf-118-v1-comparison/README.md) and
[IEEE-300](../experiments/acopf-300-v1-comparison/README.md) comparisons.
[Comparison reproduction](comparisons.md#acopf-comparisons) consumes saved
measurements; it does not repeat this acquisition/audit/run workflow or either
verifier. IEEE-14 stays a separate saved reference.

### IEEE-14 ACOPF 1.0

Use the same workflow with `--category ml4acopf_2024`, benchmark directory
`.benchmarks/acopf-v1`, and a fresh experiment output directory. Acquisition
selects exactly `./onnx/14_ieee_ml4acopf.onnx` and its 14 properties at the pinned
revision, excluding linear/residual aliases and other models. It preserves the
complete original category manifest as `source-instances.csv` and records the
exact-model selection used to derive the 14-row execution `instances.csv`.
The audit retains original artifact hashes, full tensor-DAG operations and scalar
relation counts, and the distinction between properties 3/4 (structural output
bounds) and the other 12 (physical residuals). All deadlines are 600 seconds;
the worst-case query budget is 140 minutes plus separately measured overhead.

Review the implementation and tiny solver-backed cases, then inspect all 14 audit
entries before the full run. Do not substitute a property-2 encoder or discard
unsupported/failed cases to reduce this study. Actual construction/solve failures
and timeouts belong in the archive. Published ABC outcomes are comparison evidence,
not independent certificates or correctness oracles.

### Sigmoid MNIST 1.0

Use the same acquisition/audit/run/report commands with category
`--category dist_shift_2023`, benchmark directory `.benchmarks/mnist-sigmoid-v1`
and a fresh experiment output directory. Acquisition verifies exactly 72 rows,
all naming `./onnx/mnist_concat.onnx`, with 300-second deadlines, from version
1.0 at the pinned revision. It downloads no other models or version aliases.
The worst-case query budget is six hours plus separately measured acquisition,
audit and supervision overhead. The original duplicate opset-11 imports and
INT64 reshape metadata are preserved. Native global nonlinear logistic
relations represent internal sigmoids; original-shape FLOAT32 replay is required
for SAT. See `experiments/mnist-sigmoid-v1/README.md` for the measured archive.

### ReLUSplitter 1.0

Use the same workflow for the complete 120-row ReLUSplitter selection:

```sh
uv run --locked python -m nvvcomp_gurobi.experiment acquire .benchmarks/relusplitter-v1 --category relusplitter_2026
uv run --locked python -m nvvcomp_gurobi.experiment audit .benchmarks/relusplitter-v1/instances.csv experiments/relusplitter-v1
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/relusplitter-v1/instances.csv experiments/relusplitter-v1 --stop-after 1
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/relusplitter-v1/instances.csv experiments/relusplitter-v1
uv run --locked python -m nvvcomp_gurobi.experiment report experiments/relusplitter-v1
```

Acquisition verifies 120 rows with 180-second deadlines at the same pinned
benchmark revision. The worst-case query budget is six hours, plus acquisition,
audit and supervision overhead. These are experiments, never routine tests.
The audit inspects every original graph and property using the execution
interpreter. Descriptors record hidden ReLU depth and widths, output alternative
counts, and original-model group (filename prefix before `~`, with `.onnx` removed, not a functional
equivalence claim). Generated variants can vary width and stability as well as
depth. Per-result provenance records the actual formulation, pre-presolve model
size, solver defaults and environment. Construction failures remain unresolved
attempts, not exclusions or numerical UNSAT.

### SAT ReLU 1.0

All 100 network/property pairs are audited before any solving. Eligibility uses
the existing verification grammar and never filenames, claimed labels, runtime,
or solver results. Only explicit unsupported semantics justify exclusion.
The full category uses original ONNX opset 9 models; support was completed before
solving, with unchanged FLOAT32 Gemm/ReLU semantics and no opset conversion.
Missing/corrupt artifacts and unexpected audit failures abort the preflight for
repair, rather than reducing the eligible denominator. Conversion/solver errors,
validation failures, and timeouts after selection remain eligible records.

The audit is separately measured **category selection work**, not per-instance
solver preparation. It is not reused by verification: each invocation rereads,
interprets, constructs, solves, and validates within its prescribed deadline.
Preparation is a no-op, matching the competition wrapper's no-analysis policy;
its analysis time is zero. No platform preparation subprocess is invoked by this
direct Python experiment. This is contract-aligned local execution, not an
execution of the official distributed runner.

Execution is sequential, uses one Gurobi thread, and retains the pinned CPU
validator's 12 intra/inter-op threads. No memory cap or numerical/performance
tuning is introduced. Budget 100 × 100 seconds = **2h46m40s**, plus acquisition,
audit, supervision/cleanup, persistence, inspection, and reporting overhead. Early
solves can reduce runtime. Per-instance whole-run timing includes startup and all
verification stages, not just optimization. Invocation wall time additionally
measures supervision and cleanup. No startup subtraction or kill-grace credit.

## Saved artifacts

- `experiment.json`: complete pre-solve audit, semantic exclusions, architecture
  dimensions, original/compressed and decompressed hashes, acquisition inventory,
  source and lockfile hashes, reference revisions, packages, hardware, resources.
- `instances.csv`: original manifest bytes, or the documented exact-model
  selection for ACOPF (with its full source manifest in the acquisition inventory).
- `records/<id>.json`: manifest-order identity, eligibility, artifact hashes,
  preparation/invocation times, structured verification result, raw status,
  witness, strict/tolerance-only/invalid classification, diagnostics, stage times,
  effective solver settings, encoding/validator/package provenance.
- `summary.json`, `report.md`: regenerated from saved inputs without artifacts,
  Gurobi, or a license. Missing and malformed records are visible. Runtime
  summaries state their population; unknown/missing stage times are not zero.

Each per-instance record is atomically replaced, flushed, and fsynced (including
the containing directory) before proceeding. A start record is persisted before
invocation; if interrupted before completion, it remains an unresolved
`interrupted` result with unavailable timing, never silently retried. Completed
failures are not retried. Reports may be generated for an interrupted experiment.

## Interpretation and scoring

The category varies width, not architecture: one hidden ReLU layer between two
Gemm operations, two outputs, 5–95 inputs, hidden widths 29–1,071, and
234–100,676 stored weight/bias elements. See the audit for measured dimensions.
FLOAT32 replay and unchanged Gurobi numerical defaults do not constitute exact
arithmetic. Numerical UNSAT is solver-reported, not independently certified.

References are pinned in `experiment.json` and [verification.md](verification.md).
At scoring revision `eea564f5d0a8751d8321a409214db14d03f452b8`,
`SCORING/process_results.py:get_score` awards 10 points for an accepted SAT witness;
the time bonus is disabled. The report gives this **SAT-only subset contribution**,
not an assumed 10 points for every numerical UNSAT. Strict witnesses can refute
UNSAT; tolerance-only witnesses receive SAT credit but cannot refute UNSAT.

Full eligible-subset points and category-normalized scores remain unavailable
without artifact-matched cross-tool conflict evidence and participating-tool
context. Published result CSVs and witness-check caches exist at that revision,
but the inspected cache records contain witness hashes and name/version identity,
not network/property artifact hashes. They are not automatically treated as
proof of correspondence with this pinned benchmark. No filename becomes ground
truth. Matching and comparing published ABC measurements belongs to issue #5;
this report makes no cross-hardware speed or solver-superiority claim.

## Tests

```sh
uv run --locked pytest tests/test_experiment.py
```

Tests cross the experiment's public run/report interface with small manifests,
original artifact fixtures, controlled verification outcomes, and saved records.
They establish accounting, argument forwarding, progressive persistence,
exclusions, resume safety, failure retention, validation distinctions, missing or
corrupt records, runtime summaries, and scoring limitations. Existing verification
tests own numerical correctness; this ticket does not duplicate them or add a
real-category regression suite.
