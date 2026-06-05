#!/bin/bash

set -euo pipefail

IMAGE_NAME="cryptic-cipher-station-test"

echo "Building test Docker image: ${IMAGE_NAME}"
docker build -t "${IMAGE_NAME}" -f tests/Dockerfile.test .

echo "Running tests in container..."
docker run --rm "${IMAGE_NAME}"

if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Tests failed!"
    exit 1
fi
