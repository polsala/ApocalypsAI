#!/usr/bin/env bash
# Tests for nightly-uptime-emoji-report

set -e

# Helper to capture output
run() {
  MOCK_UPTIME=$1 ./src/main.sh
}

# Test less than 1 day
output=$(run 3600) # 1 hour
expected="Uptime: 0 days, 1 hours, 0 minutes 🌱"
[[ "$output" == "$expected" ]]

# Test between 1 and 7 days
output=$(run 200000) # ~2.31 days
expected="Uptime: 2 days, 7 hours, 33 minutes 🌿"
[[ "$output" == "$expected" ]]

# Test between 7 and 30 days
output=$(run 1200000) # ~13.89 days
expected="Uptime: 13 days, 21 hours, 20 minutes 🌳"
[[ "$output" == "$expected" ]]

# Test more than 30 days
output=$(run 4000000) # ~46.3 days
expected="Uptime: 46 days, 5 hours, 33 minutes 🏜️"
[[ "$output" == "$expected" ]]

echo "All tests passed."
