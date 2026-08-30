#!/usr/bin/env bash
set -e

# Path to the script under test
SCRIPT="../src/disk_guardian.sh"

# Helper to run a test case
run_test() {
  description=$1
  expected_exit=$2
  mock_output=$3
  export MOCK_DF_OUTPUT="$mock_output"
  export THRESHOLD=${4:-80}
  if "$SCRIPT"; then
    actual_exit=0
  else
    actual_exit=$?
  fi
  if [[ $actual_exit -eq $expected_exit ]]; then
    echo "[PASS] $description"
  else
    echo "[FAIL] $description (expected exit $expected_exit, got $actual_exit)"
    exit 1
  fi
}

# Test 1: usage below threshold (60% < 80%)
run_test "usage below threshold" 0 $'Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        50G   30G   20G  60% /'

# Test 2: usage above threshold (90% >= 80%)
run_test "usage above threshold" 1 $'Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        50G   45G   5G  90% /'

# Test 3: custom higher threshold (90% < 95%)
run_test "custom threshold not exceeded" 0 $'Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        50G   45G   5G  90% /' 95

echo "All tests passed"
