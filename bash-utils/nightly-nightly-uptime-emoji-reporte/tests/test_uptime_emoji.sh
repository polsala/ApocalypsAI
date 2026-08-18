#!/usr/bin/env bash
# test_uptime_emoji.sh - deterministic tests for uptime_emoji.sh

set -euo pipefail

SCRIPT="../src/uptime_emoji.sh"

run_test() {
  local input=$1
  local expected=$2
  local output
  output=$($SCRIPT "$input")
  if [[ "$output" == "$expected" ]]; then
    echo "PASS: $input -> $output"
  else
    echo "FAIL: $input -> $output (expected $expected)"
    exit 1
  fi
}

run_test 0 "🚀"
run_test 3599 "🚀"
run_test 3600 "🌞"
run_test 86399 "🌞"
run_test 86400 "🌤"
run_test 604799 "🌤"
run_test 604800 "🌧"
run_test 2591999 "🌧"
run_test 2592000 "🐢"
run_test 10000000 "🐢"

echo "All tests passed."
