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
| all selected | 4 | 4 | 1 | 3 | 0 | 1 | 3 | 0 | 3 | 0 | 0 | 1 | 0.4078508994306766 | 0.4078508994306766 |
| property_class: physical_residual | 2 | 2 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 1 | 0.4078508994306766 | 0.4078508994306766 |
| property_class: structural_output_bound | 2 | 2 | 0 | 2 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 0 | — | — |
| network: onnx/300_ieee_ml4acopf.onnx | 4 | 4 | 1 | 3 | 0 | 1 | 3 | 0 | 3 | 0 | 0 | 1 | 0.4078508994306766 | 0.4078508994306766 |
| network_property_class: onnx/300_ieee_ml4acopf.onnx: physical_residual | 2 | 2 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 1 | 0.4078508994306766 | 0.4078508994306766 |
| network_property_class: onnx/300_ieee_ml4acopf.onnx: structural_output_bound | 2 | 2 | 0 | 2 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 0 | — | — |

## Outcome cross-tab (Gurobi / ABC)

```json
{
  "unknown": {
    "unsat": 2,
    "sat": 1
  },
  "unsat": {
    "unsat": 1
  }
}
```

## Timing fields (seconds, separate populations)

```json
{
  "gurobi": {
    "all_recorded": {
      "count": 4,
      "sum": 1819.6558479168452,
      "min": 19.578616457991302,
      "median": 600.0201738750329,
      "max": 600.0368837087881
    },
    "solved": {
      "count": 1,
      "sum": 19.578616457991302,
      "min": 19.578616457991302,
      "median": 19.578616457991302,
      "max": 19.578616457991302
    },
    "preparation": {
      "count": 4,
      "sum": 0.0,
      "min": 0.0,
      "median": 0.0,
      "max": 0.0
    }
  },
  "abc": {
    "all_recorded": {
      "count": 4,
      "sum": 56.033593553,
      "min": 6.210085112,
      "median": 11.214824879,
      "max": 27.393858683
    },
    "solved": {
      "count": 4,
      "sum": 56.033593553,
      "min": 6.210085112,
      "median": 11.214824879,
      "max": 27.393858683
    },
    "preparation": {
      "count": 4,
      "sum": 80.269484446,
      "min": 19.307872751,
      "median": 19.4891235425,
      "max": 21.98336461
    }
  }
}
```
