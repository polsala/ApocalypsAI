#!/bin/bash
set -euo pipefail

IMAGE_NAME="chrono-container-test"
SNAPSHOTS_HOST_DIR="./test_snapshots"
WORKSPACE_VOLUME="chrono_test_workspace"

# Cleanup function to run on exit
cleanup() {
    echo "Cleaning up test artifacts..."
    docker rmi -f "$IMAGE_NAME" >/dev/null 2>&1 || true
    docker volume rm "$WORKSPACE_VOLUME" >/dev/null 2>&1 || true
    rm -rf "$SNAPSHOTS_HOST_DIR"
}
trap cleanup EXIT

echo "--- Building Docker image ---"
docker build -t "$IMAGE_NAME" . >/dev/null
echo "Image built: $IMAGE_NAME"

mkdir -p "$SNAPSHOTS_HOST_DIR"
docker volume create "$WORKSPACE_VOLUME" >/dev/null

echo "--- Test 1: Run a simple command and verify output ---"
# Mock rationale: This tests basic container execution and file creation.
# The output is captured and compared against expected values.
# The file system interaction is isolated within the container and host-mounted volume.
OUTPUT=$(docker run --rm -v "$SNAPSHOTS_HOST_DIR":/snapshots -v "$WORKSPACE_VOLUME":/workspace "$IMAGE_NAME" bash -c "echo 'Hello Chrono!' > /workspace/greeting.txt && cat /workspace/greeting.txt")
if [[ "$OUTPUT" == "Hello Chrono!" ]]; then
    echo "Test 1 PASSED: Simple command executed successfully."
else
    echo "Test 1 FAILED: Expected 'Hello Chrono!', got '$OUTPUT'"
    exit 1
fi

echo "--- Test 2: Create a snapshot ---"
# Mock rationale: This tests the snapshot command.
# It verifies the creation of a tar.gz file on the host-mounted volume.
docker run --rm -v "$SNAPSHOTS_HOST_DIR":/snapshots -v "$WORKSPACE_VOLUME":/workspace "$IMAGE_NAME" snapshot "initial_state" >/dev/null
if [ -f "${SNAPSHOTS_HOST_DIR}/initial_state.tar.gz" ]; then
    echo "Test 2 PASSED: Snapshot 'initial_state' created."
else
    echo "Test 2 FAILED: Snapshot 'initial_state' not found."
    exit 1
fi

echo "--- Test 3: Modify workspace and verify changes ---"
# Mock rationale: This tests that the workspace can be modified.
# It creates a new file and verifies its existence.
docker run --rm -v "$SNAPSHOTS_HOST_DIR":/snapshots -v "$WORKSPACE_VOLUME":/workspace "$IMAGE_NAME" bash -c "echo 'New content' > /workspace/new_file.txt" >/dev/null
FILE_EXISTS=$(docker run --rm -v "$SNAPSHOTS_HOST_DIR":/snapshots -v "$WORKSPACE_VOLUME":/workspace "$IMAGE_NAME" bash -c "test -f /workspace/new_file.txt && echo 'true' || echo 'false'")
if [[ "$FILE_EXISTS" == "true" ]]; then
    echo "Test 3 PASSED: Workspace modified successfully."
else
    echo "Test 3 FAILED: New file not found in workspace."
    exit 1
fi

echo "--- Test 4: Restore from snapshot and verify old state ---"
# Mock rationale: This tests the restore command.
# It verifies that the 'new_file.txt' is gone and 'greeting.txt' is present with its original content.
docker run --rm -v "$SNAPSHOTS_HOST_DIR":/snapshots -v "$WORKSPACE_VOLUME":/workspace "$IMAGE_NAME" restore "initial_state" >/dev/null
NEW_FILE_GONE=$(docker run --rm -v "$SNAPSHOTS_HOST_DIR":/snapshots -v "$WORKSPACE_VOLUME":/workspace "$IMAGE_NAME" bash -c "test -f /workspace/new_file.txt && echo 'true' || echo 'false'")
GREETING_CONTENT=$(docker run --rm -v "$SNAPSHOTS_HOST_DIR":/snapshots -v "$WORKSPACE_VOLUME":/workspace "$IMAGE_NAME" bash -c "cat /workspace/greeting.txt")
if [[ "$NEW_FILE_GONE" == "false" && "$GREETING_CONTENT" == "Hello Chrono!" ]]; then
    echo "Test 4 PASSED: Workspace restored to 'initial_state'."
else
    echo "Test 4 FAILED: Workspace not restored correctly. New file gone: $NEW_FILE_GONE, Greeting content: '$GREETING_CONTENT'"
    exit 1
fi

echo "--- Test 5: List snapshots ---"
# Mock rationale: This tests the list-snapshots command.
# It verifies that the output contains the expected snapshot name.
LIST_OUTPUT=$(docker run --rm -v "$SNAPSHOTS_HOST_DIR":/snapshots -v "$WORKSPACE_VOLUME":/workspace "$IMAGE_NAME" list-snapshots)
if [[ "$LIST_OUTPUT" == *"initial_state"* ]]; then
    echo "Test 5 PASSED: Snapshot 'initial_state' listed."
else
    echo "Test 5 FAILED: Snapshot 'initial_state' not found in list output: '$LIST_OUTPUT'"
    exit 1
fi

echo "--- Test 6: Cleanup snapshots ---"
# Mock rationale: This tests the cleanup command.
# It verifies that the snapshot file is removed from the host-mounted volume.
docker run --rm -v "$SNAPSHOTS_HOST_DIR":/snapshots -v "$WORKSPACE_VOLUME":/workspace "$IMAGE_NAME" cleanup >/dev/null
if [ ! -f "${SNAPSHOTS_HOST_DIR}/initial_state.tar.gz" ]; then
    echo "Test 6 PASSED: Snapshots cleaned up."
else
    echo "Test 6 FAILED: Snapshot 'initial_state' still exists after cleanup."
    exit 1
fi

echo "All tests completed successfully!"
