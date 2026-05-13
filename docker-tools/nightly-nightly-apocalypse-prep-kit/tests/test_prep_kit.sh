#!/bin/bash

set -euo pipefail

IMAGE_NAME="apocalypsai-prep-kit-test"
CONTAINER_NAME="apocalypsai-prep-kit-test-instance"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" &> /dev/null && pwd)" # Point to src directory for Dockerfile

echo "--- Starting tests for Apocalypse Prep Kit ---"

# Cleanup function
cleanup() {
    echo "Cleaning up..."
    docker rm -f "$CONTAINER_NAME" &> /dev/null || true
    docker rmi "$IMAGE_NAME" &> /dev/null || true
}
trap cleanup EXIT

# Test 1: Build the Docker image
echo "Test 1: Building Docker image..."
docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"
if [ $? -ne 0 ]; then
    echo "FAIL: Docker image build failed."
    exit 1
fi
echo "PASS: Docker image built successfully."

# Test 2: Run the container in detached mode and check if it starts
echo "Test 2: Running container in detached mode..."
CONTAINER_ID=$(docker run -d --name "$CONTAINER_NAME" "$IMAGE_NAME" sleep 5)
if [ -z "$CONTAINER_ID" ]; then
    echo "FAIL: Container failed to start."
    exit 1
fi
echo "PASS: Container started with ID: $CONTAINER_ID"

# Test 3: Verify essential tools are available inside the container
echo "Test 3: Verifying essential tools..."
TOOLS=("bash" "git" "nano" "less" "tar" "gzip" "unzip" "curl" "wget" "jq" "grep" "sed" "awk" "python3" "pip")
for tool in "${TOOLS[@]}"; do
    echo "  Checking for $tool..."
    docker exec "$CONTAINER_NAME" which "$tool" > /dev/null
    if [ $? -ne 0 ]; then
        echo "FAIL: Tool '$tool' not found in container."
        exit 1
    fi
done
echo "PASS: All essential tools found."

# Test 4: Verify Python's http.server can be run (basic functionality check)
echo "Test 4: Verifying Python http.server..."
docker exec "$CONTAINER_NAME" python3 -c "import http.server; import socketserver; print('Server test successful')" > /dev/null
if [ $? -ne 0 ]; then
    echo "FAIL: Python http.server test failed."
    exit 1
fi
echo "PASS: Python http.server import successful."

# Test 5: Verify /workspace exists and is writable
echo "Test 5: Verifying /workspace exists and is writable..."
docker exec "$CONTAINER_NAME" bash -c "test -d /workspace && touch /workspace/test_writable.tmp && rm /workspace/test_writable.tmp"
if [ $? -ne 0 ]; then
    echo "FAIL: /workspace does not exist or is not writable."
    exit 1
fi
echo "PASS: /workspace exists and is writable."

echo "--- All tests passed for Apocalypse Prep Kit! ---"

# Mock rationale:
# The tests interact with Docker, which is an external dependency. However, the Docker daemon
# is assumed to be available in the test environment. The tests are deterministic because they
# build a specific image, run a specific container, and execute predefined commands within it.
# They do not rely on external network calls beyond the initial Docker Hub pull for the base
# image (alpine:latest), which is a standard and stable dependency. The tests verify the
# container's internal environment and readiness for volume mounts, rather than simulating
# complex host-to-container volume interactions directly within the detached test.
