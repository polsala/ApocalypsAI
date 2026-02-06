#!/usr/bin/env bash
set -euo pipefail

# Simple assertion helper
assert_eq() {
  local expected="$1"
  local actual="$2"
  if [[ "$expected" != "$actual" ]]; then
    echo "FAIL: expected '$expected' but got '$actual'"
    exit 1
  fi
}

# Test cases: input uptime string -> expected output line
declare -A cases=(
  ["up 30 minutes"]="Uptime: 0h 30m 🌱"
  ["up 2 hours, 15 minutes"]="Uptime: 2h 15m 🌞"
  ["up 8 hours, 0 minutes"]="Uptime: 8h 0m 🌆"
  ["up 2 days, 3 hours"]="Uptime: 51h 0m 🌙"
)

for input in "${!cases[@]}"; do
  expected="${cases[$input]}"
  actual=$(bash ../src/uptime_emoji.sh "$input")
  assert_eq "$expected" "$actual"
done

echo "All tests passed."
