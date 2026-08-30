#!/usr/bin/env bash
set -euo pipefail

# Path to the script under test.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/disk_alert.sh"

# Helper to run the script with a mocked `df` output.
run_with_mock() {
  local mock_df="$1"
  local threshold="${2:-}"
  DISK_ALERT_DF_MOCK="$mock_df" bash "$SCRIPT" $threshold
}

# Test 1: No filesystem exceeds the default 80% threshold.
mock1="Filesystem Size Used Avail Use% Mounted on
/dev/sda1 100G 40G 60G 40% /
/dev/sda2 200G 100G 100G 50% /home"
output=$(run_with_mock "$mock1")
if [[ -n "$output" ]]; then
  echo "Test 1 failed: expected no output, got '$output'"
  exit 1
fi

# Test 2: One filesystem exceeds the default threshold.
mock2="Filesystem Size Used Avail Use% Mounted on
/dev/sda1 100G 95G 5G 95% /
/dev/sda2 200G 100G 100G 50% /home"
output=$(run_with_mock "$mock2")
expected="ALERT: / at 95% usage"
if [[ "$output" != "$expected" ]]; then
  echo "Test 2 failed: expected '$expected', got '$output'"
  exit 1
fi

# Test 3: Custom threshold higher than usage; should produce no alert.
mock3="Filesystem Size Used Avail Use% Mounted on
/dev/sda1 100G 85G 15G 85% /"
output=$(run_with_mock "$mock3" 90)
if [[ -n "$output" ]]; then
  echo "Test 3 failed: expected no output with threshold 90, got '$output'"
  exit 1
fi

echo "All tests passed."
