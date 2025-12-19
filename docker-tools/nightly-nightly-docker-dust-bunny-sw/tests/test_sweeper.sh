#!/bin/bash

# Mock rationale: We need to prevent the script from actually interacting with the Docker daemon
# during tests. By defining a 'docker' function, we intercept all calls to 'docker' and
# can simulate its behavior, record arguments, and return predefined exit codes/outputs.
MOCK_DOCKER_CALLS=""
MOCK_DOCKER_EXIT_CODE=0
MOCK_DOCKER_OUTPUT=""

docker() {
    MOCK_DOCKER_CALLS+="docker $*"$'
'
    echo "$MOCK_DOCKER_OUTPUT"
    return $MOCK_DOCKER_EXIT_CODE
}

# Set MOCK_DOCKER environment variable to point to our mock function
export MOCK_DOCKER="docker"

# Source the script to be tested
SCRIPT_TO_TEST="./src/dust_bunny_sweeper.sh"

# --- Test Helper Functions ---
assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" == *"$needle"* ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  Expected to contain: '$needle'"
        echo "  Actual content: '$haystack'"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" != *"$needle"* ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  Expected NOT to contain: '$needle'"
        echo "  Actual content: '$haystack'"
        exit 1
    fi
}

assert_equals() {
    local actual="$1"
    local expected="$2"
    local message="$3"
    if [[ "$actual" == "$expected" ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  Expected: '$expected'"
        echo "  Actual: '$actual'"
        exit 1
    fi
}

reset_mocks() {
    MOCK_DOCKER_CALLS=""
    MOCK_DOCKER_EXIT_CODE=0
    MOCK_DOCKER_OUTPUT=""
}

# --- Test Cases ---

echo "--- Running Tests for Digital Dust Bunny Sweeper ---"

# Test 1: Default behavior (prune all) - no args
reset_mocks
echo "Test 1: Default behavior (prune all) - no args"
output=$($SCRIPT_TO_TEST)
assert_contains "$output" "Sweeping all unused Docker objects..." "Output indicates pruning all"
assert_contains "$MOCK_DOCKER_CALLS" "docker system prune --all --volumes" "Correct docker command for all"
assert_not_contains "$output" "(Dry Run)" "Not a dry run by default"

# Test 2: Dry run for all
reset_mocks
echo "Test 2: Dry run for all"
output=$($SCRIPT_TO_TEST --dry-run)
assert_contains "$output" "(Dry Run) Would execute: docker system prune --all --volumes" "Dry run message for all"
assert_equals "$MOCK_DOCKER_CALLS" "" "No docker commands executed in dry run"

# Test 3: Force prune for all
reset_mocks
echo "Test 3: Force prune for all"
output=$($SCRIPT_TO_TEST --force)
assert_contains "$output" "Sweeping all unused Docker objects..." "Output indicates pruning all"
assert_contains "$MOCK_DOCKER_CALLS" "docker system prune --all --volumes --force" "Correct docker command with force for all"

# Test 4: Prune images only
reset_mocks
echo "Test 4: Prune images only"
output=$($SCRIPT_TO_TEST --images)
assert_contains "$output" "Sweeping unused images..." "Output indicates pruning images"
assert_contains "$MOCK_DOCKER_CALLS" "docker image prune" "Correct docker command for images"
assert_not_contains "$MOCK_DOCKER_CALLS" "system prune" "Did not prune system"

# Test 5: Dry run for images only
reset_mocks
echo "Test 5: Dry run for images only"
output=$($SCRIPT_TO_TEST --images --dry-run)
assert_contains "$output" "(Dry Run) Would execute: docker image prune" "Dry run message for images"
assert_equals "$MOCK_DOCKER_CALLS" "" "No docker commands executed in dry run for images"

# Test 6: Prune volumes only
reset_mocks
echo "Test 6: Prune volumes only"
output=$($SCRIPT_TO_TEST --volumes)
assert_contains "$output" "Sweeping unused volumes..." "Output indicates pruning volumes"
assert_contains "$MOCK_DOCKER_CALLS" "docker volume prune" "Correct docker command for volumes"

# Test 7: Prune networks only
reset_mocks
echo "Test 7: Prune networks only"
output=$($SCRIPT_TO_TEST --networks)
assert_contains "$output" "Sweeping unused networks..." "Output indicates pruning networks"
assert_contains "$MOCK_DOCKER_CALLS" "docker network prune" "Correct docker command for networks"

# Test 8: Prune build cache only
reset_mocks
echo "Test 8: Prune build cache only"
output=$($SCRIPT_TO_TEST --build-cache)
assert_contains "$output" "Sweeping build cache..." "Output indicates pruning build cache"
assert_contains "$MOCK_DOCKER_CALLS" "docker builder prune" "Correct docker command for build cache"

# Test 9: Prune multiple types (images and volumes)
reset_mocks
echo "Test 9: Prune multiple types (images and volumes)"
output=$($SCRIPT_TO_TEST --images --volumes)
assert_contains "$output" "Sweeping unused images..." "Output indicates pruning images"
assert_contains "$output" "Sweeping unused volumes..." "Output indicates pruning volumes"
assert_contains "$MOCK_DOCKER_CALLS" "docker image prune" "Correct docker command for images"
assert_contains "$MOCK_DOCKER_CALLS" "docker volume prune" "Correct docker command for volumes"
assert_not_contains "$MOCK_DOCKER_CALLS" "system prune" "Did not prune system"

# Test 10: Error handling for docker command
reset_mocks
echo "Test 10: Error handling for docker command"
MOCK_DOCKER_EXIT_CODE=1
MOCK_DOCKER_OUTPUT="Error: Something went wrong with docker"
output=$($SCRIPT_TO_TEST --images)
assert_contains "$output" "Error sweeping unused images." "Error message displayed"
assert_contains "$output" "Error: Something went wrong with docker" "Docker error output included"
assert_equals "$MOCK_DOCKER_CALLS" "docker image prune"$'
' "Docker command was called"

echo "--- All tests completed ---"
