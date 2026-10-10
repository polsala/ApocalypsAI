#!/usr/bin/env bash
set -e

SCRIPT="../src/main.sh"

run_test() {
  local input=$1
  local expected=$2
  output=$($SCRIPT "$input")
  if [[ "$output" == "$expected" ]]; then
    echo "PASS: input=$input"
  else
    echo "FAIL: input=$input"
    echo "  Expected: $expected"
    echo "  Got:      $output"
    exit 1
  fi
}

# 5 minutes (300 seconds) -> 🚀
run_test 300 "Uptime: 5 minutes 🚀"

# 2 hours (7200 seconds) -> 😊
run_test 7200 "Uptime: 2 hours 😊"

# 25 hours (90000 seconds) -> 💤
run_test 90000 "Uptime: 25 hours 💤"

echo "All tests passed."
