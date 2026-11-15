# Verification experiment report

Listed: 4; eligible: 4; excluded: 0.
Recorded eligible results: 4; Missing records: 0; corrupt records: 0.
Solver-reported, accepted solves: 1. Outcomes: {'unknown': 3, 'unsat': 1}.
Validation: {'none': 4}. Unresolved reasons: {'timeout': 3}.
Property classes (where selected): {'structural_output_bound': {'listed': 2, 'eligible': 2, 'unknown': 2}, 'physical_residual': {'listed': 2, 'eligible': 2, 'unsat': 1, 'unknown': 1}}.

## Interpretation

SAT is accepted only after pinned FLOAT32 ONNX replay. Strict and tolerance-only classifications are separate; tolerance-only SAT does not refute an UNSAT claim. Numerical UNSAT is not an independently certified UNSAT or an exact-real proof. Solver outcomes are not independent ground truth. Filename labels never determine verdicts.

## Timings and resources

Whole-run time includes subprocess startup, reads/decompression, interpretation, encoding, solving, and validation. No startup overhead is subtracted; no kill-grace result gets solve credit. Invocation wall time additionally includes supervising/cleanup overhead. Preparation is a no-op (0 seconds); category eligibility audit is separately measured, not hidden preparation or cached solving analysis.

Runtime seconds: `{'all': {'count': 4, 'sum': 1819.6558479168452, 'min': 19.578616457991302, 'median': 600.0201738750329, 'max': 600.0368837087881}, 'solved': {'count': 1, 'sum': 19.578616457991302, 'min': 19.578616457991302, 'median': 19.578616457991302, 'max': 19.578616457991302}}`.
Invocation seconds: `{'count': 4, 'sum': 1819.6565664173104, 'min': 19.578796916175634, 'median': 600.0203349795192, 'max': 600.0370995420963}`.
Audit seconds: 1.871125.
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
| 0000 | unknown | timeout | — | 600.022790875053 |
| 0001 | unsat | infeasible | — | 19.578616457991302 |
| 0002 | unknown | timeout | — | 600.0368837087881 |
| 0003 | unknown | timeout | — | 600.0175568750128 |

## Reproduce

See docs/experiments.md for acquisition, audit, sequential execution, and solver-free report commands. Pinned references and source hashes are in experiment.json. Raw records are the authoritative report inputs.
