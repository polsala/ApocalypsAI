#!/usr/bin/env bash
set -e

# Build the Docker image (quietly)
docker build -t test-quote-roulette . > /dev/null

# Run the container with a fixed QUOTE_INDEX to make the output deterministic
output=$(docker run --rm -e QUOTE_INDEX=2 test-quote-roulette)

expected="May your commits be small and your merges be clean."

if [[ "$output" == "$expected" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$expected' but got '$output'"
  exit 1
fi
