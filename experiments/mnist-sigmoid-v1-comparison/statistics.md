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
| all selected | 72 | 72 | 42 | 64 | 6 | 8 | 24 | 0 | 24 | 0 | 0 | 42 | 0.04849193274977243 | 0.052465460408613135 |
| published_outcome: sat | 8 | 8 | 0 | 0 | 6 | 8 | 2 | 0 | 2 | 0 | 0 | 0 | — | — |
| published_outcome: unsat | 64 | 64 | 42 | 64 | 0 | 0 | 22 | 0 | 22 | 0 | 0 | 42 | 0.04849193274977243 | 0.052465460408613135 |

## Outcome cross-tab (Gurobi / ABC)

```json
{
  "unsat": {
    "unsat": 42
  },
  "unknown": {
    "sat": 2,
    "unsat": 22
  },
  "sat": {
    "sat": 6
  }
}
```

## Timing fields (seconds, separate populations)

```json
{
  "gurobi": {
    "all_recorded": {
      "count": 72,
      "sum": 13338.851826245897,
      "min": 25.600724500138313,
      "median": 151.50117549998686,
      "max": 300.0175339579582
    },
    "solved": {
      "count": 48,
      "sum": 6138.477964707883,
      "min": 25.600724500138313,
      "median": 116.85881054203492,
      "max": 292.5636682920158
    },
    "preparation": {
      "count": 72,
      "sum": 0.0,
      "min": 0.0,
      "median": 0.0,
      "max": 0.0
    }
  },
  "abc": {
    "all_recorded": {
      "count": 72,
      "sum": 476.884783859,
      "min": 6.029835112,
      "median": 6.054374655,
      "max": 12.566627631
    },
    "solved": {
      "count": 72,
      "sum": 476.884783859,
      "min": 6.029835112,
      "median": 6.054374655,
      "max": 12.566627631
    },
    "preparation": {
      "count": 72,
      "sum": 1385.975949333,
      "min": 19.183832731,
      "median": 19.2516351885,
      "max": 19.445575865
    }
  }
}
```
