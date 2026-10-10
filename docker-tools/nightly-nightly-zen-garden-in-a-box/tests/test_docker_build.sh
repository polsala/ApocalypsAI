#!/bin/bash
set -euo pipefail

IMAGE_NAME="nightly-zen-garden-test"

echo "--- Testing Docker image build ---"

# Attempt to build the Docker image
docker build -t "$IMAGE_NAME" . > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Build successful for image: $IMAGE_NAME"
    # Clean up the image
    docker rmi "$IMAGE_NAME" > /dev/null 2>&1
    exit 0
else
    echo "Build failed for image: $IMAGE_NAME"
    # Attempt to clean up any partial image if build failed
    docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true
    exit 1
fi

# Mock rationale: This test directly interacts with the Docker daemon.
# For a truly offline test, one would need to mock the 'docker build' command.
# However, the purpose here is to verify the Dockerfile's syntax and
# dependencies are correctly specified for a successful image creation,
# which requires a functional Docker environment. The test is deterministic
# in its outcome given a consistent Dockerfile and build context.
