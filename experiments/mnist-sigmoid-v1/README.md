# Sigmoid MNIST 1.0 Gurobi experiment

Issue #9, implementing the internal-sigmoid slice of #7. This archive uses the
existing `verify(Instance, ExecutionLimits)` workflow, original artifacts,
sequential execution, one Gurobi thread, unchanged numerical defaults, and
independent FLOAT32 original-ONNX witness replay. Numerical UNSAT is not an
independently certified exact-real proof. Benchmark runs are experiments, not tests.

## Selection and graph audit

Benchmark revision: `303f2327a8e8411efc4457da03d2016ce42733cf`, category
`dist_shift_2023`, version `1.0`, `mnist_concat` only. The pinned manifest contains
exactly 72 rows, each with a 300-second deadline. Acquisition preserves 74 files:
the manifest, one compressed original model and 72 compressed properties, with
URLs, stored-byte SHA256 and decompressed artifact hashes. No other models or
version aliases are acquired. All 72 original queries were audited as eligible.

The model has static FLOAT32 input `[1,792]` and output `[1,10]`, five Gemm
layers, three ReLU layers (200/32/32 scalar outputs), one sigmoid layer (784
scalar outputs), and two reshapes. Hidden affine widths are `[200,784,32,32]`.
Both default-domain imports are opset 11. INT64 initializer shapes
`[-1,1,28,28]` and `[-1,784]` reshape the internal sigmoid output without
permuting its C-order coordinates. Original imports, tensor order and bytes are
preserved; the model is neither converted nor normalized for replay.

Construction uses native Gurobi affine equalities, max/ReLU constraints and
logistic relations with `FuncNonlinear=1`, not fixed piecewise approximations.
Sigmoid outputs have valid conservative bounds `[0,1]`, ReLU outputs are
nonnegative, and affine values are free. No extra domain restrictions or
numerical tuning are applied. The existing affine/ReLU-only importer remains in
use for that subset. Compact real-verifier tests independently establish a
reachable smooth output with original-shape replay and an impossible threshold
above the analytic range; published ABC outcomes are not test oracles.

## Recorded outcomes

All 72 original queries were attempted, with **42 numerical UNSAT, 6 strict
replay-accepted SAT and 24 unknown/timeouts**. There are no missing, corrupt or
excluded records, and no tolerance-only accepted witnesses. SAT IDs in manifest
order are `0013`, `0025`, `0038`, `0043`, `0055`, and `0068`.

All formulations finished construction (0.063–0.298 seconds per query; 20.416
seconds summed). Each pre-presolve model has 2,908 variables, zero explicit
binary variables, 1,069 linear constraints, 1,048 general constraints (784
logistic and 264 ReLU), and 342,712 linear nonzeros. General constraints may
introduce internal solver structure; these are not post-presolve size claims.
No construction or license failure was observed.

Summed whole-run time is 13,338.852 seconds (about 3h42m19s); summed invocation
time is 13,338.866 seconds. Acquisition took 242.363 seconds and audit took 0.587
seconds, measured separately. Preparation performed no analysis. Of 24 timeouts,
13 retain raw Gurobi status 9; 11 have no completed-status checkpoint before
supervision terminated the worker. Completed solve-stage timings exist for 61
queries, validation timings for the six SAT candidates. Unavailable stage times
are not zero. Every record retains construction provenance and whole-run timing.

Implementation commit: `3633256b54f1f3daf8e9e4d970e41a216b6c4341`. The audit records
the measured source and lockfile hashes. All 132 tests, including opted-in tiny
real-Gurobi tests and runner integration, passed before benchmark execution;
typechecking and lint also passed. No tests ran concurrently with this experiment.

The parent spec reports a published ABC baseline of 64 UNSAT and eight SAT rows.
That contextual count is not ground truth or an artifact-paired comparison here.
Published-source pairing, disagreements and comparative statistics belong to
the shared comparison slice. This archive preserves every query and unresolved
outcome for that work, without claiming matched hardware, ABC execution-bound
artifact hashes, or a solver speed advantage.

## Reproduce

Install the locked solver extra and use a suitable Gurobi license. Use a fresh
output path for new measurements; do not overwrite this archive or retry its
unresolved rows within it.

```sh
uv sync --locked --extra solver
uv run --locked python -m nvvcomp_gurobi.experiment acquire .benchmarks/mnist-sigmoid-v1 --category dist_shift_2023
uv run --locked python -m nvvcomp_gurobi.experiment audit .benchmarks/mnist-sigmoid-v1/instances.csv experiments/mnist-sigmoid-v1
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/mnist-sigmoid-v1/instances.csv experiments/mnist-sigmoid-v1
uv run --locked python -m nvvcomp_gurobi.experiment report experiments/mnist-sigmoid-v1
```

The whole-run query deadline includes startup, reads/decompression,
interpretation, construction, solving and validation. Gurobi receives only
remaining time; the supervisor rejects late results. Invocation wall time also
includes cleanup. Acquisition and eligibility audit are separate, not hidden
solver preparation. Execution used an Apple M4, 10 logical CPUs and 16 GiB RAM
on macOS, with one Gurobi thread. No memory cap was imposed. Pinned replay uses
12 intra/inter-op CPU threads separately. These accounting and resource choices
do not establish identical execution conditions to competition measurements.

## Record inventory

- `instances.csv`: original 72-row manifest, byte-for-byte.
- `experiment.json`: complete eligibility audit, original shapes and operations,
  actual-formulation descriptor, artifact hashes and acquisition URLs, package
  versions, hardware/resources, pinned tooling revisions, measured implementation
  commit, and source/lockfile hashes. Original compressed bytes are reproducibly
  downloaded into ignored `.benchmarks/`, not duplicated here.
- `records/0000.json` through `records/0071.json`: original-query identities,
  limits, conservative outcomes, raw solver status, invocation/stage timings,
  formulation sizes, effective solver defaults, environment, and witness/replay
  evidence where available.
- `summary.json`, `report.md`: solver-free reports regenerated from those records.
- `review.md`: independent Standards/Spec reviews with GPT-6 Astra medium,
  including baseline, findings and disposition.
