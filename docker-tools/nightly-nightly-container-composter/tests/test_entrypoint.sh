#!/bin/bash
set -e

# Mock rationale: We cannot run actual docker commands in a self-contained, offline test.
# Instead, we mock the 'docker' command to capture its arguments and simulate its output.
# This allows us to verify that the entrypoint script calls 'docker' with the expected parameters.

MOCKED_DOCKER_CALLS=""

# Mock the docker command
docker() {
    local cmd="$1"
    shift
    local args="$@"
    MOCKED_DOCKER_CALLS+="docker $cmd $args\n"
    echo "MOCK: docker $cmd $args" >&2 # Log to stderr for visibility during test run
    # Simulate success for all prune commands
    echo "Total reclaimed space: 100MB"
    return 0
}

# Source the script to be tested
source src/entrypoint.sh

# --- Test Cases ---

# Test 1: Default run (only container and dangling image prune)
echo "--- Running Test 1: Default prune ---"
MOCKED_DOCKER_CALLS="" # Reset calls
PRUNE_ALL_VOLUMES="false" PRUNE_ALL_IMAGES="false" PRUNE_NETWORKS="false" PRUNE_BUILD_CACHE="false" /app/entrypoint.sh > /dev/null 2>&1
EXPECTED_CALLS_1="docker container prune -f\ndocker image prune -f\n"
if [[ "$MOCKED_DOCKER_CALLS" == "$EXPECTED_CALLS_1" ]]; then
    echo "Test 1 PASSED: Default prune calls correct."
else
    echo "Test 1 FAILED: Default prune calls incorrect."
    echo "Expected:\n$EXPECTED_CALLS_1"
    echo "Got:\n$MOCKED_DOCKER_CALLS"
    exit 1
fi

# Test 2: Prune all volumes
echo "--- Running Test 2: Prune all volumes ---"
MOCKED_DOCKER_CALLS="" # Reset calls
PRUNE_ALL_VOLUMES="true" PRUNE_ALL_IMAGES="false" PRUNE_NETWORKS="false" PRUNE_BUILD_CACHE="false" /app/entrypoint.sh > /dev/null 2>&1
EXPECTED_CALLS_2="docker container prune -f\ndocker image prune -f\ndocker volume prune -f\n"
if [[ "$MOCKED_DOCKER_CALLS" == "$EXPECTED_CALLS_2" ]]; then
    echo "Test 2 PASSED: Prune all volumes calls correct."
else
    echo "Test 2 FAILED: Prune all volumes calls incorrect."
    echo "Expected:\n$EXPECTED_CALLS_2"
    echo "Got:\n$MOCKED_DOCKER_CALLS"
    exit 1
fi

# Test 3: Prune all images
echo "--- Running Test 3: Prune all images ---"
MOCKED_DOCKER_CALLS="" # Reset calls
PRUNE_ALL_VOLUMES="false" PRUNE_ALL_IMAGES="true" PRUNE_NETWORKS="false" PRUNE_BUILD_CACHE="false" /app/entrypoint.sh > /dev/null 2>&1
EXPECTED_CALLS_3="docker container prune -f\ndocker image prune -f\ndocker image prune -a -f\n"
if [[ "$MOCKED_DOCKER_CALLS" == "$EXPECTED_CALLS_3" ]]; then
    echo "Test 3 PASSED: Prune all images calls correct."
else
    echo "Test 3 FAILED: Prune all images calls incorrect."
    echo "Expected:\n$EXPECTED_CALLS_3"
    echo "Got:\n$MOCKED_DOCKER_CALLS"
    exit 1
fi

# Test 4: Prune networks
echo "--- Running Test 4: Prune networks ---"
MOCKED_DOCKER_CALLS="" # Reset calls
PRUNE_ALL_VOLUMES="false" PRUNE_ALL_IMAGES="false" PRUNE_NETWORKS="true" PRUNE_BUILD_CACHE="false" /app/entrypoint.sh > /dev/null 2>&1
EXPECTED_CALLS_4="docker container prune -f\ndocker image prune -f\ndocker network prune -f\n"
if [[ "$MOCKED_DOCKER_CALLS" == "$EXPECTED_CALLS_4" ]]; then
    echo "Test 4 PASSED: Prune networks calls correct."
else
    echo "Test 4 FAILED: Prune networks calls incorrect."
    echo "Expected:\n$EXPECTED_CALLS_4"
    echo "Got:\n$MOCKED_DOCKER_CALLS"
    exit 1
fi

# Test 5: Prune build cache
echo "--- Running Test 5: Prune build cache ---"
MOCKED_DOCKER_CALLS="" # Reset calls
PRUNE_ALL_VOLUMES="false" PRUNE_ALL_IMAGES="false" PRUNE_NETWORKS="false" PRUNE_BUILD_CACHE="true" /app/entrypoint.sh > /dev/null 2>&1
EXPECTED_CALLS_5="docker container prune -f\ndocker image prune -f\ndocker builder prune -f\n"
if [[ "$MOCKED_DOCKER_CALLS" == "$EXPECTED_CALLS_5" ]]; then
    echo "Test 5 PASSED: Prune build cache calls correct."
else
    echo "Test 5 FAILED: Prune build cache calls incorrect."
    echo "Expected:\n$EXPECTED_CALLS_5"
    echo "Got:\n$MOCKED_DOCKER_CALLS"
    exit 1
fi

# Test 6: Prune everything
echo "--- Running Test 6: Prune everything ---"
MOCKED_DOCKER_CALLS="" # Reset calls
PRUNE_ALL_VOLUMES="true" PRUNE_ALL_IMAGES="true" PRUNE_NETWORKS="true" PRUNE_BUILD_CACHE="true" /app/entrypoint.sh > /dev/null 2>&1
EXPECTED_CALLS_6="docker container prune -f\ndocker image prune -f\ndocker image prune -a -f\ndocker volume prune -f\ndocker network prune -f\ndocker builder prune -f\n"
if [[ "$MOCKED_DOCKER_CALLS" == "$EXPECTED_CALLS_6" ]]; then
    echo "Test 6 PASSED: Prune everything calls correct."
else
    echo "Test 6 FAILED: Prune everything calls incorrect."
    echo "Expected:\n$EXPECTED_CALLS_6"
    echo "Got:\n$MOCKED_DOCKER_CALLS"
    exit 1
fi

echo "All tests completed."
