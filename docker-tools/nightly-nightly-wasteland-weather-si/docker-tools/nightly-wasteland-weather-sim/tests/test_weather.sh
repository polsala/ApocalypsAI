#!/usr/bin/env bash
set -euo pipefail

# Build the Docker image
docker build -t wasteland-weather-test -f Dockerfile . > /dev/null

# Run container with known arguments
output=$(docker run --rm wasteland-weather-test "Testville" "1")

# Expected deterministic output based on ASCII sum of "Testville:1"
expected="Forecast for Testville (day 1): Silent dust."

# Mock rationale: the sum of ASCII codes selects "Silent dust"
if [[ "$output" == "$expected" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: got '$output', expected '$expected'"
  exit 1
fi
