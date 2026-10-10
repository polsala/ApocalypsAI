#!/bin/bash

set -euo pipefail

IMAGE_NAME="apocalypsai-cli-kit-test"
CONTAINER_NAME="apocalypsai-cli-kit-container-test"

# Ensure Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker daemon is not running. Please start Docker and try again."
    exit 1
fi

echo "---\n--- Building Docker image ---\n---"
docker build -t "$IMAGE_NAME" .

echo "---\n--- Running container and testing tools ---\n---"

# Test 1: Ensure the container runs and drops into bash
echo "Testing container entrypoint (default bash)..."
docker run --name "$CONTAINER_NAME" -d "$IMAGE_NAME" sleep 5 # Run in detached mode, then exec
docker exec "$CONTAINER_NAME" bash -c "echo 'Container is running'"
docker rm -f "$CONTAINER_NAME" > /dev/null # Clean up
echo "Container entrypoint test passed."

# Test 2: Check if essential tools are available
TOOLS=("jq" "curl" "grep" "tldr" "htop" "bat" "fzf")
for tool in "${TOOLS[@]}"; do
    echo "Checking for tool: $tool..."
    # Run a command inside the container to check for the tool's existence
    # We use 'which' to find the executable.
    # Mock rationale: This test runs against a real Docker container, but the *environment* inside the container is isolated and deterministic.
    # The 'which' command is a standard shell utility and its behavior is predictable.
    # We are not mocking external services or non-deterministic inputs.
    if ! docker run --rm "$IMAGE_NAME" which "$tool" > /dev/null; then
        echo "Error: Tool '$tool' not found in container."
        exit 1
    fi
    echo "Tool '$tool' found."
done

# Test 3: Check the 'list-tools' command
echo "Testing 'list-tools' command..."
# Mock rationale: The 'list-tools' command is a simple shell function defined within the entrypoint script.
# Its output is entirely deterministic based on the script's content.
# We are not mocking external services or non-deterministic inputs.
OUTPUT=$(docker run --rm "$IMAGE_NAME" list-tools)
if ! echo "$OUTPUT" | grep -q "jq: JSON processor"; then
    echo "Error: 'list-tools' output does not contain expected text for jq."
    echo "Output was:\n$OUTPUT"
    exit 1
fi
if ! echo "$OUTPUT" | grep -q "fzf: Fuzzy finder"; then
    echo "Error: 'list-tools' output does not contain expected text for fzf."
    echo "Output was:\n$OUTPUT"
    exit 1
fi
echo "'list-tools' command test passed."

echo "---\n--- All tests passed successfully! ---\n---"

# Clean up image
echo "---\n--- Cleaning up Docker image ---\n---"
docker rmi "$IMAGE_NAME" > /dev/null
