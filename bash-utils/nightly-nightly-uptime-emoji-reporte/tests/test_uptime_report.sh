#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/src/uptime_report.sh"

run_test() {
  local mock_seconds=$1
  local expected_output=$2
  local actual_output
  actual_output=$(UPTIME_MOCK=$mock_seconds bash "$SCRIPT_PATH")
  if [[ "$actual_output" != "$expected_output" ]]; then
    echo "FAIL: mock $mock_seconds seconds\nExpected: $expected_output\nGot:      $actual_output"
    exit 1
  else
    echo "PASS: $mock_seconds seconds"
  fi
}

# 12 hours -> 0d 12h 0m 🌱
run_test 43200 "Uptime: 12h 0m 🌱"

# 2 days 3 hours 15 minutes -> 2d 3h 15m 🌿
run_test $((2*86400 + 3*3600 + 15*60)) "Uptime: 2d 3h 15m 🌿"

# 15 days 0h 5 minutes -> 15d 0h 5m 🌳
run_test $((15*86400 + 5*60)) "Uptime: 15d 0h 5m 🌳"

# 45 days 1 hour 0 minutes -> 45d 1h 0m 🌲
run_test $((45*86400 + 3600)) "Uptime: 45d 1h 0m 🌲"

echo "All tests passed."
