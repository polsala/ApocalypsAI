#!/usr/bin/env bash
set -e

# Build the Docker image (quiet output)
docker build -t nightly-dockerized-quote-mixer-test . > /dev/null

# Run the container with a fixed seed
output=$(docker run --rm -e SEED=42 nightly-dockerized-quote-mixer-test)
expected="The early bird catches the worm. Also, Even the stars need a night to shine."

if [[ "$output" == "$expected" ]]; then
  echo "PASS"
else
  echo "FAIL: expected '$expected' but got '$output'"
  exit 1
fi
