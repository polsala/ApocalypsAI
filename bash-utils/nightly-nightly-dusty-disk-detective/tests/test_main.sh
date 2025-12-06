#!/usr/bin/env bash
set -euo pipefail

# Resolve the repository root for this utility
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)

# Prepend the mock directory to PATH so our mock `df` is used
export PATH="${ROOT}/tests/mocks:${PATH}"

# Helper to run the script and capture output
run_script() {
  local threshold=$1
  DISK_USAGE=$2 "${ROOT}/src/main.sh" "${threshold}"
}

# Test case 1: usage below threshold (no warning)
output=$(run_script 90 30)
if [[ "$output" != *"within safe limits"* ]]; then
  echo "FAIL: Expected safe‑limit message, got: $output"
  exit 1
fi

# Test case 2: usage above threshold (warning with ASCII art)
output=$(run_script 50 90)
if [[ "$output" != *"Warning"* || "$output" != *"_____"* ]]; then
  echo "FAIL: Expected warning with ASCII art, got: $output"
  exit 1
fi

echo "All tests passed"
