#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/uptime_emoji.sh"

# Helper to run the script with overrides and capture output
run_test() {
  local uptime=$1
  local load=$2
  local cores=$3
  local expected_emoji=$4
  local output
  output=$(UPTIME_SECONDS="$uptime" LOADAVG_1="$load" CORES_OVERRIDE="$cores" "$SCRIPT")
  echo "$output"
  if [[ "$output" != *"$expected_emoji"* ]]; then
    echo "Expected emoji $expected_emoji not found in output" >&2
    exit 1
  fi
}

# Low load test (emoji 🌞)
run_test 7200 0.2 4 "🌞"

# Moderate load test (emoji 🌤)
run_test 7200 2.5 4 "🌤"

# High load test (emoji 🌩)
run_test 7200 5 4 "🌩"

echo "All tests passed."
