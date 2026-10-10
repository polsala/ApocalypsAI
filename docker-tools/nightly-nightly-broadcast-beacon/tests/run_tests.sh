#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Building test image for Nightly Broadcast Beacon..."
docker build -f tests/Dockerfile.test -t nightly-broadcast-beacon-test .

echo "Running tests for Nightly Broadcast Beacon..."
docker run --rm nightly-broadcast-beacon-test

echo "Tests completed."
