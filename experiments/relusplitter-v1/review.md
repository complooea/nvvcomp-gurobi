# Implementation and archive review

Both axes ran independently with **GPT-6 Astra, medium**
(`openai/gpt-6-astra#medium`). User-confirmed baseline: session-start commit
`6133be90c036612ba898d81f2276d1e04afd4bd3`.

Reviewed command: `git diff 6133be90c036612ba898d81f2276d1e04afd4bd3...7bd1f6e`.
Reviewed commits: `e40e792` (implementation), `2ba2eb4` (group correction), and
`7bd1f6e` (complete archive). All 124 routine tests, including real-Gurobi and
runner/archive integration cases, passed. Hooks and typechecking passed.
Reviewers made no edits and did not rerun benchmarks.

## Standards

No hard violations found. Added tests meaningfully exercise real-Gurobi
disjunction SAT/UNSAT behavior, replay, unsupported syntax, and audit grouping.
No weakened assertions or suppressed diagnostics require justification.

One baseline smell, a judgment call: **Duplicated Code** in
`src/nvvcomp_gurobi/_interpretation.py:66–81`. The grammar repeats comparison and
AND syntax across validation and extraction:

```python
r"\( assert \( or (?:\( and (?:\( (?:<=|>=) [^\s()]+ [^\s()]+ \) )+\) )+\) \)"

re.findall(r"\( (<=|>=) (\S+) (\S+) \)", clause)
r"\( and ((?:\( (?:<=|>=) [^\s()]+ [^\s()]+ \) )+)\)"
```

Future grammar changes must keep these patterns synchronized; otherwise accepted
comparisons could fail extraction. Consider shared comparison/alternative regex
fragments so validation and extraction use the same grammar. **Low priority; not
a documented-standard breach or demonstrated current defect.**

The reviewer checked source/test/doc changes and both experiment READMEs, and
programmatically checked manifest counts, record-to-audit identities, outcome
totals, and summed runtimes in both archives; all matched.

## Spec

**No actionable spec/correctness findings.** No missing/partial requirements,
scope creep, or incorrect implementations were identified within issue #8.

Selectors enforce at least one complete branch, outside comparisons remain
unconditional, and multiple OR assertions remain conjunctive. Replay preserves
statement/operand order and scalar spellings; the pinned replay parser retains
unconditional constraints and combines multiple disjunctions correctly.

The public `verify(Instance, ExecutionLimits)` seam, original-ONNX replay,
numerical defaults, and shared whole-query deadline are preserved. Both requested
real-Gurobi integration cases exercise that production seam.

Programmatic archive checks confirmed 120 manifest rows and 120 matching
audit/result records; matching manifest, artifact, and source/lockfile hashes;
2 strict SAT, 1 numerical UNSAT, 117 timeouts; depth counts 6/44/70 for 4/5/6
layers; consistent original/generated groups; and implementation commit
`2ba2eb4`. The earlier pilot and descriptor correction are explicitly disclosed.

Nonblocking observation: the first full-run query overlapped approximately
16 seconds of routine tests. This is transparently documented and does not
violate reporting actual resources/timing without claiming matched conditions.

## Initial disposition

No correctness or standards fix was required. The low-priority regex
deduplication suggestion is deferred: no current defect was demonstrated, and
the experiment-bound implementation remains unchanged and hash-identifiable.

Summary: Standards — 1 low-priority smell, 0 documented violations;
Spec — 0 findings.

## Follow-up

The user requested the suggested cleanup. Comparison and conjunction regex
fragments are now shared by both full-statement validation and clause extraction;
the supported property grammar is unchanged. The complete archive was renamed
from `relusplitter-v1-full` to canonical `relusplitter-v1`, and the redundant pilot
was removed from the current tree (it remains available in Git history). All 120
full-run records, audit/source hashes, manifest, and generated reports were
preserved byte-for-byte. Their provenance continues to identify the measured
implementation commit, not the later grammar refactor.
