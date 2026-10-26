#!/usr/bin/env bash
# Test suite for nightly-disk-guardian
#
# These tests are deliberately simple and run with POSIX sh.
# They rely on the script's --mock-output flag to provide deterministic input.

set -euo pipefail
SCRIPT_DIR=$(cd "$(dirname "$0")/.." && pwd)
UTIL="$SCRIPT_DIR/src/disk_guardian.sh"

# Helper to run the script and capture exit code and output
run_guardian() {
  local mock_output="$1"
  local threshold="$2"
  if [[ -z "$threshold" ]]; then
    output=$($UTIL --mock-output "$mock_output" 2>&1) || rc=$?
  else
    output=$($UTIL "$threshold" --mock-output "$mock_output" 2>&1) || rc=$?
  fi
  rc=${rc:-0}
  echo "RC=$rc"
  echo "$output"
}

# Test 1: Usage below threshold (expect happy message, exit 0)
mock_low="Filesystem Size Used Avail Use% Mounted on\n/dev/sda1 100G 40G 60G 40% /"
result=$(run_guardian "$mock_low" 80)
if echo "$result" | grep -q "All clear" && echo "$result" | grep -q "RC=0"; then
  echo "PASS: low usage below threshold"
else
  echo "FAIL: low usage test" >&2
  exit 1
fi

# Test 2: Usage above threshold (expect warning, exit 1)
mock_high="Filesystem Size Used Avail Use% Mounted on\n/dev/sda1 100G 85G 15G 85% /"
result=$(run_guardian "$mock_high" 80)
if echo "$result" | grep -q "WARNING" && echo "$result" | grep -q "RC=1"; then
  echo "PASS: high usage above threshold"
else
  echo "FAIL: high usage test" >&2
  exit 1
fi

# Test 3: Custom threshold (90%) with 85% usage should be OK
mock_mid="Filesystem Size Used Avail Use% Mounted on\n/dev/sda1 100G 85G 15G 85% /"
result=$(run_guardian "$mock_mid" 90)
if echo "$result" | grep -q "All clear" && echo "$result" | grep -q "RC=0"; then
  echo "PASS: custom threshold respected"
else
  echo "FAIL: custom threshold test" >&2
  exit 1
fi

echo "All tests passed."
