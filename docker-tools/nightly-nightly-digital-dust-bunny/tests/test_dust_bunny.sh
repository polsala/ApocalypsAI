#!/bin/bash
set -euo pipefail

# Mock rationale: This test creates specific, controlled Docker resources
# (dangling image, exited container, dangling volume) to simulate a Docker
# environment with "dust bunnies". The tool's output is then verified against
# these known, test-specific resources, making the test deterministic.
# It does not rely on any pre-existing or external Docker state.

IMAGE_NAME="nightly-digital-dust-bunny"
TEST_IMAGE_TAG="test-dangling-image"
TEST_CONTAINER_NAME="test-exited-container"
TEST_VOLUME_NAME="test-dangling-volume"

cleanup() {
    echo "--- Cleaning up test Docker environment ---"
    docker rm -f "$TEST_CONTAINER_NAME" > /dev/null 2>&1 || true
    if [ -n "${DANGLING_IMAGE_ID:-}" ]; then
        docker rmi -f "$DANGLING_IMAGE_ID" > /dev/null 2>&1 || true
    fi
    docker volume rm -f "$TEST_VOLUME_NAME" > /dev/null 2>&1 || true
    docker rmi -f "$IMAGE_NAME" > /dev/null 2>&1 || true
    # Aggressive prune to ensure no test artifacts remain
    docker system prune -f --all --volumes > /dev/null 2>&1 || true
}

trap cleanup EXIT

echo "--- Building Docker image: $IMAGE_NAME ---"
docker build -t "$IMAGE_NAME" . > /dev/null

echo "--- Setting up test Docker environment ---"

# 1. Create a dangling image
# Build a simple image and then remove its tag to make it dangling
docker build -t "$TEST_IMAGE_TAG" -f - . <<EOF > /dev/null
FROM alpine
CMD ["echo", "hello"]
EOF
DANGLING_IMAGE_ID=$(docker images -q "$TEST_IMAGE_TAG")
docker rmi "$TEST_IMAGE_TAG" > /dev/null
echo "  - Created dangling image with ID: $DANGLING_IMAGE_ID"

# 2. Create an exited container
docker run --name "$TEST_CONTAINER_NAME" alpine echo "I exited" > /dev/null
echo "  - Created exited container: $TEST_CONTAINER_NAME"

# 3. Create a dangling volume
docker volume create "$TEST_VOLUME_NAME" > /dev/null
echo "  - Created dangling volume: $TEST_VOLUME_NAME"

echo "--- Running $IMAGE_NAME to find dust bunnies ---"
OUTPUT=$(docker run --rm -v /var/run/docker.sock:/var/run/docker.sock "$IMAGE_NAME")
EXIT_CODE=$?

echo "--- Verifying output ---"
if [ "$EXIT_CODE" -ne 0 ]; then
    echo "Test failed: Container exited with non-zero status $EXIT_CODE"
    echo "$OUTPUT"
    exit 1
fi

if ! echo "$OUTPUT" | grep -q "Oh dear! I've found 3 digital dust bunnies lurking around:"; then
    echo "Test failed: Expected total dust bunnies count not found."
    echo "$OUTPUT"
    exit 1
fi

if ! echo "$OUTPUT" | grep -q "1 dangling image"; then
    echo "Test failed: Expected dangling image count not found."
    echo "$OUTPUT"
    exit 1
fi

if ! echo "$OUTPUT" | grep -q "1 exited container"; then
    echo "Test failed: Expected exited container count not found."
    echo "$OUTPUT"
    exit 1
fi

if ! echo "$OUTPUT" | grep -q "1 dangling volume"; then
    echo "Test failed: Expected dangling volume count not found."
    echo "$OUTPUT"
    exit 1
fi

if ! echo "$OUTPUT" | grep -q "Container Name: $TEST_CONTAINER_NAME"; then
    echo "Test failed: Exited container name not found."
    echo "$OUTPUT"
    exit 1
fi

if ! echo "$OUTPUT" | grep -q "Volume Name: $TEST_VOLUME_NAME"; then
    echo "Test failed: Dangling volume name not found."
    echo "$OUTPUT"
    exit 1
fi

echo "All tests passed!"
