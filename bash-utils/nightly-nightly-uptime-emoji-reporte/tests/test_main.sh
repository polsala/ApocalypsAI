#!/usr/bin/env bash
# Tests for nightly-uptime-emoji-reporter

set -euo pipefail

SCRIPT_PATH="../src/main.sh"

run_and_check() {
  local uptime_input="$1"
  local expected_emoji="$2"
  local output
  output=$("$SCRIPT_PATH" "$uptime_input")
  if [[ "$output" != *"$expected_emoji"* ]]; then
    echo "FAIL: for input '$uptime_input' expected emoji $expected_emoji but got: $output"
    exit 1
  fi
}

# < 1 hour → 🚀
run_and_check "300 0" "🚀"
# 1–6 hours → 🌱 (2 hours)
run_and_check "7200 0" "🌱"
# 6–24 hours → 🐢 (≈6.94 hours)
run_and_check "25000 0" "🐢"
# 1–7 days → 🌞 (≈55.56 hours)
run_and_check "200000 0" "🌞"
# > 7 days → 🌙 (≈194.44 hours)
run_and_check "700000 0" "🌙"

echo "All tests passed."
