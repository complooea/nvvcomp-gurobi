# SAT ReLU V1 experiment report

Listed: 100; eligible: 100; excluded: 0.
Recorded eligible results: 100; Missing records: 0; corrupt records: 0.
Solver-reported, accepted solves: 83. Outcomes: {'sat': 50, 'unsat': 33, 'unknown': 17}.
Validation: {'strict': 50, 'none': 50}. Unresolved reasons: {'timeout': 17}.

## Interpretation

SAT is accepted only after pinned FLOAT32 ONNX replay. Strict and tolerance-only classifications are separate; tolerance-only SAT does not refute an UNSAT claim. Numerical UNSAT is not an independently certified UNSAT or an exact-real proof. Solver outcomes are not independent ground truth. Filename labels never determine verdicts.

## Timings and resources

Whole-run time includes subprocess startup, reads/decompression, interpretation, encoding, solving, and validation. No startup overhead is subtracted; no kill-grace result gets solve credit. Invocation wall time additionally includes supervising/cleanup overhead. Preparation is a no-op (0 seconds); category eligibility audit is separately measured, not hidden preparation or cached solving analysis.

Runtime seconds: `{'all': {'count': 100, 'sum': 1769.4100494189188, 'min': 0.1951379580423236, 'median': 0.8744456875137985, 'max': 100.01528854086064}, 'solved': {'count': 83, 'sum': 69.19981846422888, 'min': 0.1951379580423236, 'median': 0.8239486671518534, 'max': 1.9551102500408888}}`.
Invocation seconds: `{'count': 100, 'sum': 1769.4249412054196, 'min': 0.19519870821386576, 'median': 0.8746254375437275, 'max': 100.01546137500554}`.
Audit seconds: 0.068048.
Resources: `{'platform': 'macOS-26.6.2-arm64-arm-64bit', 'machine': 'arm64', 'processor': 'arm', 'logical_cpus': 10, 'hw.memsize': '17179869184', 'hw.physicalcpu': '10', 'machdep.cpu.brand_string': 'Apple M4'}`; execution: `{'threads': 1, 'sequential': True, 'preparation_analysis': False}`.
Pinned replay uses 12 intra/inter-op CPU threads separately from the Gurobi Threads limit. No memory cap, performance tuning, or numerical tolerance tuning is applied.

## Architecture and numerical scope

The pinned category has one hidden ReLU layer between two Gemm operations, two outputs, 5–95 inputs, hidden widths 29–1,071, and 234–100,676 stored weight/bias elements. This is width variation, not depth or architectural diversity. Eligibility uses the verification contract's sequential FLOAT32 affine/ReLU and conjunctive property grammar, independently of solve outcomes.
Gurobi numerical defaults are unchanged; effective settings, package versions, witnesses, and validation diagnostics are retained in individual records. These are floating-point results, not exact-arithmetic certification.

## Competition scoring

Subset score unavailable: Artifact-matched other-tool outcomes and strict witness checks needed to assess conflicts and UNSAT correctness; Complete participating-tool context for category normalization; cross-tool caches do not bind benchmark artifact hashes.
Accepted SAT-only subset contribution: 500 points across 50 instances (10 each under pinned get_score; not the full eligible/category score). Numerical UNSAT contributions remain unassessed without artifact-matched cross-tool strict-witness evidence.
Pinned get_score awards 10 per accepted solve; time bonus disabled. Strict witnesses can refute UNSAT; tolerance-only witnesses earn SAT credit but cannot refute UNSAT. No score inferred from our own verdicts or filenames.
No ABC speed ratio or hardware-independent performance claim is made without matching artifacts and execution resources.

## Per-instance records

Manifest order identifies rows; original names and artifact hashes are in experiment.json and records/<id>.json.

| ID | Outcome | Reason | Validation | Whole-run seconds |
| --- | --- | --- | --- | --- |
| 0000 | sat | validated_witness | strict | 0.20545829110778868 |
| 0001 | unsat | infeasible | — | 0.4506156670395285 |
| 0002 | sat | validated_witness | strict | 0.25794862513430417 |
| 0003 | unknown | timeout | — | 100.00558524997905 |
| 0004 | sat | validated_witness | strict | 0.1951379580423236 |
| 0005 | unsat | infeasible | — | 0.21067679091356695 |
| 0006 | sat | validated_witness | strict | 0.21100254193879664 |
| 0007 | unsat | infeasible | — | 0.3305969589855522 |
| 0008 | sat | validated_witness | strict | 0.20187683287076652 |
| 0009 | unsat | infeasible | — | 0.21015229099430144 |
| 0010 | sat | validated_witness | strict | 0.21084720781072974 |
| 0011 | unsat | infeasible | — | 0.3305389580782503 |
| 0012 | sat | validated_witness | strict | 0.2108790830243379 |
| 0013 | unknown | timeout | — | 100.00829637493007 |
| 0014 | sat | validated_witness | strict | 0.21064429194666445 |
| 0015 | unsat | infeasible | — | 0.3305246669333428 |
| 0016 | sat | validated_witness | strict | 0.21076954109594226 |
| 0017 | unknown | timeout | — | 100.01190445804968 |
| 0018 | sat | validated_witness | strict | 0.210003666812554 |
| 0019 | unsat | infeasible | — | 0.39080229215323925 |
| 0020 | sat | validated_witness | strict | 0.2661294168792665 |
| 0021 | unsat | infeasible | — | 0.39066995889879763 |
| 0022 | sat | validated_witness | strict | 0.2694840421900153 |
| 0023 | unknown | timeout | — | 100.01494395802729 |
| 0024 | sat | validated_witness | strict | 0.8844043749850243 |
| 0025 | unknown | timeout | — | 100.01506695896387 |
| 0026 | sat | validated_witness | strict | 0.9937092498876154 |
| 0027 | unknown | timeout | — | 100.01528854086064 |
| 0028 | sat | validated_witness | strict | 0.8145923749543726 |
| 0029 | unsat | infeasible | — | 0.8143749588634819 |
| 0030 | sat | validated_witness | strict | 0.8699433750007302 |
| 0031 | unknown | timeout | — | 100.01479241601191 |
| 0032 | sat | validated_witness | strict | 0.8086946250405163 |
| 0033 | unsat | infeasible | — | 1.1146073339041322 |
| 0034 | sat | validated_witness | strict | 0.8173150410875678 |
| 0035 | unsat | infeasible | — | 1.2346561250742525 |
| 0036 | sat | validated_witness | strict | 0.877855374943465 |
| 0037 | unknown | timeout | — | 100.01178508298472 |
| 0038 | sat | validated_witness | strict | 0.8089112921152264 |
| 0039 | unsat | infeasible | — | 1.054581540869549 |
| 0040 | sat | validated_witness | strict | 0.8733297500293702 |
| 0041 | unsat | infeasible | — | 1.6548837500158697 |
| 0042 | sat | validated_witness | strict | 0.8052877921145409 |
| 0043 | unsat | infeasible | — | 1.0526067081373185 |
| 0044 | sat | validated_witness | strict | 0.8236637499649078 |
| 0045 | unsat | infeasible | — | 1.1660140841268003 |
| 0046 | sat | validated_witness | strict | 0.9259407920762897 |
| 0047 | unknown | timeout | — | 100.01445154100657 |
| 0048 | sat | validated_witness | strict | 0.9846662501804531 |
| 0049 | unknown | timeout | — | 100.01514924992807 |
| 0050 | sat | validated_witness | strict | 0.8079962080810219 |
| 0051 | unsat | infeasible | — | 1.414618375012651 |
| 0052 | sat | validated_witness | strict | 0.8687017909251153 |
| 0053 | unknown | timeout | — | 100.01489900005981 |
| 0054 | sat | validated_witness | strict | 0.8166332500986755 |
| 0055 | unsat | infeasible | — | 1.1661374168470502 |
| 0056 | sat | validated_witness | strict | 0.8191042090766132 |
| 0057 | unsat | infeasible | — | 1.1146048340015113 |
| 0058 | sat | validated_witness | strict | 0.8171902089379728 |
| 0059 | unsat | infeasible | — | 1.2348195409867913 |
| 0060 | sat | validated_witness | strict | 0.8792170418892056 |
| 0061 | unsat | infeasible | — | 1.2320986669510603 |
| 0062 | sat | validated_witness | strict | 0.8734200419858098 |
| 0063 | unknown | timeout | — | 100.00818595802411 |
| 0064 | sat | validated_witness | strict | 0.8838967920746654 |
| 0065 | unsat | infeasible | — | 1.5943094580434263 |
| 0066 | sat | validated_witness | strict | 0.8754713330417871 |
| 0067 | unsat | infeasible | — | 1.3487206248100847 |
| 0068 | sat | validated_witness | strict | 0.8756479169242084 |
| 0069 | unknown | timeout | — | 100.01481879106723 |
| 0070 | sat | validated_witness | strict | 0.8714975002221763 |
| 0071 | unknown | timeout | — | 100.01486770785414 |
| 0072 | sat | validated_witness | strict | 0.8136694999411702 |
| 0073 | unsat | infeasible | — | 1.1684521248098463 |
| 0074 | sat | validated_witness | strict | 0.8239486671518534 |
| 0075 | unsat | infeasible | — | 1.2720655829180032 |
| 0076 | sat | validated_witness | strict | 0.8701772089116275 |
| 0077 | unsat | infeasible | — | 1.589340167120099 |
| 0078 | sat | validated_witness | strict | 0.9270576250273734 |
| 0079 | unknown | timeout | — | 100.01436991686933 |
| 0080 | sat | validated_witness | strict | 0.7989095838274807 |
| 0081 | unsat | infeasible | — | 0.6945963338948786 |
| 0082 | sat | validated_witness | strict | 0.8104707500897348 |
| 0083 | unsat | infeasible | — | 0.7542498749680817 |
| 0084 | sat | validated_witness | strict | 0.8202805831097066 |
| 0085 | unsat | infeasible | — | 1.6433061668649316 |
| 0086 | sat | validated_witness | strict | 0.8765700419899076 |
| 0087 | unsat | infeasible | — | 1.3515045421663672 |
| 0088 | sat | validated_witness | strict | 0.8041267078369856 |
| 0089 | unknown | timeout | — | 100.00661216606386 |
| 0090 | sat | validated_witness | strict | 0.8178515830077231 |
| 0091 | unsat | infeasible | — | 1.4662345829419792 |
| 0092 | sat | validated_witness | strict | 0.9278835000004619 |
| 0093 | unsat | infeasible | — | 1.5343895840924233 |
| 0094 | sat | validated_witness | strict | 0.8650269161444157 |
| 0095 | unknown | timeout | — | 100.00921358400956 |
| 0096 | sat | validated_witness | strict | 0.8731865000445396 |
| 0097 | unsat | infeasible | — | 1.9551102500408888 |
| 0098 | sat | validated_witness | strict | 0.8132524171378464 |
| 0099 | unsat | infeasible | — | 0.7492748340591788 |

## Reproduce

See docs/experiments.md for acquisition, audit, sequential execution, and solver-free report commands. Pinned references and source hashes are in experiment.json. Raw records are the authoritative report inputs.
