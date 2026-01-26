#!/usr/bin/env bash
# Test for emoji_uptime.sh

set -e

SCRIPT_DIR=$(dirname "$0")/../src
SCRIPT="${SCRIPT_DIR}/emoji_uptime.sh"

# Test case: 1 day 1 hour 1 minute 1 second = 90061 seconds
FAKE_UPTIME=90061 "$SCRIPT" > output.txt
expected="Uptime: 1🌞 1⏰ 1🕒"
if grep -Fxq "$expected" output.txt; then
  echo "PASS"
else
  echo "FAIL: expected '$expected' got '$(cat output.txt)'" >&2
  exit 1
fi

# Additional test: less than a minute (30 seconds)
FAKE_UPTIME=30 "$SCRIPT" > output.txt
expected="Uptime: 0🌞 0⏰ 0🕒"
if grep -Fxq "$expected" output.txt; then
  echo "PASS"
else
  echo "FAIL: expected '$expected' got '$(cat output.txt)'" >&2
  exit 1
fi
