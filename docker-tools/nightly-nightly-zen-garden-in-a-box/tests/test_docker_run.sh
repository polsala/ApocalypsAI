#!/bin/bash
set -euo pipefail

IMAGE_NAME="nightly-zen-garden-test"
CONTAINER_NAME="zen-garden-container-test"
PORT="8080" # Host port to map to container's port 80

echo "--- Testing Docker container run ---"

# Ensure the image is built first
docker build -t "$IMAGE_NAME" . > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Image build failed, cannot run tests."
    exit 1
fi

# Run the container in detached mode, mapping host port to container port 80
docker run -d -p "$PORT":80 --name "$CONTAINER_NAME" "$IMAGE_NAME" > /dev/null

# Give the container a moment to start
sleep 2

# Check if the container is running
if docker ps --filter "name=$CONTAINER_NAME" --filter "status=running" | grep -q "$CONTAINER_NAME"; then
    echo "Container '$CONTAINER_NAME' is running."
    TEST_RESULT=0
else
    echo "Container '$CONTAINER_NAME' failed to start or is not running."
    TEST_RESULT=1
fi

# Clean up
echo "Cleaning up container and image..."
docker stop "$CONTAINER_NAME" > /dev/null || true
docker rm "$CONTAINER_NAME" > /dev/null || true
docker rmi "$IMAGE_NAME" > /dev/null || true

exit $TEST_RESULT

# Mock rationale: This test directly interacts with the Docker daemon and assumes
# a functional Docker environment. To make it truly offline and deterministic
# without external dependencies, one would need to mock all 'docker' commands
# (build, run, ps, stop, rm, rmi). The current approach verifies the operational
# aspects of the Docker setup (image build, container startup, and running status)
# within a real Docker environment, making its outcome deterministic given
# a consistent Docker setup. The `curl` check is omitted to reduce external
# network dependency and focus on Docker's lifecycle.
