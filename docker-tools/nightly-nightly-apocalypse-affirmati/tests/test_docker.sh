#!/usr/bin/env bash
set -e

# Build the Docker image (quietly)
docker build -t nightly-apocalypse-affirmation-test . > /dev/null

# Run the container with a fixed AFFIRM_INDEX to get a deterministic line
output=$(docker run --rm -e AFFIRM_INDEX=2 nightly-apocalypse-affirmation-test)

expected="Radiation can't dim your inner glow."

if [ "$output" = "$expected" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$expected' but got '$output'"
  exit 1
fi
