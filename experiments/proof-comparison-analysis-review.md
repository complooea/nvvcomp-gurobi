# Proof-comparison analysis review (#12)

Review baseline: task-start commit
`d504ad1d1c4c8f9c47f51020d9d9c7f172e562b5`.
Review model requested: **GPT-6 Astra, medium**, separately for Standards and Spec.
Spec: GitHub issue #12, with the scope and conventions of #7 and relation to #2.
Report: [proof-comparison-analysis.md](proof-comparison-analysis.md).

## Validation

- `uv run --locked pytest tests/test_comparison.py`: **48 passed**.
- `uv run --locked ty check`: passed.
- `uv run --locked --extra solver pytest tests --solver --cov --cov-report=term-missing`:
  **149 passed**, including tiny real-Gurobi tests; no full benchmark reruns.
- All three comparison CLIs regenerated `evidence.json`, `instances.md` and
  `statistics.md` into fresh temporary directories, byte-identical to the nine
  archived files. Calculation-source hashes matched the retained provenance.
- No ABC execution, new benchmark measurements, property changes or calculation
  code changes. TDD introduced no new seam for this report-only change.

## Review status

Awaiting independent Standards and Spec review. Update this section with findings
and disposition before completing #12.
