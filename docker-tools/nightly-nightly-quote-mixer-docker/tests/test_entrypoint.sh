#!/bin/sh
set -e

# Test that the entrypoint prints the expected quote when QUOTE_INDEX is set
output=$(QUOTE_INDEX=3 sh ./entrypoint.sh)
expected="Stay calm and carry a spare bunker."

if [ "$output" = "$expected" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$expected' got '$output'"
  exit 1
fi
