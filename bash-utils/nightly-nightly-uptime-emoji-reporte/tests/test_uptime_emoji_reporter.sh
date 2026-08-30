#!/usr/bin/env bash

# Tests for nightly-uptime-emoji-reporter
# These tests run without any external dependencies and mock /proc files via environment variables.

set -euo pipefail

# Load the script under test.
source "../src/uptime_emoji_reporter.sh"

# Helper to compare expected vs actual output.
assert_eq() {
  local expected="$1"
  local actual="$2"
  if [[ "$expected" != "$actual" ]]; then
    echo "❌ Assertion failed"
    echo "   Expected: $expected"
    echo "   Got     : $actual"
    exit 1
  else
    echo "✅ $expected"
  fi
}

# Test case 1: Low load, happy emoji.
MOCK_UPTIME="123456.78 0 0 0"
MOCK_LOADAVG="0.30 0.20 0.10 1/200 12345"
output=$(main)
expected="Uptime: 1 days, 10 hours, 17 minutes - Mood: 😊"
assert_eq "$expected" "$output"

# Test case 2: Moderate load, neutral emoji.
MOCK_UPTIME="98765.43 0 0 0"
MOCK_LOADAVG="1.00 0.80 0.60 1/200 12345"
output=$(main)
expected="Uptime: 1 days, 3 hours, 26 minutes - Mood: 😐"
assert_eq "$expected" "$output"

# Test case 3: High load, stressed emoji.
MOCK_UPTIME="86400.00 0 0 0"
MOCK_LOADAVG="2.75 2.50 2.30 1/200 12345"
output=$(main)
expected="Uptime: 1 days, 0 hours, 0 minutes - Mood: 😫"
assert_eq "$expected" "$output"

echo "All tests passed."
