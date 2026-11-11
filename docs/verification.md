# Verification contract

## Interface and execution

`nvvcomp_gurobi.verification.verify(Instance(onnx_path, vnnlib_path),
ExecutionLimits(timeout_seconds, threads=1))` is the single verification operation.
Use original artifact references, not parsed networks or solver models. Paths may
be relative to the caller's current directory. Explicit `.gz` files work; when a
manifest's uncompressed path is absent, `<path>.gz` is tried. Decompression and
replay copies are private; source files are never changed. Hashes identify both
the original bytes (including compression) and decompressed bytes.

The operation returns `VerificationResult`, serializable with `dataclasses.asdict`:

| Field | Meaning |
| --- | --- |
| `outcome` | `sat`, numerical `unsat`, or `unknown` |
| `reason`, `diagnostic` | Detailed explanation; unsupported inputs and failures remain data |
| `solver_status` | Unmodified integer Gurobi status, or `None` if solving never completed |
| `witness` | FLOAT32-representable inputs and CPU-replayed outputs, in C order; may retain an invalid/late candidate for diagnosis |
| `validation` | `strict`, `tolerance_only`, `invalid`, or `None` |
| `timings` | Completed interpretation/construction/solve/validation durations and whole-run `total`, in seconds |
| `provenance` | Artifact references/hashes, package and tooling versions, platform/CPU information, limits, and effective solver/replay settings |

`sat` requires accepted pinned validation. A tolerance-only witness is retained as
an accepted competition SAT report, **not** a strictly established SAT instance:
the pinned scorer gives it credit but does not use it to refute an UNSAT report.
`unsat` requires Gurobi's definitive `INFEASIBLE` status (3) on the complete encoded
conjunction. It is a floating-point numerical verdict, not an exact-real proof or
independently checkable UNSAT certificate.

Reasons include `unsupported`, `input_error`, `prerequisite_error`, `worker_error`,
`error`, `timeout`, `solver_timeout`, `solver_termination`, `ambiguous_status`,
`unexpected_unbounded`, `numerical_failure`, `validation_failed`, `infeasible`, and
`validated_witness`. Timeout, ambiguous infeasible-or-unbounded, numerical failure,
and failed replay are never UNSAT. A timely incumbent from a nondefinitive status
can establish SAT only after accepted replay; raw status remains available.
Invalid limits raise `ValueError` before execution. Missing/unreadable artifacts,
missing solver packages, license failures, and unsupported input return unresolved
results with diagnostics. Requested solver tests fail rather than skip prerequisites.

Interpretation, construction, solving, replay, package imports, and subprocess
startup all share the monotonic whole-run deadline. Gurobi gets only the remaining
time. A separate supervising process kills the worker process group at expiry;
cleanup is measured but never grants additional solved-result time. Late results
are downgraded even when they contain an accepted witness. Completed diagnostics
are checkpointed atomically, so raw status can survive a validation timeout. No
preparation analysis or persistent instance cache is used.

Execution is supported on POSIX (tested on macOS; CI uses Linux). Caller
interruption reaps the worker. The competition CLI handles SIGTERM for the same
reason. An uncatchable SIGKILL to the supervisor cannot perform cleanup; deployments
that require that guarantee should use a container/cgroup process-tree limit.
Threads limits Gurobi only; the pinned CPU validator uses 12 intra/inter-op threads,
recorded separately. There is no memory limit parameter or automatic hardware tuning.

## Supported input language

The subset is deliberately smaller than general ONNX and VNN-LIB:

- ONNX default-domain opsets 9 and 13–21; one FLOAT32 input and one FLOAT32 output of
  static shape `[1, width]`, C-order variable indexing.
- A connected sequential chain of `Gemm` layers, optionally followed by one
  `Relu` each, ending in `Gemm`. No branching, custom operators, local functions,
  sparse/external tensors, or implicit topology approximations.
- Gemm weights are finite FLOAT32 matrix initializers; biases are finite FLOAT32
  initializers of shape `[width]` or `[1, width]`. `alpha=beta=1`, `transA=0`;
  `transB=0` and `transB=1` are supported and checked. ONNX consistency is validated.
  Opset 9 is required by the audited SAT ReLU category. Its Gemm-9 and Relu-6
  schemas have the same FLOAT32 affine/broadcast/ReLU semantics used here as
  Gemm-13 and Relu-13; later optional-input and added-dtype differences are outside
  our grammar. Original models are neither converted nor rewritten for solving
  or replay. Tiny known-answer SAT/UNSAT tests exercise opset 9 directly.
- Exactly one declaration `(declare-const X_i Real)` / `(declare-const Y_i Real)`
  for each contiguous zero-based model variable, before its use.
- Repeated assertions form the **conjunction**. Each assertion is
  `(assert (<= variable operand))` or `(assert (>= variable operand))`.
  Input variables require finite scalar box bounds on both sides. Output operands
  are finite signed decimal/scientific-notation scalars or a *distinct* declared
  output variable. At least one output comparison is required. Comments and
  multiline statements are allowed; constants must have magnitude below `1e100`.
- Strict comparisons, `=`, arithmetic expressions, `and`/`or`/`not`, mixed
  input/output comparisons, input-variable comparisons, undeclared variables,
  extra commands, and other syntax are explicitly unsupported. Equality can be
  expressed using both non-strict inequalities. Distinct-output restriction also
  avoids the pinned validator's self-comparison coefficient-overwrite behavior.

For replay, whitespace/comments are normalized into one statement per line,
without changing statement order, operands, numeric spellings, declarations, or
assertions. This accommodates the pinned validator's line-oriented parser even
when the original uses multiple statements per line or spaces before `)`. The
original artifact is unchanged and its hash retained; provenance also records the
normalized replay property's hash. No semantic normalization is performed.

Example for a two-input/two-output model:

```lisp
(declare-const X_0 Real)
(declare-const X_1 Real)
(declare-const Y_0 Real)
(declare-const Y_1 Real)
(assert (>= X_0 -1))
(assert (<= X_0 1))
(assert (>= X_1 -1))
(assert (<= X_1 1))
(assert (>= Y_0 0.5))
(assert (<= Y_1 0))
```

The asserted formula is encoded directly as feasibility constraints with a
constant zero objective, never negated or replaced by a classification objective.
Gurobi-machinelearning supplies the network constraints. Gurobi numerical defaults
are unchanged; only logging, Threads, and remaining TimeLimit are set. Effective
tolerances and relevant numerical controls are recorded. Default tolerances and
FLOAT32 replay are not exact-real arithmetic; encoding feasibility alone is not SAT.

## Pinned dependencies and independent replay

`pyproject.toml` and `uv.lock` pin Gurobi **13.0.1**, gurobi-machinelearning
**1.7.0**, ONNX **1.21.0**, ONNX Runtime **1.26.0**, NumPy **2.2.6**, and cachier
**2.2.2**. Gurobi dependencies are the optional `solver` extra. Without that extra,
input rejection, protocol, and process/deadline tests still run. Tiny solver tests
isolate HOME and unset `GRB_LICENSE_FILE`; they run within the pip-bundled restricted
license limits, without personal credentials. Full benchmarks need a suitable license.

The upstream scoring environment uses Python 3.12, including `vnnlib==1.0.2` for
V2 validation. This project also moves development/CI to Python 3.12; it does not
replace validation to keep the former 3.11 environment. Only the V1 replay dependency
closure is included: `vnnlib_v1.py`, required functions from `counterexamples.py`,
and their actual runtime dependencies. V2's `vnnlib` package and reporting-only
dependencies are not imported or needed. Transitive dependencies are locked by uv;
we do not copy the full reporter's unrelated requirements (including its older
protobuf pin) into the verifier environment.

Vendored replay code is from the exact revision below, with its MIT license,
upstream hashes, and extraction description in `src/nvvcomp_gurobi/_vendor/`.
`uv run python scripts/vendor_validator.py` regenerates that subset. Only import
wiring/provider naming changes; replay, parser, dtype, and tolerance logic stay
upstream. Lint/type/whitespace tools exclude preserved upstream code, not maintained
verification code. The upstream cachier caches live only in the disposable worker
directory, not across runs.

Replay uses the original decompressed ONNX bytes on ONNX Runtime's CPU provider,
with FLOAT32 inputs. Solver-provided outputs are ignored. Strict acceptance uses
zero added input/output tolerance; tolerance-only acceptance permits `1e-4` on
input bounds and **still zero** on outputs. NumPy's pinned scalar/dtype comparison
behavior is preserved, not replaced with custom real-arithmetic checks. Invalid
replay stays unresolved, with candidate and diagnostic retained.

## Competition invocation and source alignment

Run these scripts from a checkout after installing uv 0.13.6. Installation resolves
only locked packages; it does not acquire a personal license automatically.

```sh
./install_tool.sh v1
./prepare_instance.sh v1 sat_relu /path/model.onnx /path/property.vnnlib
./run_instance.sh v1 sat_relu /path/model.onnx /path/property.vnnlib /path/result.txt 100
```

Preparation validates invocation shape only, performs **no artifact analysis**, and
prints separately measurable `preparation_seconds` and `analysis_performed=false`.
The official runner measures full preparation and run wall time externally as well.
Run uses the installed environment directly (no dependency synchronization in the
run budget) and writes `result.txt` plus `result.txt.json` with the structured result.
Executable startup accounting begins at package import, before CLI imports; the
runner additionally measures shell/interpreter startup and output I/O. There is no
startup-overhead subtraction or kill-grace credit in our verification verdicts.

The first result line is `sat`, `unsat`, `timeout`, `error`, or `unknown`.
SAT adds all X then all Y assignments, for example:

```text
sat
((X_0 1)
 (X_1 0)
 (Y_0 1)
 (Y_1 0))
```

### Automated runner/archive integration

Use the repo-owned **runner-copy adapter**, rather than the unmodified pinned
runner. It removes the result header only when archiving a SAT counterexample;
`result.txt` and its structured JSON remain unchanged. Both upstream
`check_results.sh` and `export_results.sh` copy/gzip that same witness-only archive,
so the pinned V1 validator can consume it directly. There is no ignored sidecar or
manual witness extraction step. Preparation, verification, deadlines, and numerical
policy are unchanged; extraction happens after the measured invocation.

Generate a standalone runner (Python standard library only):

```sh
curl -fL https://raw.githubusercontent.com/VNN-COMP/vnn-eval-platform/3d5a8848169fc5f0cc03ab9722865235e9857f16/vnn_comp/scripts/toolkit/run_instances.sh -o /path/run_instances.upstream.sh
uv run --locked python scripts/adapt_runner.py /path/run_instances.upstream.sh /path/staging/run_instances.sh
```

The adapter checks the **entire upstream file's SHA256**, rejects any other
revision/content, and refuses to overwrite its output. It never edits an external
checkout. The generated file embeds the extraction code and needs only `python3`
on the node, not an import from this repository. In a platform deployment, use this
generated file in the staged toolkit: the pinned `run_benchmark.sh` executes/ships
the `run_instances.sh` beside itself. Stage copies of the platform scripts; do not
point the launcher back at its original, unadapted runner. Keep the scorer pinned
to `eea564f5d0a8751d8321a409214db14d03f452b8`. No check/export/validator patch is needed.

For a direct local replay, on Linux with Bash, GNU `date`, `timeout`, `awk`, and
Python 3, first install this tool (`./install_tool.sh v1`). Use a fresh node folder
and stage a benchmark directory containing its relative-path `instances.csv`:

```sh
mkdir -p /path/node/toolkit
ln -s /absolute/path/to/this/repo /path/node/toolkit/gurobi
# Copy the benchmark to /path/node/vnncomp2026_benchmarks/benchmarks/sat_relu/1.0.
# Minimal console helpers for standalone replay; platform deployments supply their own.
cat > /path/staging/console.sh <<'SH'
log_superstage() { echo "$@"; }
log_stage() { echo "$@"; }
log_info() { echo "$@"; }
log_box_open() { echo "$@"; }
log_box_note() { echo "$@"; }
log_box_close() { :; }
log_wall() { cat; }
SH
NVVCOMP_BASE_DIR=/path/node \
NVVCOMP_BENCH_REL=vnncomp2026_benchmarks/benchmarks/sat_relu/1.0 \
NVVCOMP_NO_REPORT=1 COMP_LOG_LIB=/path/staging/console.sh \
competition_year=2026 benchmark_name=sat_relu vnnlib_version=1.0 \
script_dir=gurobi run_networks=all run_as_root=false task_id=local \
bash /path/staging/run_instances.sh
```

`NVVCOMP_BASE_DIR`/`NVVCOMP_BENCH_REL` relocate the pinned loop; without them its
platform paths are unchanged. `NVVCOMP_NO_REPORT=1` disables only backend HTTP
callbacks. `TMPDIR` optionally relocates its standard `result_<task_id>.txt`.
Use unique task IDs and fresh run directories, as with upstream. Results land in
`/path/node/logs/results_sat_relu.csv`, with witness-only `.counterexample` files
in `logs/counterexamples/sat_relu/`. Gzip those files unchanged for the pinned
scorer's archive layout. This is compression only, not format repair.

Missing witnesses or malformed/nonfinite/duplicate SAT assignments produce no counterexample
and an `error_invalid_counterexample` CSV verdict, never a credited SAT or UNSAT.
Structural checks are not semantic validation: the pinned validator remains the
acceptance authority. Non-SAT results create no counterexample, and an old witness
at that instance's archive path is removed. The integration test runs the actual
hash-pinned runner through the actual tool scripts, compresses its archive exactly
as check/export do, and passes that archive directly to pinned `get_ce_diff`.
This establishes tiny V1 integration, not an AWS/backend deployment test or full
report-generation/scoring test.

Pinned primary sources:

| Source | Revision |
| --- | --- |
| [Benchmarks, SAT ReLU 1.0](https://github.com/VNN-COMP/vnncomp2026_benchmarks/tree/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks/sat_relu/1.0) | `303f2327a8e8411efc4457da03d2016ce42733cf` |
| [Rules](https://github.com/VNN-COMP/vnncomp2026/blob/b0ec5ac3c8f39262f07a1c67919fbb89fa42a245/rules.md) | `b0ec5ac3c8f39262f07a1c67919fbb89fa42a245` |
| [Runner](https://github.com/VNN-COMP/vnn-eval-platform/blob/3d5a8848169fc5f0cc03ab9722865235e9857f16/vnn_comp/scripts/toolkit/run_instances.sh) | `3d5a8848169fc5f0cc03ab9722865235e9857f16` |
| [Validator/scoring](https://github.com/VNN-COMP/vnncomp2026_results/tree/eea564f5d0a8751d8321a409214db14d03f452b8/SCORING) | `eea564f5d0a8751d8321a409214db14d03f452b8` |

These are reference tooling revisions, **not a claim that arbitrary caller artifacts
belong to that benchmark revision**; artifact hashes are authoritative for a run.
This implementation establishes tiny-instance integration, not full category
eligibility, a permanent benchmark smoke suite, or benchmark performance results.

Known upstream discrepancies are kept explicit:

1. The rules' main output section and runner accept `sat`/`unsat`; the older script
   paragraph says `violated`/`holds`. We emit the former, which scoring normalizes.
2. Prose mentions output agreement within `1e-3` relative and constraints within
   `1e-4` absolute. Executable V1 validation ignores supplied Y values and allows
   tolerance only on input bounds. We follow that pinned executable policy.
3. The unmodified runner archives the SAT header, whereas pinned V1 validation
   expects only the witness. The runner-copy adapter above resolves this mismatch
   automatically at the archive boundary without changing either the standard
   result format or the upstream validator. Use that entry point for integration.
4. Scoring subtracts observed startup overhead before its timeout comparison. Our
   local results retain actual whole-run time and reject late solves regardless;
   any future experiment summaries must retain this distinction.
