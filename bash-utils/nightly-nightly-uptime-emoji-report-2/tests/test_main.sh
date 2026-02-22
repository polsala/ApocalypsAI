#!/usr/bin/env bash
set -e

SCRIPT="../src/main.sh"

run_test() {
  local input=$1
  local expected=$2
  local output
  output=$($SCRIPT "$input")
  if [[ "$output" != "$expected" ]]; then
    echo "FAIL: input=$input expected='$expected' got='$output'"
    exit 1
  fi
  echo "PASS: input=$input"
}

# Test cases using explicit seconds (no reliance on /proc/uptime).
run_test 1800 "☕️ System just woke up! Time for coffee."
run_test 7200 "🚀 System is cruising."
run_test 90000 "🛌 System has been up a long time, maybe a nap?"

echo "All tests passed."
