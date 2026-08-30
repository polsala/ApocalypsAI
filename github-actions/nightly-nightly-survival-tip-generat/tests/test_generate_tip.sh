#!/usr/bin/env bash
set -euo pipefail

# Create a temporary file to mock GITHUB_OUTPUT
tmp_output=$(mktemp)
export GITHUB_OUTPUT="$tmp_output"

# Run the script with a known seed (3) – expected tip is the 4th entry
./src/generate_tip.sh 3

# Capture the output written by the script
output=$(cat "$tmp_output")
expected="survival_tip=Map your shelter with chalk before the dust settles."

if [[ "$output" == "$expected" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$expected' but got '$output'"
  exit 1
fi
