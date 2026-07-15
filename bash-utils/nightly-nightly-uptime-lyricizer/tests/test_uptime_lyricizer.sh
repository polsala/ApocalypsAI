#!/usr/bin/env bash
set -e

# Mock uptime file with a known value: 90061.23 seconds
# 90061 seconds = 1 day, 1 hour, 1 minute (86400 + 3600 + 60 = 90060)
mock_file=$(mktemp)
echo "90061.23 0.00" > "$mock_file"

export UPTIME_FILE="$mock_file"

# Run the script and capture output
output=$(../src/uptime_lyricizer.sh)

expected="The system has been alive for 1 days, 1 hours, 1 minutes. Time flies!"

if [[ "$output" != "$expected" ]]; then
  echo "Test failed"
  echo "Got: $output"
  echo "Expected: $expected"
  exit 1
fi

echo "Test passed"
