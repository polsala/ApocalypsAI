#!/usr/bin/env bash
set -euo pipefail

# Mock environment variable with a known set of changed files
export CHANGED_FILES="README.md,src/app.js,server/main.py"

# Run the labeler script
output=$(bash $(dirname "$0")/../src/labeler.sh)

# Expected comma‑separated labels (order matches detection order)
expected="docs,frontend,backend"

if [[ "$output" == "$expected" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$expected' but got '$output'"
  exit 1
fi
