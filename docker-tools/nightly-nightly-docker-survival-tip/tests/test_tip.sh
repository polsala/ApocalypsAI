#!/usr/bin/env bash
set -e
# Mock rationale: deterministic test using fixed TIP_INDEX.

# Build the Docker image (tagged for testing)
docker build -t nightly-docker-survival-tip-test -f Dockerfile .

# Run the container with a known TIP_INDEX and capture its output
output=$(docker run --rm -e TIP_INDEX=1 nightly-docker-survival-tip-test)

expected="When in doubt, add more coffee. It fuels both code and courage."

if [ "$output" = "$expected" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$expected' but got '$output'"
  exit 1
fi
