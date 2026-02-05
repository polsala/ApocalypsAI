#!/usr/bin/env bash
set -e

# Mock inputs
export INPUT_MESSAGE="Hello world"
export SEED=0

# Capture output
output=$(node src/main.js)

# Expected annotation
expected="Hello world 🌟"

if [[ "$output" == *"$expected"* ]]; then
  echo "Test passed"
  exit 0
else
  echo "Test failed"
  echo "Got: $output"
  exit 1
fi
