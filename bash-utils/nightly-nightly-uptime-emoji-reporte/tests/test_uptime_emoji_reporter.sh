#!/usr/bin/env bash
# test_uptime_emoji_reporter.sh
# Mock rationale: we pass explicit seconds to avoid reading real /proc/uptime.

set -e

SCRIPT_DIR=$(dirname "$0")/../src
SCRIPT="${SCRIPT_DIR}/uptime_emoji_reporter.sh"

run_test() {
  local seconds=$1
  local expected=$2
  output=$("$SCRIPT" "$seconds")
  if [[ "$output" != "$expected" ]]; then
    echo "FAIL for $seconds seconds. Expected: '$expected', Got: '$output'"
    exit 1
  fi
}

run_test 1800 "Uptime: 30m 🚀"
run_test 7200 "Uptime: 2h 0m 🌞"
run_test 30000 "Uptime: 8h 20m 🌤"
run_test 70000 "Uptime: 19h 26m 🌙"
run_test 200000 "Uptime: 2d 7h 33m 💤"

echo "All tests passed."
