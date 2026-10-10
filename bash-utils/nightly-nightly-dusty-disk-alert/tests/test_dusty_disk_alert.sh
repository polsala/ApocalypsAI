#!/usr/bin/env bash
set -euo pipefail

# Path to the script under test
SCRIPT="../src/dusty_disk_alert.sh"

# Helper function for assertions
assert_equals() {
  local expected="$1"
  local actual="$2"
  local test_name="$3"
  if [[ "$expected" == "$actual" ]]; then
    echo "[PASS] $test_name"
  else
    echo "[FAIL] $test_name"
    echo "  Expected: $expected"
    echo "  Actual  : $actual"
    exit 1
  fi
}

# Mock df output with 85% usage
MOCK_DF_HIGH="Filesystem      Size  Used Avail Use% Mounted on\n/dev/root        20G   17G   3G  85% /"
# Run script with threshold 80 and mock flag
OUTPUT_HIGH=$(echo "$MOCK_DF_HIGH" | bash "$SCRIPT" 80 --mock)
# Expect a warning line starting with the warning emoji
if [[ "$OUTPUT_HIGH" =~ ^⚠️ ]]; then
  echo "[PASS] High usage warning emitted"
else
  echo "[FAIL] High usage warning not emitted"
  echo "Output: $OUTPUT_HIGH"
  exit 1
fi

# Mock df output with 50% usage
MOCK_DF_LOW="Filesystem      Size  Used Avail Use% Mounted on\n/dev/root        20G   10G   10G  50% /"
OUTPUT_LOW=$(echo "$MOCK_DF_LOW" | bash "$SCRIPT" 80 --mock)
EXPECTED_LOW="✅ All clear: 50% used"
assert_equals "$EXPECTED_LOW" "$OUTPUT_LOW" "Low usage all‑clear message"

# End of tests
