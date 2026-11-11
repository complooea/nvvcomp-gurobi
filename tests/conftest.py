import importlib.util
import os
from pathlib import Path

import numpy as np
import onnx
import pytest
from onnx import TensorProto, helper, numpy_helper

from nvvcomp_gurobi.verification import Instance


def pytest_addoption(parser):
    parser.addoption(
        "--solver",
        action="store_true",
        help="Run real Gurobi tests (prerequisites required)",
    )


def pytest_sessionstart(session):
    if session.config.getoption("--solver"):
        if any(
            importlib.util.find_spec(name) is None for name in ["gurobipy", "gurobi_ml"]
        ):
            raise pytest.UsageError(
                "--solver requires: uv sync --locked --extra solver"
            )


@pytest.fixture(autouse=True)
def isolated_solver_license(request, tmp_path, monkeypatch):
    if request.node.get_closest_marker("solver"):
        home = tmp_path / "license-home"
        home.mkdir()
        monkeypatch.setenv("HOME", str(home))
        monkeypatch.delenv("GRB_LICENSE_FILE", raising=False)


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--solver"):
        for item in items:
            if "solver" in item.keywords:
                item.add_marker(
                    pytest.mark.skip(reason="request real Gurobi tests with --solver")
                )


@pytest.fixture
def worker_startup(tmp_path: Path, monkeypatch):
    """Inject deterministic external-boundary behavior at Python startup.

    Used for the external Gurobi SDK and deliberately blocking process startup,
    never for replacing our own pipeline. Encoding/replay stay in use.
    """

    def install(code: str):
        startup = tmp_path / "startup"
        startup.mkdir()
        (startup / "sitecustomize.py").write_text(code)
        monkeypatch.setenv(
            "PYTHONPATH", str(startup) + os.pathsep + os.environ.get("PYTHONPATH", "")
        )

    return install


@pytest.fixture
def instance_factory(tmp_path: Path):
    """Analytic network: Y_0 = X_0, Y_1 = max(X_1, 0)."""

    def make(
        assertions: str, *, op: str = "Relu", trans_a: int = 0, opset: int = 17
    ) -> Instance:
        nodes = [
            helper.make_node(
                "Gemm", ["x", "w1", "b1"], ["h"], transB=1, transA=trans_a
            ),
            helper.make_node(op, ["h"], ["r"]),
            helper.make_node("Gemm", ["r", "w2", "b2"], ["y"]),
        ]
        arrays = {
            "w1": [[1, 0], [-1, 0], [0, 1]],
            "b1": [0, 0, 0],
            "w2": [[1, 0], [-1, 0], [0, 1]],
            "b2": [0, 0],
        }
        graph = helper.make_graph(
            nodes,
            "analytic",
            [helper.make_tensor_value_info("x", TensorProto.FLOAT, [1, 2])],
            [helper.make_tensor_value_info("y", TensorProto.FLOAT, [1, 2])],
            [
                numpy_helper.from_array(np.array(a, dtype=np.float32), name)
                for name, a in arrays.items()
            ],
        )
        model = helper.make_model(
            graph, opset_imports=[helper.make_opsetid("", opset)], ir_version=8
        )
        network = tmp_path / "network.onnx"
        onnx.save(model, network)
        prop = tmp_path / "property.vnnlib"
        prop.write_text(
            "\n".join(
                f"(declare-const {kind}_{i} Real)" for kind in "XY" for i in range(2)
            )
            + "\n(assert (>= X_0 -1))\n(assert (<= X_0 1))"
            + "\n(assert (>= X_1 -1))\n(assert (<= X_1 1))\n"
            + assertions
        )
        return Instance(network, prop)

    return make
