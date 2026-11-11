#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec "$ROOT/.venv/bin/python" -m nvvcomp_gurobi.competition run "$@"
