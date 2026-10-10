#!/bin/bash

set -euo pipefail

# Mock rationale: This test suite directly interacts with the Docker daemon
# to create, modify, and remove real Docker volumes and containers.
# Mocking the Docker daemon itself would be overly complex and defeat the
# purpose of testing a Docker-centric utility. Instead, we ensure tests are
# isolated by using unique names for volumes and containers, and cleaning up
# thoroughly. The "mock" here is the isolation and cleanup, ensuring
# deterministic results without external dependencies beyond a functional Docker daemon.

# --- Configuration ---
TEST_VOLUME_NAME="test_volume_$(date +%s%N)"
TEST_SNAPSHOT_DATA_VOLUME="temporal-echo-data" # This should be pre-created or created by setup
IMAGE_NAME="temporal-volume-echo-test"
SNAPSHOT_DIR="/snapshots" # Inside the container, where TEST_SNAPSHOT_DATA_VOLUME is mounted

# --- Helper Functions ---
cleanup() {
    echo "--- Cleaning up ---"
    # Remove any lingering temporary containers
    docker rm -f $(docker ps -aq --filter name="temp-volume-echo-") 2>/dev/null || true
    # Remove the test volume
    docker volume rm "${TEST_VOLUME_NAME}" 2>/dev/null || true
    # Clean up specific test volume snapshots from the shared snapshot data volume
    if docker volume inspect "${TEST_SNAPSHOT_DATA_VOLUME}" >/dev/null 2>&1; then
        SNAPSHOT_MOUNT_PATH=$(docker volume inspect "${TEST_SNAPSHOT_DATA_VOLUME}" --format '{{ .Mountpoint }}')
        rm -rf "${SNAPSHOT_MOUNT_PATH}/${TEST_VOLUME_NAME}" 2>/dev/null || true
    fi
    echo "Cleanup complete."
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [ "$expected" != "$actual" ]; then
        echo "FAIL: ${message}"
        echo "  Expected: '${expected}'"
        echo "  Actual:   '${actual}'"
        cleanup
        exit 1
    else
        echo "PASS: ${message}"
    fi
}

# Run the echo_manager.sh script inside its own Docker container
run_echo_manager() {
    docker run --rm \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v "${TEST_SNAPSHOT_DATA_VOLUME}":"${SNAPSHOT_DIR}" \
        "${IMAGE_NAME}" "$@"
}

# Create a dummy file in a volume
create_file_in_volume() {
    local volume="$1"
    local filename="$2"
    local content="$3"
    docker run --rm -v "${volume}:/data" alpine:latest sh -c "echo '${content}' > /data/${filename}"
}

# Read a file from a volume
read_file_from_volume() {
    local volume="$1"
    local filename="$2"
    docker run --rm -v "${volume}:/data" alpine:latest cat "/data/${filename}"
}

# --- Test Suite ---

# Ensure cleanup runs on exit, even if tests fail
trap cleanup EXIT

echo "--- Building test image ---"
docker build -t "${IMAGE_NAME}" .

echo "--- Setting up test environment ---"
docker volume create "${TEST_VOLUME_NAME}"
# Ensure the snapshot data volume exists, create if not
if ! docker volume inspect "${TEST_SNAPSHOT_DATA_VOLUME}" >/dev/null 2>&1; then
    docker volume create "${TEST_SNAPSHOT_DATA_VOLUME}"
fi

# Test 1: Capture an echo with auto-generated name
echo "\n--- Test 1: Capture an echo with auto-generated name ---"
create_file_in_volume "${TEST_VOLUME_NAME}" "file1.txt" "initial content"
run_echo_manager capture "${TEST_VOLUME_NAME}"
# Verify a snapshot was created (by listing)
SNAPSHOTS=$(run_echo_manager list "${TEST_VOLUME_NAME}")
assert_equals 1 $(echo "${SNAPSHOTS}" | wc -l) "Snapshot count after first capture"
FIRST_SNAPSHOT_NAME=$(echo "${SNAPSHOTS}" | head -n 1)
assert_equals 1 $(echo "${FIRST_SNAPSHOT_NAME}" | grep -E '^[0-9]{14}$' | wc -l) "Auto-generated snapshot name format"

# Test 2: Capture an echo with a specific name
echo "\n--- Test 2: Capture an echo with a specific name ---"
create_file_in_volume "${TEST_VOLUME_NAME}" "file2.txt" "second content"
run_echo_manager capture "${TEST_VOLUME_NAME}" "my_custom_echo"
SNAPSHOTS=$(run_echo_manager list "${TEST_VOLUME_NAME}")
assert_equals 2 $(echo "${SNAPSHOTS}" | wc -l) "Snapshot count after second capture"
assert_equals 1 $(echo "${SNAPSHOTS}" | grep "my_custom_echo" | wc -l) "Custom snapshot name exists"

# Test 3: Restore an echo
echo "\n--- Test 3: Restore an echo ---"
# Modify the volume to simulate changes
create_file_in_volume "${TEST_VOLUME_NAME}" "file1.txt" "modified content"
create_file_in_volume "${TEST_VOLUME_NAME}" "new_file.txt" "this should be gone"
assert_equals "modified content" "$(read_file_from_volume "${TEST_VOLUME_NAME}" "file1.txt")" "File1 content before restore"
assert_equals "this should be gone" "$(read_file_from_volume "${TEST_VOLUME_NAME}" "new_file.txt")" "New file content before restore"

run_echo_manager restore "${TEST_VOLUME_NAME}" "${FIRST_SNAPSHOT_NAME}"

# Verify content after restore
assert_equals "initial content" "$(read_file_from_volume "${TEST_VOLUME_NAME}" "file1.txt")" "File1 content after restore"
if read_file_from_volume "${TEST_VOLUME_NAME}" "new_file.txt" >/dev/null 2>&1; then
    echo "FAIL: new_file.txt should have been removed after restore."
    cleanup
    exit 1
else
    echo "PASS: new_file.txt was removed after restore."
fi
if read_file_from_volume "${TEST_VOLUME_NAME}" "file2.txt" >/dev/null 2>&1; then
    echo "FAIL: file2.txt should have been removed after restore."
    cleanup
    exit 1
else
    echo "PASS: file2.2txt was removed after restore."
fi

# Test 4: List echoes for a non-existent volume
echo "\n--- Test 4: List echoes for a non-existent volume ---"
OUTPUT=$(run_echo_manager list "non_existent_volume" || true) # Allow failure for expected output
assert_equals "No echoes found for volume 'non_existent_volume'." "${OUTPUT}" "List for non-existent volume"

# Test 5: Restore non-existent snapshot
echo "\n--- Test 5: Restore non-existent snapshot ---"
OUTPUT=$(run_echo_manager restore "${TEST_VOLUME_NAME}" "non_existent_snapshot" 2>&1 || true)
assert_equals 1 $(echo "${OUTPUT}" | grep "Error: Snapshot 'non_existent_snapshot' not found for volume '${TEST_VOLUME_NAME}'." | wc -l) "Restore non-existent snapshot error"

echo "\nAll tests passed!"
