# Proof-comparison analysis review (#12)

Review baseline: task-start commit
`d504ad1d1c4c8f9c47f51020d9d9c7f172e562b5`.
Reviewed report commit: `4d37e7e`.
Diff: `git diff d504ad1d1c4c8f9c47f51020d9d9c7f172e562b5...4d37e7e`.
Review model: **GPT-6 Astra, medium**, separately for Standards and Spec.
Spec: GitHub issue #12, with the scope and conventions of #7 and relation to #2.
Report: [proof-comparison-analysis.md](../proof-comparison-analysis.md).

Scope: the review below covers the original three-study report at `4d37e7e`,
before consolidation with the MVP narrative. It is not a review of later report
revisions. Historical MVP report checks/reviews are retained separately in
[MVP comparison review](sat-relu-comparison-review.md).

## Validation

- `uv run --locked pytest tests/test_comparison.py`: **48 passed**.
- `uv run --locked ty check`: passed.
- `uv run --locked prek run --all-files`: passed (lint, formatting, typing and
  repository hygiene).
- `uv run --locked --extra solver pytest tests --solver --cov --cov-report=term-missing`:
  **149 passed**, including tiny real-Gurobi tests; no full benchmark reruns.
- All three comparison CLIs regenerated `evidence.json`, `instances.md` and
  `statistics.md` into fresh temporary directories, byte-identical to the nine
  archived files. Calculation-source hashes matched the retained provenance.
- No ABC execution, new benchmark measurements, property changes or calculation
  code changes. TDD introduced no new seam for this report-only change.

## Standards

No documented-standard violations or actionable heuristic smells found. The
review checked all twelve baseline smells, separation of authored interpretation
from calculations, and explicit fingerprint/definition maintenance triggers.

## Spec

No missing/partial requirements, scope creep or incorrect implementation found.
The reviewer cross-checked complete 120/72/14 populations, common-UNSAT timings,
depth/original-model grouping, sigmoid-specific claims, every ACOPF property,
MVP proof-only figures, fingerprints, revisions and resource qualifications against
the retained evidence and original audits/records.

Summary: **Standards: 0 findings. Spec: 0 findings.** No outstanding findings;
neither review edited files or executed a verifier or benchmark. This final
review-record update does not change the reviewed analytical report.
