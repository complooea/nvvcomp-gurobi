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


@pytest.fixture
def dag_instance_factory(tmp_path):
    """Shared u=x+offset; y=sum(u² + u*reverse(u) + sin(u)+cos(u)).

    At x=[0,0], offset=[0,1], y=2+sin(1)+cos(1)=3.3817733.
    For x in [0,1]^2: u_0 in [0,1], u_1 in [1,2], so y > .5.
    """

    def make(assertions, *, fixed=False):
        nodes = [
            helper.make_node("Add", ["x", "offset"], ["u"]),
            helper.make_node("Gather", ["u", "reverse"], ["v"], axis=1),
            helper.make_node("Mul", ["u", "v"], ["product"]),
            helper.make_node("Pow", ["u", "two"], ["square"]),
            helper.make_node("Sin", ["u"], ["sine"]),
            helper.make_node("Cos", ["u"], ["cosine"]),
            helper.make_node("Add", ["product", "square"], ["a"]),
            helper.make_node("Add", ["sine", "cosine"], ["b"]),
            helper.make_node("Add", ["a", "b"], ["c"]),
            helper.make_node("MatMul", ["c", "ones"], ["y"]),
        ]
        arrays = {
            "offset": np.array([0, 1], np.float32),
            "reverse": np.array([1, 0], np.int64),
            "two": np.array(2, np.float32),
            "ones": np.ones((2, 1), np.float32),
        }
        graph = helper.make_graph(
            nodes,
            "shared-dag",
            [helper.make_tensor_value_info("x", TensorProto.FLOAT, [1, 2])],
            [helper.make_tensor_value_info("y", TensorProto.FLOAT, [1, 1])],
            [numpy_helper.from_array(a, n) for n, a in arrays.items()],
        )
        model = helper.make_model(
            graph, opset_imports=[helper.make_opsetid("", 13)], ir_version=8
        )
        network, prop = tmp_path / "dag.onnx", tmp_path / "dag.vnnlib"
        onnx.save(model, network)
        prop.write_text(
            "\n".join(
                [f"(declare-const X_{i} Real)" for i in range(2)]
                + ["(declare-const Y_0 Real)"]
                + [
                    f"(assert ({op} X_{i} {value}))"
                    for i in range(2)
                    for op, value in ((">=", 0), ("<=", 0 if fixed else 1))
                ]
            )
            + "\n"
            + assertions
        )
        return Instance(network, prop)

    return make


@pytest.fixture
def smooth_instance_factory(tmp_path):
    """C-order [0,1,2,3] gives z=[0,2], Y=[sigmoid(0)+2*sigmoid(2),-.5]."""

    def make(assertions):
        nodes = [
            helper.make_node(
                "Constant",
                [],
                ["shape"],
                value=numpy_helper.from_array(np.array([1, -1], dtype=np.int64)),
            ),
            helper.make_node("Reshape", ["x", "shape"], ["flat"]),
            helper.make_node("Gemm", ["flat", "w1", "b1"], ["z"]),
            helper.make_node("Sigmoid", ["z"], ["s"]),
            helper.make_node("Gemm", ["s", "w2", "b2"], ["y"]),
        ]
        arrays = {
            "w1": [[1, 0], [2, -1], [-1, 0], [0, 1]],
            "b1": [0, 0],
            "w2": [[1, -1], [2, 0]],
            "b2": [0, 0],
        }
        graph = helper.make_graph(
            nodes,
            "smooth",
            [helper.make_tensor_value_info("x", TensorProto.FLOAT, [1, 1, 2, 2])],
            [helper.make_tensor_value_info("y", TensorProto.FLOAT, [1, 2])],
            [
                numpy_helper.from_array(np.array(a, dtype=np.float32), name)
                for name, a in arrays.items()
            ],
        )
        model = helper.make_model(
            graph,
            opset_imports=[helper.make_opsetid("", 11), helper.make_opsetid("", 11)],
            ir_version=8,
        )
        network = tmp_path / "smooth.onnx"
        onnx.save(model, network)
        prop = tmp_path / "smooth.vnnlib"
        prop.write_text(
            "\n".join(
                [f"(declare-const X_{i} Real)" for i in range(4)]
                + [f"(declare-const Y_{i} Real)" for i in range(2)]
                + [
                    f"(assert ({op} X_{i} {i}))"
                    for i in range(4)
                    for op in (">=", "<=")
                ]
            )
            + "\n"
            + assertions
        )
        return Instance(network, prop)

    return make
