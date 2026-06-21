#!/usr/bin/env bash
set -e

# Test short uptime (<1 day)
output=$(bash ../src/uptime_emoji.sh 3600)
expected="Uptime: 3600 seconds 🌱"
if [[ "$output" != "$expected" ]]; then
  echo "FAIL: expected '$expected', got '$output'"
  exit 1
fi

# Test medium uptime (1-7 days)
output=$(bash ../src/uptime_emoji.sh 200000)
expected="Uptime: 200000 seconds 🌳"
if [[ "$output" != "$expected" ]]; then
  echo "FAIL: expected '$expected', got '$output'"
  exit 1
fi

# Test long uptime (>7 days)
output=$(bash ../src/uptime_emoji.sh 1000000)
expected="Uptime: 1000000 seconds 🏔️"
if [[ "$output" != "$expected" ]]; then
  echo "FAIL: expected '$expected', got '$output'"
  exit 1
fi

echo "All tests passed"
