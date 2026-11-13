# ACOPF implementation review

Two independent review axes used **GPT-6 Astra medium** before benchmark
execution. Baseline: `52ee71662c3c62a2f39ae7db07cf1e5cbd1ad8e0`;
reviewed implementation: `0709a01`. Diff command:
`git diff 52ee71662c3c62a2f39ae7db07cf1e5cbd1ad8e0...0709a01`.

## Standards

Documented standards: **pass**, with no breaches found. Sources included
`CODING_STANDARDS.md`, `CONTRIBUTING.md`, `docs/verification.md`, and the lint,
typechecking, hook and CI configuration. The intentionally changed rejection
test documents removal of the sequential affine-output restriction.

One heuristic finding (Repeated Switches / Primitive Obsession): relation names
were unrestricted strings and interval dispatch implicitly treated its final
case as multiplication. A future binary operation added to construction without
matching bounds could therefore inherit incorrect multiplication bounds.
This was not a demonstrated defect for the currently supported operations.

Disposition: `5444475` gives relation operations a closed `Literal` annotation,
makes multiplication an explicit interval case, and rejects unhandled relations.
No backend registry or adapter hierarchy was introduced.

## Spec

**Pass**, with no actionable implementation findings against #10, parent #7,
and the settled design. The review covered shared-DAG lowering, native global
relations, conservative bounds, prior affine/ReLU construction dispatch,
exact-model acquisition, property descriptors, and compact solver-backed cases.
The full experiment was deliberately gated on this review and the subsequent audit.

Limitation: the review agent's checkout did not expose ignored downloaded
artifacts, so it did not independently inspect the acquired original graph.
The execution checkout subsequently audited all 14 original queries using the
same interpreter as verification; its results are retained in `experiment.json`.

## Validation after disposition

All **143 tests passed**, including opted-in tiny real-Gurobi cases and runner
integration, before any ACOPF benchmark execution. Typechecking and lint passed.
The two shared-DAG cases establish a reachable output with strict original-ONNX
replay and numerical infeasibility below an independently derived range. The
UNSAT threshold lies inside coarse propagated intervals, requiring actual
trigonometric constraints. One focused coordinate-sensitive case covers static
views, sparse constant-left MatMul, and constant-only Boolean/shape scaffolding;
solver-independent rejection cases cover data-dependent Equal/Where, general
exponents and division, including unused nodes.

Summary: Standards — zero documented violations, one heuristic addressed;
Spec — zero actionable findings. Numerical UNSAT remains solver-reported, not
an independently checked exact-real certificate.
