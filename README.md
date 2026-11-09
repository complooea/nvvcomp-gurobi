# nvvcomp-gurobi

A research project measuring Gurobi-based neural network verification performance
on a supported subset of VNN-COMP 2026 benchmarks. Published α,β-CROWN results will
provide an initial comparison; no performance winner is presumed.

The project currently contains the Python tooling foundation. Network conversion,
verification, benchmark execution, and tests will be introduced in subsequent work.

## Getting started

Requires Python 3.11 or newer and [uv](https://docs.astral.sh/uv/).
Development and CI currently use Python 3.11.

```sh
uv sync --locked
uv run --locked prek install
uv run --locked prek run --all-files
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for checks, testing, CI, and the solo
development workflow, and [GLOSSARY.md](GLOSSARY.md) for domain terminology.
