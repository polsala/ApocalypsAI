#!/usr/bin/env bash
set -euo pipefail

# Test with arguments
output=$(./src/run.sh \"Hello, World!\")
expected=\"Uryyb, Jbeyq!\"
if [ "$output" != "$expected" ]; then
  echo \"FAIL: args test failed. Expected '$expected', got '$output'\"
  exit 1
fi

# Test with stdin
output=$(echo \"Hello\" | ./src/run.sh)
expected=\"Uryyb\"
if [ "$output" != "$expected" ]; then
  echo \"FAIL: stdin test failed. Expected '$expected', got '$output'\"
  exit 1
fi

echo \"All tests passed.\"
