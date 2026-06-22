#!/usr/bin/env bash
set -euo pipefail

# Path to the script under test
SCRIPT="../src/disk_alert.sh"

# Helper to run the script with a mock df output and optional threshold
run_test() {
  local mock_df="$1"
  local threshold="$2"
  local expected_exit="$3"
  local expected_msg="$4"

  if [[ -n "$threshold" ]]; then
    THRESHOLD="$threshold" DISK_USAGE_OUTPUT="$mock_df" bash "$SCRIPT" >output.txt 2>&1
  else
    DISK_USAGE_OUTPUT="$mock_df" bash "$SCRIPT" >output.txt 2>&1
  fi
  local exit_code=$?
  local output=$(cat output.txt)

  if [[ $exit_code -ne $expected_exit ]]; then
    echo "FAIL: expected exit $expected_exit, got $exit_code"
    echo "Output: $output"
    exit 1
  fi
  if [[ "$output" != *"$expected_msg"* ]]; then
    echo "FAIL: expected message containing '$expected_msg', got '$output'"
    exit 1
  fi
  echo "PASS"
}

# Mock df outputs
mock_low="Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        100G   30G   70G  30% /"
mock_high="Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        100G   95G    5G  95% /"
mock_invalid="Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        100G   30G   70G  N/A /"

echo "Test low usage (below default threshold)..."
run_test "$mock_low" "" 0 "OK: disk usage is 30%"

echo "Test high usage (above default threshold)..."
run_test "$mock_high" "" 1 "Warning: disk usage is 95%"

echo "Test custom threshold 90% with high usage..."
run_test "$mock_high" "90" 1 "Warning: disk usage is 95%"

echo "Test custom threshold 99% with high usage..."
run_test "$mock_high" "99" 0 "OK: disk usage is 95%"

echo "Test invalid usage parsing..."
run_test "$mock_invalid" "" 2 "Error: non‑numeric usage value"
