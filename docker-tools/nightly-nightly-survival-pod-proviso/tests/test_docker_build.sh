#!/bin/bash
set -euo pipefail

IMAGE_NAME="nightly-survival-pod-provisor-test"

echo "--- Building Docker image for Nightly Survival Pod Provisor ---"

# Mock rationale: This test verifies the Dockerfile can be built. While it requires a Docker daemon,
# it does not involve external network calls or non-deterministic runtime behavior within the container.
# The build process itself is deterministic given the Dockerfile and base image. The test ensures
# the packaging aspect of the 'docker-tools' utility is functional.

# Build the Docker image
docker build -t "${IMAGE_NAME}" .

if [ $? -eq 0 ]; then
    echo "Docker image build successful: ${IMAGE_NAME}"
    # Clean up the image to ensure determinism for subsequent runs
    docker rmi "${IMAGE_NAME}"
    exit 0
else
    echo "Docker image build failed."
    exit 1
fi
