#!/usr/bin/env bash
set -euo pipefail

# Helper to run the script with optional threshold and mocked df output
run_main() {
  local thresh="${1:-}"
  local mock_output="${2:-}"
  export MOCK_DF_OUTPUT="$mock_output"
  local script_path="$(dirname "${BASH_SOURCE[0]}")/../src/disk_warden.sh"
  local out
  local code
  if [[ -z "$thresh" ]]; then
    out=$(bash "$script_path" 2>&1)
    code=$?
  else
    out=$(bash "$script_path" "$thresh" 2>&1)
    code=$?
  fi
  unset MOCK_DF_OUTPUT
  echo "$code:$out"
}

# Test 1: usage below threshold (should succeed)
test_below_threshold() {
  local result
  result=$(run_main 80 "15")
  local code="${result%%:*}"
  local output="${result#*:}"
  if [[ "$code" -ne 0 ]] || [[ "$output" != *"✅"* ]]; then
    echo "FAIL: expected success below threshold"
    exit 1
  fi
}

# Test 2: usage above threshold (should warn)
test_above_threshold() {
  local result
  result=$(run_main 50 "75")
  local code="${result%%:*}"
  local output="${result#*:}"
  if [[ "$code" -ne 2 ]] || [[ "$output" != *"⚠️"* ]]; then
    echo "FAIL: expected warning above threshold"
    exit 1
  fi
}

# Test 3: invalid threshold argument (should error)
test_invalid_threshold() {
  local result
  result=$(run_main "abc" "10")
  local code="${result%%:*}"
  if [[ "$code" -ne 1 ]]; then
    echo "FAIL: expected error on invalid threshold"
    exit 1
  fi
}

test_below_threshold
test_above_threshold
test_invalid_threshold

echo "All tests passed."
