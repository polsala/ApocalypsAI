#!/usr/bin/env bash
# Tests for nightly-ramen-noodle-timer

set -euo pipefail

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)/timer.sh"

# Helper to capture output
run_timer() {
  env SKIP_SLEEP=1 "$SCRIPT_PATH" "$@"
}

# Test 1: Known noodle type (ramen)
output=$(run_timer ramen)
expected="Recommended cooking time for ramen: 8 minute(s)."
if [[ "$output" != "$expected" ]]; then
  echo "FAIL: ramen test. Expected '$expected', got '$output'"
  exit 1
fi

echo "PASS: ramen test"

# Test 2: Unknown noodle type should exit with usage message
set +e
run_output=$(env SKIP_SLEEP=1 "$SCRIPT_PATH" unknown 2>&1)
status=$?
set -e
if [[ $status -eq 0 ]]; then
  echo "FAIL: unknown noodle type did not exit with error"
  exit 1
fi
if [[ "$run_output" != *"Error: Unknown noodle type 'unknown'."* ]]; then
  echo "FAIL: unknown noodle type error message mismatch"
  exit 1
fi

echo "PASS: unknown noodle type test"

# Test 3: Case‑insensitivity (Udon)
output=$(run_timer UDoN)
expected="Recommended cooking time for udon: 12 minute(s)."
if [[ "$output" != "$expected" ]]; then
  echo "FAIL: case‑insensitivity test. Expected '$expected', got '$output'"
  exit 1
fi

echo "PASS: case‑insensitivity test"

# All tests passed
exit 0
