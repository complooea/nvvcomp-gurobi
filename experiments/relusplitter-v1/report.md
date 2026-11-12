# Verification experiment report

Listed: 120; eligible: 120; excluded: 0.
Recorded eligible results: 1; Missing records: 119; corrupt records: 0.
Solver-reported, accepted solves: 0. Outcomes: {'unknown': 1}.
Validation: {'none': 1}. Unresolved reasons: {'timeout': 1}.

## Interpretation

SAT is accepted only after pinned FLOAT32 ONNX replay. Strict and tolerance-only classifications are separate; tolerance-only SAT does not refute an UNSAT claim. Numerical UNSAT is not an independently certified UNSAT or an exact-real proof. Solver outcomes are not independent ground truth. Filename labels never determine verdicts.

## Timings and resources

Whole-run time includes subprocess startup, reads/decompression, interpretation, encoding, solving, and validation. No startup overhead is subtracted; no kill-grace result gets solve credit. Invocation wall time additionally includes supervising/cleanup overhead. Preparation is a no-op (0 seconds); category eligibility audit is separately measured, not hidden preparation or cached solving analysis.

Runtime seconds: `{'all': {'count': 1, 'sum': 180.01287941704504, 'min': 180.01287941704504, 'median': 180.01287941704504, 'max': 180.01287941704504}, 'solved': {'count': 0, 'sum': 0, 'min': None, 'median': None, 'max': None}}`.
Invocation seconds: `{'count': 1, 'sum': 180.0129315839149, 'min': 180.0129315839149, 'median': 180.0129315839149, 'max': 180.0129315839149}`.
Audit seconds: 1.091024.
Resources: `{'platform': 'macOS-26.6.2-arm64-arm-64bit', 'machine': 'arm64', 'processor': 'arm', 'logical_cpus': 10, 'hw.memsize': '17179869184', 'hw.physicalcpu': '10', 'machdep.cpu.brand_string': 'Apple M4'}`; execution: `{'threads': 1, 'sequential': True, 'preparation_analysis': False}`.
Pinned replay uses 12 intra/inter-op CPU threads separately from the Gurobi Threads limit. No memory cap, performance tuning, or numerical tolerance tuning is applied.

## Architecture and numerical scope

Eligibility uses the verification contract's sequential FLOAT32 affine/ReLU and supported conjunctive/disjunctive property grammar, independently of solve outcomes. Each eligible row's architecture descriptor records the audited operations, hidden widths and ReLU depth, input/output dimensions, parameter count, and output comparison/alternative counts. Original-model groups are source-name groups, not evidence of functional equivalence. Depth comparisons may also vary width and neuron stability; no causal depth effect is inferred.
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
| 0000 | unknown | timeout | — | 180.01287941704504 |
| 0001 | missing | not recorded | — | — |
| 0002 | missing | not recorded | — | — |
| 0003 | missing | not recorded | — | — |
| 0004 | missing | not recorded | — | — |
| 0005 | missing | not recorded | — | — |
| 0006 | missing | not recorded | — | — |
| 0007 | missing | not recorded | — | — |
| 0008 | missing | not recorded | — | — |
| 0009 | missing | not recorded | — | — |
| 0010 | missing | not recorded | — | — |
| 0011 | missing | not recorded | — | — |
| 0012 | missing | not recorded | — | — |
| 0013 | missing | not recorded | — | — |
| 0014 | missing | not recorded | — | — |
| 0015 | missing | not recorded | — | — |
| 0016 | missing | not recorded | — | — |
| 0017 | missing | not recorded | — | — |
| 0018 | missing | not recorded | — | — |
| 0019 | missing | not recorded | — | — |
| 0020 | missing | not recorded | — | — |
| 0021 | missing | not recorded | — | — |
| 0022 | missing | not recorded | — | — |
| 0023 | missing | not recorded | — | — |
| 0024 | missing | not recorded | — | — |
| 0025 | missing | not recorded | — | — |
| 0026 | missing | not recorded | — | — |
| 0027 | missing | not recorded | — | — |
| 0028 | missing | not recorded | — | — |
| 0029 | missing | not recorded | — | — |
| 0030 | missing | not recorded | — | — |
| 0031 | missing | not recorded | — | — |
| 0032 | missing | not recorded | — | — |
| 0033 | missing | not recorded | — | — |
| 0034 | missing | not recorded | — | — |
| 0035 | missing | not recorded | — | — |
| 0036 | missing | not recorded | — | — |
| 0037 | missing | not recorded | — | — |
| 0038 | missing | not recorded | — | — |
| 0039 | missing | not recorded | — | — |
| 0040 | missing | not recorded | — | — |
| 0041 | missing | not recorded | — | — |
| 0042 | missing | not recorded | — | — |
| 0043 | missing | not recorded | — | — |
| 0044 | missing | not recorded | — | — |
| 0045 | missing | not recorded | — | — |
| 0046 | missing | not recorded | — | — |
| 0047 | missing | not recorded | — | — |
| 0048 | missing | not recorded | — | — |
| 0049 | missing | not recorded | — | — |
| 0050 | missing | not recorded | — | — |
| 0051 | missing | not recorded | — | — |
| 0052 | missing | not recorded | — | — |
| 0053 | missing | not recorded | — | — |
| 0054 | missing | not recorded | — | — |
| 0055 | missing | not recorded | — | — |
| 0056 | missing | not recorded | — | — |
| 0057 | missing | not recorded | — | — |
| 0058 | missing | not recorded | — | — |
| 0059 | missing | not recorded | — | — |
| 0060 | missing | not recorded | — | — |
| 0061 | missing | not recorded | — | — |
| 0062 | missing | not recorded | — | — |
| 0063 | missing | not recorded | — | — |
| 0064 | missing | not recorded | — | — |
| 0065 | missing | not recorded | — | — |
| 0066 | missing | not recorded | — | — |
| 0067 | missing | not recorded | — | — |
| 0068 | missing | not recorded | — | — |
| 0069 | missing | not recorded | — | — |
| 0070 | missing | not recorded | — | — |
| 0071 | missing | not recorded | — | — |
| 0072 | missing | not recorded | — | — |
| 0073 | missing | not recorded | — | — |
| 0074 | missing | not recorded | — | — |
| 0075 | missing | not recorded | — | — |
| 0076 | missing | not recorded | — | — |
| 0077 | missing | not recorded | — | — |
| 0078 | missing | not recorded | — | — |
| 0079 | missing | not recorded | — | — |
| 0080 | missing | not recorded | — | — |
| 0081 | missing | not recorded | — | — |
| 0082 | missing | not recorded | — | — |
| 0083 | missing | not recorded | — | — |
| 0084 | missing | not recorded | — | — |
| 0085 | missing | not recorded | — | — |
| 0086 | missing | not recorded | — | — |
| 0087 | missing | not recorded | — | — |
| 0088 | missing | not recorded | — | — |
| 0089 | missing | not recorded | — | — |
| 0090 | missing | not recorded | — | — |
| 0091 | missing | not recorded | — | — |
| 0092 | missing | not recorded | — | — |
| 0093 | missing | not recorded | — | — |
| 0094 | missing | not recorded | — | — |
| 0095 | missing | not recorded | — | — |
| 0096 | missing | not recorded | — | — |
| 0097 | missing | not recorded | — | — |
| 0098 | missing | not recorded | — | — |
| 0099 | missing | not recorded | — | — |
| 0100 | missing | not recorded | — | — |
| 0101 | missing | not recorded | — | — |
| 0102 | missing | not recorded | — | — |
| 0103 | missing | not recorded | — | — |
| 0104 | missing | not recorded | — | — |
| 0105 | missing | not recorded | — | — |
| 0106 | missing | not recorded | — | — |
| 0107 | missing | not recorded | — | — |
| 0108 | missing | not recorded | — | — |
| 0109 | missing | not recorded | — | — |
| 0110 | missing | not recorded | — | — |
| 0111 | missing | not recorded | — | — |
| 0112 | missing | not recorded | — | — |
| 0113 | missing | not recorded | — | — |
| 0114 | missing | not recorded | — | — |
| 0115 | missing | not recorded | — | — |
| 0116 | missing | not recorded | — | — |
| 0117 | missing | not recorded | — | — |
| 0118 | missing | not recorded | — | — |
| 0119 | missing | not recorded | — | — |

## Reproduce

See docs/experiments.md for acquisition, audit, sequential execution, and solver-free report commands. Pinned references and source hashes are in experiment.json. Raw records are the authoritative report inputs.
