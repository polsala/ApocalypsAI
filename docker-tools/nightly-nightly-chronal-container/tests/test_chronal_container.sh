#!/bin/bash
set -euo pipefail

IMAGE_NAME="chronal-container-test"
CONTAINER_NAME="chronal-container-run-test"

echo "--- Building Docker image: $IMAGE_NAME ---"
docker build -t "$IMAGE_NAME" . > /dev/null

if [ $? -ne 0 ]; then
    echo "ERROR: Docker image build failed."
    exit 1
fi
echo "Build successful."

echo "--- Running command inside container: python3 --version ---"
# Run a command and capture its output
OUTPUT=$(docker run --rm --name "$CONTAINER_NAME" "$IMAGE_NAME" python3 --version 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "ERROR: Command 'python3 --version' failed inside container. Output:"
    echo "$OUTPUT"
    docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true # Clean up image even on failure
    exit 1
fi

# Check if the output contains expected version for Ubuntu 20.04
# Mock rationale: We expect a specific Python version based on the Ubuntu 20.04 base image.
# This is deterministic as long as the base image doesn't change its default python3 version.
# If it did, the test would fail, indicating a change in the "past" environment.
if echo "$OUTPUT" | grep -q "Python 3.8"; then
    echo "SUCCESS: Python 3.8 detected as expected."
else
    echo "ERROR: Unexpected Python version detected. Expected Python 3.8, got:"
    echo "$OUTPUT"
    docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true
    exit 1
fi

echo "--- Running default command (bash) and checking for output ---"
# Test the default CMD (bash) by running a simple command and checking for its output
OUTPUT_BASH=$(docker run --rm --name "$CONTAINER_NAME-bash" "$IMAGE_NAME" bash -c "echo Chronal Echo" 2>&1)
EXIT_CODE_BASH=$?

if [ $EXIT_CODE_BASH -ne 0 ]; then
    echo "ERROR: Default command 'bash -c \"echo Chronal Echo\"' failed. Output:"
    echo "$OUTPUT_BASH"
    docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true
    exit 1
fi

if echo "$OUTPUT_BASH" | grep -q "Chronal Echo"; then
    echo "SUCCESS: Default command executed and output 'Chronal Echo' as expected."
else
    echo "ERROR: Default command output unexpected. Expected 'Chronal Echo', got:"
    echo "$OUTPUT_BASH"
    docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true
    exit 1
fi

echo "--- Cleaning up Docker image ---"
docker rmi "$IMAGE_NAME" > /dev/null
if [ $? -ne 0 ]; then
    echo "WARNING: Failed to remove Docker image $IMAGE_NAME. You may need to remove it manually."
fi

echo "All tests passed for Nightly Chronal Container!"
