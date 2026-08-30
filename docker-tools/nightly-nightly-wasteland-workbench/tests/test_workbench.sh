#!/bin/bash

set -euo pipefail

IMAGE_NAME="wasteland-workbench-test"
CONTAINER_NAME="test-workbench-container"
BUILD_DIR="$(dirname "$0")"/.. # Go up one level to the util_name directory

echo "--- Building Docker image: $IMAGE_NAME ---"
docker build -t "$IMAGE_NAME" "$BUILD_DIR" > /dev/null

echo "--- Running basic command test (jq --version) ---"
OUTPUT=$(docker run --rm "$IMAGE_NAME" jq --version)

if echo "$OUTPUT" | grep -q "Welcome, Wanderer" && echo "$OUTPUT" | grep -q "jq-"; then
  echo "✅ Basic command test passed: Welcome message and jq version found."
else
  echo "❌ Basic command test failed. Output:"
  echo "$OUTPUT"
  exit 1
fi

echo "--- Running Python command test ---"
PYTHON_OUTPUT=$(docker run --rm "$IMAGE_NAME" python3 -c "print('Wasteland Python says hello!')")

if echo "$PYTHON_OUTPUT" | grep -q "Welcome, Wanderer" && echo "$PYTHON_OUTPUT" | grep -q "Wasteland Python says hello!"; then
  echo "✅ Python command test passed: Welcome message and Python output found."
else
  echo "❌ Python command test failed. Output:"
  echo "$PYTHON_OUTPUT"
  exit 1
fi

echo "--- Running interactive shell test (non-interactive check) ---"
# We can't truly test an interactive shell, but we can test the entrypoint's output
# when it's about to drop into a shell. We run a simple command that exits immediately.
# Mock rationale: We're simulating the start of an interactive session by running
# the container with a simple command that would typically follow the entrypoint.
# This verifies the entrypoint executes and allows the subsequent command to run,
# without requiring actual interactive input.
INTERACTIVE_OUTPUT=$(docker run --rm "$IMAGE_NAME" /bin/bash -c "echo 'Shell ready!'; exit 0")

if echo "$INTERACTIVE_OUTPUT" | grep -q "Welcome, Wanderer" && echo "$INTERACTIVE_OUTPUT" | grep -q "Shell ready!"; then
  echo "✅ Interactive shell entrypoint test passed: Welcome message and shell readiness found."
else
  echo "❌ Interactive shell entrypoint test failed. Output:"
  echo "$INTERACTIVE_OUTPUT"
  exit 1
fi

echo "--- All tests passed! ---"

# Clean up the image
echo "--- Cleaning up Docker image: $IMAGE_NAME ---"
docker rmi "$IMAGE_NAME" > /dev/null
