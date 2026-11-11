#!/bin/sh
set -eu
if [ "$#" -ne 1 ] || [ "$1" != v1 ]; then
    echo "Usage: install_tool.sh v1" >&2
    exit 2
fi
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
command -v uv >/dev/null 2>&1 || { echo "Install uv 0.13.6 before running this script" >&2; exit 1; }
cd "$ROOT"
exec uv sync --locked --extra solver --no-dev
