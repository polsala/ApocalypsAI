#!/usr/bin/env bash
set -e

# Load the utility functions.
source "$(dirname "$0")/../src/main.sh"

# Simple assertion helper.
function assert_eq() {
  local got=$1
  local expected=$2
  local msg=$3
  if [[ "$got" != "$expected" ]]; then
    echo "FAIL: $msg - expected '$expected', got '$got'"
    exit 1
  fi
  echo "PASS: $msg"
}

# Test cases for format_uptime.
# 1 day, 2 hours, 3 minutes => "1📅 2🕒 3⏱️"
result=$(format_uptime $((1*86400 + 2*3600 + 3*60)))
assert_eq "$result" "1📅 2🕒 3⏱️" "format 1d2h3m"

# Only hours and minutes => "5🕒 7⏱️"
result=$(format_uptime $((5*3600 + 7*60)))
assert_eq "$result" "5🕒 7⏱️" "format 5h7m"

# Only minutes => "9⏱️"
result=$(format_uptime $((9*60)))
assert_eq "$result" "9⏱️" "format 9m"

# Zero uptime => empty string
result=$(format_uptime 0)
assert_eq "$result" "" "format zero"

echo "All tests passed."
