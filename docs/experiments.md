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
- `instances.csv`: exact original manifest bytes.
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
