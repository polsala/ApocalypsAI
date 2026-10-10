#!/usr/bin/env bash
set -e

# Build the Docker image (quietly)
docker build -t test-apocalypse-day-counter . > /dev/null

# Run the container with a fixed date to make the test deterministic
# Mock rationale: using a known date ensures the test does not depend on the current day.
output=$(docker run --rm test-apocalypse-day-counter 2020-01-02)

expected="Days since the Great Collapse: 1"

if [ "$output" = "$expected" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$expected' got '$output'"
  exit 1
fi
