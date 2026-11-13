# Proof-focused statistics

Generated from saved records; source-matched ABC identity is not execution-bound. Ratios are ABC/Gurobi observed run time, not matched-hardware speedups. SAT claims and accepted SAT are retained separately in evidence.json. Preparation and run times are not combined.

## Denominators

- **selected**: Every original audited query, including missing, corrupt, excluded and unresolved records. Property alternatives are not queries.
- **outcome_cross_tab**: Raw Gurobi claims versus uniquely source-hash-matched ABC claims; unavailable/corrupt/unverified ABC measurements use missing_or_corrupt.
- **numerical_unsat**: Recorded UNSAT with run time within the original deadline when known; no exact-real certificate. ABC additionally requires a unique source-hash match, not execution binding.
- **unresolved**: No deadline-qualified accepted solve, including missing/corrupt/identity-unverified measurements, errors, timeouts and rejected or unvalidated SAT.
- **paired_unsat**: Common deadline-qualified numerical UNSAT, both run times available, positive Gurobi time. Each summary includes exact IDs and timing counts; no timeout imputation.
- **ratios**: ABC/Gurobi observed run seconds, not matched-hardware speedups. Preparation is separate; combined ratios require explicit source.prepare_plus_run_comparable=true.
- **cohorts**: Audited ReLUSplitter depth/original-model descriptors, matched published MNIST outcome claims, or audited ACOPF property classes. Unavailable labels remain explicit. No cross-study pooling.

## Query populations

| Cohort | Selected | Matched | G UNSAT | ABC UNSAT | G accepted SAT | ABC accepted SAT | G unresolved | ABC unresolved | G timeout | ABC timeout | Disagreements | Common UNSAT timing n | ABC/G sum ratio | ABC/G median ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all selected | 120 | 120 | 1 | 96 | 2 | 24 | 117 | 0 | 117 | 0 | 0 | 1 | 0.29286079205811555 | 0.29286079205811555 |
| hidden_relu_layers: 4 | 6 | 6 | 1 | 4 | 0 | 2 | 5 | 0 | 5 | 0 | 0 | 1 | 0.29286079205811555 | 0.29286079205811555 |
| hidden_relu_layers: 5 | 44 | 44 | 0 | 32 | 0 | 12 | 44 | 0 | 44 | 0 | 0 | 0 | — | — |
| hidden_relu_layers: 6 | 70 | 70 | 0 | 60 | 2 | 10 | 68 | 0 | 68 | 0 | 0 | 0 | — | — |
| original_model_group: model_0_0 | 12 | 12 | 0 | 0 | 0 | 12 | 12 | 0 | 12 | 0 | 0 | 0 | — | — |
| original_model_group: model_1_1 | 48 | 48 | 0 | 36 | 2 | 12 | 46 | 0 | 46 | 0 | 0 | 0 | — | — |
| original_model_group: model_2_2 | 24 | 24 | 1 | 24 | 0 | 0 | 23 | 0 | 23 | 0 | 0 | 1 | 0.29286079205811555 | 0.29286079205811555 |
| original_model_group: model_3_3 | 36 | 36 | 0 | 36 | 0 | 0 | 36 | 0 | 36 | 0 | 0 | 0 | — | — |

## Outcome cross-tab (Gurobi / ABC)

```json
{
  "unknown": {
    "unsat": 95,
    "sat": 22
  },
  "unsat": {
    "unsat": 1
  },
  "sat": {
    "sat": 2
  }
}
```

## Timing fields (seconds, separate populations)

```json
{
  "gurobi": {
    "all_recorded": {
      "count": 120,
      "sum": 21217.76457855315,
      "min": 22.28398908278905,
      "median": 180.0162144789938,
      "max": 180.01982333301567
    },
    "solved": {
      "count": 3,
      "sum": 156.06316304183565,
      "min": 22.28398908278905,
      "median": 60.26639241701923,
      "max": 73.51278154202737
    },
    "preparation": {
      "count": 120,
      "sum": 0.0,
      "min": 0.0,
      "median": 0.0,
      "max": 0.0
    }
  },
  "abc": {
    "all_recorded": {
      "count": 120,
      "sum": 1169.158709334,
      "min": 5.989366339,
      "median": 6.6939804015,
      "max": 70.719883759
    },
    "solved": {
      "count": 120,
      "sum": 1169.158709334,
      "min": 5.989366339,
      "median": 6.6939804015,
      "max": 70.719883759
    },
    "preparation": {
      "count": 120,
      "sum": 2390.793172279,
      "min": 19.397280644,
      "median": 20.0004690395,
      "max": 20.210550393
    }
  }
}
```
