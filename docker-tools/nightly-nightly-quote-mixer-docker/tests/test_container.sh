#!/usr/bin/env bash
set -euo pipefail

# Build the image (quietly)
docker build -t nightly-quote-mixer-test . > /dev/null

# Run container with line 2 and capture output
OUTPUT=$(docker run --rm nightly-quote-mixer-test 2)

# Expected output (must match exactly)
EXPECTED='"Every step forward is a victory over inertia." — Ash falls like snow, covering the remnants of hope.'

if [[ "$OUTPUT" == "$EXPECTED" ]]; then
  echo "Test passed"
  exit 0
else
  echo "Test failed"
  echo "Got: $OUTPUT"
  echo "Expected: $EXPECTED"
  exit 1
fi
