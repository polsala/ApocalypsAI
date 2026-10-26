#!/bin/bash

set -euo pipefail

# --- Mocking setup ---
# MOCK_LOG will capture calls to our mocked 'docker' function.
MOCK_LOG="/tmp/mock_docker_log.txt"
# MOCK_EXIT_CODE determines the exit status of the mocked 'docker' command.
MOCK_EXIT_CODE=0
# MOCK_OUTPUT provides the stdout of the mocked 'docker' command.
MOCK_OUTPUT=""

# Mock rationale: The 'docker' command interacts with the Docker daemon,
# which is an external dependency. To ensure deterministic and offline tests,
# we replace the actual 'docker' command with a mock function. This mock
# captures the arguments passed to 'docker', allows setting a predefined
# exit code and output, and avoids actual interaction with the Docker daemon.
docker() {
    echo "MOCK_DOCKER_CALL: $@" >> "$MOCK_LOG"
    echo "$MOCK_OUTPUT"
    return $MOCK_EXIT_CODE
}

# --- Helper functions ---
# Runs the sweep.sh script with specified environment variables.
run_sweep_script() {
    local DRY_RUN_VAL="$1"
    local INCLUDE_VOLUMES_VAL="$2"
    # Execute the script in a subshell to isolate environment variables
    DRY_RUN="$DRY_RUN_VAL" INCLUDE_VOLUMES="$INCLUDE_VOLUMES_VAL" bash -c "$(cat src/sweep.sh)"
    return $?
}

# Asserts that a string contains a specific substring.
assert_contains() {
    local expected="$1"
    local actual="$2"
    if ! echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: Expected output to contain '$expected'\nActual output:\n$actual"
        exit 1
    fi
}

# Asserts that a string does NOT contain a specific substring.
assert_not_contains() {
    local expected="$1"
    local actual="$2"
    if echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: Expected output NOT to contain '$expected'\nActual output:\n$actual"
        exit 1
    fi
}

# Asserts that the actual exit code matches the expected exit code.
assert_exit_code() {
    local expected="$1"
    local actual="$2"
    if [ "$expected" -ne "$actual" ]; then
        echo "FAIL: Expected exit code $expected, got $actual"
        exit 1
    fi
}

# --- Test Cases ---

echo "Running tests for nightly-cosmic-dust-sweeper..."

# Ensure src/sweep.sh exists for the test script to source/execute
if [ ! -f "src/sweep.sh" ]; then
    echo "Error: src/sweep.sh not found. Please ensure the script is in the correct path."
    exit 1
fi

# Test 1: Dry run, include volumes
echo "\n--- Test 1: Dry run, include volumes ---"
rm -f "$MOCK_LOG" # Clear mock log for each test
MOCK_EXIT_CODE=0
MOCK_OUTPUT="MOCK: Dry run output from docker"
OUTPUT=$(run_sweep_script "true" "true" 2>&1)
assert_exit_code 0 $?
assert_contains "🔭 Performing a dry run." "$OUTPUT"
assert_contains "MOCK: This would execute 'docker system prune --all --force --volumes'" "$OUTPUT"
assert_contains "MOCK: No changes made during dry run." "$OUTPUT"
assert_not_contains "MOCK_DOCKER_CALL" "$(cat "$MOCK_LOG" 2>/dev/null || true)" # No actual docker call in dry run mock
echo "Test 1 passed."

# Test 2: Actual run, include volumes
echo "\n--- Test 2: Actual run, include volumes ---"
rm -f "$MOCK_LOG"
MOCK_EXIT_CODE=0
MOCK_OUTPUT="Total reclaimed space: 100MB\nDeleted Images: ..."
OUTPUT=$(run_sweep_script "false" "true" 2>&1)
assert_exit_code 0 $?
assert_contains "Executing: docker system prune --all --force --volumes" "$OUTPUT"
assert_contains "✨ Cosmic Dust Sweep complete!" "$OUTPUT"
assert_contains "MOCK_DOCKER_CALL: system prune --all --force --volumes" "$(cat "$MOCK_LOG")"
echo "Test 2 passed."

# Test 3: Actual run, skip volumes
echo "\n--- Test 3: Actual run, skip volumes ---"
rm -f "$MOCK_LOG"
MOCK_EXIT_CODE=0
MOCK_OUTPUT="Total reclaimed space: 50MB\nDeleted Images: ..."
OUTPUT=$(run_sweep_script "false" "false" 2>&1)
assert_exit_code 0 $?
assert_contains "Executing: docker system prune --all --force" "$OUTPUT"
assert_contains "🚫 Skipping unused volume pruning." "$OUTPUT"
assert_contains "✨ Cosmic Dust Sweep complete!" "$OUTPUT"
assert_contains "MOCK_DOCKER_CALL: system prune --all --force" "$(cat "$MOCK_LOG")"
assert_not_contains "--volumes" "$(cat "$MOCK_LOG")"
echo "Test 3 passed."

# Test 4: Actual run, docker command fails
echo "\n--- Test 4: Actual run, docker command fails ---"
rm -f "$MOCK_LOG"
MOCK_EXIT_CODE=1
MOCK_OUTPUT="Error: Something went wrong with docker daemon connection."
OUTPUT=$(run_sweep_script "false" "true" 2>&1)
assert_exit_code 1 $?
assert_contains "Executing: docker system prune --all --force --volumes" "$OUTPUT"
assert_contains "⚠️ Cosmic Dust Sweep encountered anomalies." "$OUTPUT"
assert_contains "MOCK_DOCKER_CALL: system prune --all --force --volumes" "$(cat "$MOCK_LOG")"
echo "Test 4 passed."

echo "\nAll tests passed!"
