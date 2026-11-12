# nvvcomp-gurobi

A research project measuring Gurobi-based neural network verification performance
on a supported subset of VNN-COMP 2026 benchmarks. Saved measurements support a
preliminary comparison with published α,β-CROWN results; no performance winner is
presumed.

The initial verifier supports narrow sequential FLOAT32 affine/ReLU ONNX networks
and conjunctive / output OR-of-AND VNN-LIB 1.0 queries. SAT witnesses are independently replayed with
pinned VNN-COMP validation code. Manifest-driven experiments retain per-instance
records and produce reports without rerunning the solver.

## Getting started

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/) 0.13.6.
Development and CI use Python 3.12 to align with competition validation.

```sh
uv sync --locked --extra solver
uv run --locked prek install
uv run --locked prek run --all-files
```

```python
from pathlib import Path
from nvvcomp_gurobi.verification import ExecutionLimits, Instance, verify

result = verify(
    Instance(Path("network.onnx"), Path("property.vnnlib")),
    ExecutionLimits(timeout_seconds=100, threads=1),
)
print(result.outcome, result.reason, result.validation)
```

See [the verification contract](docs/verification.md) for supported syntax,
numerical assumptions, result meanings, dependencies, and competition scripts.

See [experiment instructions](docs/experiments.md) for the pinned full-category
audit, local execution, saved records, and solver-free reports.

The [ReLUSplitter results](experiments/relusplitter-v1/README.md) archive all
120 queries, including unresolved outcomes and reproduction instructions.

See the [preliminary ABC comparison](experiments/sat-relu-v1-comparison/README.md)
for coverage, observed runtimes, and network-scale descriptors, and
[comparison instructions](docs/comparisons.md) to regenerate its evidence.

See [CONTRIBUTING.md](CONTRIBUTING.md) for checks, testing, CI, and the solo
development workflow, and [GLOSSARY.md](GLOSSARY.md) for domain terminology.
