#!/bin/bash
set -euo pipefail

# Define the image name
TEST_IMAGE_NAME="chrono-compass-oracle-test"

echo "Building test container image: ${TEST_IMAGE_NAME}..."
docker build -f tests/Dockerfile.test -t "${TEST_IMAGE_NAME}" .

echo "Running tests in container..."
# Run the tests, removing the container after execution
docker run --rm "${TEST_IMAGE_NAME}"

echo "Tests finished."
