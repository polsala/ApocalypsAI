#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="${SCRIPT_DIR}/disk_usage_alert.sh"

PASS=0

run_test() {
  local df_output="$1"
  local threshold="$2"
  local expected_exit="$3"
  local expected_msg="$4"

  DF_OUTPUT="$df_output" "$SCRIPT" "$threshold" >output.txt 2>&1
  local exit_code=$?
  local output
  output=$(cat output.txt)

  if [[ $exit_code -ne $expected_exit ]]; then
    echo "FAIL: Expected exit $expected_exit, got $exit_code"
    echo "Output: $output"
    return 1
  fi
  if [[ "$output" != *"$expected_msg"* ]]; then
    echo "FAIL: Expected message containing '$expected_msg'"
    echo "Output: $output"
    return 1
  fi
  echo "PASS"
  return 0
}

# Test 1: usage 50%, threshold 80 -> OK
df1="Filesystem Size Used Avail Use% Mounted on\n/dev/sda1 100G 50G 50G 50% /"
run_test "$df1" "80" 0 "OK: usage 50%" && PASS=$((PASS+1))

# Test 2: usage 90%, threshold 80 -> ALERT
df2="Filesystem Size Used Avail Use% Mounted on\n/dev/sda1 100G 90G 10G 90% /"
run_test "$df2" "80" 1 "ALERT: usage 90% exceeds threshold 80%" && PASS=$((PASS+1))

if [[ $PASS -eq 2 ]]; then
  echo "All tests passed"
  exit 0
else
  echo "$PASS/2 tests passed"
  exit 1
fi
