#!/usr/bin/env bash

# nightly-uptime-chronicle tests
# These tests run without any external dependencies and do not touch the real system uptime.

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
UTIL="$PROJECT_ROOT/src/uptime-chronicle.sh"

# Helper to run the script with a fixed seed for deterministic suffix selection
run_with_seed() {
  local seconds=$1
  local seed=$2
  UPTIME_CHRONICLE_SEED=$seed "$UTIL" "$seconds"
}

# Test 1: 1 day, 1 hour, 1 minute (90061 seconds)
output=$(run_with_seed 90061 0)
# Expected phrase (suffix may vary, so we only check the time part)
if [[ "$output" != *"1 day, 1 hour, and 1 minute"* ]]; then
  echo "Test 1 failed: unexpected output -> $output"
  exit 1
fi

echo "Test 1 passed"

# Test 2: zero uptime
output=$(run_with_seed 0 1)
if [[ "$output" != *"0 days, 0 hours, and 0 minutes"* ]]; then
  echo "Test 2 failed: unexpected output -> $output"
  exit 1
fi

echo "Test 2 passed"

# Test 3: Verify deterministic suffix selection with same seed
out_a=$(run_with_seed 12345 42)
out_b=$(run_with_seed 12345 42)
if [[ "$out_a" != "$out_b" ]]; then
  echo "Test 3 failed: outputs differ with same seed"
  echo "A: $out_a"
  echo "B: $out_b"
  exit 1
fi

echo "Test 3 passed"

# All tests passed
exit 0
