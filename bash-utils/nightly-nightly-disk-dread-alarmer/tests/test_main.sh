#!/usr/bin/env bash
set -euo pipefail

# Load the implementation (functions only, no execution)
source "$(dirname "$0")/../src/main.sh"

# Mock numfmt to produce deterministic output (simply echo the raw argument)
numfmt() {
  echo "$1"
}

# Test: size below threshold should yield a success message
output=$(check_size "testdir" 50000 102400)
expected="✅  testdir is within safe limits."
if [[ "$output" != "$expected" ]]; then
  echo "FAIL: expected '$expected' but got '$output'"
  exit 1
fi

# Test: size above threshold should yield a warning message
output=$(check_size "testdir" 200000 102400)
expected="⚠️  The abyss of testdir grows to 200000K!"
if [[ "$output" != "$expected" ]]; then
  echo "FAIL: expected '$expected' but got '$output'"
  exit 1
fi

echo "All tests passed."
