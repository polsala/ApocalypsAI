#!/usr/bin/env bash
# Test suite for uptime-emoji.sh
# All tests are deterministic – they pass explicit seconds to the script.

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)
SCRIPT="$SCRIPT_DIR/uptime-emoji.sh"

run_test() {
  local secs=$1
  local expected=$2
  local output
  output=$("$SCRIPT" "$secs")
  if [[ "$output" != "$expected" ]]; then
    echo "FAIL: seconds=$secs expected='$expected' got='$output'"
    exit 1
  fi
}

# Edge cases and typical ranges
run_test 30 "🌱"          # < 1 hour
run_test 3599 "🌱"        # just under 1 hour
run_test 3600 "🌿"        # exactly 1 hour
run_test 86399 "🌿"       # just under 1 day
run_test 86400 "🌳"       # exactly 1 day
run_test 604799 "🌳"      # just under 1 week
run_test 604800 "🌲"      # exactly 1 week
run_test 1234567 "🌲"    # many weeks

echo "All tests passed."
