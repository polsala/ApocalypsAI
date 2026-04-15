#!/usr/bin/env bash
# Tests for nightly-disk-guardian

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT_PATH="${SCRIPT_DIR}/disk_guardian.sh"

# Helper to run script and capture exit code
run_script() {
  local mount="$1"
  local threshold="$2"
  local df_output="$3"
  DF_OUTPUT="${df_output}" "${SCRIPT_PATH}" "${mount}" "${threshold}"
  echo "$?"
}

# Test 1: usage below threshold (45% < 80%)
exit_code=$(run_script "/" "80" "45%")
if [[ "$exit_code" -ne 0 ]]; then
  echo "Test 1 failed: expected exit 0, got $exit_code"
  exit 1
fi

# Test 2: usage above threshold (92% > 80%)
output=$(DF_OUTPUT="92%" "${SCRIPT_PATH}" "/" "80" 2>&1) || true
exit_code=$?
if [[ "$exit_code" -ne 1 ]]; then
  echo "Test 2 failed: expected exit 1, got $exit_code"
  exit 1
fi
# Ensure output contains one of the warning messages
if ! echo "$output" | grep -E "The void|fire|Radiation|Zombies|tornado"; then
  echo "Test 2 failed: warning message not found"
  exit 1
fi

echo "All tests passed."
