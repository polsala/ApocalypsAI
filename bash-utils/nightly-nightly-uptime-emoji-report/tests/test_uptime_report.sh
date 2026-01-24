#!/usr/bin/env bash

# Tests for nightly-uptime-emoji-report
# These tests create temporary mock files for /proc/uptime and /proc/loadavg
# and verify that the script selects the correct emoji.

set -e

SCRIPT_PATH="../src/uptime_report.sh"

# Helper to create a temporary file with given content
make_temp_file() {
  local content="$1"
  local tmp=$(mktemp)
  echo -e "$content" > "$tmp"
  echo "$tmp"
}

# Test case: low load → 😊
UPTIME_MOCK=$(make_temp_file "12345.67 0.00")
LOADAVG_MOCK=$(make_temp_file "0.23 0.15 0.10 1/200 12345")
OUTPUT_LOW=$($SCRIPT_PATH --uptime-file "$UPTIME_MOCK" --loadavg-file "$LOADAVG_MOCK")
if [[ "$OUTPUT_LOW" != *"😊"* ]]; then
  echo "FAIL: Low load did not produce 😊"
  exit 1
fi

# Test case: moderate load → 😐
UPTIME_MOCK=$(make_temp_file "54321.00 0.00")
LOADAVG_MOCK=$(make_temp_file "1.02 0.80 0.60 2/200 54321")
OUTPUT_MOD=$($SCRIPT_PATH --uptime-file "$UPTIME_MOCK" --loadavg-file "$LOADAVG_MOCK")
if [[ "$OUTPUT_MOD" != *"😐"* ]]; then
  echo "FAIL: Moderate load did not produce 😐"
  exit 1
fi

# Test case: high load → 😫
UPTIME_MOCK=$(make_temp_file "98765.00 0.00")
LOADAVG_MOCK=$(make_temp_file "2.73 2.10 1.95 3/200 98765")
OUTPUT_HIGH=$($SCRIPT_PATH --uptime-file "$UPTIME_MOCK" --loadavg-file "$LOADAVG_MOCK")
if [[ "$OUTPUT_HIGH" != *"😫"* ]]; then
  echo "FAIL: High load did not produce 😫"
  exit 1
fi

# Clean up temporary files
rm -f "$UPTIME_MOCK" "$LOADAVG_MOCK"

echo "All tests passed."
