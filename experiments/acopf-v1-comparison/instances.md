# Per-instance comparison evidence

All comparisons are conditional where execution artifact binding is unavailable. Ratios are ABC/Gurobi measured time, not hardware-normalized speedups. W labels group structural descriptors only, not weights or properties.

| ID | Network | Inputs | Hidden widths | Elements | Width group | Match | Gurobi (validation) | ABC (validation) | Gurobi run s | ABC run s | ABC prep s | Comparison | ABC/G run |
| --- | --- | ---: | --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | --- | ---: |
| 0000 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.14026904106140137 | 7.856594821 | 20.923695592 | both_same_answer | 56.010897070016 |
| 0001 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.26976204104721546 | 7.786240561 | 19.410763163 | both_same_answer | 28.863366138444967 |
| 0002 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.26848908397369087 | 7.85624464 | 19.384077451 | both_same_answer | 29.26094619463125 |
| 0003 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.14163708314299583 | 7.789269688 | 19.399243285 | both_same_answer | 54.9945643835097 |
| 0004 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.1503490840550512 | 7.712828834 | 19.408319736 | both_same_answer | 51.29947337208853 |
| 0005 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.14742162497714162 | 7.792860494 | 19.404003594 | both_same_answer | 52.86104053735887 |
| 0006 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.14333000010810792 | 7.821793356 | 19.396861641 | both_same_answer | 54.571920394197605 |
| 0007 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.15032975003123283 | 7.783760477 | 19.421875595 | both_same_answer | 51.77791139400438 |
| 0008 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.15038383402861655 | 7.784515062 | 19.374815062 | both_same_answer | 51.764307728174316 |
| 0009 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.3224193751811981 | 7.808368088 | 19.386315647 | both_same_answer | 24.21804856985327 |
| 0010 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unknown (invalid) | unsat (—) | 0.2650304581038654 | 8.029991616 | 19.401580151 | abc_only | None |
| 0011 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.15046704094856977 | 7.800394806 | 19.401177175 | both_same_answer | 51.841218893021264 |
| 0012 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.15028908313252032 | 7.799210904 | 19.418756841 | both_same_answer | 51.89472675884844 |
| 0013 | 14_ieee_ml4acopf.onnx | 22 | [32, 32, 32, 38] | 4150 | — | source_verified_execution_unbound | unsat (—) | unsat (—) | 0.14732541586272418 | 7.785914656 | 19.367899858 | both_same_answer | 52.84841458214385 |

## Unmatched published rows

```json
[
  {
    "row": 1,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop9.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 8.131918704,
    "preparation_seconds": 21.538719897,
    "artifact_sha256": {
      "vnnlib": "2dde4d75239c1404e113d7e6600c4f6daaea0f177cd4f6b3a7419ee71d216b4b"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 2,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop7.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.986316913,
    "preparation_seconds": 19.529136517,
    "artifact_sha256": {
      "vnnlib": "41bd1a6e235b0e409396014a80621c82799678abfacbea819f6f50a0a3494cea"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 3,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop2.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 8.069524669,
    "preparation_seconds": 19.421880866,
    "artifact_sha256": {
      "vnnlib": "8010bc224a98b75e1f5c304c702dbf998561f606754b3f1fd25bf3a00b924a4f"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 4,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop8.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.999753715,
    "preparation_seconds": 19.407906693,
    "artifact_sha256": {
      "vnnlib": "d7e077e7401d0699d7a1751faf7f9443adb413592756cffb8bc74873b820f7c5"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 5,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop4.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.80884309,
    "preparation_seconds": 19.446593346,
    "artifact_sha256": {
      "vnnlib": "6820056ac173bbe93a4676ee54edfeb4efe949e5e2b28a9aa7ab30f96f015eaf"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 6,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop6.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.996646957,
    "preparation_seconds": 19.396777818,
    "artifact_sha256": {
      "vnnlib": "4464b1c6d6bf7966fa665637f261c00c9ac18445b60549167e1f77e70d7fd702"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 7,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop12.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 8.013907894,
    "preparation_seconds": 19.44172292,
    "artifact_sha256": {
      "vnnlib": "c27b5031c89c34346e806dd193feb435e6561f02a71b78d4152adce36c934199"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 8,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop13.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 8.001773975,
    "preparation_seconds": 19.449473413,
    "artifact_sha256": {
      "vnnlib": "52d52a433504c3f7e9901d7b7bc8c97158d24da3546c27a3ab25601d331b2630"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 9,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop11.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 8.035316189,
    "preparation_seconds": 19.414925901,
    "artifact_sha256": {
      "vnnlib": "eee92efd8c12f9fd2fd848b30556891da5587dd380d940ad3ffbf790c3d8171f"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 10,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop1.vnnlib",
    "outcome": "sat",
    "raw_outcome": "sat",
    "validation": "strict",
    "check_status": "published_cache_row_and_witness_verified_execution_unbound",
    "run_seconds": 6.004792589,
    "preparation_seconds": 19.390508017,
    "artifact_sha256": {
      "vnnlib": "da6545188374ed1117b38cbe2db0cfa51a9f3ba7491a5ab0737ae4a2441b7cfc"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 11,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop3.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.982248279,
    "preparation_seconds": 19.396966645,
    "artifact_sha256": {
      "vnnlib": "db7d7f1b9b1a48e035622ffc3038164b60555ee3406c6c0eb3e8ce3aed82e747"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 12,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop14.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 8.022623199,
    "preparation_seconds": 19.406901182,
    "artifact_sha256": {
      "vnnlib": "ef72bf773659efef496be8ff92526a04f11e1b144633ca19f608394e180ce443"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 13,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop10.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.996385079,
    "preparation_seconds": 19.419857724,
    "artifact_sha256": {
      "vnnlib": "5e7440450540fd3ca2853ed1c1a1a4e0f726db8aba36b039fa1859e29ce96e0d"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 14,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/14_ieee_prop5.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 8.029582291,
    "preparation_seconds": 19.387276491,
    "artifact_sha256": {
      "vnnlib": "ad92e595d0e603f449ee47ce285bbacaaff8893078da47f36af792813ac7fb7f"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 15,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf.onnx",
    "property": "vnnlib/118_ieee_prop2.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 105.509718394,
    "preparation_seconds": 21.132091634,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 16,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf.onnx",
    "property": "vnnlib/118_ieee_prop4.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 9.618825788,
    "preparation_seconds": 19.720577913,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 17,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf.onnx",
    "property": "vnnlib/118_ieee_prop3.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 23.460834998,
    "preparation_seconds": 19.494861726,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 18,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf.onnx",
    "property": "vnnlib/118_ieee_prop5.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.931145067,
    "preparation_seconds": 19.525217551,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 19,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf.onnx",
    "property": "vnnlib/118_ieee_prop6.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.944183497,
    "preparation_seconds": 19.39806613,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 20,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/300_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/300_ieee_prop3.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 75.216856226,
    "preparation_seconds": 22.676247362,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 21,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/300_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/300_ieee_prop105.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.770772552,
    "preparation_seconds": 19.504150284,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 22,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/300_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/300_ieee_prop2.vnnlib",
    "outcome": "sat",
    "raw_outcome": "sat",
    "validation": "strict",
    "check_status": "published_cache_row_and_witness_verified_execution_unbound",
    "run_seconds": 6.134151062,
    "preparation_seconds": 19.402097494,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 23,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/300_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/300_ieee_prop4.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 276.376908524,
    "preparation_seconds": 20.510802549,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 24,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop9.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.585142782,
    "preparation_seconds": 21.042569161,
    "artifact_sha256": {
      "vnnlib": "2dde4d75239c1404e113d7e6600c4f6daaea0f177cd4f6b3a7419ee71d216b4b"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 25,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop7.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.558575013,
    "preparation_seconds": 19.396026768,
    "artifact_sha256": {
      "vnnlib": "41bd1a6e235b0e409396014a80621c82799678abfacbea819f6f50a0a3494cea"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 26,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop2.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.594456208,
    "preparation_seconds": 19.398375029,
    "artifact_sha256": {
      "vnnlib": "8010bc224a98b75e1f5c304c702dbf998561f606754b3f1fd25bf3a00b924a4f"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 27,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop8.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.545480088,
    "preparation_seconds": 19.400422842,
    "artifact_sha256": {
      "vnnlib": "d7e077e7401d0699d7a1751faf7f9443adb413592756cffb8bc74873b820f7c5"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 28,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop4.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.512027854,
    "preparation_seconds": 19.394719356,
    "artifact_sha256": {
      "vnnlib": "6820056ac173bbe93a4676ee54edfeb4efe949e5e2b28a9aa7ab30f96f015eaf"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 29,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop6.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.566045036,
    "preparation_seconds": 19.407861327,
    "artifact_sha256": {
      "vnnlib": "4464b1c6d6bf7966fa665637f261c00c9ac18445b60549167e1f77e70d7fd702"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 30,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop12.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.542843659,
    "preparation_seconds": 19.438474865,
    "artifact_sha256": {
      "vnnlib": "c27b5031c89c34346e806dd193feb435e6561f02a71b78d4152adce36c934199"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 31,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop13.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.54112753,
    "preparation_seconds": 19.382476206,
    "artifact_sha256": {
      "vnnlib": "52d52a433504c3f7e9901d7b7bc8c97158d24da3546c27a3ab25601d331b2630"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 32,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop11.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.55758282,
    "preparation_seconds": 19.384414326,
    "artifact_sha256": {
      "vnnlib": "eee92efd8c12f9fd2fd848b30556891da5587dd380d940ad3ffbf790c3d8171f"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 33,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop1.vnnlib",
    "outcome": "sat",
    "raw_outcome": "sat",
    "validation": "strict",
    "check_status": "published_cache_row_and_witness_verified_execution_unbound",
    "run_seconds": 6.062600569,
    "preparation_seconds": 19.408552352,
    "artifact_sha256": {
      "vnnlib": "da6545188374ed1117b38cbe2db0cfa51a9f3ba7491a5ab0737ae4a2441b7cfc"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 34,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop3.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.639232496,
    "preparation_seconds": 19.400166702,
    "artifact_sha256": {
      "vnnlib": "db7d7f1b9b1a48e035622ffc3038164b60555ee3406c6c0eb3e8ce3aed82e747"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 35,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop14.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.548376346,
    "preparation_seconds": 19.409617806,
    "artifact_sha256": {
      "vnnlib": "ef72bf773659efef496be8ff92526a04f11e1b144633ca19f608394e180ce443"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 36,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop10.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.535109738,
    "preparation_seconds": 19.443359611,
    "artifact_sha256": {
      "vnnlib": "5e7440450540fd3ca2853ed1c1a1a4e0f726db8aba36b039fa1859e29ce96e0d"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 37,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/14_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/14_ieee_prop5.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.555943999,
    "preparation_seconds": 19.427248053,
    "artifact_sha256": {
      "vnnlib": "ad92e595d0e603f449ee47ce285bbacaaff8893078da47f36af792813ac7fb7f"
    },
    "execution_artifact_binding": false
  },
  {
    "row": 38,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/118_ieee_prop2.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 77.69233453,
    "preparation_seconds": 21.205078689,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 39,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/118_ieee_prop4.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 24.386241558,
    "preparation_seconds": 19.478843193,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 40,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/118_ieee_prop3.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 26.285860571,
    "preparation_seconds": 19.461893214,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 41,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/118_ieee_prop5.vnnlib",
    "outcome": "sat",
    "raw_outcome": "sat",
    "validation": "strict",
    "check_status": "published_cache_row_and_witness_verified_execution_unbound",
    "run_seconds": 5.905206305,
    "preparation_seconds": 19.524951568,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 42,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf-linear-nonresidual.onnx",
    "property": "vnnlib/118_ieee_prop6.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.70251645,
    "preparation_seconds": 19.380896887,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 57,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/300_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/300_ieee_prop3.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 79.183889662,
    "preparation_seconds": 22.507277238,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 58,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/300_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/300_ieee_prop105.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 8.244473685,
    "preparation_seconds": 19.489227157,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 59,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/300_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/300_ieee_prop2.vnnlib",
    "outcome": "sat",
    "raw_outcome": "sat",
    "validation": "strict",
    "check_status": "published_cache_row_and_witness_verified_execution_unbound",
    "run_seconds": 6.151468912,
    "preparation_seconds": 19.402656579,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 60,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/300_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/300_ieee_prop4.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 313.180126112,
    "preparation_seconds": 19.332948236,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 61,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/118_ieee_prop2.vnnlib",
    "outcome": "timeout",
    "raw_outcome": "timeout",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 607.788178023,
    "preparation_seconds": 21.779804708,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 62,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/118_ieee_prop4.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 25.482689508,
    "preparation_seconds": 19.439580913,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 63,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/118_ieee_prop3.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 27.338587728,
    "preparation_seconds": 19.438030499,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 64,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/118_ieee_prop5.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 8.123120349,
    "preparation_seconds": 19.469347881,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 65,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/118_ieee_ml4acopf-linear-residual.onnx",
    "property": "vnnlib/118_ieee_prop6.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 8.088559149,
    "preparation_seconds": 19.456154354,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 66,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/300_ieee_ml4acopf.onnx",
    "property": "vnnlib/300_ieee_prop3.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 27.393858683,
    "preparation_seconds": 21.98336461,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 67,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/300_ieee_ml4acopf.onnx",
    "property": "vnnlib/300_ieee_prop105.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 7.985156332,
    "preparation_seconds": 19.537712838,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 68,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/300_ieee_ml4acopf.onnx",
    "property": "vnnlib/300_ieee_prop2.vnnlib",
    "outcome": "sat",
    "raw_outcome": "sat",
    "validation": "strict",
    "check_status": "published_cache_row_and_witness_verified_execution_unbound",
    "run_seconds": 6.210085112,
    "preparation_seconds": 19.440534247,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 69,
    "category": "ml4acopf_2024",
    "version": "1.0",
    "network": "onnx/300_ieee_ml4acopf.onnx",
    "property": "vnnlib/300_ieee_prop4.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 14.444493426,
    "preparation_seconds": 19.307872751,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  },
  {
    "row": 70,
    "category": "inconsistent_paths",
    "version": "1.0",
    "network": "onnx/test_nano.onnx",
    "property": "vnnlib/test_nano.vnnlib",
    "outcome": "unsat",
    "raw_outcome": "unsat",
    "validation": null,
    "check_status": "not_applicable",
    "run_seconds": 5.787142915,
    "preparation_seconds": 19.19837343,
    "artifact_sha256": {},
    "execution_artifact_binding": false
  }
]
```
