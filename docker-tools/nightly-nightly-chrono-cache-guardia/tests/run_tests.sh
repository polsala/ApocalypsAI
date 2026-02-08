#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

IMAGE_NAME="chrono-cache-guardian-test"

echo "Building test Docker image: $IMAGE_NAME"
docker build -f tests/Dockerfile.test -t $IMAGE_NAME .

echo "Running tests in container..."
docker run --rm $IMAGE_NAME

echo "Tests finished."
