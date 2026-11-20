#!/usr/bin/env bash
# tests for nightly-disk-usage-watcher

set -euo pipefail

SCRIPT="../src/disk-watcher.sh"

# Helper to run script with mock df and capture output and exit code
run_test() {
  local df_mock="$1"
  local threshold="${2:-}"
  local expected_output="$3"
  local expected_exit="$4"

  if [[ -n "$threshold" ]]; then
    THRESHOLD="$threshold" DF_MOCK="$df_mock" bash "$SCRIPT" >out.txt 2>&1
    exit_code=$?
  else
    DF_MOCK="$df_mock" bash "$SCRIPT" >out.txt 2>&1
    exit_code=$?
  fi

  output=$(cat out.txt)

  if [[ "$output" != "$expected_output" ]]; then
    echo "FAIL: Unexpected output"
    echo "Got: $output"
    echo "Expected: $expected_output"
    exit 1
  fi

  if [[ "$exit_code" -ne "$expected_exit" ]]; then
    echo "FAIL: Unexpected exit code $exit_code, expected $expected_exit"
    exit 1
  fi
}

# Mock df output with two filesystems, one at 75%, one at 85%
MOCK_DF="Filesystem Size Used Avail Use% Mounted_on
/dev/sda1 100G 75G 25G 75% /
/dev/sda2 200G 170G 30G 85% /data"

# Test 1: default threshold 80, expect warning for /data
run_test "$MOCK_DF" "" "Warning: /data is at 85% usage (threshold 80%)" 1

# Test 2: higher threshold 90, no warnings
run_test "$MOCK_DF" "90" "" 0

echo "All tests passed."
