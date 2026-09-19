#!/bin/bash

# Mock rationale: We need to test the script's logic for constructing and calling docker commands
# without actually executing any docker commands on the host system, which would be non-deterministic
# and potentially destructive. The 'docker' command is redefined to capture its arguments.

# --- Test Setup ---

# Variable to store mocked docker calls
MOCKED_DOCKER_CALLS=""

# Redefine the docker command for testing
docker() {
    MOCKED_DOCKER_CALLS+="docker $@\n"
    # Simulate success for prune commands
    if [[ "$1" == "system" && "$2" == "prune" ]]; then
        echo "Total reclaimed space: 100MB"
    elif [[ "$1" == "image" && "$2" == "prune" ]]; then
        echo "Total reclaimed space: 50MB"
    elif [[ "$1" == "container" && "$2" == "prune" ]]; then
        echo "Total reclaimed space: 30MB"
    elif [[ "$1" == "volume" && "$2" == "prune" ]]; then
        echo "Total reclaimed space: 20MB"
    else
        echo "MOCK: docker $@"
    fi
    return 0 # Always succeed in mock
}

# Helper function to run the script and capture output/calls
run_script() {
    MOCKED_DOCKER_CALLS="" # Reset calls for each test
    bash src/compost_bin.sh "$@"
}

# Helper function to assert expected docker calls
assert_calls() {
    local expected_calls="$1"
    local actual_calls="$MOCKED_DOCKER_CALLS"
    if [[ "$actual_calls" == "$expected_calls" ]]; then
        echo "PASS: Expected calls matched."
    else
        echo "FAIL: Expected calls did NOT match."
        echo "  Expected:\n$expected_calls"
        echo "  Actual:\n$actual_calls"
        exit 1
    fi
}

# Helper function to assert expected dry-run output
assert_dry_run_output() {
    local expected_substring="$1"
    local actual_output="$2"
    if [[ "$actual_output" == *"$expected_substring"* ]]; then
        echo "PASS: Dry run output contains expected substring."
    else
        echo "FAIL: Dry run output does NOT contain expected substring."
        echo "  Expected substring: '$expected_substring'"
        echo "  Actual output: '$actual_output'"
        exit 1
    fi
}

# --- Test Cases ---

echo "Running tests for compost_bin.sh..."

# Test 1: Default behavior (all prune with force)
echo "\n--- Test 1: Default behavior (all prune with force) ---"
run_script --force
assert_calls "docker system prune -a -f\n"

# Test 2: Default behavior (all prune without force)
echo "\n--- Test 2: Default behavior (all prune without force) ---"
run_script
assert_calls "docker system prune -a \n"

# Test 3: Prune images only with force
echo "\n--- Test 3: Prune images only with force ---"
run_script --images --force
assert_calls "docker image prune -a -f\n"

# Test 4: Prune containers only without force
echo "\n--- Test 4: Prune containers only without force ---"
run_script --containers
assert_calls "docker container prune \n"

# Test 5: Prune volumes only with force
echo "\n--- Test 5: Prune volumes only with force ---"
run_script --volumes --force
assert_calls "docker volume prune -f\n"

# Test 6: Prune images and containers without force
echo "\n--- Test 6: Prune images and containers without force ---"
run_script --images --containers
assert_calls "docker image prune -a \ndocker container prune \n"

# Test 7: Dry run for all
echo "\n--- Test 7: Dry run for all ---"
output=$(run_script --all --dry-run)
assert_calls ""
assert_dry_run_output "DRY RUN: Would execute: docker system prune -a \n" "$output"

# Test 8: Dry run for images and volumes with force
echo "\n--- Test 8: Dry run for images and volumes with force ---"
output=$(run_script --images --volumes --force --dry-run)
assert_calls ""
assert_dry_run_output "DRY RUN: Would execute: docker image prune -a -f\n" "$output"
assert_dry_run_output "DRY RUN: Would execute: docker volume prune -f\n" "$output"

# Test 9: Help message
echo "\n--- Test 9: Help message ---"
output=$(run_script --help)
if [[ "$output" == *"Usage: compost_bin.sh [OPTIONS]"* ]]; then
    echo "PASS: Help message displayed."
else
    echo "FAIL: Help message not displayed correctly."
    exit 1
fi

echo "\nAll tests passed!"
