#!/usr/bin/env bash

# Tests for nightly-uptime-emoji_report.sh
# These tests are deterministic and do not rely on the actual system state.

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SCRIPT="$SCRIPT_DIR/src/uptime_emoji_report.sh"

# Helper to run the script with optional mocks and capture output
run_script() {
  MOCK_LOAD=$1 MOCK_CORES=$2 bash "$SCRIPT"
}

# Test case 1: Light load → 😊
output=$(run_script 0.3 4)
expected="System uptime:"
if [[ "$output" != *"😊"* ]]; then
  echo "FAIL: Light load should produce 😊. Got: $output"
  exit 1
fi

# Test case 2: Moderate load → 😐
output=$(run_script 2.0 4)  # 2.0/4 = 0.5 per core (boundary case, still 😊)
# Adjust to 2.5 to be >0.5 but <=1.0 per core
output=$(run_script 2.5 4)  # 0.625 per core → 😐
if [[ "$output" != *"😐"* ]]; then
  echo "FAIL: Moderate load should produce 😐. Got: $output"
  exit 1
fi

# Test case 3: Heavy load → 😫
output=$(run_script 5.0 4)  # 1.25 per core → 😫
if [[ "$output" != *"😫"* ]]; then
  echo "FAIL: Heavy load should produce 😫. Got: $output"
  exit 1
fi

# Test case 4: Zero cores fallback (should not divide by zero)
output=$(run_script 0.5 0)
if [[ "$output" == *"division by zero"* ]]; then
  echo "FAIL: Division by zero occurred when cores=0"
  exit 1
fi

# All tests passed
echo "All tests passed."
exit 0
