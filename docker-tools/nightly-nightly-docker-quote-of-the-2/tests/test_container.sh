#!/usr/bin/env bash
set -e

# Build the Docker image (quiet output)
docker build -t nightly-docker-quote-test . > /dev/null

# Run the container with a known seed to get a deterministic quote
output=$(docker run --rm -e SEED=0 nightly-docker-quote-test)
expected='The stars whisper, "Stay hydrated."'

if [ "$output" != "$expected" ]; then
  echo "Test failed: expected '$expected' but got '$output'"
  exit 1
fi

echo "Test passed: deterministic quote matches expected output."
