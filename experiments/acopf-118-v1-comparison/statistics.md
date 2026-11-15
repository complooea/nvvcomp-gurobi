# Proof-focused statistics

Generated from saved records; source-matched ABC identity is not execution-bound. Ratios are ABC/Gurobi observed run time, not matched-hardware speedups. SAT claims and accepted SAT are retained separately in evidence.json. Preparation and run times are not combined.

## Denominators

- **selected**: Every original audited query, including missing, corrupt, excluded and unresolved records. Property alternatives are not queries.
- **outcome_cross_tab**: Raw Gurobi claims versus uniquely source-hash-matched ABC claims; unavailable/corrupt/unverified ABC measurements use missing_or_corrupt.
- **numerical_unsat**: Recorded UNSAT with run time within the original deadline when known; no exact-real certificate. ABC additionally requires a unique source-hash match, not execution binding.
- **unresolved**: No deadline-qualified accepted solve, including missing/corrupt/identity-unverified measurements, errors, timeouts and rejected or unvalidated SAT.
- **paired_unsat**: Common deadline-qualified numerical UNSAT, both run times available, positive Gurobi time. Each summary includes exact IDs and timing counts; no timeout imputation.
- **ratios**: ABC/Gurobi observed run seconds, not matched-hardware speedups. Preparation is separate; combined ratios require explicit source.prepare_plus_run_comparable=true.
- **cohorts**: Audited ReLUSplitter depth/original-model descriptors, matched published MNIST outcome claims, or exact ACOPF networks and audited property classes. Unavailable labels remain explicit. No cross-study pooling.

## Query populations

| Cohort | Selected | Matched | G UNSAT | ABC UNSAT | G accepted SAT | ABC accepted SAT | G unresolved | ABC unresolved | G timeout | ABC timeout | Disagreements | Common UNSAT timing n | ABC/G sum ratio | ABC/G median ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all selected | 5 | 5 | 3 | 5 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 3 | 0.25385290285470785 | 1.382788190557376 |
| property_class: physical_residual | 3 | 3 | 2 | 3 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 2 | 1.7729544042775893 | 1.9255194196086127 |
| property_class: structural_output_bound | 2 | 2 | 1 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0.10515287628355714 | 0.10515287628355714 |
| network: onnx/118_ieee_ml4acopf.onnx | 5 | 5 | 3 | 5 | 0 | 0 | 2 | 0 | 1 | 0 | 0 | 3 | 0.25385290285470785 | 1.382788190557376 |
| network_property_class: onnx/118_ieee_ml4acopf.onnx: physical_residual | 3 | 3 | 2 | 3 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 2 | 1.7729544042775893 | 1.9255194196086127 |
| network_property_class: onnx/118_ieee_ml4acopf.onnx: structural_output_bound | 2 | 2 | 1 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0.10515287628355714 | 0.10515287628355714 |

## Outcome cross-tab (Gurobi / ABC)

```json
{
  "unknown": {
    "unsat": 2
  },
  "unsat": {
    "unsat": 3
  }
}
```

## Timing fields (seconds, separate populations)

```json
{
  "gurobi": {
    "all_recorded": {
      "count": 5,
      "sum": 710.5832750003319,
      "min": 3.218548124888912,
      "median": 10.1399171249941,
      "max": 600.0145108331926
    },
    "solved": {
      "count": 3,
      "sum": 100.42884704214521,
      "min": 3.218548124888912,
      "median": 5.735618167091161,
      "max": 91.47468075016513
    },
    "preparation": {
      "count": 5,
      "sum": 0.0,
      "min": 0.0,
      "median": 0.0,
      "max": 0.0
    }
  },
  "abc": {
    "all_recorded": {
      "count": 5,
      "sum": 154.464707744,
      "min": 7.931145067,
      "median": 9.618825788,
      "max": 105.509718394
    },
    "solved": {
      "count": 5,
      "sum": 154.464707744,
      "min": 7.931145067,
      "median": 9.618825788,
      "max": 105.509718394
    },
    "preparation": {
      "count": 5,
      "sum": 99.270814954,
      "min": 19.39806613,
      "median": 19.525217551,
      "max": 21.132091634
    }
  }
}
```
