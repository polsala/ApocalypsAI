#!/usr/bin/env bash

# Tests for nightly-disk-space-guardian
# These tests mock the `df` command to provide deterministic output.

set -euo pipefail

# Load the script under test
source "../src/check_disk.sh"

# Helper to run a check and capture output and exit code
run_check() {
  local threshold=$1
  local output
  local exit_code
  output=$(check_disk_usage "$threshold" 2>&1) || exit_code=$?
  # If the function returned 0, the above || does not set exit_code, so capture it manually
  if [[ -z ${exit_code+x} ]]; then
    exit_code=0
  fi
  echo "$output"
  return $exit_code
}

# Mock df for low usage (60%)
df() {
  echo -e "Filesystem\tSize\tUsed\tAvail\tUse%\tMounted on"
  echo -e "/dev/sda1\t20G\t12G\t8G\t60%\t/"
}

# Test: usage below threshold
output=$(run_check 80)
code=$?
if [[ $code -ne 0 ]]; then
  echo "FAIL: Expected exit code 0 for low usage, got $code"
  exit 1
fi
expected="✅ Disk usage is at 60%, below threshold 80%."
if [[ "$output" != "$expected" ]]; then
  echo "FAIL: Unexpected output for low usage."
  echo "Got:    $output"
  echo "Expect: $expected"
  exit 1
fi

# Mock df for high usage (92%)
df() {
  echo -e "Filesystem\tSize\tUsed\tAvail\tUse%\tMounted on"
  echo -e "/dev/sda1\t20G\t18G\t2G\t92%\t/"
}

# Test: usage above threshold
output=$(run_check 80)
code=$?
if [[ $code -ne 1 ]]; then
  echo "FAIL: Expected exit code 1 for high usage, got $code"
  exit 1
fi
expected="⚠️ Disk usage is at 92%, exceeds threshold 80%!"
if [[ "$output" != "$expected" ]]; then
  echo "FAIL: Unexpected output for high usage."
  echo "Got:    $output"
  echo "Expect: $expected"
  exit 1
fi

echo "All tests passed."
