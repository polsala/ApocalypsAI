#!/usr/bin/env bash
set -e

# Path to the script under test
SCRIPT_PATH="../src/disk_emoji_report.sh"

# Helper to run a single test case
run_test() {
  local mock_df="$1"
  local expected="$2"
  export MOCK_DF="$mock_df"
  result=$($SCRIPT_PATH "/")
  if [[ "$result" != "$expected" ]]; then
    echo "Test failed: expected '$expected', got '$result'"
    exit 1
  fi
}

# Test case 1: low usage (30%) → 🟢
run_test "Filesystem Size Used Avail Use% Mounted on\n/dev/sda1 100G 30G 70G 30% /" "🟢 30% /"

# Test case 2: medium usage (70%) → 🟡
run_test "Filesystem Size Used Avail Use% Mounted on\n/dev/sda1 100G 70G 30G 70% /" "🟡 70% /"

# Test case 3: high usage (95%) → 🔴
run_test "Filesystem Size Used Avail Use% Mounted on\n/dev/sda1 100G 95G 5G 95% /" "🔴 95% /"

echo "All tests passed."
