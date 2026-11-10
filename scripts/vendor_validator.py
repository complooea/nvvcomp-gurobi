"""Refresh the pinned V1 validator subset without changing replay behavior."""

import ast
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

REVISION = "eea564f5d0a8751d8321a409214db14d03f452b8"
BASE = f"https://raw.githubusercontent.com/VNN-COMP/vnncomp2026_results/{REVISION}/"
DEST = Path(__file__).resolve().parents[1] / "src/nvvcomp_gurobi/_vendor"


def main():
    DEST.mkdir(exist_ok=True)
    sources = {}
    for name in ["SCORING/counterexamples.py", "SCORING/vnnlib_v1.py", "LICENSE"]:
        with urlopen(BASE + name) as response:
            sources[name] = response.read().decode()
    counterexamples = sources["SCORING/counterexamples.py"]
    prefix = counterexamples[: counterexamples.index("def _rebased_benchmark_path")]
    prefix = prefix.replace("from vnnlib_v1 import", "from .vnnlib_v1 import")
    prefix = prefix.replace(
        "from cex_checks import CPU_PROVIDER", 'CPU_PROVIDER = "CPUExecutionProvider"'
    )
    prefix = prefix.replace("from settings import Settings", "")
    selected = {"CounterexampleResult", "get_ce_diff", "is_specification_vio"}
    lines = counterexamples.splitlines(keepends=True)
    pieces = [prefix]
    for node in ast.parse(counterexamples).body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in selected:
            start = min([node.lineno] + [d.lineno for d in node.decorator_list])
            pieces.append("".join(lines[start - 1 : node.end_lineno]) + "\n\n")
    (DEST / "counterexamples.py").write_text("".join(pieces).rstrip() + "\n")
    (DEST / "vnnlib_v1.py").write_text(sources["SCORING/vnnlib_v1.py"])
    (DEST / "LICENSE").write_text(sources["LICENSE"])
    (DEST / "sources.json").write_text(
        json.dumps(
            {
                "repository": "VNN-COMP/vnncomp2026_results",
                "revision": REVISION,
                "upstream_sha256": {
                    name: hashlib.sha256(text.encode()).hexdigest()
                    for name, text in sources.items()
                },
                "changes": "V1 replay dependency closure only; relative import and CPU provider constant. No replay logic changes.",
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
