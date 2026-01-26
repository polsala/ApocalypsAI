#!/usr/bin/env bash
set -euo pipefail

# Helper to run script and capture output and exit code
run_script() {
  local proc_file=$1
  local threshold=$2
  local output
  local exit_code

  export PROC_STAT="$proc_file"
  output=$(./src/main.sh "$threshold" 2>&1)
  exit_code=$?
  echo "$output"
  return $exit_code
}

# Test 1: usage below threshold
tmpfile=$(mktemp)
echo "cpu  100 0 100 700 0 0 0 0 0 0" > "$tmpfile"
output=$(run_script "$tmpfile" 80)
exit_code=$?
if [[ $exit_code -ne 0 ]]; then
  echo "Test 1 failed: expected exit 0, got $exit_code"
  exit 1
fi
if [[ $output != *"CPU is calm"* ]]; then
  echo "Test 1 failed: output does not contain 'CPU is calm'"
  exit 1
fi

# Test 2: usage above threshold

echo "cpu  100 0 100 10 0 0 0 0 0 0" > "$tmpfile"
output=$(run_script "$tmpfile" 80)
exit_code=$?
if [[ $exit_code -ne 1 ]]; then
  echo "Test 2 failed: expected exit 1, got $exit_code"
  exit 1
fi
if [[ $output != *"CPU is feeling hungry"* ]]; then
  echo "Test 2 failed: output does not contain 'CPU is feeling hungry'"
  exit 1
fi

rm -f "$tmpfile"
echo "All tests passed."
