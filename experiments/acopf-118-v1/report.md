# Verification experiment report

Listed: 5; eligible: 5; excluded: 0.
Recorded eligible results: 5; Missing records: 0; corrupt records: 0.
Solver-reported, accepted solves: 3. Outcomes: {'unknown': 2, 'unsat': 3}.
Validation: {'none': 4, 'invalid': 1}. Unresolved reasons: {'timeout': 1, 'validation_failed': 1}.
Property classes (where selected): {'physical_residual': {'listed': 3, 'eligible': 3, 'unknown': 1, 'unsat': 2}, 'structural_output_bound': {'listed': 2, 'eligible': 2, 'unsat': 1, 'unknown': 1}}.

## Interpretation

SAT is accepted only after pinned FLOAT32 ONNX replay. Strict and tolerance-only classifications are separate; tolerance-only SAT does not refute an UNSAT claim. Numerical UNSAT is not an independently certified UNSAT or an exact-real proof. Solver outcomes are not independent ground truth. Filename labels never determine verdicts.

## Timings and resources

Whole-run time includes subprocess startup, reads/decompression, interpretation, encoding, solving, and validation. No startup overhead is subtracted; no kill-grace result gets solve credit. Invocation wall time additionally includes supervising/cleanup overhead. Preparation is a no-op (0 seconds); category eligibility audit is separately measured, not hidden preparation or cached solving analysis.

Runtime seconds: `{'all': {'count': 5, 'sum': 710.5832750003319, 'min': 3.218548124888912, 'median': 10.1399171249941, 'max': 600.0145108331926}, 'solved': {'count': 3, 'sum': 100.42884704214521, 'min': 3.218548124888912, 'median': 5.735618167091161, 'max': 91.47468075016513}}`.
Invocation seconds: `{'count': 5, 'sum': 710.5837179182563, 'min': 3.218603749992326, 'median': 10.139981959015131, 'max': 600.0146854170598}`.
Audit seconds: 0.656554.
Resources: `{'platform': 'macOS-26.6.2-arm64-arm-64bit', 'machine': 'arm64', 'processor': 'arm', 'logical_cpus': 10, 'hw.memsize': '17179869184', 'hw.physicalcpu': '10', 'machdep.cpu.brand_string': 'Apple M4'}`; execution: `{'threads': 1, 'sequential': True, 'preparation_analysis': False}`.
Pinned replay uses 12 intra/inter-op CPU threads separately from the Gurobi Threads limit. No memory cap, performance tuning, or numerical tolerance tuning is applied.

## Architecture and numerical scope

Eligibility uses the verification contract's static FLOAT32 tensor-DAG and supported conjunctive/disjunctive property grammar, independently of solve outcomes. Each eligible row records the actual formulation, tensor shapes, operations, scalar relation counts, affine widths and ReLU node counts, input/output dimensions, initializer count, and output comparison/alternative counts. ReLU node counts describe hidden-layer depth only for sequential networks. Original-model groups are source-name groups, not evidence of functional equivalence. Original ACOPF properties 3/4 describe structural output bounds (generation/voltage respectively); other selected properties describe physical residuals. Every query represents the complete graph. Stored initializer elements, tensor nodes, scalar relations and measured optimization-encoding sizes are distinct metrics. Depth comparisons may also vary width and neuron stability; no causal depth effect is inferred.
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
| 0000 | unknown | timeout | — | 600.0145108331926 |
| 0001 | unsat | infeasible | — | 91.47468075016513 |
| 0002 | unknown | validation_failed | invalid | 10.1399171249941 |
| 0003 | unsat | infeasible | — | 5.735618167091161 |
| 0004 | unsat | infeasible | — | 3.218548124888912 |

## Reproduce

See docs/experiments.md for acquisition, audit, sequential execution, and solver-free report commands. Pinned references and source hashes are in experiment.json. Raw records are the authoritative report inputs.
