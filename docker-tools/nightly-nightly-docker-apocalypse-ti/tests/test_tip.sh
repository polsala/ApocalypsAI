#!/usr/bin/env bash
set -e

# Mock rationale: using a fixed seed ensures the test is deterministic and offline.

# Build the Docker image (quietly)
docker build -t nightly-docker-apocalypse-tip . > /dev/null

# Run the container with a known seed (42) and capture output
OUTPUT=$(docker run --rm nightly-docker-apocalypse-tip 42)

EXPECTED="Water is more valuable than gold."

if [ "$OUTPUT" = "$EXPECTED" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$EXPECTED' but got '$OUTPUT'"
  exit 1
fi
