#!/bin/bash
set -euo pipefail

# Mock rationale: We cannot run actual Docker commands in a CI/CD environment
# without a Docker daemon, and we want deterministic, offline tests.
# This mock captures the 'docker' command calls and their arguments to a log file.

MOCK_DOCKER_LOG="mock_docker.log"
MOCK_EXIT_CODE=0

# Mock the 'docker' command
docker() {
    echo "MOCKED DOCKER CALL: $@" >> "$MOCK_DOCKER_LOG"
    # Simulate success for most calls, or specific exit codes if needed
    return "$MOCK_EXIT_CODE"
}

# Mock the 'test -S' command for docker socket check
test() {
    if [[ "$1" == "-S" && "$2" == "/var/run/docker.sock" ]]; then
        # Simulate docker socket existence based on MOCK_DOCKER_SOCKET_EXISTS
        if [ "${MOCK_DOCKER_SOCKET_EXISTS:-true}" = "true" ]; then
            return 0 # Socket exists
        else
            return 1 # Socket does not exist
        fi
    else
        # Call original test for other cases
        command test "$@"
    fi
}

# Helper function to run a test case
run_test() {
    local test_name="$1"
    local expected_output_regex="$2"
    local expected_exit_code="$3"
    local expected_docker_log_regex="$4"
    shift 4
    local command_to_run=($@)

    echo "Running test: $test_name"
    rm -f "$MOCK_DOCKER_LOG" # Clean log for each test
    MOCK_EXIT_CODE=0 # Reset mock exit code

    # Capture stdout/stderr of the script
    local output
    if ! output=$(bash src/run_courier.sh "${command_to_run[@]}" 2>&1); then
        local actual_exit_code=$?
    else
        local actual_exit_code=0
    fi

    if [ "$actual_exit_code" -ne "$expected_exit_code" ]; then
        echo "FAIL: $test_name - Expected exit code $expected_exit_code, got $actual_exit_code"
        echo "Output: $output"
        return 1
    fi

    if [[ ! "$output" =~ $expected_output_regex ]]; then
        echo "FAIL: $test_name - Output mismatch"
        echo "Expected regex: $expected_output_regex"
        echo "Actual output: $output"
        return 1
    fi

    if [ -n "$expected_docker_log_regex" ]; then
        if ! grep -qE "$expected_docker_log_regex" "$MOCK_DOCKER_LOG"; then
            echo "FAIL: $test_name - Docker command not logged correctly."
            echo "Expected Docker log regex: $expected_docker_log_regex"
            echo "Actual Docker log content:"
            cat "$MOCK_DOCKER_LOG"
            return 1
        fi
    fi

    echo "PASS: $test_name"
    return 0
}

# --- Test Cases ---

# Test 1: No arguments
run_test "No arguments" "Usage: run_courier.sh <target_image> \[docker_run_args_for_target_container...\]" 1 "" ""

# Test 2: Missing target image (only docker socket check passes)
run_test "Missing target image" "Usage: run_courier.sh <target_image> \[docker_run_args_for_target_container...\]" 1 "" ""

# Test 3: Docker socket missing
MOCK_DOCKER_SOCKET_EXISTS="false"
run_test "Docker socket missing" "Error: Docker socket /var/run/docker.sock not found or not accessible." 1 "" "python:3.9-slim" "echo hello"
MOCK_DOCKER_SOCKET_EXISTS="true" # Reset for subsequent tests

# Test 4: Valid call with simple command
run_test "Valid call with simple command" "--- Chrono-Container Courier Dispatch ---\nTarget Image: python:3.9-slim\nTarget Container Args: echo hello world\n-----------------------------------------" 0 "MOCKED DOCKER CALL: run --rm -v /app_host_mount:/app python:3.9-slim echo hello world" "python:3.9-slim" "echo" "hello" "world"

# Test 5: Valid call with script execution
run_test "Valid call with script execution" "--- Chrono-Container Courier Dispatch ---\nTarget Image: node:16-alpine\nTarget Container Args: node /app/script.js\n-----------------------------------------" 0 "MOCKED DOCKER CALL: run --rm -v /app_host_mount:/app node:16-alpine node /app/script.js" "node:16-alpine" "node" "/app/script.js"

# Test 6: Valid call with additional docker run flags (e.g., environment variable)
run_test "Valid call with additional docker run flags" "--- Chrono-Container Courier Dispatch ---\nTarget Image: ubuntu:latest\nTarget Container Args: -e MY_VAR=value bash -c ls -l /app\n-----------------------------------------" 0 "MOCKED DOCKER CALL: run --rm -v /app_host_mount:/app ubuntu:latest -e MY_VAR=value bash -c ls -l /app" "ubuntu:latest" "-e" "MY_VAR=value" "bash" "-c" "ls -l /app"

# Test 7: Target container command fails (simulated by MOCK_EXIT_CODE)
MOCK_EXIT_CODE=127 # Simulate command not found or script error
run_test "Target container command fails" "--- Chrono-Container Courier Dispatch ---\nTarget Image: busybox\nTarget Container Args: non_existent_command\n-----------------------------------------" 127 "MOCKED DOCKER CALL: run --rm -v /app_host_mount:/app busybox non_existent_command" "busybox" "non_existent_command"
MOCK_EXIT_CODE=0 # Reset

echo "All tests completed successfully!"
