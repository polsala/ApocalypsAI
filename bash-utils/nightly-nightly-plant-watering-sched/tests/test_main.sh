#!/usr/bin/env bash
set -euo pipefail

# Locate the script under test
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/main.sh"

# Create a temporary data file for isolation
TMP_DATA=$(mktemp)
export PLANT_DATA_FILE="$TMP_DATA"
export INTERVAL_DAYS=7

# Helper to run the script and capture output
run() {
  "$SCRIPT" "$@"
}

# Test 1: No data file present
output=$(run 2>/dev/null || true)
if [[ "$output" != "No plant data found." ]]; then
  echo "Test 1 failed: expected 'No plant data found.', got '$output'"
  exit 1
fi

# Test 2: Plant overdue for water
printf "cactus:2023-01-01\n" > "$TMP_DATA"
export CURRENT_DATE="2023-01-10"
output=$(run)
expected="cactus needs watering (last watered 2023-01-01, 9 days ago)"
if [[ "$output" != "$expected" ]]; then
  echo "Test 2 failed: expected '$expected', got '$output'"
  exit 1
fi

# Test 3: Plant not yet overdue
printf "succulent:2023-01-09\n" > "$TMP_DATA"
export CURRENT_DATE="2023-01-10"
output=$(run)
if [[ -n "$output" ]]; then
  echo "Test 3 failed: expected no output, got '$output'"
  exit 1
fi

# Test 4: Recording a watering event via --water
export CURRENT_DATE="2023-01-15"
run --water fern > /dev/null
if ! grep -q "^fern:2023-01-15$" "$TMP_DATA"; then
  echo "Test 4 failed: watering record not written to data file"
  exit 1
fi

# Clean up
rm -f "$TMP_DATA"

echo "All tests passed"
