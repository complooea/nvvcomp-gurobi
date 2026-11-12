# Verification experiment report

Listed: 120; eligible: 120; excluded: 0.
Recorded eligible results: 120; Missing records: 0; corrupt records: 0.
Solver-reported, accepted solves: 3. Outcomes: {'unknown': 117, 'unsat': 1, 'sat': 2}.
Validation: {'none': 118, 'strict': 2}. Unresolved reasons: {'timeout': 117}.

## Interpretation

SAT is accepted only after pinned FLOAT32 ONNX replay. Strict and tolerance-only classifications are separate; tolerance-only SAT does not refute an UNSAT claim. Numerical UNSAT is not an independently certified UNSAT or an exact-real proof. Solver outcomes are not independent ground truth. Filename labels never determine verdicts.

## Timings and resources

Whole-run time includes subprocess startup, reads/decompression, interpretation, encoding, solving, and validation. No startup overhead is subtracted; no kill-grace result gets solve credit. Invocation wall time additionally includes supervising/cleanup overhead. Preparation is a no-op (0 seconds); category eligibility audit is separately measured, not hidden preparation or cached solving analysis.

Runtime seconds: `{'all': {'count': 120, 'sum': 21217.76457855315, 'min': 22.28398908278905, 'median': 180.0162144789938, 'max': 180.01982333301567}, 'solved': {'count': 3, 'sum': 156.06316304183565, 'min': 22.28398908278905, 'median': 60.26639241701923, 'max': 73.51278154202737}}`.
Invocation seconds: `{'count': 120, 'sum': 21217.786657297052, 'min': 22.284187084063888, 'median': 180.0163973539602, 'max': 180.0200067081023}`.
Audit seconds: 1.188444.
Resources: `{'platform': 'macOS-26.6.2-arm64-arm-64bit', 'machine': 'arm64', 'processor': 'arm', 'logical_cpus': 10, 'hw.memsize': '17179869184', 'hw.physicalcpu': '10', 'machdep.cpu.brand_string': 'Apple M4'}`; execution: `{'threads': 1, 'sequential': True, 'preparation_analysis': False}`.
Pinned replay uses 12 intra/inter-op CPU threads separately from the Gurobi Threads limit. No memory cap, performance tuning, or numerical tolerance tuning is applied.

## Architecture and numerical scope

Eligibility uses the verification contract's sequential FLOAT32 affine/ReLU and supported conjunctive/disjunctive property grammar, independently of solve outcomes. Each eligible row's architecture descriptor records the audited operations, hidden widths and ReLU depth, input/output dimensions, parameter count, and output comparison/alternative counts. Original-model groups are source-name groups, not evidence of functional equivalence. Depth comparisons may also vary width and neuron stability; no causal depth effect is inferred.
Gurobi numerical defaults are unchanged; effective settings, package versions, witnesses, and validation diagnostics are retained in individual records. These are floating-point results, not exact-arithmetic certification.

## Competition scoring

Subset score unavailable: Artifact-matched other-tool outcomes and strict witness checks needed to assess conflicts and UNSAT correctness; Complete participating-tool context for category normalization; cross-tool caches do not bind benchmark artifact hashes.
Accepted SAT-only subset contribution: 20 points across 2 instances (10 each under pinned get_score; not the full eligible/category score). Numerical UNSAT contributions remain unassessed without artifact-matched cross-tool strict-witness evidence.
Pinned get_score awards 10 per accepted solve; time bonus disabled. Strict witnesses can refute UNSAT; tolerance-only witnesses earn SAT credit but cannot refute UNSAT. No score inferred from our own verdicts or filenames.
No ABC speed ratio or hardware-independent performance claim is made without matching artifacts and execution resources.

## Per-instance records

Manifest order identifies rows; original names and artifact hashes are in experiment.json and records/<id>.json.

| ID | Outcome | Reason | Validation | Whole-run seconds |
| --- | --- | --- | --- | --- |
| 0000 | unknown | timeout | — | 180.01203208393417 |
| 0001 | unknown | timeout | — | 180.0169420419261 |
| 0002 | unknown | timeout | — | 180.0162879161071 |
| 0003 | unknown | timeout | — | 180.00956525001675 |
| 0004 | unknown | timeout | — | 180.0119787498843 |
| 0005 | unknown | timeout | — | 180.01759241707623 |
| 0006 | unknown | timeout | — | 180.0159585000947 |
| 0007 | unknown | timeout | — | 180.01769404206425 |
| 0008 | unknown | timeout | — | 180.0175594999455 |
| 0009 | unknown | timeout | — | 180.01665175007656 |
| 0010 | unknown | timeout | — | 180.01774862478487 |
| 0011 | unknown | timeout | — | 180.01696308306418 |
| 0012 | unknown | timeout | — | 180.01649366691709 |
| 0013 | unknown | timeout | — | 180.00689691700973 |
| 0014 | unknown | timeout | — | 180.01614104188047 |
| 0015 | unknown | timeout | — | 180.01630983292125 |
| 0016 | unknown | timeout | — | 180.01639374997467 |
| 0017 | unknown | timeout | — | 180.01589041715488 |
| 0018 | unknown | timeout | — | 180.0106278329622 |
| 0019 | unknown | timeout | — | 180.011552833952 |
| 0020 | unknown | timeout | — | 180.01178349996917 |
| 0021 | unknown | timeout | — | 180.00932008307427 |
| 0022 | unknown | timeout | — | 180.01009133295156 |
| 0023 | unknown | timeout | — | 180.00994687504135 |
| 0024 | unknown | timeout | — | 180.00877033290453 |
| 0025 | unknown | timeout | — | 180.014886375051 |
| 0026 | unknown | timeout | — | 180.0167749999091 |
| 0027 | unknown | timeout | — | 180.01796520897187 |
| 0028 | unknown | timeout | — | 180.01060391706415 |
| 0029 | unknown | timeout | — | 180.01753654214554 |
| 0030 | unknown | timeout | — | 180.0163757498376 |
| 0031 | unknown | timeout | — | 180.0179415838793 |
| 0032 | unknown | timeout | — | 180.00893004098907 |
| 0033 | unknown | timeout | — | 180.01734745898284 |
| 0034 | unknown | timeout | — | 180.01094029215164 |
| 0035 | unknown | timeout | — | 180.01705270819366 |
| 0036 | unknown | timeout | — | 180.01028308295645 |
| 0037 | unknown | timeout | — | 180.01368149998598 |
| 0038 | unknown | timeout | — | 180.01686891703866 |
| 0039 | unknown | timeout | — | 180.0170511668548 |
| 0040 | unknown | timeout | — | 180.01351120811887 |
| 0041 | unknown | timeout | — | 180.01574758300558 |
| 0042 | unknown | timeout | — | 180.01669691712596 |
| 0043 | unknown | timeout | — | 180.01693795900792 |
| 0044 | unknown | timeout | — | 180.0167437500786 |
| 0045 | unknown | timeout | — | 180.01672483282164 |
| 0046 | unknown | timeout | — | 180.0164941670373 |
| 0047 | unknown | timeout | — | 180.01486120885238 |
| 0048 | unknown | timeout | — | 180.01484249997884 |
| 0049 | unknown | timeout | — | 180.01547641702928 |
| 0050 | unknown | timeout | — | 180.01823620893992 |
| 0051 | unknown | timeout | — | 180.01068591699004 |
| 0052 | unknown | timeout | — | 180.01112679205835 |
| 0053 | unknown | timeout | — | 180.0136837910395 |
| 0054 | unknown | timeout | — | 180.0165500000585 |
| 0055 | unknown | timeout | — | 180.01663912506774 |
| 0056 | unknown | timeout | — | 180.01640120800585 |
| 0057 | unknown | timeout | — | 180.01654808409512 |
| 0058 | unknown | timeout | — | 180.01655358402058 |
| 0059 | unknown | timeout | — | 180.0167519999668 |
| 0060 | unknown | timeout | — | 180.0174632500857 |
| 0061 | unknown | timeout | — | 180.01291866693646 |
| 0062 | unknown | timeout | — | 180.01686695800163 |
| 0063 | unknown | timeout | — | 180.0172228750307 |
| 0064 | unknown | timeout | — | 180.0155318749603 |
| 0065 | unknown | timeout | — | 180.01171774999239 |
| 0066 | unsat | infeasible | — | 22.28398908278905 |
| 0067 | unknown | timeout | — | 180.01107775000855 |
| 0068 | unknown | timeout | — | 180.0168818330858 |
| 0069 | unknown | timeout | — | 180.01671704207547 |
| 0070 | unknown | timeout | — | 180.0069646248594 |
| 0071 | unknown | timeout | — | 180.0176355841104 |
| 0072 | unknown | timeout | — | 180.0096826250665 |
| 0073 | unknown | timeout | — | 180.01030249986798 |
| 0074 | sat | validated_witness | strict | 60.26639241701923 |
| 0075 | sat | validated_witness | strict | 73.51278154202737 |
| 0076 | unknown | timeout | — | 180.01968104206026 |
| 0077 | unknown | timeout | — | 180.01982333301567 |
| 0078 | unknown | timeout | — | 180.00830429210328 |
| 0079 | unknown | timeout | — | 180.0140559170395 |
| 0080 | unknown | timeout | — | 180.01073400001042 |
| 0081 | unknown | timeout | — | 180.01738958409987 |
| 0082 | unknown | timeout | — | 180.00818508304656 |
| 0083 | unknown | timeout | — | 180.01774416700937 |
| 0084 | unknown | timeout | — | 180.01751533313654 |
| 0085 | unknown | timeout | — | 180.01730974996462 |
| 0086 | unknown | timeout | — | 180.01719912490807 |
| 0087 | unknown | timeout | — | 180.01925929100253 |
| 0088 | unknown | timeout | — | 180.01257504103705 |
| 0089 | unknown | timeout | — | 180.01504174992442 |
| 0090 | unknown | timeout | — | 180.01777520799078 |
| 0091 | unknown | timeout | — | 180.01084587490186 |
| 0092 | unknown | timeout | — | 180.01146245910786 |
| 0093 | unknown | timeout | — | 180.01732583297417 |
| 0094 | unknown | timeout | — | 180.00970970792696 |
| 0095 | unknown | timeout | — | 180.0097540419083 |
| 0096 | unknown | timeout | — | 180.01725466689095 |
| 0097 | unknown | timeout | — | 180.01153575000353 |
| 0098 | unknown | timeout | — | 180.0160380420275 |
| 0099 | unknown | timeout | — | 180.01383104198612 |
| 0100 | unknown | timeout | — | 180.00726937502623 |
| 0101 | unknown | timeout | — | 180.00872899987735 |
| 0102 | unknown | timeout | — | 180.01643475005403 |
| 0103 | unknown | timeout | — | 180.00696366699412 |
| 0104 | unknown | timeout | — | 180.01104420912452 |
| 0105 | unknown | timeout | — | 180.01688537513837 |
| 0106 | unknown | timeout | — | 180.0094767920673 |
| 0107 | unknown | timeout | — | 180.01772954198532 |
| 0108 | unknown | timeout | — | 180.01908733393066 |
| 0109 | unknown | timeout | — | 180.01822337508202 |
| 0110 | unknown | timeout | — | 180.01792545896024 |
| 0111 | unknown | timeout | — | 180.01779549987987 |
| 0112 | unknown | timeout | — | 180.01851062499918 |
| 0113 | unknown | timeout | — | 180.0185662501026 |
| 0114 | unknown | timeout | — | 180.01245799986646 |
| 0115 | unknown | timeout | — | 180.01723925000988 |
| 0116 | unknown | timeout | — | 180.01302270800807 |
| 0117 | unknown | timeout | — | 180.0094819169026 |
| 0118 | unknown | timeout | — | 180.0183251670096 |
| 0119 | unknown | timeout | — | 180.01226837513968 |

## Reproduce

See docs/experiments.md for acquisition, audit, sequential execution, and solver-free report commands. Pinned references and source hashes are in experiment.json. Raw records are the authoritative report inputs.
