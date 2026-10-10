#!/usr/bin/env bash
set -euo pipefail

# Load the entrypoint script from the repository root
SCRIPT_PATH="$(dirname "${BASH_SOURCE[0]}")/../src/entrypoint.sh"

# Mock a morning timestamp (08:00 UTC) via DATE_OVERRIDE
export DATE_OVERRIDE="2023-01-01T08:00:00Z"

# Capture the script output
output=$(bash "$SCRIPT_PATH")

# Expected emoji for morning period is the first in the list: ☀️
expected="☀️"

if [[ "$output" == "$expected" ]]; then
  echo "PASS: Expected '$expected', got '$output'"
  exit 0
else
  echo "FAIL: Expected '$expected', got '$output'"
  exit 1
fi
