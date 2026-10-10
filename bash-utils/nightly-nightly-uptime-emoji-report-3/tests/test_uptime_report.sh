#!/usr/bin/env bash
# Tests for uptime_report.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/uptime_report.sh"

run_test() {
  local input=$1
  local expected_emoji=$2
  output=$("$SCRIPT" "$input")
  if [[ "$output" == "$expected_emoji"* ]]; then
    echo "PASS for input $input"
  else
    echo "FAIL for input $input: got '$output'"
    exit 1
  fi
}

# Mock scenarios
run_test 1800 "🚀"
run_test 7200 "🌞"
run_test 200000 "🌤"
run_test 1000000 "🐢"

echo "All tests passed."
