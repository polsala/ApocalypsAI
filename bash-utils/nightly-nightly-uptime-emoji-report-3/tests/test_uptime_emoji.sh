#!/usr/bin/env bash
# Tests for nightly-uptime-emoji-report

# Helper to run script with mocked uptime and capture output
run_script() {
  MOCK_UPTIME_SECONDS="$1" ./src/uptime_emoji.sh
}

# Test cases: format "seconds|expected substring"
declare -a cases=(
  "3600|0 days, 1 hours, 0 minutes 🌱"
  "90000|1 days, 1 hours, 0 minutes 🌿"
  "900000|10 days, 10 hours, 0 minutes 🌳"
)

pass=0
fail=0

for case in "${cases[@]}"; do
  IFS='|' read -r seconds expected <<< "$case"
  output=$(run_script "$seconds")
  if [[ "$output" == *"$expected"* ]]; then
    echo "PASS: $seconds seconds => $expected"
    ((pass++))
  else
    echo "FAIL: $seconds seconds => expected $expected, got $output"
    ((fail++))
  fi
done

echo "$pass passed, $fail failed."

# Mock rationale:
# The script's get_uptime_seconds function checks MOCK_UPTIME_SECONDS env var.
# By setting it, we avoid reading real /proc/uptime, ensuring deterministic tests.
