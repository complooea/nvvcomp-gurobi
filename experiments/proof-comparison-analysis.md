# Gurobi versus published ABC: four-study comparison

Authored analysis for [#12](https://github.com/complooea/nvvcomp-gurobi/issues/12),
part of [#7](https://github.com/complooea/nvvcomp-gurobi/issues/7), incorporating
the MVP originating in [#2](https://github.com/complooea/nvvcomp-gurobi/issues/2)
and its original [#5 comparison](https://github.com/complooea/nvvcomp-gurobi/issues/5).
Updated: 2026-11-13 (MVP narrative consolidated; original analyses 2026-11-10/12).
This report interprets completed experiments and #11's
saved calculations; **neither verifier was rerun for this analysis**. No properties,
models, deadlines or numerical settings were changed. Calculation code contains
no new interpretation. Revisit this narrative if its input fingerprints or the
comparison definitions change.

## Findings

- **Shallow-ReLU MVP:** Gurobi completed 33 numerical UNSAT versus ABC's 50 across
  100 queries. Both accepted 50 strict SAT witnesses; Gurobi timed out on 17
  published-UNSAT queries. Gurobi's observed time was lower on every common solve,
  including the 33 common proofs. Greater coverage and lower paired runtime are
  different claims, not a single winner.
- **Deeper ReLU:** Gurobi completed 1 numerical UNSAT versus ABC's 96 published
  UNSAT claims across 120 ReLUSplitter queries. On the one common proof, ABC's
  observed run time was lower. Depth cohorts show limited Gurobi completion, but
  do not isolate a depth effect.
- **Internal sigmoid:** Gurobi completed 42 numerical UNSAT versus ABC's 64 across
  72 MNIST queries. ABC's observed run time was lower on all 42 common proofs.
  This is evidence about this sigmoid-containing workload, **not tanh**, and not
  a measurement of raw ABC bound tightness.
- **Power-system arithmetic:** both tools report UNSAT on all 12 selected IEEE-14
  physical-residual queries; Gurobi's observed run time was lower on each. The two
  structural-output checks are separate: Gurobi completed one and rejected a
  candidate on the other; ABC reports UNSAT on both.
- **Relative to the MVP:** greater published ABC coverage persists, but the
  direction of common-proof runtime differences depends on the workload. There
  is no blanket winner, pooled speed ratio or arbitrary advantage threshold.

Every ABC comparison below is conditional on **source correspondence, not proven
execution identity**, and uses unmatched execution environments. Numerical UNSAT
and published ABC UNSAT are claims, not independently checked proof certificates.

## Evidence and populations

The links in each row are the numerical source of the study-specific conclusions.
Manifest IDs identify original queries, not property disjunction branches.

| Study (all version 1.0) | Selected queries / deadline | Statistics | Exact pair records | Original audit and records | Published inventory |
| --- | --- | --- | --- | --- | --- |
| `sat_relu`, entire manifest (MVP) | 100 / 100 s | [saved calculations](sat-relu-v1-comparison/evidence.json) | [table](sat-relu-v1-comparison/instances.md), [JSON](sat-relu-v1-comparison/evidence.json) | [audit](sat-relu-v1/experiment.json), [records](sat-relu-v1/records/) | [source](sat-relu-v1-comparison/published/source.json) |
| `relusplitter_2026`, entire manifest | 120 / 180 s | [statistics](relusplitter-v1-comparison/statistics.md) | [table](relusplitter-v1-comparison/instances.md), [JSON](relusplitter-v1-comparison/evidence.json) | [audit](relusplitter-v1/experiment.json), [records](relusplitter-v1/records/) | [source](relusplitter-v1-comparison/published/source.json) |
| `dist_shift_2023`, `mnist_concat` | 72 / 300 s | [statistics](mnist-sigmoid-v1-comparison/statistics.md) | [table](mnist-sigmoid-v1-comparison/instances.md), [JSON](mnist-sigmoid-v1-comparison/evidence.json) | [audit](mnist-sigmoid-v1/experiment.json), [records](mnist-sigmoid-v1/records/) | [source](mnist-sigmoid-v1-comparison/published/source.json) |
| `ml4acopf_2024`, exactly `14_ieee_ml4acopf.onnx` | 14 / 600 s | [statistics](acopf-v1-comparison/statistics.md) | [table](acopf-v1-comparison/instances.md), [JSON](acopf-v1-comparison/evidence.json) | [audit](acopf-v1/experiment.json), [records](acopf-v1/records/) | [source](acopf-v1-comparison/published/source.json) |

The MVP's 100 queries and the expansion's 120/72/14 queries each have eligible,
non-corrupt Gurobi records and unique source-hash ABC matches; none were excluded
or missing. These counts inventory separate workloads, not a pooled performance
population. The MVP, ReLUSplitter and MNIST
each retain an appended smoke row outside the population. ACOPF retains 56
unselected rows (other models/aliases and a smoke row) outside its denominator.
No version duplicates, alternative networks or additional families are pooled in.

### Completion, including unresolved queries

| Study | Gurobi numerical UNSAT / selected | ABC UNSAT / selected | Accepted SAT G / ABC | Unresolved G / ABC | Gurobi unresolved reason |
| --- | ---: | ---: | ---: | ---: | --- |
| Shallow-ReLU MVP | 33/100 | 50/100 | 50 / 50 | 17 / 0 | 17 timeouts |
| ReLUSplitter | 1/120 | 96/120 | 2 / 24 | 117 / 0 | 117 timeouts |
| Sigmoid MNIST | 42/72 | 64/72 | 6 / 8 | 24 / 0 | 24 timeouts |
| IEEE-14 ACOPF | 13/14 | 14/14 | 0 / 0 | 1 / 0 | 1 rejected replay, not timeout |

There are **zero accepted-answer disagreements** in each study, not independent
confirmation of correctness. A timeout opposite ABC UNSAT is a coverage gap, not
a conflicting SAT verdict. The ACOPF invalid candidate is likewise not accepted
SAT opposite UNSAT. No construction or license failures were recorded. Missing
solver-stage checkpoints on supervised timeouts remain unavailable rather than
being fabricated as successful solver terminations.

For the three expanded studies, `proof.numerical_unsat_ids`, `accepted_sat_ids`, `unresolved_ids`, `timeout_ids`,
`outcome_cross_tab` and `disagreement_ids` in each linked JSON define these exact
populations. Numerical UNSAT requires the recorded claim within the raw query
deadline; accepted SAT additionally requires accepted replay. All recorded timings
are available here. Agreement, filenames and published outcome cohorts are not
ground truth. The historical MVP JSON predates `proof`; its `instances`,
`populations`, `outcomes`, `unresolved_reasons` and `runtime` retain the corresponding
records. Its proof-only timings below filter `instances` for mutual numerical UNSAT.

### Runtime on commonly completed numerical proofs only

| Population | n | Gurobi run sum s | ABC run sum s | ABC/Gurobi ratio of sums | Median individual ABC/Gurobi ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| Shallow-ReLU MVP common UNSAT | 33 | 34.0201 | 210.2795 | 6.1810 | 5.504 |
| ReLUSplitter common UNSAT | 1 | 22.284 | 6.526 | 0.2929 | 0.2929 |
| MNIST common UNSAT | 42 | 5,259.061 | 255.022 | 0.04849 | 0.05247 |
| ACOPF common UNSAT, all classes | 13 | 2.3325 | 101.3780 | 43.464 | 51.841 |
| ACOPF physical-residual common UNSAT | 12 | 2.1821 | 93.6652 | 42.924 | 51.868 |

Sources: expanded-study JSONs' `proof.paired_unsat`; the last row uses
`cohorts.property_class.physical_residual.paired_unsat`. Exact included IDs and
unrounded numbers live there. Ratios above one mean lower observed Gurobi time;
ratios below one mean lower observed ABC time. The median is of individual
ratios, not the ratio of median runtimes. Every row requires both UNSAT claims,
known run times and a positive Gurobi denominator. Timeouts, invalid candidates,
SAT and disagreements do not enter. No deadline is imputed as a solve time.
These selected common-proof populations cannot describe speed on the unresolved
queries. In particular, n=1 is not a stable estimate for all ReLUSplitter proofs.

## Shallow-ReLU MVP: coverage, width and runtime

The [original Gurobi experiment](sat-relu-v1/README.md) executed all 100 eligible
`sat_relu/1.0` queries using a sequential affine/ReLU feasibility encoding with
gurobi-machinelearning. All 50 local SAT witnesses are strict; the 33 numerical
UNSAT and 17 timeouts are retained without exclusions, errors or missing/corrupt
records. ABC reports 50 UNSAT and 50 strict SAT, with no opposing accepted answers.
The population has 83 same-answer mutual solves, 17 ABC-only solves, zero
Gurobi-only solves and zero neither-solved queries. The appended `test_nano`
CSV row 101 is excluded by its artifact paths despite its `sat_relu` category label.

### All 17 queries completed only by ABC

Every local result below is unresolved `timeout`, raw solver status 9, with about
100 s whole-run time. Neither that time nor the deadline is a successful solve
time, so no paired speed ratio is assigned. IDs link the original records;
full property paths and hashes are in the [audit](sat-relu-v1/experiment.json),
[source inventory](sat-relu-v1-comparison/published/source.json) and
[per-instance table](sat-relu-v1-comparison/instances.md).

| ID / record | Original network stem | Inputs | Hidden width | Stored elements | Descriptor group | ABC run s |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| [0003](sat-relu-v1/records/0003.json) | unsat_v90_c811_k3 | 90 | 991 | 92,165 | W01 | 6.702 |
| [0013](sat-relu-v1/records/0013.json) | unsat_v78_c478_k13 | 78 | 634 | 51,356 | — | 6.484 |
| [0017](sat-relu-v1/records/0017.json) | unsat_v91_c116_k17 | 91 | 298 | 28,014 | W06 | 6.385 |
| [0023](sat-relu-v1/records/0023.json) | unsat_v68_c337_k23 | 68 | 473 | 33,585 | — | 6.439 |
| [0025](sat-relu-v1/records/0025.json) | unsat_v73_c501_k25 | 73 | 647 | 49,174 | W07 | 6.517 |
| [0027](sat-relu-v1/records/0027.json) | unsat_v91_c889_k27 | 91 | 1,071 | 100,676 | W06 | 6.755 |
| [0031](sat-relu-v1/records/0031.json) | unsat_v65_c209_k31 | 65 | 339 | 23,054 | — | 6.378 |
| [0037](sat-relu-v1/records/0037.json) | unsat_v87_c231_k37 | 87 | 405 | 36,452 | — | 6.411 |
| [0047](sat-relu-v1/records/0047.json) | unsat_v88_c453_k47 | 88 | 629 | 57,241 | — | 6.483 |
| [0049](sat-relu-v1/records/0049.json) | unsat_v94_c784_k49 | 94 | 972 | 94,286 | — | 6.691 |
| [0053](sat-relu-v1/records/0053.json) | unsat_v95_c183_k53 | 95 | 373 | 36,556 | — | 6.395 |
| [0063](sat-relu-v1/records/0063.json) | unsat_v51_c288_k63 | 51 | 390 | 21,062 | W12 | 6.378 |
| [0069](sat-relu-v1/records/0069.json) | unsat_v67_c223_k69 | 67 | 357 | 24,992 | W05 | 6.375 |
| [0071](sat-relu-v1/records/0071.json) | unsat_v47_c384_k71 | 47 | 478 | 23,902 | W14 | 6.459 |
| [0079](sat-relu-v1/records/0079.json) | unsat_v75_c586_k79 | 75 | 736 | 57,410 | — | 6.531 |
| [0089](sat-relu-v1/records/0089.json) | unsat_v59_c154_k89 | 59 | 272 | 16,866 | — | 6.369 |
| [0095](sat-relu-v1/records/0095.json) | unsat_v83_c233_k95 | 83 | 399 | 34,316 | W16 | 6.407 |

Names identify artifacts only; `sat`/`unsat` prefixes do not establish truth.
ABC's 6.369–6.755 s observations here are UNSAT claims, not independent proofs.

### Width variation is not depth scaling

All networks have Gemm → ReLU → Gemm, one hidden layer and two outputs. Inputs
vary 5–95, hidden widths 29–1,071, stored weight/bias elements 234–100,676.
The whole category therefore varies in input dimension as well as width.

The exploratory bins below use all 100 audited descriptors, with integer width
intervals `[0,199]`, `[200,399]`, `[400,599]`, `[600,799]`, `[800,∞)`.
SAT and UNSAT columns reflect accepted witnesses and ABC claims, not filenames.

| Hidden width | Queries | SAT / ABC UNSAT | G timeouts | Timeout fraction among ABC UNSAT |
| --- | ---: | --- | ---: | ---: |
| <200 | 24 | 12 / 12 | 0 | 0/12 |
| 200–399 | 52 | 26 / 26 | 7 | 7/26 |
| 400–599 | 10 | 5 / 5 | 3 | 3/5 |
| 600–799 | 8 | 4 / 4 | 4 | 4/4 |
| ≥800 | 6 | 3 / 3 | 3 | 3/3 |

Increasing width is associated with more Gurobi timeout incidence on the
UNSAT-claim sample; all 50 strict SAT queries complete for both tools, including
wide networks. ABC's narrow observed timing range does not establish constant
computational complexity or reveal an internal timing mechanism.

The [evidence](sat-relu-v1-comparison/evidence.json) identifies 16 `Wxx` groups
holding input/output dimensions, operation sequence and hidden-layer count fixed
while widths vary. These are descriptor matches, not controlled width-only
changes: weights and properties differ, and descriptors do not prove graph
equivalence. Selected UNSAT-claim examples retain that qualification:

| Group / fixed inputs | Narrower ID: width, G result | Wider ID: width, G result |
| --- | --- | --- |
| W05 / 67 | 0015: 273, UNSAT in 0.331 s | 0069: 357, timeout |
| W07 / 73 | 0085: 222, UNSAT in 1.643 s | 0025: 647, timeout |
| W12 / 51 | 0087: 384, UNSAT in 1.352 s | 0063: 390, timeout |
| W16 / 83 | 0097: 346, UNSAT in 1.955 s | 0095: 399, timeout |

W06 times out at both width 298 (0017) and 1,071 (0027). W12's six-unit difference
accompanies a large outcome difference: width alone is not an adequate explanation.
Instance structure, property, input dimension, parameter values and measurement
order are not controlled. These are descriptive bins, not a fitted scaling law.
Recompute them by filtering `instances[].architecture.hidden_widths[0]`,
`gurobi.outcome`, `abc.outcome` and `comparison` in the unchanged MVP JSON.

### Separate proof, falsification and total recorded cost

Gurobi has lower observed run time on every one of the 83 mutual solves. That
population mixes 33 common UNSAT and 50 common strict SAT: its median individual
ABC/G run ratio is 7.032, sum ratio 7.247. The SAT-only median is 7.125; the
proof-only median is 5.504, with proof sums and ratio in the common-proof table
above. `runtime.paired_same_answer.ids` lists all 83; neither the SAT-only nor the
mixed population substitutes for a proof-only comparison.

| Recorded population | Gurobi | ABC |
| --- | ---: | ---: |
| All 100 runs, sum s | 1,769.410 | 611.661 |
| All 100 runs, median s | 0.874 | 6.032 |
| 83 mutual solves, run sum s | 69.200 | 501.499 |
| 83 mutual solves, run median s | 0.824 | 5.841 |
| All 100 preparation measurements, sum s | 0 | 1,926.310 |
| All 100 preparation measurements, median s | 0 | 19.224 |

ABC's lower all-run total includes avoiding the 17 long local timeouts. The
historical archive additionally reports a 30.383 median preparation-plus-run
ratio on the 83 pairs and all-record preparation-plus-run sums of 2,537.970 s ABC
versus 1,769.410 s Gurobi. These historical accounting quantities are retained
for traceability, **not endorsed as comparable speed ratios**: preparation reuse
and stage accounting are unavailable, and the archive predates the explicit
prepare-plus-run comparability opt-in. Current regeneration leaves combined
ratios null. Neither all-run cost total is a successful-solve time or an
equal-coverage speed ratio.

The 50 accepted-SAT candidate queries contribute 500 Gurobi points and
provisionally 500 ABC points under pinned `get_score` (10 each, time bonus
disabled, incorrect-result penalty −150). ABC credit remains conditional on
artifact correspondence/check correctness. The 50 UNSAT-claim queries remain
unassessed for full scoring without execution-bound identity and complete
participating-tool strict-witness conflict evidence; normalization also requires
participating-tool context. This is not an official full-category score, and
two-tool agreement is not grounds for awarding UNSAT points.

All 200 source-artifact decompressed hashes match the local audit. All 50 ABC
SAT caches correspond to normalized CSV rows and witness hashes, use
`vnncomp2026-cex-1` on the CPU provider and report strict acceptance. Published
validator dependencies are Python 3.12.13, ONNX 1.21.0 and ONNX Runtime 1.26.0:
these are not ABC execution-environment versions. No published check was rerun.
Source verification, floating-point replay and the common hardware/timing limits
below apply equally to this MVP study.

## ReLUSplitter: depth, original groups and confounders

The [graph audit](relusplitter-v1/README.md#selection-and-graph-audit) verifies
784 inputs, 10 outputs and 4/5/6 hidden ReLU layers, not arbitrary graph-node
counts. The depth cohorts retain all queries:

| Hidden ReLU layers | Queries | G UNSAT | ABC UNSAT | G strict SAT / ABC accepted SAT | G timeouts |
| --- | ---: | ---: | ---: | ---: | ---: |
| 4 | 6 | 1 | 4 | 0 / 2 | 5 |
| 5 | 44 | 0 | 32 | 0 / 12 | 44 |
| 6 | 70 | 0 | 60 | 2 / 10 | 68 |

Original and generated variants need to be read within their source-name groups.
The following cross-grouping filters `instances[].architecture` by
`original_model_group` and `hidden_relu_layers` (not filename verdict labels):

| Original group | Original depth / n: G UNSAT, ABC UNSAT | Generated depth / n: G UNSAT, ABC UNSAT | G accepted SAT original / generated | G timeouts original / generated |
| --- | --- | --- | ---: | ---: |
| `model_0_0` | 4 / 2: 0, 0 | 5 / 10: 0, 0 | 0 / 0 | 2 / 10 |
| `model_1_1` | 5 / 8: 0, 6 | 6 / 40: 0, 30 | 0 / 2 | 8 / 38 |
| `model_2_2` | 4 / 4: 1, 4 | 5 / 20: 0, 20 | 0 / 0 | 3 / 20 |
| `model_3_3` | 5 / 6: 0, 6 | 6 / 30: 0, 30 | 0 / 0 | 6 / 30 |

ABC's remaining rows in this table are accepted SAT: 2/10 in `model_0_0` and
2/10 in `model_1_1` (original/generated). Thus the all-SAT `model_0_0` group
cannot establish proof-completion behavior. Even within `model_2_2`, one original
proof versus zero generated proofs is descriptive, not a depth-only experiment.

Four-layer originals have widths `[128,256,256,256]`; five-layer originals have
`[128,256,256,256,256]`. Generated variants prepend a width-256 ReLU layer, changing
the width sequence as well as depth, with neuron-stability confounding also
identified by the study design. No controlled stability measurement or independent
functional-equivalence proof was collected. Source-name grouping and a generator's
intent do not establish equivalence of modified and original models. Group mix,
properties, width and stability prevent attributing changes solely to depth.

The only common numerical proof is [Gurobi record 0066](relusplitter-v1/records/0066.json):
`model_2_2.onnx`, `d2_eps_0.01_sample_8_label_3.vnnlib`, four hidden ReLU layers,
22.283989 s versus ABC CSV row 67's 6.526107 s. The other 95 ABC UNSAT claims face
Gurobi timeouts. Separately, [0074](relusplitter-v1/records/0074.json) and
[0075](relusplitter-v1/records/0075.json) are strict SAT in the generated
`model_1_1` six-layer group; another 22 published SAT queries time out locally.
Those falsification outcomes are retained, not used as proof timings.

All 120 formulations finished construction, while 117 runs timed out: this
distinguishes observed deadline non-completion from unsupported input or failed
construction. Of those timeouts, 69 retain raw status 9 and 48 lack a completed
status checkpoint. This does not identify a causal search or bound mechanism.

## MNIST: internal sigmoid, not tanh or raw-bound evidence

The [audited model and formulation](mnist-sigmoid-v1/README.md#selection-and-graph-audit)
contain five Gemm, three ReLU, one internal sigmoid and two reshape nodes:
784 scalar logistic relations and 264 scalar ReLUs. The encoding uses native
global nonlinear logistic relations (`FuncNonlinear=1`), not a fixed piecewise
approximation. This single model is an internal-sigmoid study; it does not test
tanh, nor isolate sigmoid cost from the other operations and properties.

Within the **64 published-UNSAT** queries, Gurobi completes 42 and times out on
22; ABC reports all 64 complete. On the 42 common proofs, Gurobi run times span
40.949–292.564 s (median 115.163), ABC 6.030–6.464 s (median 6.047).
The ratios above show lower observed ABC runtime even after conditioning on
Gurobi completion, while the 22 unresolved proofs remain a separate coverage gap.
For example, [0000](mnist-sigmoid-v1/records/0000.json) is numerical UNSAT;
[0004](mnist-sigmoid-v1/records/0004.json) is a timeout. The full proof IDs,
including all 22 unresolved cases, are in the linked JSON rather than a successful
subset masquerading as the whole study.

The **eight published-SAT** queries are separate. Gurobi strictly replays six
(`0013`, `0025`, `0038`, `0043`, `0055`, `0068`); `0001` and `0011` time out.
All eight ABC SAT caches report strict acceptance. These outcome cohorts follow
published claims, not independently certified labels. All 72 formulations finished
construction; among the 24 timeouts, 13 retain status 9 and 11 lack a completed
status checkpoint. No absent stage timing is treated as zero.

Published outcomes and runner times reveal neither raw ABC bound values nor
bound gaps, tightening trajectories or comparable intermediate Gurobi bounds.
The evidence therefore supports a numerical proof-completion/runtime comparison,
not a claim that ABC's sigmoid bounds are tighter, or an explanation of why these
queries differ. No such uncollected measurement or causal mechanism is inferred.

## ACOPF: all 14 properties, two different classes

The [audit and formulation](acopf-v1/README.md#selection-and-graph-audit) represent
the complete selected graph for every property, including property 2, with native
quadratic squares/products and global sigmoid/sine/cosine relations. The graph
includes 96 scalar ReLUs, 24 sigmoids, 134 squares, 60 variable products and
20 sine/20 cosine relations; angles are in radians. This establishes represented
semantics, not how much each operation contributed to proof difficulty.

Every row below links its original record; ABC times and row correspondence are
in the [paired evidence](acopf-v1-comparison/evidence.json). All ABC rows claim
UNSAT. `Physical` means physical-residual property, `structural` a bounded-output
check. Times are run seconds, rounded here only.

| ID / record | Property | Class | Gurobi outcome | G run s | ABC run s |
| --- | ---: | --- | --- | ---: | ---: |
| [0000](acopf-v1/records/0000.json) | 9 | Physical | numerical UNSAT | 0.1403 | 7.8566 |
| [0001](acopf-v1/records/0001.json) | 7 | Physical | numerical UNSAT | 0.2698 | 7.7862 |
| [0002](acopf-v1/records/0002.json) | 2 | Physical | numerical UNSAT | 0.2685 | 7.8562 |
| [0003](acopf-v1/records/0003.json) | 8 | Physical | numerical UNSAT | 0.1416 | 7.7893 |
| [0004](acopf-v1/records/0004.json) | 4 | Structural | numerical UNSAT | 0.1503 | 7.7128 |
| [0005](acopf-v1/records/0005.json) | 6 | Physical | numerical UNSAT | 0.1474 | 7.7929 |
| [0006](acopf-v1/records/0006.json) | 12 | Physical | numerical UNSAT | 0.1433 | 7.8218 |
| [0007](acopf-v1/records/0007.json) | 13 | Physical | numerical UNSAT | 0.1503 | 7.7838 |
| [0008](acopf-v1/records/0008.json) | 11 | Physical | numerical UNSAT | 0.1504 | 7.7845 |
| [0009](acopf-v1/records/0009.json) | 1 | Physical | numerical UNSAT | 0.3224 | 7.8084 |
| [0010](acopf-v1/records/0010.json) | 3 | Structural | unresolved: invalid replay | 0.2650 | 8.0300 |
| [0011](acopf-v1/records/0011.json) | 14 | Physical | numerical UNSAT | 0.1505 | 7.8004 |
| [0012](acopf-v1/records/0012.json) | 10 | Physical | numerical UNSAT | 0.1503 | 7.7992 |
| [0013](acopf-v1/records/0013.json) | 5 | Physical | numerical UNSAT | 0.1473 | 7.7859 |

The **12 physical-residual** queries all complete numerically for both tools,
with lower observed Gurobi run time on every pair (sum ratio 42.924, median
individual ratio 51.868). Thus the favorable observed runtime is not merely an
artifact of including the easy structural property 4. Conversely, completion on
these residual queries does not prove general tractability of physical arithmetic,
larger grids, other models or stronger properties. The entire model was encoded,
but the records do not isolate difficulty or bound tightness by operator.

The **two structural** checks must not be sold as physical-residual proofs.
Property 4 completes numerically; property 3 remains unresolved. For property 3,
Gurobi status 2 supplied a candidate, but FLOAT32 original-ONNX replay satisfied
no original output alternative, with either strict or tolerated input bounds.
The recorded `validation_failed`/`invalid` is not SAT, UNSAT or a timeout. Its
zero-output thresholds have magnitude `1e-6`, the same scale as the unchanged
feasibility tolerance. That numerical context is **not a demonstrated cause** of
the rejection. No retry or tolerance change repairs it in this report. ABC's
UNSAT claim does not authorize replacing the unresolved local outcome.

## Cross-study interpretation

The [MVP evidence](sat-relu-v1-comparison/evidence.json) retains 100 separate queries,
100 s each, all one-hidden-layer Gemm/ReLU/Gemm networks. It records Gurobi/ABC
UNSAT 33/50, strict SAT 50/50, and 17 Gurobi timeouts (all opposite ABC UNSAT).
The 83 mutual solves mix 50 SAT with 33 UNSAT; their median run ratio 7.032 and
sum ratio 7.247 must not be compared as though they were proof-only statistics.
On just its 33 common UNSAT records, the saved per-instance ratios give median
**5.504**; their [saved evidence](sat-relu-v1-comparison/evidence.json) sums to
34.020135 s Gurobi and 210.279466 s ABC. These are a separate shallow population.

The MVP pattern was greater ABC coverage but lower Gurobi time on common solves.
The expanded studies qualify, rather than universally reverse, it:
ReLUSplitter and MNIST show greater published ABC proof coverage **and** lower
ABC observed time on common proofs; ACOPF physical residuals show equal reported
proof completion and lower Gurobi observed time. ACOPF's overall 13/14 versus
14/14 coverage still includes a local validation failure, not a clean sweep.

Different architectures, properties, dimensionality, deadlines, formulations and
measured source revisions prevent pooling or treating this as a controlled
shallow-to-deep/nonlinear transition. Width variation in the MVP was not a
depth experiment either. Neither these timings nor completion fractions identify
an intrinsic MILP/nonlinear-versus-ABC advantage or an activation-specific cause.

## Provenance, accounting and claim limits

All studies pin benchmark revision
[`303f2327a8e8411efc4457da03d2016ce42733cf`](https://github.com/VNN-COMP/vnncomp2026_benchmarks/tree/303f2327a8e8411efc4457da03d2016ce42733cf/benchmarks)
and ABC results/scoring/validator revision
[`eea564f5d0a8751d8321a409214db14d03f452b8`](https://github.com/VNN-COMP/vnncomp2026_results/tree/eea564f5d0a8751d8321a409214db14d03f452b8/alpha_beta_crown).
Rules revision is `b0ec5ac3c8f39262f07a1c67919fbb89fa42a245`, runner revision
`3d5a8848169fc5f0cc03ab9722865235e9857f16`. The results publication revision is
not an ABC executable revision or a known execution date.

Measured Gurobi implementation revisions (full source/lockfile hashes are in the
linked audits and expanded-study JSON `provenance.experiment_context.revision`;
the MVP audit retains its own measured revision):

| Study | Measured commit |
| --- | --- |
| Shallow-ReLU MVP | `a8d72471637100a7f5d6e36f8f824883be4e7ebe` |
| ReLUSplitter | `2ba2eb4242bd55cda799867d41e82a6a96b237d2` |
| MNIST | `3633256b54f1f3daf8e9e4d970e41a216b6c4341` |
| ACOPF | `54444759a50f54df94be2763689ffc51b351f0ba` |

- **Identity:** source inventories verify original compressed benchmark Git blobs
  at the pinned revision and match decompressed ONNX/VNNLIB SHA256s with each
  Gurobi audit. Full category/version/network/property identities select rows, not
  row order. Every selected ABC pair is source-verified and **execution-unbound**;
  zero have independent evidence tying the measured ABC execution to those bytes.
  SAT cache row/witness correspondence does not supply that missing binding or
  establish cache correctness. Comparison does not rerun the published checks.
- **Hardware/resources:** all four Gurobi archives used Apple M4, 10 logical CPUs,
  16 GiB RAM, macOS 26.6.2 arm64, Python 3.12.16, Gurobi 13.0.1 and
  gurobi-machinelearning 1.7.0; ONNX 1.21.0, ONNX Runtime 1.26.0, NumPy 2.2.6.
  Queries ran sequentially, Gurobi Threads=1, replay separately configured for
  12 intra/inter-op CPU threads, no memory cap or numerical/performance tuning.
  ReLUSplitter's first query overlapped about 16 seconds of tiny-suite checking;
  [the archive](relusplitter-v1/README.md#reproduce) discloses it. The ABC inputs
  do not disclose execution CPU/GPU, thread/memory allocation, exclusive-node
  status, tool commit/configuration or package environment. CPU witness checks
  are not evidence of CPU-only ABC execution. No matched-resource claim follows.
- **Timing:** Gurobi run time includes subprocess startup, artifact reading,
  interpretation, construction, optimization and candidate replay. Invocation wall
  time additionally includes supervision/cleanup. Acquisition and audit are
  separately recorded; per-query preparation is a no-op, zero seconds. ABC's CSV
  supplies preparation and run fields, not comparable internal stage accounting.
  All-selected preparation sums G/ABC are 0/1,926.310 s (MVP), 0/2,390.793 s (ReLUSplitter),
  0/1,385.976 s (MNIST), 0/273.099 s (ACOPF), from `runtime.*.preparation`.
  These are **not added** to paired run ratios. No comparable prepare-plus-run
  opt-in exists here. The MVP's historical combined ratios predate that opt-in;
  they are not carried forward as comparable speed evidence.
- **Deadlines:** the original 100/180/300/600 s run budgets remain; no startup
  subtraction, grace-period solve credit or timeout imputation is applied. The
  pinned results README describes raw scoring deadlines, but executable scoring
  subtracts fastest-observed overhead for plots and deadline enforcement (see
  [accounting notes](../docs/comparisons.md#evidence-interpretation) and retained
  `published/raw/SCORING/` snapshots). We do not reproduce adjusted official
  scores. Every selected ABC run is below its raw deadline, so that discrepancy
  does not alter these ABC completion counts.
- **Correctness:** definitive global Gurobi infeasibility of the encoded query is
  numerical UNSAT under floating-point assumptions, not independently certified
  exact-real UNSAT. ABC UNSAT is a published verifier claim, also without an
  independently checked certificate in these archives. Strict local SAT witnesses
  were independently replayed on original FLOAT32 ONNX; published SAT acceptance
  is from retained check caches. Strict witnesses can refute matching UNSAT;
  tolerance-only acceptance cannot. Invalid replay never becomes a proof. Zero
  observed disagreements does not establish soundness of either verifier.
- **Scoring/scope:** complete participating-tool correctness-conflict evidence and
  execution-bound identity are absent. No full category score, blanket winner,
  raw-bound comparison, general scaling law or tanh conclusion is supported.

## Reproduce and audit the report

For the MVP, use the solver-free command in
[comparison instructions](../docs/comparisons.md#regenerate-the-retained-evidence).
For the expansion, use the commands in the [ReLUSplitter](relusplitter-v1-comparison/README.md#regenerate-without-solver-or-network),
[MNIST](mnist-sigmoid-v1-comparison/README.md#regenerate-without-solver-or-network)
and [ACOPF](acopf-v1-comparison/README.md#regenerate-without-solver-or-network)
comparison READMEs, or write to a fresh output directory to preserve the archives.
Inputs are `experiment.json`, `records/*.json` and each retained `published/`
inventory/CSV/check-cache/witness snapshot. No benchmark download, solver license,
network, ABC execution or new witness replay is needed to recalculate statistics.
Original experiment READMEs separately document reproducible benchmark acquisition
and formulations; they are not instructions to rerun measurements for this report.

The archived `evidence.json` fingerprints analyzed here are:

| Study | Evidence SHA256 |
| --- | --- |
| Shallow-ReLU MVP | `994f40873f56b7716289fa02eea252998a1fe08bb70d26066cfa94dae5611f72` |
| ReLUSplitter | `fc98c2215828159f32f14f02c9a8a8795d15cbc192a85ae5a0a77004278d8800` |
| MNIST | `49a14f653ead958bfc6eeddb9630086fe14985365533a66e1c1b5344d3ff3fb6` |
| ACOPF | `da345451ee8c930ccd2cf8e40f1a6c1566dabb200a89c26790fc0f4d193152e7` |

Those three use calculation-source SHA256
`56fb07f6be040835f14cb331b6453977964f3f99651cc94dad0ddb8e70589abb`.
The historical MVP JSON uses calculation-source SHA256
`fb1d7bce1eb31ff73f590a93ef75d03ba9e94ba61c2dac60316ba5a34dfc14d4`;
current regeneration intentionally differs in schema/provenance and removes
unapproved combined ratios. Its retained inputs remain reproducible; do not
overwrite the historical archive to obtain a purported byte-identical modern run.
`provenance.experiment_sha256`, `published_source_sha256`, `record_sha256` and
`published.files` retain the transitive input fingerprints. The review/check
records are in [reviews/](reviews/): the [analysis and consolidation reviews](reviews/proof-comparison-analysis-review.md),
[#11 statistics implementation review](reviews/proof-comparison-statistics-review.md)
and [historical MVP review](reviews/sat-relu-comparison-review.md) identify their
respective reviewed revisions, not blanket approval of subsequent edits.
