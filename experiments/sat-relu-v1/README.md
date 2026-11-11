# Completed SAT ReLU V1 local experiment

Completion evidence for [issue #4](https://github.com/complooea/nvvcomp-gurobi/issues/4).
All 100 prescribed instances were audited before solving and executed sequentially
on 2026-11-10, using their original 100-second whole-run deadlines.

| Result | Count |
| --- | ---: |
| Listed / eligible / recorded | 100 / 100 / 100 |
| Excluded / missing / corrupt | 0 / 0 / 0 |
| SAT, independently replayed strictly valid | 50 |
| Numerical UNSAT, raw Gurobi status 3 | 33 |
| Unresolved timeout, retained raw Gurobi status 9 | 17 |
| Conversion / solver / validation errors | 0 |

The 50 accepted witnesses are strict; none are tolerance-only or invalid.
Numerical UNSAT is not independently certified correctness or an exact-real proof.
No result is inferred from a filename label. All raw statuses survived deadline
enforcement: 50 status-2 results, 33 status-3 results, and 17 status-9 results.
Timeout records retain diagnostics and completed stages, not UNSAT verdicts.

## Timings and resources

- Sum of 100 whole-run times: **1,769.410049 seconds (29m29.410s)**.
- Sum of invocation wall times: **1,769.424941 seconds**; includes supervision and
  cleanup beyond the verifier's whole-run accounting.
- Solved-instance whole-run times: median **0.823949s**, maximum **1.955110s**.
  All-instance median **0.874446s**. No startup subtraction was applied.
- Longest recorded whole-run time: **100.015289s**, an unresolved timeout;
  termination/cleanup overhead is measured, never extra solve credit.
- Original-artifact acquisition: **362.254742s**; complete eligibility audit:
  **0.068048s**. Preparation analysis: **0s**, with no preparation subprocess or
  cached encoding. Each verification reread and interpreted its original files.
- First execution began at **15:16:59.677942 UTC**. The remaining 99 began at
  **15:17:20.441703 UTC**, after first-result inspection; their first-start to
  last-completion wall span was **1,769.462647s**, including loop/persistence
  overhead. The inspection pause is not attributed to solver runtime.
- Solver-free report command measured externally with `/usr/bin/time -p`:
  **0.39s real**, 0.31s user, 0.07s system (includes uv/Python startup and output).
- Apple M4, 10 logical/physical CPUs, **16 GiB RAM**, macOS 26.6.2 arm64;
  Python 3.12.16. Gurobi Threads=1; pinned CPU replay has 12 intra/inter-op threads.
  No affinity or memory cap, numerical/performance tuning, or exclusive-node
  reservation. See [measurement context](checkpoint.md#measurement-context).

Budgets allowed 10,000 seconds (2h46m40s) plus separately accounted overhead;
early solves reduced actual execution time. These shallow-network results show
width variation, not architectural/depth scalability or intrinsic superiority
over another verifier. No ABC runtime comparison is made here.

## Retained artifacts

- [Generated report](report.md) and [machine-readable summary](summary.json).
- [Pre-solve audit, acquisition inventory, source/hardware provenance](experiment.json).
- [Original manifest](instances.csv) and **all 100 raw JSON records** in [records/](records/),
  including witnesses, replay classifications, original/compressed and
  decompressed SHA256 identities, raw statuses, diagnostics, stage timings,
  execution limits, numerical settings, and package/validator provenance.
- [First-execution inspection](checkpoint.md), completed before the remaining run.

Every record's original artifact hashes match its audit identities. All records
have identical package versions and numerical settings (only remaining TimeLimit
varies). Original compressed artifacts remain locally in `.benchmarks/sat-relu-v1`;
they are reproducibly downloadable from the immutable URLs and SHA256 inventory
embedded in `experiment.json`, rather than duplicated in Git.

Execution code: commit **`a8d7247`**, with full source and lockfile hashes captured
before solving. A report-only fix at **`44155dc`** handles unavailable preparation
timings; `summary.json` identifies the exact reporter source hash. Verification
and the running experiment were not changed during execution.

The pinned scorer supports **500 points for the 50-instance accepted-SAT-only
subset** (10 per accepted witness, time bonus disabled). This is not the full
eligible-subset or category-normalized score. Those remain unavailable without
artifact-matched cross-tool conflict evidence and participating-tool context.
Strict witnesses may refute UNSAT; tolerance-only witnesses earn SAT credit but
cannot refute UNSAT. Our own numerical UNSAT verdicts are not used as ground truth.

## Commands and checks

From the repository checkout, with Python 3.12, uv 0.13.6, and a suitable local
Gurobi license (credentials are never included in these artifacts):

```sh
uv sync --locked --extra solver
uv run --locked python -m nvvcomp_gurobi.experiment acquire .benchmarks/sat-relu-v1
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment audit .benchmarks/sat-relu-v1/instances.csv experiments/sat-relu-v1
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/sat-relu-v1/instances.csv experiments/sat-relu-v1 --stop-after 1
# Inspect records/0000.json, then resume without changing source/settings:
uv run --locked --extra solver python -m nvvcomp_gurobi.experiment run .benchmarks/sat-relu-v1/instances.csv experiments/sat-relu-v1
```

Use a **new output directory** when reproducing measurements. The commands above
describe the retained execution; its immutable source fingerprint intentionally
prevents resuming it with changed source. To regenerate the existing report,
without downloading artifacts or rerunning Gurobi:

```sh
uv run --locked python -m nvvcomp_gurobi.experiment report experiments/sat-relu-v1
```

Final checks after full benchmark completion:

```sh
uv run --locked --extra solver pytest tests --solver --cov --cov-report=term-missing
# 73 passed; full benchmark execution is not part of this suite.
uv run --locked prek run --all-files
# All checks passed, including lint, formatting, and typechecking.
```

Final review used **GPT-6 Astra medium**, independently on Standards and Spec
axes, against task-start commit `ce2dcf96e6b795b902a326f505956616cb927987`.
Both axes reported no remaining actionable findings after inspecting the code and
completed experiment evidence. The earlier unavailable-preparation-time finding
was fixed test-first in `44155dc`.

See [durable experiment guidance](../../docs/experiments.md) and
[verification assumptions](../../docs/verification.md) for detailed contracts.
