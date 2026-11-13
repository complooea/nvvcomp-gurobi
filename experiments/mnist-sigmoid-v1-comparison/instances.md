# Per-instance comparison evidence

All comparisons are conditional where execution artifact binding is unavailable. Ratios are ABC/Gurobi measured time, not hardware-normalized speedups. W labels group structural descriptors only, not weights or properties.

| ID | Network | Inputs | Hidden widths | Elements | Width group | Match | Gurobi (validation) | ABC (validation) | Gurobi run s | ABC run s | ABC prep s | Comparison | ABC/G run |
| --- | --- | ---: | --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | --- | ---: |
| 0000 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 109.3683935829904 | 6.04583116 | 19.445575865 | both_same_answer | 0.05527950957250123 |
| 0001 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | sat (strict) | 300.0174386249855 | 6.56815962 | 19.254377952 | abc_only | None |
| 0002 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 90.25075370911509 | 6.043347582 | 19.194028 | both_same_answer | 0.06696174085679284 |
| 0003 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 203.7485520830378 | 6.039239047 | 19.281070637 | both_same_answer | 0.029640647677038244 |
| 0004 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.01662108302116 | 7.856662937 | 19.238173059 | abc_only | None |
| 0005 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 107.8572415409144 | 6.029835112 | 19.236897689 | both_same_answer | 0.05590570485443624 |
| 0006 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 55.356394374975935 | 6.040190146 | 19.268884876 | both_same_answer | 0.10911458764970593 |
| 0007 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 224.81010358291678 | 6.318873915 | 19.250526837 | both_same_answer | 0.02810760643891349 |
| 0008 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 128.31549679208547 | 6.054257937 | 19.261756644 | both_same_answer | 0.047182593594364886 |
| 0009 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 114.38961604214273 | 6.040355405 | 19.254966356 | both_same_answer | 0.05280510254335191 |
| 0010 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 70.06191937508993 | 6.039395981 | 19.2601435 | both_same_answer | 0.0862008354162685 |
| 0011 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | sat (strict) | 300.0175339579582 | 6.513876643 | 19.255630844 | abc_only | None |
| 0012 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 100.89522929210216 | 6.066665396 | 19.223778085 | both_same_answer | 0.060128367203927696 |
| 0013 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 125.17522079101764 | 6.467497831 | 19.25786373 | both_same_answer | 0.05166755680661118 |
| 0014 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 122.4765872079879 | 6.050118961 | 19.297187667 | both_same_answer | 0.04939816742873296 |
| 0015 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 235.89853312494233 | 6.050409181 | 19.21228904 | both_same_answer | 0.025648354404117616 |
| 0016 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.0172054581344 | 7.796757085 | 19.230652705 | abc_only | None |
| 0017 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.0169024579227 | 6.035023778 | 19.223414752 | abc_only | None |
| 0018 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 67.08671787497588 | 6.058983333 | 19.238867479 | both_same_answer | 0.09031569176318388 |
| 0019 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 144.47033412498422 | 6.037754606 | 19.25470649 | both_same_answer | 0.04179234887611332 |
| 0020 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.0171240409836 | 6.046940617 | 19.245853636 | abc_only | None |
| 0021 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.01749462494627 | 6.321707134 | 19.245783128 | abc_only | None |
| 0022 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 171.62328220903873 | 6.037419509 | 19.286438483 | both_same_answer | 0.03517832447491808 |
| 0023 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.010038041044 | 8.28263073 | 19.264089248 | abc_only | None |
| 0024 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.01731979101896 | 6.036341651 | 19.183832731 | abc_only | None |
| 0025 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 25.600724500138313 | 6.449240929 | 19.269606024 | both_same_answer | 0.2519163443583465 |
| 0026 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 117.78190937498584 | 6.043858552 | 19.282645383 | both_same_answer | 0.051313980084649366 |
| 0027 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 124.78237529098988 | 6.052578496 | 19.25274354 | both_same_answer | 0.04850507519099163 |
| 0028 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 235.4408987921197 | 6.044328007 | 19.254119233 | both_same_answer | 0.025672379089653332 |
| 0029 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 123.87437683297321 | 6.045083226 | 19.230034592 | both_same_answer | 0.04880011008370945 |
| 0030 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 58.030665666097775 | 6.038791925 | 19.239792017 | both_same_answer | 0.10406208261932684 |
| 0031 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.0165992078837 | 8.694268997 | 19.274204648 | abc_only | None |
| 0032 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.00987704191357 | 7.8385752 | 19.202669285 | abc_only | None |
| 0033 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 115.93571170908399 | 6.04324384 | 19.204792038 | both_same_answer | 0.05212581827387436 |
| 0034 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 45.945866875117645 | 6.034317716 | 19.262891466 | both_same_answer | 0.13133537631146391 |
| 0035 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 139.44080695789307 | 6.054491373 | 19.269086385 | both_same_answer | 0.0434197958623997 |
| 0036 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 180.19018699997105 | 6.043360256 | 19.25436652 | both_same_answer | 0.03353878674869776 |
| 0037 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 71.67122370796278 | 6.055348372 | 19.23362114 | both_same_answer | 0.08448786079994391 |
| 0038 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 172.26113625010476 | 6.458619762 | 19.269888217 | both_same_answer | 0.03749319145685173 |
| 0039 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 102.04538883408532 | 6.082025243 | 19.215720174 | both_same_answer | 0.0596011766184625 |
| 0040 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 52.971824208972976 | 6.048546989 | 19.247236585 | both_same_answer | 0.11418423056639661 |
| 0041 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 91.24599900003523 | 6.04689525 | 19.233528158 | both_same_answer | 0.0662702509290042 |
| 0042 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.0172819159925 | 6.059348738 | 19.282261592 | abc_only | None |
| 0043 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 282.4656004579738 | 6.443671738 | 19.215528358 | both_same_answer | 0.02281223528653611 |
| 0044 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.01708966703154 | 8.238316652 | 19.230646263 | abc_only | None |
| 0045 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.0134409170132 | 7.876847573 | 19.19186659 | abc_only | None |
| 0046 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 114.15689616603777 | 6.041145084 | 19.211019289 | both_same_answer | 0.05291966834148448 |
| 0047 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 123.90792370820418 | 6.058090092 | 19.265198092 | both_same_answer | 0.048891869952291694 |
| 0048 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 255.70084641687572 | 6.38713112 | 19.284522733 | both_same_answer | 0.02497892052178386 |
| 0049 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 84.95508545800112 | 6.04705581 | 19.262970047 | both_same_answer | 0.07117944473129224 |
| 0050 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.01296108285896 | 7.840135692 | 19.225743487 | abc_only | None |
| 0051 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 99.02213258389384 | 6.048118879 | 19.210940319 | both_same_answer | 0.06107845510069068 |
| 0052 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 127.5390049580019 | 6.047673249 | 19.245594627 | both_same_answer | 0.047418225122514285 |
| 0053 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 68.96148395887576 | 6.046508305 | 19.300496739 | both_same_answer | 0.08767949814719406 |
| 0054 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.0170257501304 | 6.453163574 | 19.24773492 | abc_only | None |
| 0055 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 102.15751308319159 | 6.530542163 | 19.25750225 | both_same_answer | 0.06392620538522582 |
| 0056 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.01734787481837 | 7.856299926 | 19.270844257 | abc_only | None |
| 0057 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.01676058303565 | 9.829466931 | 19.221848757 | abc_only | None |
| 0058 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.017390916124 | 9.171039344 | 19.219026502 | abc_only | None |
| 0059 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 129.6258408341091 | 6.463669932 | 19.223150919 | both_same_answer | 0.04986405403743527 |
| 0060 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 147.11261170799844 | 6.065235046 | 19.260357116 | both_same_answer | 0.04122851858574023 |
| 0061 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.0084322919138 | 9.129472457 | 19.272564323 | abc_only | None |
| 0062 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.0173691669479 | 6.048613095 | 19.208232129 | abc_only | None |
| 0063 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.014147750102 | 12.566627631 | 19.244109817 | abc_only | None |
| 0064 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 155.88973929197527 | 6.0499841 | 19.216275009 | both_same_answer | 0.03880937980573962 |
| 0065 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 40.949168500024825 | 6.057552162 | 19.310937257 | both_same_answer | 0.1479285754482738 |
| 0066 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.01306350016966 | 7.875394574 | 19.257763534 | abc_only | None |
| 0067 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 102.04453483293764 | 6.048903944 | 19.237921038 | both_same_answer | 0.05927709851294802 |
| 0068 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | sat (strict) | sat (strict) | 171.75710504106246 | 6.537439926 | 19.259004443 | both_same_answer | 0.03806212223032681 |
| 0069 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 292.5636682920158 | 6.035583686 | 19.261890567 | both_same_answer | 0.020629983624541236 |
| 0070 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 110.66533870785497 | 6.039818149 | 19.272706237 | both_same_answer | 0.054577324928670706 |
| 0071 | mnist_concat.onnx | 792 | [200, 784, 32, 32] | 342696 | — | source_verified_execution_unbound | unknown (—) | unsat (—) | 300.0173957920633 | 6.040084857 | 19.243557284 | abc_only | None |

## Unmatched published rows

```json
[
  {
    "row": 73,
    "category": "inconsistent_paths",
    "version": "1.0",
    "network": "onnx/test_nano.onnx",
    "property": "vnnlib/test_nano.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 5.809495982,
    "preparation_seconds": 19.215396553,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  }
]
```
