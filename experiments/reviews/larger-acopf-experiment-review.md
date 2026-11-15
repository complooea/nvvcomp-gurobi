# Original IEEE-118/300 experiment review

Issue [#21](https://github.com/complooea/nvvcomp-gurobi/issues/21), under
[#20](https://github.com/complooea/nvvcomp-gurobi/issues/20).
Date: 2026-11-15.

## Scope and revisions

User-approved baseline: `c9aba39c823c4c1e80358e4052bd2493b1784ab6`.
Reviewed archive HEAD: `35c6611`.
Diff command: `git diff c9aba39c823c4c1e80358e4052bd2493b1784ab6...35c6611`.

- `9b954b3`: exact original larger-model acquisition, property classifications,
  public-interface tests and population-neutral reporter wording.
- `35c6611`: both complete outcome inventories, semantic audit, raw records,
  generated solver-free reports and reproduction documentation.

Both review axes ran independently in fresh subagent contexts using the
user-requested **GPT-6 Astra medium** (`openai/gpt-6-astra#medium`).
Reviewers were read-only and did not run benchmarks or tests.
This review artifact itself was added after the reviewed archive revision;
neither measurement source nor raw outcomes were changed after review.

## Standards

**Hard standard violations: None found.**

Reviewed the committed changes from `c9aba39` through `35c6611` against
`AGENTS.md`, domain guidance and glossary, `CODING_STANDARDS.md`,
`CONTRIBUTING.md`, and the specified tooling configurations. No additional
coding-standards documents or applicable ADRs were found.

**Baseline smells (judgment calls): None actionable.**

The acquisition selection, audit classifications, and added tests fit the
existing experiment interface. No abstraction or refactoring is warranted
solely by these changes.

Tooling-enforced findings and the planned review-artifact link were excluded.
No files were edited or benchmark experiments run.

## Spec

**No actionable spec findings** against issue #21 in `c9aba39...35c6611`.

- **Missing/partial requirements:** No missing implementation or archive
  artifacts identified. The retained IEEE-118 property-2 interruption limits
  measurement completeness: nine outcomes are archived, but only eight
  invocations ran uninterrupted. This is clearly documented, with unavailable
  timings/settings/sizes preserved. Retention follows the requirement:
  “Follow existing interruption/resume behavior without hidden retries or
  replacing completed failures.” It should not be hidden or retried.
- **Unrequested scope:** None identified. Changes reuse existing acquisition,
  audit, run and report interfaces. Broader comparison and root README work
  remain appropriately deferred.
- **Implemented but wrong:** None identified. Selected identities/order,
  record-to-audit identities, outcomes, classifications, reported timing totals
  and measured formulation sizes agree with persisted records. The invalid
  IEEE-118 candidate remains unresolved following original-ONNX replay; timeout
  and interrupted timings are not fabricated.

The archive distinguishes graph descriptors from measured encoding sizes,
preserves provenance and effective settings, and documents solver versus
replay threading. Public-interface tests cover selection, deadline/thread
propagation, retention and solver-free reporting.

Review was read-only; no benchmarks or tests were rerun. Reported check results
and fresh byte-identical regeneration were supplied by the parent session.
Published ABC verdicts were not used as correctness oracles.

## Validation and disposition

- Red/green public-interface tests demonstrated the previously absent larger
  acquisition selection and property classifications before implementation.
  Existing fixture factories and injected verifier outcomes were reused.
- Pre-measurement: 107 tests passed across `test_experiment.py`, `test_solver.py`,
  `test_verification.py`, `test_competition.py` and `test_runner_integration.py`
  with `--solver`. Lint, formatting, typechecking and all repository hooks passed.
- Final full suite:
  `uv run --locked --extra solver pytest tests --solver --cov --cov-report=term-missing`
  — **155 passed**, 88% reported coverage; no coverage threshold used as a
  correctness gate.
- `uv run --locked prek run --all-files` — all checks passed.
- Fresh-directory regeneration copied only each `experiment.json` and `records/`,
  then called public `report_experiment`. Both `summary.json` and `report.md`
  were byte-identical to their archived outputs.
- All nine selected identities, source order, source-manifest hashes, compressed
  and decompressed artifact hashes and report record inventories were verified.
- Historical IEEE-14 and other measurement paths were unchanged. Local Markdown
  targets were checked; the review-artifact target is supplied by this file.
- No tests ran concurrently with measured invocations.

No review-driven code changes or outcome replacements were required. The
external one-second shell-timeout incident is explicitly retained in
`acopf-118-v1/orchestration.json`, not counted as a benchmark timeout or proof.
It remains a limitation for the dependent comparison.

**Summary: Standards 0 findings; Spec 0 actionable findings. The retained
interruption limits measurement completeness, not outcome-inventory completeness.**
