#!/bin/sh
set -e

# Build the Docker image (quiet output)
docker build -t wasteland-tips-test . > /dev/null

# Run container with a known SEED value
OUTPUT=$(docker run --rm -e SEED=2 wasteland-tips-test)
EXPECTED="A well‑sharpened machete is worth more than gold."

if [ "$OUTPUT" = "$EXPECTED" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$EXPECTED' but got '$OUTPUT'"
  exit 1
fi
