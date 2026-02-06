#!/usr/bin/env bash
set -euo pipefail

# Path to the utility under test
UTIL="./src/main.sh"

# ------------------------------------------------------------
# Test 1: Argument input
# ------------------------------------------------------------
output=$($UTIL "Hello")
expected="VXJ5eWI="
if [[ "$output" == "$expected" ]]; then
  echo "Test 1 passed"
else
  echo "Test 1 failed: expected $expected, got $output"
  exit 1
fi

# ------------------------------------------------------------
# Test 2: Piped input
# ------------------------------------------------------------
output=$(echo "Secret" | $UTIL)
expected2="RnJwZXJn"
if [[ "$output" == "$expected2" ]]; then
  echo "Test 2 passed"
else
  echo "Test 2 failed: expected $expected2, got $output"
  exit 1
fi

# ------------------------------------------------------------
# Test 3: No input should exit with status 1
# ------------------------------------------------------------
set +e
$UTIL >/dev/null 2>&1
status=$?
set -e
if [[ $status -ne 1 ]]; then
  echo "Test 3 failed: expected exit status 1, got $status"
  exit 1
else
  echo "Test 3 passed"
fi

echo "All tests passed"
