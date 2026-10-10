#!/usr/bin/env bash

# Test suite for disk_guardian.sh

set -euo pipefail

SCRIPT="../src/disk_guardian.sh"

run_test() {
  local mock_output="$1"
  local threshold="$2"
  local expected_exit="$3"
  local expected_substring="$4"

  export DF_OUTPUT="$mock_output"

  # Capture output and exit code
  output=$($SCRIPT "$threshold" 2>&1) || exit_code=$?
  exit_code=${exit_code:-0}

  if [[ $exit_code -ne $expected_exit ]]; then
    echo "FAIL: Expected exit $expected_exit, got $exit_code"
    echo "Output: $output"
    exit 1
  fi

  if [[ -n "$expected_substring" && "$output" != *"$expected_substring"* ]]; then
    echo "FAIL: Expected output to contain '$expected_substring'"
    echo "Output: $output"
    exit 1
  fi

  echo "PASS"
}

# Test 1: usage below default threshold (80%)
run_test "dev/sda1 100G 30G 70G 30% /" "80" 0 "all clear"

# Test 2: usage above default threshold (80%)
run_test "dev/sda1 100G 85G 15G 85% /" "80" 1 "Disk usage is at 85%"

# Test 3: custom lower threshold triggers warning
run_test "dev/sda1 100G 60G 40G 60% /" "50" 1 "Disk usage is at 60%"

echo "All tests passed."
