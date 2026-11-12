# Retained ReLUSplitter pilot (not the full experiment)

This directory retains one original invocation, manifest row `0000`, and the
120-row preflight that preceded it. The pilot constructed successfully in about
0.07 seconds and exhausted its 180-second whole-run deadline. Its raw solver
status is 9 (TIME_LIMIT); the accepted outcome is unknown/timeout. It has no
witness and supplies no numerical UNSAT result.

The pilot exposed a bookkeeping defect in the original-model group descriptor:
original names retained `.onnx`, whereas generated names used the prefix before
`~` without that suffix. Commit `2ba2eb4` normalizes both to the same group. No
encoding, numerical parameter, or deadline changed. This audit and result are
preserved unchanged rather than retrospectively rewritten.

The complete, corrected 120-query experiment is in
[`../relusplitter-v1-full/`](../relusplitter-v1-full/README.md). The full population
starts afresh, including row `0000`; the pilot is separately disclosed and never
counted as a 121st query or pooled into its statistics. The 119 missing rows in
this pilot's generated summary are intentional: this directory is not resumed.

Inventory: `experiment.json`, original `instances.csv`, `records/0000.json`, and
solver-free `summary.json` / `report.md`. Acquisition and artifact hashes,
implementation source hashes, effective settings, construction/model size,
timings, environment, and timeout evidence are retained in those JSON files.
