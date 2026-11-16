#!/bin/bash
set -euo pipefail

IMAGE_NAME="nightly-temporal-drift-stabilizer-test"
CONTAINER_NAME="drift-stabilizer-test-container"
MOCK_NTPDATE_PATH="$(pwd)/tests/mock_ntpdate.sh"

cleanup() {
    echo "--- Cleaning up container (if running) ---"
    docker stop "${CONTAINER_NAME}" > /dev/null 2>&1 || true
    docker rm "${CONTAINER_NAME}" > /dev/null 2>&1 || true
}

trap cleanup EXIT

echo "--- Building Docker image ---"
docker build -t "${IMAGE_NAME}" -f src/Dockerfile .

echo "--- Running container with mocked ntpdate ---"
# Run the container, mounting the mock ntpdate over the real one
# and setting a short sync interval for faster testing.
docker run -d \
           --name "${CONTAINER_NAME}" \
           -v "${MOCK_NTPDATE_PATH}:/usr/sbin/ntpdate:ro" \
           -e SYNC_INTERVAL=5 \
           --cap-add=SYS_TIME \
           "${IMAGE_NAME}"

echo "--- Waiting for stabilization attempt (10 seconds) ---"
sleep 10

echo "--- Checking container logs for success message ---"
LOGS=$(docker logs "${CONTAINER_NAME}")

if echo "${LOGS}" | grep -q "Time synchronization successful."; then
    echo "TEST PASSED: 'Time synchronization successful.' found in logs."
else
    echo "TEST FAILED: 'Time synchronization successful.' not found in logs."
    echo "Container logs:"
    echo "${LOGS}"
    exit 1
fi

echo "All tests completed successfully."
