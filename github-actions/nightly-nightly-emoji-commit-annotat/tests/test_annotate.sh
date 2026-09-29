#!/usr/bin/env bash
set -e

# Mock the GITHUB_OUTPUT file that the action writes to
export GITHUB_OUTPUT=$(mktemp)

# Force a known seed so the emoji selection is predictable (index 2 -> "🔥")
export SEED=2

# Sample commit message
message="Fix bug in parser"

# Run the script (relative path assumes execution from repository root)
./src/annotate.sh "$message"

# Capture the output written by the script
output=$(cat "$GITHUB_OUTPUT")
expected="annotated_message=🔥 Fix bug in parser"

if [[ "$output" == "$expected" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$expected' but got '$output'"
  exit 1
fi
