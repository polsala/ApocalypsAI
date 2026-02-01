#!/usr/bin/env bash
set -euo pipefail

# Determine repository root (two levels up from this file)
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$DIR/src/main.sh"

run() {
  "$SCRIPT" "$@"
}

assert_eq() {
  local expected="$1"
  local actual="$2"
  if [[ "$expected" != "$actual" ]]; then
    echo "Assertion failed: expected '$expected', got '$actual'"
    exit 1
  fi
}

# ------------------------------------------------------------
# Test 1 – mixed hours and minutes
# ------------------------------------------------------------
out=$(run 2h15m)
assert_eq "8100" "$out"

# ------------------------------------------------------------
# Test 2 – seconds only
# ------------------------------------------------------------
out=$(run 45s)
assert_eq "45" "$out"

# ------------------------------------------------------------
# Test 3 – egg mode includes ASCII art
# ------------------------------------------------------------
out=$(run --egg 10s)
first_line=$(echo "$out" | head -n1)
assert_eq "10" "$first_line"
if ! echo "$out" | grep -q "crack"; then
  echo "Egg art not found in output"
  exit 1
fi

echo "All tests passed"
