#!/bin/bash

set -e

# Mock rationale: This script tests the Dockerfile build and a basic container run. 
# No external dependencies are required, and the tests are deterministic.

IMAGE_NAME="apoc-env-builder-test"

echo "--- Building Docker image ---"
docker build -t "$IMAGE_NAME" .

echo "--- Running container for basic command test ---"
# Test if the container can start and execute a simple command
if docker run --rm "$IMAGE_NAME" echo "Hello from container"; then
    echo "Container started and executed command successfully."
else
    echo "Error: Container failed to start or execute command."
    exit 1
fi

echo "--- Running container for bash shell test ---"
# Test if the container can start and drop into bash
if docker run -it --rm "$IMAGE_NAME" bash -c "exit 0"; then
    echo "Container started and bash shell is accessible."
else
    echo "Error: Container failed to start bash shell."
    exit 1
fi

# Clean up the test image
echo "--- Cleaning up test image ---"
docker rmi "$IMAGE_NAME"

echo "--- Dockerfile tests passed! ---"
exit 0
