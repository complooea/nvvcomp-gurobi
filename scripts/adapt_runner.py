"""Make a standalone, version-guarded VNN-COMP runner copy; never edit upstream."""

import argparse
import hashlib
from pathlib import Path

REVISION = "3d5a8848169fc5f0cc03ab9722865235e9857f16"
SHA256 = "2c69d6606c4bf6888de6c198fe27f000219b64bee2fc24460781752d536e14f7"

# Embedded so run_benchmark.sh can ship the resulting single file to the node.
# No tool-environment imports or validation policy changes at the archive boundary.
ARCHIVE = """    # Repo-owned adapter: keep result intact, archive only the SAT witness.
    ce="${ce_dir}/$(basename "$onnx" .onnx)_$(basename "$vnnlib" .vnnlib).counterexample"
    rm -f "$ce"
    if [ "$verdict" = "sat" ] || [ "$verdict" = "violated" ]; then
        if ! python3 - "$out" "$ce" <<'NVVCOMP_ARCHIVE'
import pathlib
import math
import re
import sys

source, destination = map(pathlib.Path, sys.argv[1:])
header, separator, body = source.read_bytes().partition(b"\\n")
if header.strip() not in (b"sat", b"violated") or not separator or not body.strip():
    sys.exit("Invalid SAT result: missing witness")
number = rb"[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?"
assignment = rb"\\(\\s*([XY]_[0-9]+)\\s+(" + number + rb")\\s*\\)"
if not re.fullmatch(rb"\\s*\\(\\s*(?:" + assignment + rb"\\s*)+\\)\\s*", body):
    sys.exit("Invalid SAT result: malformed witness")
values = re.findall(assignment, body)
if len({name for name, _ in values}) != len(values) or not all(
    math.isfinite(float(value)) for _, value in values
):
    sys.exit("Invalid SAT result: duplicate or nonfinite assignment")
temporary = destination.with_suffix(".counterexample.tmp")
temporary.write_bytes(body)
temporary.replace(destination)
NVVCOMP_ARCHIVE
        then
            verdict=error_invalid_counterexample
        fi
    fi
    record "$prepare_time" "$verdict" "$runtime"
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help=f"run_instances.sh at {REVISION}")
    parser.add_argument(
        "output", type=Path, help="new standalone runner (must not exist)"
    )
    args = parser.parse_args()
    original = args.source.read_bytes()
    if hashlib.sha256(original).hexdigest() != SHA256:
        parser.error(f"runner does not match pinned revision {REVISION} ({SHA256})")
    text = original.decode()
    # Optional relocation for local replay; normal platform paths remain unchanged.
    text = text.replace(
        'if [ -d "/app" ]',
        'if [ -n "${NVVCOMP_BASE_DIR:-}" ]; then\n'
        '    IS_LOCAL=1\n    BASE_DIR="${NVVCOMP_BASE_DIR}"\n'
        '    bench_rel="${NVVCOMP_BENCH_REL:?set benchmark-relative directory}"\n'
        'elif [ -d "/app" ]',
        1,
    )
    text = text.replace(
        'out="/tmp/result_${task_id}.txt"',
        'out="${TMPDIR:-/tmp}/result_${task_id}.txt"',
    )
    text = text.replace(
        "report() {  # success|failure — POST the log tail so it survives node teardown\n",
        "report() {  # success|failure — POST the log tail so it survives node teardown\n"
        '    [ "${NVVCOMP_NO_REPORT:-0}" = "1" ] && return 0\n',
    )
    start = text.index('    record "$prepare_time" "$verdict" "$runtime"')
    end = text.index("done <<EOF", start)
    text = text[:start] + ARCHIVE + text[end:]
    with args.output.open("x") as stream:
        stream.write(text)
    args.output.chmod(0o755)


if __name__ == "__main__":
    main()
