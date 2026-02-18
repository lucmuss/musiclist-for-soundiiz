#!/usr/bin/env bash
set -euo pipefail

echo "Running tests..."
python -m pytest tests/ -v --tb=short
echo "Tests passed."

exec /app/scripts/bootstrap.sh run "$@"
