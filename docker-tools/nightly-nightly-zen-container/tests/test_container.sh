#!/bin/bash
set -euo pipefail

IMAGE_NAME="nightly-zen-container-test"
CONTAINER_NAME="zen-test-instance"

echo "---\n--- Building Docker image ---\n---"
docker build -t "$IMAGE_NAME" .

echo "---\n--- Running container with Zen Mode enabled ---\n---"
# Run the container, setting ZEN_MODE=true. The entrypoint will start zen_mode.sh in background.
# We then sleep for a bit to allow the background process to write to stdout/stderr (which docker logs captures).
docker run -d --name "$CONTAINER_NAME" -e ZEN_MODE=true "$IMAGE_NAME" bash -c "sleep 5"

# Mock rationale: Running 'sleep 5' ensures the container stays alive long enough for the background
# zen_mode.sh script (started by entrypoint.sh) to execute and write its output to the container's logs,
# which we then capture with 'docker logs'. This simulates the real-world execution flow.

echo "---\n--- Waiting for Zen Mode output in logs ---\n---"
sleep 2 # Give zen_mode.sh a moment to run and write to logs
CONTAINER_LOGS=$(docker logs "$CONTAINER_NAME")

if echo "$CONTAINER_LOGS" | grep -q "Zen Mode:"; then
    echo "PASS: Zen Mode output detected in container logs."
else
    echo "FAIL: Zen Mode output not detected in container logs. Logs were: $CONTAINER_LOGS"
    docker stop "$CONTAINER_NAME" > /dev/null
    docker rm "$CONTAINER_NAME" > /dev/null
    exit 1
fi

echo "---\n--- Verifying basic tools inside container ---\n---"
docker exec "$CONTAINER_NAME" bash -c "command -v bash && command -v git && command -v vim && command -v nano"
if [ $? -ne 0 ]; then
    echo "FAIL: Essential tools not found."
    docker stop "$CONTAINER_NAME" > /dev/null
    docker rm "$CONTAINER_NAME" > /dev/null
    exit 1
fi
echo "PASS: Essential tools found."

echo "---\n--- Verifying entrypoint script exists and is executable ---\n---"
docker exec "$CONTAINER_NAME" bash -c "test -f /usr/local/bin/entrypoint.sh && test -x /usr/local/bin/entrypoint.sh"
if [ $? -ne 0 ]; then
    echo "FAIL: entrypoint.sh not found or not executable."
    docker stop "$CONTAINER_NAME" > /dev/null
    docker rm "$CONTAINER_NAME" > /dev/null
    exit 1
fi
echo "PASS: entrypoint.sh exists and is executable."

echo "---\n--- Verifying zen_mode script exists and is executable ---\n---"
docker exec "$CONTAINER_NAME" bash -c "test -f /usr/local/bin/zen_mode.sh && test -x /usr/local/bin/zen_mode.sh"
if [ $? -ne 0 ]; then
    echo "FAIL: zen_mode.sh not found or not executable."
    docker stop "$CONTAINER_NAME" > /dev/null
    docker rm "$CONTAINER_NAME" > /dev/null
    exit 1
fi
echo "PASS: zen_mode.sh exists and is executable."

echo "---\n--- Cleaning up container ---\n---"
docker stop "$CONTAINER_NAME" > /dev/null
docker rm "$CONTAINER_NAME" > /dev/null

echo "---\n--- All tests passed for Nightly Zen Container! ---\n---"
