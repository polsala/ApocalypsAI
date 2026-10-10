#!/usr/bin/env bash
set -e

# Build the Docker image (quiet output for test cleanliness)
docker build -t quote-test . > /dev/null

# Run the container with a known seed (4) and capture its output
output=$(docker run --rm -e SEED=4 quote-test)

# Expected quote for seed 4 (index = 4 % 5 = 4)
expected="Talk is cheap. Show me the code."

if [[ "$output" == "$expected" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$expected' but got '$output'"
  exit 1
fi
