# Verification experiment report

Listed: 14; eligible: 14; excluded: 0.
Recorded eligible results: 14; Missing records: 0; corrupt records: 0.
Solver-reported, accepted solves: 13. Outcomes: {'unsat': 13, 'unknown': 1}.
Validation: {'none': 13, 'invalid': 1}. Unresolved reasons: {'validation_failed': 1}.
Property classes (where selected): {'physical_residual': {'listed': 12, 'eligible': 12, 'unsat': 12}, 'structural_output_bound': {'listed': 2, 'eligible': 2, 'unsat': 1, 'unknown': 1}}.

## Interpretation

SAT is accepted only after pinned FLOAT32 ONNX replay. Strict and tolerance-only classifications are separate; tolerance-only SAT does not refute an UNSAT claim. Numerical UNSAT is not an independently certified UNSAT or an exact-real proof. Solver outcomes are not independent ground truth. Filename labels never determine verdicts.

## Timings and resources

Whole-run time includes subprocess startup, reads/decompression, interpretation, encoding, solving, and validation. No startup overhead is subtracted; no kill-grace result gets solve credit. Invocation wall time additionally includes supervising/cleanup overhead. Preparation is a no-op (0 seconds); category eligibility audit is separately measured, not hidden preparation or cached solving analysis.

Runtime seconds: `{'all': {'count': 14, 'sum': 2.5975029156543314, 'min': 0.14026904106140137, 'median': 0.15033941704314202, 'max': 0.3224193751811981}, 'solved': {'count': 13, 'sum': 2.332472457550466, 'min': 0.14026904106140137, 'median': 0.15032975003123283, 'max': 0.3224193751811981}}`.
Invocation seconds: `{'count': 14, 'sum': 2.598174456972629, 'min': 0.1403166251257062, 'median': 0.15038556256331503, 'max': 0.3224718749988824}`.
Audit seconds: 0.170873.
Resources: `{'platform': 'macOS-26.6.2-arm64-arm-64bit', 'machine': 'arm64', 'processor': 'arm', 'logical_cpus': 10, 'hw.memsize': '17179869184', 'hw.physicalcpu': '10', 'machdep.cpu.brand_string': 'Apple M4'}`; execution: `{'threads': 1, 'sequential': True, 'preparation_analysis': False}`.
Pinned replay uses 12 intra/inter-op CPU threads separately from the Gurobi Threads limit. No memory cap, performance tuning, or numerical tolerance tuning is applied.

## Architecture and numerical scope

Eligibility uses the verification contract's static FLOAT32 tensor-DAG and supported conjunctive/disjunctive property grammar, independently of solve outcomes. Each eligible row records the actual formulation, tensor shapes, operations, scalar relation counts, affine widths and ReLU node counts, input/output dimensions, initializer count, and output comparison/alternative counts. ReLU node counts describe hidden-layer depth only for sequential networks. Original-model groups are source-name groups, not evidence of functional equivalence. ACOPF properties 3/4 describe structural output bounds; the other 12 describe physical residuals. Depth comparisons may also vary width and neuron stability; no causal depth effect is inferred.
Gurobi numerical defaults are unchanged; effective settings, package versions, witnesses, and validation diagnostics are retained in individual records. These are floating-point results, not exact-arithmetic certification.

## Competition scoring

Subset score unavailable: Artifact-matched other-tool outcomes and strict witness checks needed to assess conflicts and UNSAT correctness; Complete participating-tool context for category normalization; cross-tool caches do not bind benchmark artifact hashes.
Accepted SAT-only subset contribution: 0 points across 0 instances (10 each under pinned get_score; not the full eligible/category score). Numerical UNSAT contributions remain unassessed without artifact-matched cross-tool strict-witness evidence.
Pinned get_score awards 10 per accepted solve; time bonus disabled. Strict witnesses can refute UNSAT; tolerance-only witnesses earn SAT credit but cannot refute UNSAT. No score inferred from our own verdicts or filenames.
No ABC speed ratio or hardware-independent performance claim is made without matching artifacts and execution resources.

## Per-instance records

Manifest order identifies rows; original names and artifact hashes are in experiment.json and records/<id>.json.

| ID | Outcome | Reason | Validation | Whole-run seconds |
| --- | --- | --- | --- | --- |
| 0000 | unsat | infeasible | — | 0.14026904106140137 |
| 0001 | unsat | infeasible | — | 0.26976204104721546 |
| 0002 | unsat | infeasible | — | 0.26848908397369087 |
| 0003 | unsat | infeasible | — | 0.14163708314299583 |
| 0004 | unsat | infeasible | — | 0.1503490840550512 |
| 0005 | unsat | infeasible | — | 0.14742162497714162 |
| 0006 | unsat | infeasible | — | 0.14333000010810792 |
| 0007 | unsat | infeasible | — | 0.15032975003123283 |
| 0008 | unsat | infeasible | — | 0.15038383402861655 |
| 0009 | unsat | infeasible | — | 0.3224193751811981 |
| 0010 | unknown | validation_failed | invalid | 0.2650304581038654 |
| 0011 | unsat | infeasible | — | 0.15046704094856977 |
| 0012 | unsat | infeasible | — | 0.15028908313252032 |
| 0013 | unsat | infeasible | — | 0.14732541586272418 |

## Reproduce

See docs/experiments.md for acquisition, audit, sequential execution, and solver-free report commands. Pinned references and source hashes are in experiment.json. Raw records are the authoritative report inputs.
