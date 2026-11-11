# Development

For code review, apply [CODING_STANDARDS.md](CODING_STANDARDS.md) and the testing
and dependency conventions below. Tool settings live in `pyproject.toml`,
`.pre-commit-config.yaml`, and `.github/workflows/ci.yml`.

## Setup and checks

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run:

```sh
uv sync --locked --extra solver
uv run --locked prek install
uv run --locked prek run --all-files
```

Review and re-stage hook fixes. The [official ty hook](https://github.com/astral-sh/ty-pre-commit)
may synchronize `.venv` even with `--locked`.

## Dependency updates

Commit `uv.lock` with dependency changes. Update dependencies and pinned hooks
deliberately, review the diff, and rerun checks. Keep Ruff and ty hook versions
aligned with their locked development versions.

## Testing

Add meaningful tests under `tests/` alongside functionality. Run:

```sh
uv sync --locked
uv run --locked pytest tests                          # no solver installation needed
uv sync --locked --extra solver
uv run --locked --extra solver pytest tests --solver --cov --cov-report=term-missing
```

Solver tests run only with `--solver`. Requesting them without the pinned solver
extra is an error, not a skip. They isolate the home directory and unset
`GRB_LICENSE_FILE` so personal license credentials are not needed. CI runs both
the full tiny real-Gurobi suite and an independent environment without the solver
extra. Typechecking (including the ty hook) installs the solver extra so its SDK
types are available. Coverage includes verification subprocesses and excludes
vendored upstream source. No coverage percentage is used as a correctness gate.

- Validate solver behavior with tiny real-Gurobi tests and analytically known
  outcomes. Keep encoded models within the [bundled license limits](https://support.gurobi.com/hc/en-us/articles/360051597492)
  so CI needs no local license credentials.
- Make solver tests explicitly selectable and fail clearly when a requested run
  lacks prerequisites. Keep non-solver tests runnable without Gurobi.
- Run full benchmark experiments separately and explicitly, using the appropriate
  local license. Keep tests out of commit hooks to avoid unpredictable latency.

## Solo workflow

1. Start a short-lived branch from current `main` for one coherent change.
2. Commit complete, reviewable increments with descriptive messages.
3. Push at useful checkpoints and session end. Open a draft PR for early CI.
4. Review the final diff, consult `CODING_STANDARDS.md`, and use the code-review
   skill for substantive changes. Check CI before merging.
5. Squash-merge the PR, delete the branch, and update local `main`.

Open a draft PR to get CI feedback on a feature branch. A solo repository should
not require another person's approval.
Use issues for substantial work or bugs needing context; small cleanup need not
have a ticket. Follow `docs/agents/issue-tracker.md` when working with issues.

For parallel work, use a separate branch/worktree and run setup in that checkout.
Inspect remote checks with `gh pr checks`; diagnose failures with
`gh run view RUN_ID --log-failed` (authenticated GitHub CLI required).
