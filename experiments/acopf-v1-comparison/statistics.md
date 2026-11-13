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
| all selected | 14 | 14 | 13 | 14 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 13 | 43.46374854666705 | 51.841218893021264 |
| property_class: physical_residual | 12 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 12 | 42.92386429231235 | 51.86797282593486 |
| property_class: structural_output_bound | 2 | 2 | 1 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 51.29947337208853 | 51.29947337208853 |

## Outcome cross-tab (Gurobi / ABC)

```json
{
  "unsat": {
    "unsat": 13
  },
  "unknown": {
    "unsat": 1
  }
}
```

## Timing fields (seconds, separate populations)

```json
{
  "gurobi": {
    "all_recorded": {
      "count": 14,
      "sum": 2.5975029156543314,
      "min": 0.14026904106140137,
      "median": 0.15033941704314202,
      "max": 0.3224193751811981
    },
    "solved": {
      "count": 13,
      "sum": 2.332472457550466,
      "min": 0.14026904106140137,
      "median": 0.15032975003123283,
      "max": 0.3224193751811981
    },
    "preparation": {
      "count": 14,
      "sum": 0.0,
      "min": 0.0,
      "median": 0.0,
      "max": 0.0
    }
  },
  "abc": {
    "all_recorded": {
      "count": 14,
      "sum": 109.407988003,
      "min": 7.712828834,
      "median": 7.796035699,
      "max": 8.029991616
    },
    "solved": {
      "count": 14,
      "sum": 109.407988003,
      "min": 7.712828834,
      "median": 7.796035699,
      "max": 8.029991616
    },
    "preparation": {
      "count": 14,
      "sum": 273.099384791,
      "min": 19.367899858,
      "median": 19.401378663000003,
      "max": 20.923695592
    }
  }
}
```
