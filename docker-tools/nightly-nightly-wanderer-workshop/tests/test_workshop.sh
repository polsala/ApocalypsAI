#!/bin/bash

set -euo pipefail

IMAGE_NAME="wanderer-workshop-test"
CONTAINER_NAME="workshop-test-container"
PORT="8001" # Use a different port to avoid conflicts

echo "--- Building Docker image: $IMAGE_NAME ---"
docker build -t "$IMAGE_NAME" . > /dev/null

if [ $? -ne 0 ]; then
    echo "ERROR: Docker image build failed."
    exit 1
fi
echo "Image built successfully."

# Mock rationale: The tests interact with the Docker daemon, which is an external dependency.
# However, the tests are deterministic as they build a specific image and verify its internal state
# and exposed services using local `docker` and `curl` commands.
# The `curl` command acts as a client to a locally running containerized service,
# ensuring the service starts and responds as expected without relying on external network resources.

# Test 1: Check if Python is installed and callable
echo "--- Test 1: Checking for python3 ---"
OUTPUT=$(docker run --rm "$IMAGE_NAME" python3 -c "print('Python OK')" 2>&1)
if [[ "$OUTPUT" == "Python OK" ]]; then
    echo "Test 1 PASSED: python3 is available."
else
    echo "Test 1 FAILED: python3 not available. Output: $OUTPUT"
    exit 1
fi

# Test 2: Check if jq is installed and callable
echo "--- Test 2: Checking for jq ---"
OUTPUT=$(docker run --rm "$IMAGE_NAME" jq --version 2>&1)
if [[ "$OUTPUT" =~ "jq-" ]]; then
    echo "Test 2 PASSED: jq is available."
else
    echo "Test 2 FAILED: jq not available. Output: $OUTPUT"
    exit 1
fi

# Test 3: Check if curl is installed and callable
echo "--- Test 3: Checking for curl ---"
OUTPUT=$(docker run --rm "$IMAGE_NAME" curl --version 2>&1)
if [[ "$OUTPUT" =~ "curl " ]]; then
    echo "Test 3 PASSED: curl is available."
else
    echo "Test 3 FAILED: curl not available. Output: $OUTPUT"
    exit 1
fi

# Test 4: Check if the HTTP server starts and responds
echo "--- Test 4: Checking HTTP server functionality ---"

# Create a dummy file to be served
echo "Hello from the workshop test!" > test_file.txt

# Run the container in detached mode, mapping a test port and mounting the current directory
docker run -d --name "$CONTAINER_NAME" -p "$PORT:8000" -v "$(pwd):/app" "$IMAGE_NAME" > /dev/null

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to start container for HTTP server test."
    rm test_file.txt
    exit 1
fi

# Give the server a moment to start
sleep 3

# Try to fetch the dummy file
HTTP_RESPONSE=$(curl -s "http://localhost:$PORT/test_file.txt")

if [[ "$HTTP_RESPONSE" == "Hello from the workshop test!" ]]; then
    echo "Test 4 PASSED: HTTP server is serving files correctly."
else
    echo "Test 4 FAILED: HTTP server did not respond as expected. Response: '$HTTP_RESPONSE'"
    docker logs "$CONTAINER_NAME"
    docker stop "$CONTAINER_NAME" > /dev/null
    docker rm "$CONTAINER_NAME" > /dev/null
    rm test_file.txt
    exit 1
fi

echo "--- Cleaning up ---"
docker stop "$CONTAINER_NAME" > /dev/null
docker rm "$CONTAINER_NAME" > /dev/null
rm test_file.txt

echo "All tests PASSED!"
