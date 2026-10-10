#!/usr/bin/env bash
# Tests for nightly-random-ansi-colorizer

set -e

# Mock RANDOM to make deterministic
RANDOM=1

# Expected color: idx = 1 % 6 = 1, colors[1]=32 (green)
expected_color=32
input="TestMessage"
output=$(./src/colorize.sh "$input")

# Build expected output
expected=$(printf "\e[%sm%s\e[0m" "$expected_color" "$input")

if [[ "$output" != "$expected" ]]; then
  echo "FAIL: Expected '$expected' but got '$output'"
  exit 1
else
  echo "PASS"
fi

# Test reading from stdin
RANDOM=3  # idx = 3 % 6 = 3, colors[3]=34 (blue)
expected_color=34
output=$(echo "$input" | ./src/colorize.sh)
expected=$(printf "\e[%sm%s\e[0m" "$expected_color" "$input")
if [[ "$output" != "$expected" ]]; then
  echo "FAIL stdin: Expected '$expected' but got '$output'"
  exit 1
else
  echo "PASS stdin"
fi
