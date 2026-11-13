# Independent review

Both axes used GPT-6 Astra (`openai/gpt-6-astra`), **medium** effort, in separate
fresh reviewer contexts. Reviews were read-only and did not execute benchmarks.

User-confirmed baseline: `c917a99bdd08402dce95551f5c23b8d1d32aeafc`.
Initial diff: `git diff c917a99bdd08402dce95551f5c23b8d1d32aeafc...5741d8c`.
Commits reviewed:

- `3633256`: native sigmoid and constant reshape verification, tests and docs.
- `5741d8c`: complete 72-query measurement archive.

Standards sources included `AGENTS.md`, `docs/agents/domain.md`, `GLOSSARY.md`,
`CODING_STANDARDS.md`, `CONTRIBUTING.md`, the verification/experiment contracts,
tool configuration and the code-review skill's Fowler smell baseline. Spec
sources were GitHub issues #9 and #7.

## Standards

The initial review identified one documented-contract violation and one
judgement-call smell:

1. **Affine-output contract.** The final-op check accepted `Gemm → Sigmoid →
   Reshape → output` and reshape-only graphs, although the documented contract
   requires ending in Gemm, optionally reshaped. Track the last computational
   operation independently of reshape nodes and add rejection coverage.
2. **Duplicated Code (judgement call).** Construction and provenance independently
   dispatched on whether the graph contained Sigmoid or Reshape. Share the
   solver-independent selection predicate to prevent descriptor/encoding drift.

No other documented-standard violations were identified in the changed tests or
archive/reporting hunks. Tooling-enforced issues were excluded.

### Disposition and follow-up

Commit `8a03f4a` resolves both findings. The reviewer independently confirmed:

> Affine-output contract: resolved. `last_computation` ignores reshapes and must
> be `Gemm`. The two public-verifier cases cover sigmoid-ending and reshape-only
> graphs, asserting the specific rejection diagnostic and no solver status.
>
> Duplicated dispatch predicate: resolved. Construction and provenance
> description now share `uses_native_construction`.
>
> No remaining Standards-axis findings in this follow-up diff.

## Spec

The initial review reported no findings: no missing/partial requirements,
unrequested scope creep or incorrect implementations were identified within
issue #9's slice.

Native logistic constraints, valid intermediate bounds, C-order reshape handling,
original-shape FLOAT32 replay and conservative status mapping align with the
specification. The two real-verifier fixtures cover independently understood
reachable and impossible outputs.

Archive checks confirmed all 72 records: 42 numerical UNSAT, six strict
replay-accepted SAT and 24 unknown/timeouts. Manifest identity, audit/record
artifact hashes, source hashes against frozen commit `3633256` and reported
runtime totals agree. Completed verdicts remained within deadlines; unresolved
outcomes are retained. Published ABC verdicts were not used as a correctness
oracle; shared comparative analysis is explicitly deferred.

The independent follow-up on `git diff 5741d8c..8a03f4a` found no new spec issues.
Both reviewers confirmed that retaining measured `3633256` source hashes is
appropriate: the selected MNIST graph ends in Gemm and its construction dispatch
is unchanged. The follow-up is not a new experiment; no measured records were
rewritten or rerun.

**Summary:** Standards: two initial findings, both resolved, none remaining.
Spec: zero initial or follow-up findings.

## Final validation

After the review fixes, `uv run --locked --extra solver pytest tests --solver
--cov --cov-report=term-missing` passed all **134 tests** (87% branch-inclusive
coverage). Typechecking, lint and commit hooks also passed. The working tree was
clean after committing the review record. No benchmark results were changed.
