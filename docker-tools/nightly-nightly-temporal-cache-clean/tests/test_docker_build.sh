#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Testing Docker image build for nightly-temporal-cache-cleaner ---"

IMAGE_NAME="test-temporal-cache-cleaner"
DOCKERFILE_PATH="../src/Dockerfile"
CONTEXT_PATH="../src"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Docker daemon is not running. Please start Docker."
  exit 1
fi

# Build the Docker image
echo "Attempting to build Docker image: $IMAGE_NAME from $DOCKERFILE_PATH (context: $CONTEXT_PATH)"
docker build -t "$IMAGE_NAME" -f "$DOCKERFILE_PATH" "$CONTEXT_PATH"

# Check if the build was successful
if [ $? -eq 0 ]; then
  echo "Docker image '$IMAGE_NAME' built successfully."
else
  echo "Failed to build Docker image '$IMAGE_NAME'."
  exit 1
fi

# Clean up: remove the built image
echo "Cleaning up: removing Docker image '$IMAGE_NAME'."
docker rmi "$IMAGE_NAME"

# Check if the image was removed
if [ $? -eq 0 ]; then
  echo "Docker image '$IMAGE_NAME' removed successfully."
else
  echo "Failed to remove Docker image '$IMAGE_NAME'. Manual cleanup might be required."
  exit 1
fi

echo "--- Docker image build test completed successfully ---"
