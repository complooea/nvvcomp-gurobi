# Historical MVP comparison review (#5)

Scope: original shallow-ReLU comparison narrative, formerly
`experiments/sat-relu-v1-comparison/README.md`, authored 2026-11-10. Its findings
are now incorporated into the [comprehensive report](../proof-comparison-analysis.md).
These historical checks and reviews do not certify later report revisions.

- `uv run --locked pytest tests/test_comparison.py`: **42 passed**.
- `uv run --locked pytest tests`: **90 passed, 25 skipped**. Solver-dependent
  tests were deliberately not enabled for this saved-evidence comparison.
- `uv run --locked prek run --all-files`: all checks passed.
- Solver-free evidence regeneration was independently reproduced byte-for-byte.
- Review baseline: `f7bf4d00f1b73967192f5705d1c70b1c68bcb4db`.
  Implementation commits: `1512141` and `b2fc6f4`.

## Standards

GPT-6 Astra medium: no remaining actionable findings. Initial findings about
non-object saved records, context selection, measurement naming and repeated
population selection were addressed with regression tests and localized cleanup.

## Spec

GPT-6 Astra medium: no remaining actionable findings. Mixed-version matching,
asymmetric missing-record statistics and late-witness conflict handling were fixed
test-first. The reviewer verified populations, timing ratios, width bins and the
16 descriptor groups against the saved evidence.
