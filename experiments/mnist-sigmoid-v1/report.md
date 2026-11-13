# Verification experiment report

Listed: 72; eligible: 72; excluded: 0.
Recorded eligible results: 72; Missing records: 0; corrupt records: 0.
Solver-reported, accepted solves: 48. Outcomes: {'unsat': 42, 'unknown': 24, 'sat': 6}.
Validation: {'none': 66, 'strict': 6}. Unresolved reasons: {'timeout': 24}.

## Interpretation

SAT is accepted only after pinned FLOAT32 ONNX replay. Strict and tolerance-only classifications are separate; tolerance-only SAT does not refute an UNSAT claim. Numerical UNSAT is not an independently certified UNSAT or an exact-real proof. Solver outcomes are not independent ground truth. Filename labels never determine verdicts.

## Timings and resources

Whole-run time includes subprocess startup, reads/decompression, interpretation, encoding, solving, and validation. No startup overhead is subtracted; no kill-grace result gets solve credit. Invocation wall time additionally includes supervising/cleanup overhead. Preparation is a no-op (0 seconds); category eligibility audit is separately measured, not hidden preparation or cached solving analysis.

Runtime seconds: `{'all': {'count': 72, 'sum': 13338.851826245897, 'min': 25.600724500138313, 'median': 151.50117549998686, 'max': 300.0175339579582}, 'solved': {'count': 48, 'sum': 6138.477964707883, 'min': 25.600724500138313, 'median': 116.85881054203492, 'max': 292.5636682920158}}`.
Invocation seconds: `{'count': 72, 'sum': 13338.866093212739, 'min': 25.600935416063294, 'median': 151.50137300009374, 'max': 300.0177164999768}`.
Audit seconds: 0.587224.
Resources: `{'platform': 'macOS-26.6.2-arm64-arm-64bit', 'machine': 'arm64', 'processor': 'arm', 'logical_cpus': 10, 'hw.memsize': '17179869184', 'hw.physicalcpu': '10', 'machdep.cpu.brand_string': 'Apple M4'}`; execution: `{'threads': 1, 'sequential': True, 'preparation_analysis': False}`.
Pinned replay uses 12 intra/inter-op CPU threads separately from the Gurobi Threads limit. No memory cap, performance tuning, or numerical tolerance tuning is applied.

## Architecture and numerical scope

Eligibility uses the verification contract's sequential FLOAT32 affine/ReLU/sigmoid/constant-reshape and supported conjunctive/disjunctive property grammar, independently of solve outcomes. Each eligible row's architecture descriptor records the actual formulation, tensor shapes, audited operations, hidden widths and ReLU depth, input/output dimensions, initializer count, and output comparison/alternative counts. Original-model groups are source-name groups, not evidence of functional equivalence. Depth comparisons may also vary width and neuron stability; no causal depth effect is inferred.
Gurobi numerical defaults are unchanged; effective settings, package versions, witnesses, and validation diagnostics are retained in individual records. These are floating-point results, not exact-arithmetic certification.

## Competition scoring

Subset score unavailable: Artifact-matched other-tool outcomes and strict witness checks needed to assess conflicts and UNSAT correctness; Complete participating-tool context for category normalization; cross-tool caches do not bind benchmark artifact hashes.
Accepted SAT-only subset contribution: 60 points across 6 instances (10 each under pinned get_score; not the full eligible/category score). Numerical UNSAT contributions remain unassessed without artifact-matched cross-tool strict-witness evidence.
Pinned get_score awards 10 per accepted solve; time bonus disabled. Strict witnesses can refute UNSAT; tolerance-only witnesses earn SAT credit but cannot refute UNSAT. No score inferred from our own verdicts or filenames.
No ABC speed ratio or hardware-independent performance claim is made without matching artifacts and execution resources.

## Per-instance records

Manifest order identifies rows; original names and artifact hashes are in experiment.json and records/<id>.json.

| ID | Outcome | Reason | Validation | Whole-run seconds |
| --- | --- | --- | --- | --- |
| 0000 | unsat | infeasible | — | 109.3683935829904 |
| 0001 | unknown | timeout | — | 300.0174386249855 |
| 0002 | unsat | infeasible | — | 90.25075370911509 |
| 0003 | unsat | infeasible | — | 203.7485520830378 |
| 0004 | unknown | timeout | — | 300.01662108302116 |
| 0005 | unsat | infeasible | — | 107.8572415409144 |
| 0006 | unsat | infeasible | — | 55.356394374975935 |
| 0007 | unsat | infeasible | — | 224.81010358291678 |
| 0008 | unsat | infeasible | — | 128.31549679208547 |
| 0009 | unsat | infeasible | — | 114.38961604214273 |
| 0010 | unsat | infeasible | — | 70.06191937508993 |
| 0011 | unknown | timeout | — | 300.0175339579582 |
| 0012 | unsat | infeasible | — | 100.89522929210216 |
| 0013 | sat | validated_witness | strict | 125.17522079101764 |
| 0014 | unsat | infeasible | — | 122.4765872079879 |
| 0015 | unsat | infeasible | — | 235.89853312494233 |
| 0016 | unknown | timeout | — | 300.0172054581344 |
| 0017 | unknown | timeout | — | 300.0169024579227 |
| 0018 | unsat | infeasible | — | 67.08671787497588 |
| 0019 | unsat | infeasible | — | 144.47033412498422 |
| 0020 | unknown | timeout | — | 300.0171240409836 |
| 0021 | unknown | timeout | — | 300.01749462494627 |
| 0022 | unsat | infeasible | — | 171.62328220903873 |
| 0023 | unknown | timeout | — | 300.010038041044 |
| 0024 | unknown | timeout | — | 300.01731979101896 |
| 0025 | sat | validated_witness | strict | 25.600724500138313 |
| 0026 | unsat | infeasible | — | 117.78190937498584 |
| 0027 | unsat | infeasible | — | 124.78237529098988 |
| 0028 | unsat | infeasible | — | 235.4408987921197 |
| 0029 | unsat | infeasible | — | 123.87437683297321 |
| 0030 | unsat | infeasible | — | 58.030665666097775 |
| 0031 | unknown | timeout | — | 300.0165992078837 |
| 0032 | unknown | timeout | — | 300.00987704191357 |
| 0033 | unsat | infeasible | — | 115.93571170908399 |
| 0034 | unsat | infeasible | — | 45.945866875117645 |
| 0035 | unsat | infeasible | — | 139.44080695789307 |
| 0036 | unsat | infeasible | — | 180.19018699997105 |
| 0037 | unsat | infeasible | — | 71.67122370796278 |
| 0038 | sat | validated_witness | strict | 172.26113625010476 |
| 0039 | unsat | infeasible | — | 102.04538883408532 |
| 0040 | unsat | infeasible | — | 52.971824208972976 |
| 0041 | unsat | infeasible | — | 91.24599900003523 |
| 0042 | unknown | timeout | — | 300.0172819159925 |
| 0043 | sat | validated_witness | strict | 282.4656004579738 |
| 0044 | unknown | timeout | — | 300.01708966703154 |
| 0045 | unknown | timeout | — | 300.0134409170132 |
| 0046 | unsat | infeasible | — | 114.15689616603777 |
| 0047 | unsat | infeasible | — | 123.90792370820418 |
| 0048 | unsat | infeasible | — | 255.70084641687572 |
| 0049 | unsat | infeasible | — | 84.95508545800112 |
| 0050 | unknown | timeout | — | 300.01296108285896 |
| 0051 | unsat | infeasible | — | 99.02213258389384 |
| 0052 | unsat | infeasible | — | 127.5390049580019 |
| 0053 | unsat | infeasible | — | 68.96148395887576 |
| 0054 | unknown | timeout | — | 300.0170257501304 |
| 0055 | sat | validated_witness | strict | 102.15751308319159 |
| 0056 | unknown | timeout | — | 300.01734787481837 |
| 0057 | unknown | timeout | — | 300.01676058303565 |
| 0058 | unknown | timeout | — | 300.017390916124 |
| 0059 | unsat | infeasible | — | 129.6258408341091 |
| 0060 | unsat | infeasible | — | 147.11261170799844 |
| 0061 | unknown | timeout | — | 300.0084322919138 |
| 0062 | unknown | timeout | — | 300.0173691669479 |
| 0063 | unknown | timeout | — | 300.014147750102 |
| 0064 | unsat | infeasible | — | 155.88973929197527 |
| 0065 | unsat | infeasible | — | 40.949168500024825 |
| 0066 | unknown | timeout | — | 300.01306350016966 |
| 0067 | unsat | infeasible | — | 102.04453483293764 |
| 0068 | sat | validated_witness | strict | 171.75710504106246 |
| 0069 | unsat | infeasible | — | 292.5636682920158 |
| 0070 | unsat | infeasible | — | 110.66533870785497 |
| 0071 | unknown | timeout | — | 300.0173957920633 |

## Reproduce

See docs/experiments.md for acquisition, audit, sequential execution, and solver-free report commands. Pinned references and source hashes are in experiment.json. Raw records are the authoritative report inputs.
