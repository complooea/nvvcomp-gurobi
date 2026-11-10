# nvvcomp-gurobi

A research project measuring Gurobi-based neural network verification performance
on a supported subset of VNN-COMP 2026 benchmarks. Published α,β-CROWN results will
provide an initial comparison; no performance winner is presumed.

The initial verifier supports narrow sequential FLOAT32 affine/ReLU ONNX networks
and conjunctive VNN-LIB 1.0 queries. SAT witnesses are independently replayed with
pinned VNN-COMP validation code. Experiment orchestration is separate future work.

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

See [CONTRIBUTING.md](CONTRIBUTING.md) for checks, testing, CI, and the solo
development workflow, and [GLOSSARY.md](GLOSSARY.md) for domain terminology.
