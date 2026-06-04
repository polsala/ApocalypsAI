#!/usr/bin/env bash

# Tests for nightly-uptime-emoji-report

# Load functions from script
source "$(dirname "$0")/../src/main.sh"

# Test format_uptime
test_format_uptime() {
  local result
  result=$(format_uptime 90061) # 1 day 1 hour 1 minute
  if [[ "$result" != "1 days 1 hours 1 minutes" ]]; then
    echo "FAIL: format_uptime"
    exit 1
  fi
}

# Test select_emoji boundaries
test_select_emoji() {
  local e
  e=$(select_emoji 0)
  [[ "$e" == "🌱" ]] || { echo "FAIL: emoji <1 day"; exit 1; }
  e=$(select_emoji 2)
  [[ "$e" == "🌿" ]] || { echo "FAIL: emoji 1-3 days"; exit 1; }
  e=$(select_emoji 5)
  [[ "$e" == "🌳" ]] || { echo "FAIL: emoji 3-7 days"; exit 1; }
  e=$(select_emoji 10)
  [[ "$e" == "🌲" ]] || { echo "FAIL: emoji >7 days"; exit 1; }
}

# Run tests
test_format_uptime
test_select_emoji

echo "All tests passed."
