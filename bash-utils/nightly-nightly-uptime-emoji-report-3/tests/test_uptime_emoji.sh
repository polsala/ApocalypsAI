#!/usr/bin/env bash
# test_uptime_emoji.sh - verifies correct emoji selection for given uptime values

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/uptime_emoji.sh"

run_test() {
  local seconds=$1
  local expected_emoji=$2
  output=$("$SCRIPT" "$seconds")
  if [[ "$output" != *"$expected_emoji"* ]]; then
    echo "FAIL: for $seconds seconds expected $expected_emoji but got $output"
    exit 1
  else
    echo "PASS: $seconds seconds => $expected_emoji"
  fi
}

run_test 1800 "🐣"
run_test 18000 "🐔"
run_test 172800 "🐓"
run_test 864000 "🦅"

echo "All tests passed."
