#!/bin/bash

# Mock rationale: We mock the 'docker' command to prevent actual Docker operations
# during testing, ensuring tests are deterministic, fast, and offline.
# This allows us to verify that the 'task_pod.sh' script constructs and attempts
# to execute the correct Docker command with the expected arguments and handles
# exit codes properly.

set -euo pipefail

TEST_DIR=$(dirname "$(realpath "$0")")
SRC_SCRIPT="$TEST_DIR/../src/task_pod.sh"
MOCK_DOCKER_LOG="/tmp/mock_docker_log_$(date +%s%N).txt"
MOCK_DOCKER_EXIT_CODE=0

# Mock docker command
docker() {
    echo "MOCK DOCKER CALLED: $@" >> "$MOCK_DOCKER_LOG"
    return "$MOCK_DOCKER_EXIT_CODE"
}
export -f docker # Export the function so subshells can use it

cleanup() {
    rm -f "$MOCK_DOCKER_LOG"
}
trap cleanup EXIT

# Test 1: Successful command execution
echo "Running Test 1: Successful command execution..."
MOCK_DOCKER_EXIT_CODE=0
"$SRC_SCRIPT" "alpine/git" "git --version" > /dev/null 2>&1
TEST_EXIT_CODE=$?

if [ "$TEST_EXIT_CODE" -eq 0 ]; then
    echo "Test 1 Passed: Script exited with 0."
else
    echo "Test 1 Failed: Script exited with $TEST_EXIT_CODE, expected 0."
    cat "$MOCK_DOCKER_LOG"
    exit 1
fi

# Verify the docker command was called correctly
EXPECTED_DOCKER_CALL_PATTERN="MOCK DOCKER CALLED: run --rm -v .* -w /workspace --name nightly-task-pod-.* alpine/git /bin/sh -c git --version"
if grep -Eq "$EXPECTED_DOCKER_CALL_PATTERN" "$MOCK_DOCKER_LOG"; then
    echo "Test 1 Passed: Correct docker run command detected."
else
    echo "Test 1 Failed: Incorrect docker run command detected."
    cat "$MOCK_DOCKER_LOG"
    exit 1
fi
rm "$MOCK_DOCKER_LOG" # Clear log for next test

# Test 2: Failed command execution
echo "Running Test 2: Failed command execution..."
MOCK_DOCKER_EXIT_CODE=1 # Simulate a failed docker run
"$SRC_SCRIPT" "ubuntu" "false" > /dev/null 2>&1
TEST_EXIT_CODE=$?

if [ "$TEST_EXIT_CODE" -eq 1 ]; then
    echo "Test 2 Passed: Script exited with 1."
else
    echo "Test 2 Failed: Script exited with $TEST_EXIT_CODE, expected 1."
    cat "$MOCK_DOCKER_LOG"
    exit 1
fi

EXPECTED_DOCKER_CALL_PATTERN="MOCK DOCKER CALLED: run --rm -v .* -w /workspace --name nightly-task-pod-.* ubuntu /bin/sh -c false"
if grep -Eq "$EXPECTED_DOCKER_CALL_PATTERN" "$MOCK_DOCKER_LOG"; then
    echo "Test 2 Passed: Correct docker run command detected for failure."
else
    echo "Test 2 Failed: Incorrect docker run command detected for failure."
    cat "$MOCK_DOCKER_LOG"
    exit 1
fi
rm "$MOCK_DOCKER_LOG" # Clear log for next test

echo "All tests passed!"
