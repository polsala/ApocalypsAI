#!/bin/bash

set -e

# Mock rationale: This test script directly interacts with the Docker daemon,
# which is the core functionality of a 'docker-tools' utility.
# It uses a minimal 'alpine' image for deterministic behavior and cleans up
# all created resources to ensure isolation and idempotence.
# No external network calls beyond Docker image pulls are made.

SCRIPT_PATH="./src/echo_chamber.sh"
TEST_CONTAINER_NAME="test-echo-chamber-container"
TEST_BASE_IMAGE="alpine:latest"

# --- Helper functions for tests ---

# Function to check if a container exists and is running
_is_container_running() {
    docker ps --format "{{.Names}}" | grep -q "^$1$"
}

# Function to check if a file exists inside a container
_file_exists_in_container() {
    docker exec "$1" test -f "$2"
}

# Function to get file content from inside a container
_get_file_content_in_container() {
    docker exec "$1" cat "$2"
}

# Function to clean up all test resources
cleanup_test_resources() {
    echo "--- Cleaning up test resources ---"
    "$SCRIPT_PATH" cleanup "$TEST_CONTAINER_NAME" > /dev/null 2>&1 || true
    # Also remove the base image if it was pulled by the test, though usually not needed
    docker rmi "$TEST_BASE_IMAGE" > /dev/null 2>&1 || true
    echo "--- Cleanup complete ---"
}

# Register cleanup function to run on exit
trap cleanup_test_resources EXIT

# --- Test Cases ---

test_init_and_snapshot() {
    echo "Running test_init_and_snapshot..."
    cleanup_test_resources # Ensure a clean slate

    # 1. Test init command
    "$SCRIPT_PATH" init "$TEST_BASE_IMAGE" "$TEST_CONTAINER_NAME" > /dev/null
    if ! _is_container_running "$TEST_CONTAINER_NAME"; then
        echo "FAIL: Container '$TEST_CONTAINER_NAME' not running after init."
        exit 1
    fi
    if ! docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^${TEST_CONTAINER_NAME}-snapshot-initial$"; then
        echo "FAIL: Initial snapshot image not created."
        exit 1
    fi
    echo "PASS: Init command successful."

    # 2. Test snapshot command
    "$SCRIPT_PATH" run "$TEST_CONTAINER_NAME" "sh -c 'echo \"Hello from snapshot 1\" > /app/file1.txt'" > /dev/null
    "$SCRIPT_PATH" snapshot "$TEST_CONTAINER_NAME" "snap1" > /dev/null
    if ! docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^${TEST_CONTAINER_NAME}-snapshot-snap1$"; then
        echo "FAIL: Snapshot 'snap1' image not created."
        exit 1
    fi
    echo "PASS: Snapshot command successful."
}

test_run_and_rewind() {
    echo "Running test_run_and_rewind..."
    cleanup_test_resources # Ensure a clean slate

    # Initialize and take a base snapshot
    "$SCRIPT_PATH" init "$TEST_BASE_IMAGE" "$TEST_CONTAINER_NAME" > /dev/null
    "$SCRIPT_PATH" run "$TEST_CONTAINER_NAME" "sh -c 'echo \"Base content\" > /app/base.txt'" > /dev/null
    "$SCRIPT_PATH" snapshot "$TEST_CONTAINER_NAME" "base-state" > /dev/null

    # Make changes for 'state1'
    "$SCRIPT_PATH" run "$TEST_CONTAINER_NAME" "sh -c 'echo \"State 1 content\" > /app/state1.txt'" > /dev/null
    "$SCRIPT_PATH" snapshot "$TEST_CONTAINER_NAME" "state1" > /dev/null

    # Make changes for 'state2' (these should be undone)
    "$SCRIPT_PATH" run "$TEST_CONTAINER_NAME" "sh -c 'echo \"State 2 content\" > /app/state2.txt; mkdir /app/temp_dir'" > /dev/null

    # Verify state2 changes are present
    if ! _file_exists_in_container "$TEST_CONTAINER_NAME" "/app/state2.txt"; then
        echo "FAIL: state2.txt not found before rewind."
        exit 1
    fi
    if ! docker exec "$TEST_CONTAINER_NAME" test -d "/app/temp_dir"; then
        echo "FAIL: temp_dir not found before rewind."
        exit 1
    fi
    echo "Verified state2 changes are present."

    # Rewind to 'state1'
    "$SCRIPT_PATH" rewind "$TEST_CONTAINER_NAME" "state1" > /dev/null

    # Verify state2 changes are gone, and state1 changes are present
    if _file_exists_in_container "$TEST_CONTAINER_NAME" "/app/state2.txt"; then
        echo "FAIL: state2.txt found after rewind to state1."
        exit 1
    fi
    if docker exec "$TEST_CONTAINER_NAME" test -d "/app/temp_dir"; then
        echo "FAIL: temp_dir found after rewind to state1."
        exit 1
    fi
    if ! _file_exists_in_container "$TEST_CONTAINER_NAME" "/app/state1.txt"; then
        echo "FAIL: state1.txt not found after rewind to state1."
        exit 1
    fi
    if [[ "$(_get_file_content_in_container "$TEST_CONTAINER_NAME" "/app/state1.txt")" != "State 1 content" ]]; then
        echo "FAIL: Content of state1.txt is incorrect after rewind."
        exit 1
    fi
    echo "PASS: Rewind command successful and state verified."
}

test_cleanup() {
    echo "Running test_cleanup..."
    cleanup_test_resources # Ensure a clean slate

    # Create some resources
    "$SCRIPT_PATH" init "$TEST_BASE_IMAGE" "$TEST_CONTAINER_NAME" > /dev/null
    "$SCRIPT_PATH" run "$TEST_CONTAINER_NAME" "sh -c 'echo \"Temp file\" > /app/temp.txt'" > /dev/null
    "$SCRIPT_PATH" snapshot "$TEST_CONTAINER_NAME" "temp-snap" > /dev/null

    # Verify resources exist
    if ! _is_container_running "$TEST_CONTAINER_NAME"; then
        echo "FAIL: Container not running before cleanup."
        exit 1
    fi
    if ! docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^${TEST_CONTAINER_NAME}-snapshot-initial$"; then
        echo "FAIL: Initial snapshot not found before cleanup."
        exit 1
    fi
    if ! docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^${TEST_CONTAINER_NAME}-snapshot-temp-snap$"; then
        echo "FAIL: Temp snapshot not found before cleanup."
        exit 1
    fi
    echo "Verified resources exist before cleanup."

    # Run cleanup
    "$SCRIPT_PATH" cleanup "$TEST_CONTAINER_NAME" > /dev/null

    # Verify resources are gone
    if _is_container_running "$TEST_CONTAINER_NAME"; then
        echo "FAIL: Container still running after cleanup."
        exit 1
    fi
    if docker ps -a --format "{{.Names}}" | grep -q "^$TEST_CONTAINER_NAME$"; then
        echo "FAIL: Container still exists after cleanup."
        exit 1
    fi
    if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^${TEST_CONTAINER_NAME}-snapshot-initial$"; then
        echo "FAIL: Initial snapshot image still exists after cleanup."
        exit 1
    fi
    if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^${TEST_CONTAINER_NAME}-snapshot-temp-snap$"; then
        echo "FAIL: Temp snapshot image still exists after cleanup."
        exit 1
    fi
    echo "PASS: Cleanup command successful and all resources removed."
}

# Run all tests
echo "--- Starting all tests for Nightly Temporal Docker Echo Chamber ---"
test_init_and_snapshot
test_run_and_rewind
test_cleanup
echo "--- All tests passed! ---"
