#!/usr/bin/env bash
set -euo pipefail

# Build the Docker image with a unique tag for testing
IMAGE_TAG="nightly-docker-survival-tips-test"

docker build -t "$IMAGE_TAG" . > /dev/null

# Run the container with a known seed
OUTPUT=$(docker run --rm -e SEED=42 "$IMAGE_TAG")

# Expected tip (seed 42 % len(tips) == 42 % 5 == 2)
EXPECTED="A well‑maintained bike is louder than a car but far quieter than a tank."

if [[ "$OUTPUT" == "$EXPECTED" ]]; then
    echo "Test passed: output matches expected tip."
    exit 0
else
    echo "Test failed: expected '$EXPECTED' but got '$OUTPUT'"
    exit 1
fi
