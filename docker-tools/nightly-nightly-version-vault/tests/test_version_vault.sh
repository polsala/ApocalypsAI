#!/bin/bash

# Mock rationale: We don't want to actually run Docker commands during tests,
# as that would make them non-deterministic, slow, and require a running Docker daemon.
# We mock 'docker' to verify that the 'nightly-version-vault' script
# calls 'docker run' with the correct arguments and handles edge cases.

# --- Mock Docker --- 
# Global variables to capture the last docker call and control its exit code
MOCKED_DOCKER_CALL=""
MOCKED_DOCKER_EXIT_CODE=0

docker() {
    MOCKED_DOCKER_CALL="$@"
    echo "MOCK: docker $@" >&2 # Output mock calls to stderr to not interfere with stdout capture
    return $MOCKED_DOCKER_EXIT_CODE
}
# --- End Mock Docker ---

# Path to the script under test
SCRIPT_PATH="./src/version_vault.sh"

# Setup a temporary directory for tests
TEST_DIR=$(mktemp -d)
cp "$SCRIPT_PATH" "$TEST_DIR/"
chmod +x "$TEST_DIR/version_vault.sh"
cd "$TEST_DIR"

# Cleanup function
cleanup() {
    cd - > /dev/null # Go back to original directory
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

echo "--- Running tests for nightly-version-vault ---"

# Test 1: No image provided
echo "Test 1: No image provided"
output=$(./version_vault.sh "" "echo hello" 2>&1)
if echo "$output" | grep -q "Error: No Docker image specified."; then
    echo "PASS: Correctly handled no image."
else
    echo "FAIL: Did not handle no image. Output: $output"
    exit 1
fi
MOCKED_DOCKER_CALL="" # Reset mock

# Test 2: No command provided
echo "Test 2: No command provided"
output=$(./version_vault.sh "ubuntu:latest" "" 2>&1)
if echo "$output" | grep -q "Error: No command to run specified."; then
    echo "PASS: Correctly handled no command."
else
    echo "FAIL: Did not handle no command. Output: $output"
    exit 1
fi
MOCKED_DOCKER_CALL="" # Reset mock

# Test 3: Valid image and command
echo "Test 3: Valid image and command"
EXPECTED_IMAGE="python:3.9-slim"
EXPECTED_COMMAND="python -c 'print(\"Hello from Python\")'"
output=$(./version_vault.sh "$EXPECTED_IMAGE" "$EXPECTED_COMMAND" 2>&1)

# Construct the expected docker run command string
# Note: $(pwd) will resolve to $TEST_DIR due to 'cd "$TEST_DIR"'
EXPECTED_DOCKER_CALL="run --rm -v \"$(pwd):/app\" -w /app \"$EXPECTED_IMAGE\" bash -c \"$EXPECTED_COMMAND\""

if [[ "$MOCKED_DOCKER_CALL" == "$EXPECTED_DOCKER_CALL" ]]; then
    echo "PASS: Correctly called docker run with image and command."
else
    echo "FAIL: Incorrect docker run call.\n  Expected: '$EXPECTED_DOCKER_CALL'\n  Got:      '$MOCKED_DOCKER_CALL'"
    exit 1
fi
MOCKED_DOCKER_CALL="" # Reset mock

# Test 4: Command with multiple arguments and special characters
echo "Test 4: Command with multiple arguments"
EXPECTED_IMAGE="node:16-alpine"
EXPECTED_COMMAND="npm install --production && node index.js --env=production"
output=$(./version_vault.sh "$EXPECTED_IMAGE" "$EXPECTED_COMMAND" 2>&1)

EXPECTED_DOCKER_CALL="run --rm -v \"$(pwd):/app\" -w /app \"$EXPECTED_IMAGE\" bash -c \"$EXPECTED_COMMAND\""

if [[ "$MOCKED_DOCKER_CALL" == "$EXPECTED_DOCKER_CALL" ]]; then
    echo "PASS: Correctly called docker run with multi-argument command."
else
    echo "FAIL: Incorrect docker run call for multi-arg command.\n  Expected: '$EXPECTED_DOCKER_CALL'\n  Got:      '$MOCKED_DOCKER_CALL'"
    exit 1
fi
MOCKED_DOCKER_CALL="" # Reset mock

echo "All tests passed!"
