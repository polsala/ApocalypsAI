#!/usr/bin/env bash
# Test suite for nightly-disk-space-guardian

SCRIPT="$(dirname "${BASH_SOURCE[0]}")/../src/disk_guardian.sh"

# Helper to compare expected vs actual output
assert_equal() {
  local expected="$1"
  local actual="$2"
  local test_name="$3"
  if [[ "$expected" != "$actual" ]]; then
    echo "FAIL [$test_name]: expected '$expected', got '$actual'"
    exit 1
  else
    echo "PASS [$test_name]"
  fi
}

# -------------------------------------------------------------------
# Test 1: Usage below threshold (should report OK)
# -------------------------------------------------------------------
export DF_OUTPUT=$'Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        100G   50G   50G  50% /'
output=$($SCRIPT 80)
expected="✅ Disk usage is safe: 50% (threshold 80%)."
assert_equal "$expected" "$output" "usage-below-threshold"

# -------------------------------------------------------------------
# Test 2: Usage above threshold (should emit a warning message)
# -------------------------------------------------------------------
export DF_OUTPUT=$'Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        100G   90G   10G  90% /'
# Capture output while allowing non‑zero exit status
output=$($SCRIPT 80 2>/dev/null || true)
# Verify that the output contains one of the known warning emojis
if [[ "$output" == *"⚠️"* || "$output" == *"🔥"* || "$output" == *"💀"* || "$output" == *"🌪️"* ]]; then
  echo "PASS [usage-above-threshold]"
else
  echo "FAIL [usage-above-threshold]: unexpected output '$output'"
  exit 1
fi

# -------------------------------------------------------------------
# Test 3: Invalid df output (should exit with code 2)
# -------------------------------------------------------------------
export DF_OUTPUT=$'invalid output that does not contain percentages'
set +e  # allow script to exit with non‑zero status
$SCRIPT 80 >/dev/null 2>&1
status=$?
set -e
if [[ $status -eq 2 ]]; then
  echo "PASS [invalid-df-output]"
else
  echo "FAIL [invalid-df-output]: expected exit code 2, got $status"
  exit 1
fi

echo "All tests passed."
