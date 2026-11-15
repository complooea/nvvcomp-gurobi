# Larger-ACOPF comparison validation and review (#22)

## Scope

Baseline: `5e30a3ec0eaa6f91eb1d7278935ba0ddcddeadd6`, the initial branch state
and `origin/main` at implementation start. This review concerns #22 under parent
#20: comparison implementation, retained published sources, IEEE-118/300
calculations and updated documentation. It does not approve new measurements;
neither benchmark verifier was rerun and no published witness was freshly replayed.
Tiny solver-enabled tests are separate from benchmark measurements.

Earlier [experiment](larger-acopf-experiment-review.md),
[statistics](proof-comparison-statistics-review.md) and
[analysis](proof-comparison-analysis-review.md) reviews remain scoped to their
recorded revisions, not these edits.

## Saved-evidence validation

- Acquisition independently verified the full pinned benchmark manifest, each
  exact model selection and original compressed Git blobs; decompressed hashes
  match all five IEEE-118 and four IEEE-300 audited pairs.
- Pinned results CSV, scoring references and SAT witness/check caches were
  acquired and hash-inventoried. Selected rows are IEEE-118 15–19 and IEEE-300
  66–69. Unselected counts are 65 and 66 respectively, never denominators.
- Selected IEEE-300 property 2 has row/witness/checker/provider correspondence
  and cached strict acceptance. This is not fresh replay or execution binding.
- Four numerical UNSAT, four timeouts and one invalid replay remain the saved
  local inventory. Exact identities, model/class populations, raw cross-tabs,
  unresolved reasons and paired-proof eligibility were reconciled with records.
- With Gurobi **uninstalled** (`uv sync --locked`, `find_spec('gurobipy') is None`),
  comparison outputs were regenerated into a fresh temporary directory and
  compared byte-for-byte with both new archives. Original experiment reports
  were also regenerated from copies of only `experiment.json` and `records/`,
  byte-identical to saved `summary.json` / `report.md`. No original model reads,
  solver, network or new measurement was needed.
- IEEE-14 and all historical record/generated-evidence bytes are preserved.
  Only maintained narrative/navigation changes outside the new evidence archives.

New calculation source SHA256:
`0d4cef2ca52ab6f6b5fc4441bf5b8dce021f3b097a2538ccf0a6d2abf8b868f3`.
Evidence SHA256s:

| Population | SHA256 |
| --- | --- |
| IEEE-118 | `6ab9518af3ae72c44b9a59aab44d70fe01766d473df8b013b0673dc3bd89373e` |
| IEEE-300 | `a08ef70b90f9e406f98995cedb95cb9687b0ae6a96ec8fd291be1bb7b0371051` |

## Checks

- TDD at the pre-agreed `compare` and comparison CLI seams: model/class grouping,
  same property numbers on distinct networks, variant exclusion, unresolved IDs
  and reasons, empty/zero/missing/late proof timing eligibility, retained cache
  correspondence and rejection of unretained check/witness files.
- Focused comparison file: **60 passed**, including with no solver installed.
- Full solver-enabled suite: **167 passed**, with coverage, including tiny
  real-Gurobi/runner checks; no full benchmark-as-test.
- Repository `prek run --all-files`: all hooks passed, including Ruff and ty.
- Local Markdown paths and anchors checked in all affected maintained reports;
  selected counts, outcome counts and stored/decompressed artifact identities
  reconciled with saved evidence. Historical measurement/generated paths have
  no diff against the baseline.

## Independent review

Reviewed implementation commit **`29040f7`** against baseline
`5e30a3ec0eaa6f91eb1d7278935ba0ddcddeadd6`, using two fresh-context
**GPT-6 Astra medium** reviewers. This section records that revision's review;
it is not blanket approval of later edits.

### Standards

No actionable findings. No documented-standard violations or baseline smells
warranting changes were identified. The reviewer checked acquisition boundaries,
saved-evidence calculations, strengthened cache acceptance, behavior tests at
the documented seams, and historical review scope. Tooling-enforced issues were
excluded; supplied passing checks were not independently rerun.

### Spec

No actionable findings against #22 and parent #20: no missing/partial
requirements, scope creep or wrong-looking implementation identified. The
reviewer independently checked retained-file hashes, selected published-row and
source-hash correspondence, selected SAT cache row/witness correspondence, record
runtimes, common-proof ratios/medians and all-run sums against the narrative.
All nine queries, separate model/classes, unresolved outcomes, unavailable empty
timings, conditional provenance and causal limits were retained. Reported test
and regeneration results were supplied context, not independently rerun.

**Summary:** Standards 0 findings; Spec 0 findings. Both reviews were read-only,
without benchmark execution or fresh published witness replay.

## Integrated narrative revision

At the user's request, documentation commit **`48b9d9d`** integrates all three
grid sizes into one ACOPF narrative rather than presenting IEEE-118/300 as an
add-on to four earlier studies. The findings, index, reproduction guidance and
report anchors are updated together. Model/class denominators, measurements,
calculation bytes and claim limits are unchanged. PR #26 links the report using
an absolute URL pinned to this commit, verified HTTP 200.

Two fresh-context **GPT-6 Astra medium** reviewers examined
`1d15bfe...48b9d9d` read-only:

- **Standards:** 0 actionable breaches; no judgement-call smells warrant changes.
  Durable navigation and historical/current calculation distinctions remain.
- **Spec:** 0 findings. Integration is substantive, with one ACOPF section,
  unified findings and class-specific progression while retaining separate
  populations, unresolved outcomes, timing/provenance and causal limitations.

Both reviewers accepted the supplied link/anchor and hook checks; neither ran
tests or benchmarks. PR-body URL verification was performed separately, not
inferred from the repository diff. This is a documentation-only revision:
all affected local links/anchors and repository hooks passed; the earlier
167-test result remains scoped to the unchanged implementation.
