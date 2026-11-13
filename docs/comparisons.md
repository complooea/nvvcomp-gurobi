# Saved-result comparisons

The comparison module owns cross-tool alignment and evidence calculations. It does
not run a verifier, replay witnesses, acquire benchmarks, or write the analytical
narrative. The CLI calls this same module and writes JSON and per-instance tables;
the report author synthesizes those outputs separately.

## Regenerate the retained evidence

From a checkout, using the locked Python environment:

```sh
uv run --locked python -m nvvcomp_gurobi.comparison experiments/sat-relu-v1 experiments/sat-relu-v1-comparison/published experiments/sat-relu-v1-comparison --category sat_relu --version 1.0
```

No network access, benchmark files, Gurobi installation/license, or ABC execution
is required. Inputs are the original `experiment.json` and `records/*.json`, plus
the retained published `source.json`, result CSV, witnesses and validation caches.
The CLI checks published-file SHA256 identities and records input/source hashes.
It overwrites only `evidence.json`, `instances.md`, and `statistics.md`, not the authored report or
original experiment. Repeated generation with unchanged inputs/source is identical.

To reacquire published inputs into a **new** directory:

```sh
uv run --locked python -m nvvcomp_gurobi.experiment acquire .benchmarks/sat-relu-v1
uv run --locked python scripts/acquire_comparison.py .benchmarks/sat-relu-v1 new-published-evidence
```

Acquisition pins results/scoring revision
`eea564f5d0a8751d8321a409214db14d03f452b8` and benchmark revision
`303f2327a8e8411efc4457da03d2016ce42733cf`. It verifies original compressed
benchmark bytes against Git blob identities and records decompressed SHA256s.
Snapshots of scoring Python are stored as `.py.txt`: reference data, not imported
project code. Their original bytes, including whitespace, must remain unchanged.

## Comparison interface

```python
from nvvcomp_gurobi.comparison import compare

evidence = compare(audit, records_by_manifest_id, published)
```

`audit` is the saved experiment audit plus explicit `category` and `version`
context; the CLI requires these because the original audit lacks those fields.
`records_by_manifest_id` contains original per-instance records. Missing keys mean
missing records, not unknown verdicts. `published` contains a `records` list of
normalized measurements and optional `source` provenance. Each measurement has:

- `category`, `version`, `network`, `property`: exact version-relative paths,
  retaining directories; matching is not positional and does not use name labels.
- `artifact_sha256`: decompressed `onnx` and `vnnlib` hashes of the pinned source.
- `execution_artifact_binding`: true only with independent evidence that the
  measurement used those exact artifacts; source correspondence alone is false.
- `outcome`, `validation`, `run_seconds`, `preparation_seconds`: normalized saved
  measurement. SAT validation is `strict`, `tolerance_only`, `invalid`,
  `unsupported`, or unavailable. Unknown timings are null, never zero.

The CLI's published-data adapter reads the six-column competition CSV, verifies
category/version paths on both files, and maps `sat`/`violated` and `unsat`/`holds`.
It authenticates published check-cache correspondence using the normalized CSV row
hash, witness hash, benchmark/version identity, checker and provider. These checks
validate **cache correspondence**, not cache correctness or execution artifact
identity. No fresh witness replay is performed.

### Evidence interpretation

- `candidate_matched` requires both artifact hashes and category/version agreement.
  `execution_bound` is a separate, stronger population. Unbound comparisons are
  explicitly conditional, including ABC SAT-only scoring contributions.
- Every audited instance remains in `instances`; missing, excluded, ambiguous,
  corrupt, mismatched and identity-unverified cases are visible. Extra published
  rows remain in `unmatched_abc`, including smoke tests and other versions. Full
  category/version/path context selects candidates before ambiguity is assessed.
  Each tool's available measurements contribute independently to its outcome and
  timing summaries, even if the other tool's record is missing or corrupt.
- Solved counts mean accepted SAT witness or numerical UNSAT claim within the raw
  run deadline when known. They do not certify correctness. Unsupported/unvalidated
  SAT is not counted as an accepted solve. Outcome summaries retain raw claims.
- Runtime ratios use **same-answer mutual solves with available run times** and a
  positive Gurobi denominator. They exclude timeouts, failures and disagreements;
  per-tool solved and all-recorded populations are reported separately with IDs.
  Preparation-plus-run ratios additionally require both preparation measurements
  and explicit `published.source.prepare_plus_run_comparable=true`; by default
  they are null. The original MVP archive predates this opt-in and retains its
  historical combined ratios; regeneration with current code leaves them null.
  All ratios are ABC/Gurobi: values above one mean lower Gurobi observed time.
- No startup subtraction or timeout-budget imputation is applied. The pinned
  scoring code subtracts fastest-observed tool overhead for plots **and deadline
  enforcement**, contradicting its README's raw-deadline description. We do not
  recreate adjusted scoring times from an incomplete multi-category context.
- The pinned scorer awards 10 for accepted SAT (strict or tolerance-only), with
  time bonuses disabled. Only strict witnesses refute UNSAT. Full points and
  category-normalized scores remain unavailable without execution-bound identity
  and complete participating-tool conflict evidence. Agreement is not ground truth.
  SAT-only contributions require available run timing; missing timing receives no
  assumed credit. Correctness conflicts are evaluated independently of solve-time
  eligibility: a late strict witness still contradicts a matching UNSAT claim,
  without earning deadline-qualified solve credit. Execution binding qualifies
  the conflict separately.
- Architecture descriptors come from the preceding audit, not filenames.
  `structural_width_groups` / `Wxx` hold input/output dimensions, operation
  sequence, and hidden-layer count fixed while hidden widths vary. These are
  **descriptor groups**, not proof that arbitrary networks differ only in width:
  weights, graph attributes/topology not represented by the descriptors, and
  properties may differ. Do not generalize to other families without sufficient
  descriptors. Missing descriptors produce no group; no architecture is guessed.

The schema is deliberately a small saved-evidence interface, not a general
competition scorer or a new experiment framework. For additional families, supply
their explicit context and original descriptors; extend the CSV adapter when its
single-network path contract is insufficient, rather than silently approximating
multi-network or different-format measurements.

## Tests

```sh
uv run --locked pytest tests/test_comparison.py
```

Behavior tests cross `compare`; a small CLI integration fixture tests loading,
cache correspondence, hash validation, and deterministic output. Neither seam
duplicates solver correctness, experiment persistence, or full-category execution.

See the [comprehensive comparison report](../experiments/proof-comparison-analysis.md)
for the actual observations and hardware/provenance limits.

## Expanded proof studies (#11)

The same `compare` and CLI seams produce `proof` and `cohorts` statistics for
the three completed studies. Reproducible commands and input inventories are in:

- [ReLUSplitter](../experiments/relusplitter-v1-comparison/README.md)
- [Sigmoid MNIST](../experiments/mnist-sigmoid-v1-comparison/README.md)
- [IEEE-14 ACOPF](../experiments/acopf-v1-comparison/README.md)

Each archive includes the entire published category CSV (including unselected
aliases and appended smoke rows), source/selected manifests, published SAT
witness/check caches, and pinned-source artifact hashes. Acquisition now accepts
`--category` for these categories; ACOPF verifies the full pinned source manifest
before deriving its exact-model selection. It never executes ABC or a validator.

`proof` and every cohort expose the selected-query denominator, matched IDs,
raw outcome cross-tab, per-tool numerical UNSAT/accepted SAT/unresolved/timeout
IDs, accepted-answer disagreements, and paired common-UNSAT timing statistics.
Unavailable or ambiguous identities cannot earn ABC proof credit or enter paired
timings. Available local measurements still contribute independently. Missing
timing is not zero: it permits an outcome claim without a known deadline breach,
but cannot enter a paired timing denominator. Numerical UNSAT remains a solver
claim, not an exact-real certificate or an ABC bound-tightness measurement.

ReLUSplitter cohorts use audited hidden ReLU depth and original-model group,
not graph-node counts or assumed functional equivalence. MNIST cohorts use
source-hash-matched published UNSAT/SAT claims, not correctness labels. ACOPF uses
audited physical-residual versus structural-output-bound classes. Each cohort
includes all its queries, regardless of difficulty; property branches are never
counted separately. Unlike studies are not pooled.

`statistics.md` is generated data and denominator guidance, not analysis. The
JSON additionally retains exact population IDs, individual timing fields, and
experiment hardware/resource/revision context alongside input hashes. The MVP
archive remains the separate population for subsequent analysis relating to #2.

See the [comprehensive comparison report](../experiments/proof-comparison-analysis.md)
for interpretation of all four completed studies, exact
evidence links, timing denominators and claim limitations. Regeneration does not
overwrite this report; reconsider it if input fingerprints or definitions change.
The [experiment index](../experiments/README.md) separates the research narrative,
archived measurements/calculations and scoped review records.
