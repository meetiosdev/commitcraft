#!/bin/bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .

echo "CommitCraft installed."
echo ""
echo "Commands:"
echo "  commitcraft"
echo "  make_commit"
echo "  make_commit_message"
echo ""
echo "Example:"
echo "  commitcraft /path/to/repo"
