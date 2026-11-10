# Preliminary Gurobi vs α,β-CROWN comparison: SAT ReLU V1

Completion artifact for [issue #5](https://github.com/complooea/nvvcomp-gurobi/issues/5).
Analysis date: 2026-11-10. **Neither verifier was executed for this comparison.**
This authored synthesis uses the [actual completed Gurobi experiment](../sat-relu-v1/README.md),
[deterministic evidence](evidence.json), and [all per-instance comparisons](instances.md).

## Where is ABC better?

**Coverage, provisionally: ABC reports solving all 100 instances; Gurobi solves
83 and times out on 17.** ABC reports UNSAT on all 17 Gurobi timeouts, with measured
runs of 6.369–6.755 seconds. These are not independently certified UNSAT answers.

**On the 83 same-answer mutual solves, Gurobi's measured run time is lower every
time.** The median per-instance ABC/Gurobi run ratio is **7.03**, and the ratio of
run-time sums is **7.25**. These are observed results in different, incompletely
documented execution environments, not hardware-independent solver speedups.

The central qualification: all 100 pairs are **source-verified candidates**, but
**zero published measurements have execution-bound benchmark hashes**. The tables
and conclusions below are conditional on ABC having used the pinned source bytes.

## Population and outcomes

All **100 listed, eligible Gurobi instances** are included, not just mutual solves.
The measured Gurobi records are exactly those retained by #4, without reruns.

| Outcome / accounting | Gurobi | ABC |
| --- | ---: | ---: |
| Category measurements | 100 | 100 |
| SAT, accepted strict witness | 50 | 50 published strict checks |
| SAT, tolerance-only / invalid / unsupported / unchecked | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| Numerical / reported UNSAT | 33 | 50 |
| Timeout | 17 | 0 |
| Error / other unresolved | 0 / 0 | 0 / 0 |
| Missing / corrupt category records | 0 / 0 | 0 / 0 |
| Excluded category instances | 0 | 0 |

- **83** same-answer mutual solves: 50 SAT and 33 UNSAT claims.
- **17 ABC-only** solves, listed below; **0 Gurobi-only**, **0 neither solved**.
- **0 opposing SAT/UNSAT claims** among the candidate pairs. Agreement is not an
  independent correctness reference.
- Missing category IDs: **[]**. Unmatched category IDs: **[]**. Excluded IDs: **[]**.
  Artifact/version mismatches among the 100 candidates: **[]**.
- The ABC CSV additionally contains one smoke row, explicitly unmatched and not
  scored: `benchmarks/test/1.0/onnx/test_nano.onnx` paired with
  `benchmarks/test/1.0/vnnlib/test_nano.vnnlib` (CSV row 101). Its misleading CSV
  category is `sat_relu`; the artifact paths identify `test`, so it is not added
  to the category population. The raw row remains in `evidence.json:unmatched_abc`.

### All 17 instances solved only by ABC

Every Gurobi result here is unresolved `timeout`, raw solver status 9, with about
100 seconds measured whole-run time. There is **no successful-solve ratio** for
these rows: neither 100 seconds nor the deadline is a Gurobi solve time.
Inputs, widths and stored weight/bias element counts are from the audited ONNX
artifacts. `Wxx` marks the descriptor groups explained below.

| ID | Original network stem | Inputs | Hidden width | Elements | Group | ABC run s |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| 0003 | unsat_v90_c811_k3 | 90 | 991 | 92,165 | W01 | 6.702 |
| 0013 | unsat_v78_c478_k13 | 78 | 634 | 51,356 | — | 6.484 |
| 0017 | unsat_v91_c116_k17 | 91 | 298 | 28,014 | W06 | 6.385 |
| 0023 | unsat_v68_c337_k23 | 68 | 473 | 33,585 | — | 6.439 |
| 0025 | unsat_v73_c501_k25 | 73 | 647 | 49,174 | W07 | 6.517 |
| 0027 | unsat_v91_c889_k27 | 91 | 1,071 | 100,676 | W06 | 6.755 |
| 0031 | unsat_v65_c209_k31 | 65 | 339 | 23,054 | — | 6.378 |
| 0037 | unsat_v87_c231_k37 | 87 | 405 | 36,452 | — | 6.411 |
| 0047 | unsat_v88_c453_k47 | 88 | 629 | 57,241 | — | 6.483 |
| 0049 | unsat_v94_c784_k49 | 94 | 972 | 94,286 | — | 6.691 |
| 0053 | unsat_v95_c183_k53 | 95 | 373 | 36,556 | — | 6.395 |
| 0063 | unsat_v51_c288_k63 | 51 | 390 | 21,062 | W12 | 6.378 |
| 0069 | unsat_v67_c223_k69 | 67 | 357 | 24,992 | W05 | 6.375 |
| 0071 | unsat_v47_c384_k71 | 47 | 478 | 23,902 | W14 | 6.459 |
| 0079 | unsat_v75_c586_k79 | 75 | 736 | 57,410 | — | 6.531 |
| 0089 | unsat_v59_c154_k89 | 59 | 272 | 16,866 | — | 6.369 |
| 0095 | unsat_v83_c233_k95 | 83 | 399 | 34,316 | W16 | 6.407 |

Names identify artifacts only; their `sat`/`unsat` prefixes never establish truth.
Each corresponding property path and both SHA256 identities are retained in the
original audit and published source inventory.

## What does network scale suggest?

All 100 networks have **Gemm → ReLU → Gemm**, one hidden layer and two outputs.
Inputs vary **5–95**, hidden widths **29–1,071**, and stored parameter elements
**234–100,676**. Thus the category is shallow and dimension-varying, **not a
depth-scaling experiment**, and the whole category does not differ only in hidden
width: input dimension also varies.

The following exploratory bins are computed from all 100 audit descriptors, with
integer width intervals `[0,199]`, `[200,399]`, `[400,599]`, `[600,799]`, `[800,∞)`.
SAT/UNSAT columns refer to accepted witnesses / ABC UNSAT claims, not filenames.

| Hidden width | All instances | SAT / ABC UNSAT | Gurobi timeouts | Timeout fraction among ABC UNSAT |
| --- | ---: | --- | ---: | ---: |
| <200 | 24 | 12 / 12 | 0 | 0/12 |
| 200–399 | 52 | 26 / 26 | 7 | 7/26 |
| 400–599 | 10 | 5 / 5 | 3 | 3/5 |
| 600–799 | 8 | 4 / 4 | 4 | 4/4 |
| ≥800 | 6 | 3 / 3 | 3 | 3/3 |

**Preliminary feeling:** increasing width is associated with a greater Gurobi
timeout fraction on the UNSAT-claim instances in this sample. All 50 strict SAT
witnesses are found by both tools, including wide networks. ABC's reported run
times stay in a narrow range across this category; fixed startup may obscure small
differences, so this is not evidence of constant computational complexity.

### Descriptor-matched width groups

The evidence identifies **16 groups** with fixed input/output dimensions, operation
sequence and hidden-layer count, but multiple observed hidden widths. Every row in
[instances.md](instances.md) carries its group label. These are **structural
descriptor matches, not controlled width-only changes**: weights and properties
differ, and descriptors are not a general graph-equivalence test.

Selected within-input examples, using only UNSAT claims for the comparison:

| Group | Fixed inputs | Narrower instance: width, Gurobi result | Wider instance: width, Gurobi result |
| --- | ---: | --- | --- |
| W05 | 67 | 0015: 273, UNSAT in 0.331s | 0069: 357, timeout |
| W07 | 73 | 0085: 222, UNSAT in 1.643s | 0025: 647, timeout |
| W12 | 51 | 0087: 384, UNSAT in 1.352s | 0063: 390, timeout |
| W16 | 83 | 0097: 346, UNSAT in 1.955s | 0095: 399, timeout |

Conversely, W06 times out at both width 298 (0017) and width 1,071 (0027).
The six-unit width difference in W12 accompanies a very large outcome difference;
that is a warning against interpreting width as the sole difficulty variable.
Instance structure, property, input dimension, parameter values and measurement
order are not controlled here. The bins are descriptive, not a fitted scaling law.

## Timing populations and conventions

All times below are **raw measured times, no startup subtraction**. Gurobi's
whole-run time includes startup, reads/decompression, interpretation, encoding,
optimization and independent replay. ABC's CSV separately records preparation and
runner-measured run time; its internal stage breakdown and any preparation reuse
are unavailable. Preparation-plus-run is therefore shown separately, not silently
charged to or removed from either run budget. Acquisition and eligibility audit
are outside Gurobi's per-instance measurements.

| Population | Gurobi | ABC |
| --- | ---: | ---: |
| All 100 measured runs, sum | 1,769.410s | 611.661s |
| All 100 measured runs, median | 0.874s | 6.032s |
| 83 same-answer mutual solves, sum | 69.200s | 501.499s |
| 83 same-answer mutual solves, median | 0.824s | 5.841s |
| All 100 preparation measurements, sum | 0s (no analysis) | 1,926.310s |
| All 100 preparation measurements, median | 0s | 19.224s |

The paired population is explicitly listed in `runtime.paired_same_answer.ids`.
Its median ABC/Gurobi per-instance run ratio is **7.032**, ratio of sums **7.247**,
and median per-instance preparation-plus-run ratio **30.383** (all 83 have both
preparation measurements). Ratio of medians is not substituted for these metrics.
Within the paired population, median run ratios are 7.125 over 50 SATs and 5.504
over 33 UNSAT claims. These are descriptive, cross-environment observations.

Across all 100 records, ABC uses less **run** time in aggregate because it avoids
the 17 long Gurobi timeouts; after adding ABC's preparation, total recorded
preparation-plus-run cost is 2,537.970s versus Gurobi's 1,769.410s. Neither all-run
cost total is a successful-solve time or an equal-coverage solver speed ratio.

**Pinned timing discrepancy:** the published results README says scoring uses
`run_time > timeout` without subtracting overhead. At the same revision,
`ToolResult.enforce_scoring_timeouts` actually subtracts the fastest observed
per-tool overhead, as does `single_result` for plots. The retained source snapshots
make this inspectable. Our evidence applies the conservative **raw 100-second
deadline**, never adds grace-period credit, and does not mimic adjusted competition
plots. This discrepancy changes none of the 100 ABC classifications: every raw
ABC run is under 7 seconds. Gurobi timeouts remain unresolved, regardless of any
overhead arithmetic.

## Sources, artifact identity and correctness

Published source: [`VNN-COMP/vnncomp2026_results` at
`eea564f5d0a8751d8321a409214db14d03f452b8`](https://github.com/VNN-COMP/vnncomp2026_results/tree/eea564f5d0a8751d8321a409214db14d03f452b8/alpha_beta_crown/2026_sat_relu).
The source commit describes imported competition results, dated 2026-08-03; that
is the publication commit date, **not** a known measurement date or ABC revision.

- The CSV references `sat_relu/1.0` for both network and property in all 100 rows.
  No VNN-LIB 2.0 result is substituted or matched by logical index.
- [Published source inventory](published/source.json) pins original CSV/check/
  witness bytes and URLs. Its network/property inventory independently verifies
  the original compressed benchmark bytes against public Git blob IDs at benchmark
  revision `303f2327a8e8411efc4457da03d2016ce42733cf`, then records decompressed
  SHA256s. All 200 decompressed artifact hashes equal the #4 audit identities.
  The original manifest is also Git-blob verified and SHA256-matched.
- **Limit:** the CSV does not record its execution benchmark commit/hashes, and the
  published witness caches bind witness hashes and CSV row identities, **not**
  network/property hashes. Hence source verification cannot prove those artifacts
  were used in the ABC run. There are 100 candidate matches and **0 execution-bound
  matches**; no unconditional exact-execution speed claim is available.
- All 50 ABC SAT caches correspond to their normalized CSV rows and retained
  witness SHA256s, use `vnncomp2026-cex-1` on the CPU provider, and report strict
  acceptance. The published dependencies record Python 3.12.13, ONNX 1.21.0 and
  ONNX Runtime 1.26.0. These are **validator** versions, not ABC's execution
  environment. We did not rerun the published checks.
- The #4 Gurobi witnesses were independently replayed with the pinned competition
  validator; numerical UNSAT remains uncertified. A strict witness can refute a
  matching UNSAT claim. A tolerance-only witness earns SAT credit under the pinned
  scorer but cannot refute UNSAT. Invalid, unsupported or missing checks are not
  promoted to strict SAT. No filename or two-tool consensus supplies ground truth.

### Competition-aligned subset scoring

At the pinned `get_score`, accepted SAT earns 10 points, time bonus disabled,
incorrect-result penalty −150. On the **50 accepted-SAT candidate instances**, the
subset contribution is **500 Gurobi points and provisionally 500 ABC points**, the
latter conditional on published artifact correspondence/check correctness. This
is not a full-category or normalized competition score.

The 50 UNSAT-claim instances remain explicitly unassessed for full scoring.
Execution-bound identity and complete participating-tool strict-witness conflict
evidence are missing; normalization also needs the participating-tool context.
We do not award points merely because two tools agree on UNSAT, assume that ABC's
17 additional UNSAT claims are ground truth, or turn our own verdicts into a
correctness reference. The scorer's timeout/overhead discrepancy is another reason
not to label this an official score reproduction.

## Hardware and scope limits

Gurobi ran on Apple M4, 10 CPUs, 16 GiB RAM, macOS 26.6.2 arm64, Python 3.12.16,
Gurobi 13.0.1 and gurobi-machinelearning 1.7.0, sequential instances, Threads=1.
The independent replay uses 12 intra/inter-op CPU threads. There was no affinity,
memory cap, exclusive-node reservation or performance/tolerance tuning. Full
source/package/settings provenance remains in the original records.

The inspected ABC category folder/CSV/checks disclose **no execution CPU/GPU model,
CPU threads, RAM/VRAM allocation, container/image, tool commit/configuration,
exclusive-node status or execution package environment**. Do not infer a particular
GPU or cloud instance from typical ABC deployments or from CPU witness validation.
Resource equivalence is not established. These ratios are observed cross-hardware/
environment measurements with the ABC side unspecified, not intrinsic superiority
of Gurobi, ABC, GPUs or MILP. Conclusions apply only to these shallow networks and
the preceding ticket's sequential affine/ReLU feasibility encoding.

## Reproduction and retained artifacts

- [evidence.json](evidence.json): complete populations, outcomes, runtime statistics,
  scoring limits, architecture groups and input/source fingerprints.
- [instances.md](instances.md): all 100 pairs with dimensions, group labels, raw
  times, validation and comparison classifications; unmatched smoke row included.
- [published/source.json](published/source.json) and [raw/](published/raw/): pinned
  source inventory, original ABC CSV, 50 witnesses, 50 check caches, and source
  snapshots. No license credentials or solver binaries are retained.
- [Original experiment report and records](../sat-relu-v1/README.md).

Regenerate calculations/tables, without network or either solver:

```sh
uv run --locked python -m nvvcomp_gurobi.comparison experiments/sat-relu-v1 experiments/sat-relu-v1-comparison/published experiments/sat-relu-v1-comparison --category sat_relu --version 1.0
```

This README is agent-authored synthesis, not generated prose. Revisit it whenever
the input fingerprints or comparison semantics change; regenerating evidence does
not overwrite the narrative. Width bins and subgroup observations can be recomputed
by filtering `evidence.json:instances` by `architecture.hidden_widths[0]`,
`gurobi.outcome`, `abc.outcome`, and `comparison`. See
[durable comparison instructions](../../docs/comparisons.md) for acquisition,
interface contracts and test commands.

## Completion checks and review

- `uv run --locked pytest tests/test_comparison.py`: **42 passed**.
- `uv run --locked pytest tests`: **90 passed, 25 skipped**. Solver-dependent
  tests were deliberately not enabled: this comparison executed neither verifier.
- `uv run --locked prek run --all-files`: all checks passed, including lint,
  formatting and typechecking.
- Solver-free evidence regeneration was independently reproduced byte-for-byte.
- Review baseline: task-start commit
  `f7bf4d00f1b73967192f5705d1c70b1c68bcb4db`. Implementation commits:
  `1512141` and `b2fc6f4`.

### Standards review

GPT-6 Astra medium: **no remaining actionable findings**. Initial findings about
non-object saved records, context selection, measurement naming and repeated
population selection were addressed with regression tests and localized cleanup.

### Spec review

GPT-6 Astra medium: **no remaining actionable findings**. Mixed-version matching,
asymmetric missing-record statistics and late-witness conflict handling were fixed
test-first. The reviewer verified the actual report's populations, timing ratios,
width bins and 16 descriptor groups against the saved evidence.
