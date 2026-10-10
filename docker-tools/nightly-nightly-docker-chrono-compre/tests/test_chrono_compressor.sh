#!/bin/bash

set -euo pipefail

# Mock rationale: The 'docker' command is an external dependency that interacts
# with the Docker daemon. For deterministic and offline testing, we must mock
# its behavior. This mock captures arguments, simulates output, and allows
# verification of correct command construction without needing a live Docker daemon.

# Global arrays to store mock calls
MOCK_DOCKER_CALLS=()

# Mock docker function
docker() {
    local cmd="$1"
    MOCK_DOCKER_CALLS+=("$@") # Store all arguments of the call

    case "$cmd" in
        "inspect")
            local container_name="$2"
            if [[ "$container_name" == "test-container-exists" ]]; then
                # Check if --format is provided
                if [[ "$#" -ge 4 && "$3" == "--format" ]]; then
                    case "$4" in
                        "'{{.HostConfig.CpuShares}}'")
                            echo "1024" # Mock original CPU shares
                            ;;
                        "'{{.HostConfig.BlkioWeight}}'")
                            echo "500" # Mock original BlkioWeight
                            ;;
                        *)
                            # Fallback for unexpected format strings, or just generic success
                            echo "{}" # Minimal valid JSON for inspect
                            ;;
                    esac
                else
                    # This branch handles 'docker inspect <container> &>/dev/null'
                    echo "{}" # Minimal valid JSON for inspect to indicate container exists
                fi
                return 0
            else
                return 1 # Container not found
            fi
            ;;
        "update")
            # Simulate success
            return 0
            ;;
        *)
            # For other commands, just succeed
            return 0
            ;;
    esac
}

# Mock sleep function for faster tests
sleep() {
    echo "MOCK: Sleeping for $1 seconds..."
}

# Source the script to be tested
SCRIPT_TO_TEST="./src/chrono_compressor.sh"

# Test helper function
assert_contains() {
    local haystack="$1"
    local needle="$2"
    if ! echo "$haystack" | grep -qF "$needle"; then
        echo "FAIL: Expected '$haystack' to contain '$needle'"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    if echo "$haystack" | grep -qF "$needle"; then
        echo "FAIL: Expected '$haystack' NOT to contain '$needle'"
        exit 1
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    if [[ "$expected" != "$actual" ]]; then
        echo "FAIL: Expected '$expected', got '$actual'"
        exit 1
    fi
}

# --- Test Cases ---

# Test 1: Help message
echo "Running Test 1: Help message"
output=$(bash "$SCRIPT_TO_TEST" --help 2>&1)
assert_contains "$output" "Usage: ./chrono_compressor.sh <target_container> <resource_type> <value> <duration_seconds>"
assert_contains "$output" "A whimsical utility to temporarily throttle CPU or I/O resources"
echo "Test 1 Passed."

# Reset mocks
MOCK_DOCKER_CALLS=()

# Test 2: Invalid container
echo "Running Test 2: Invalid container"
output=$(bash "$SCRIPT_TO_TEST" "non-existent-container" "cpu" "100" "10" 2>&1 || true)
assert_contains "$output" "Error: Target container 'non-existent-container' not found"
assert_contains "${MOCK_DOCKER_CALLS[*]}" "inspect non-existent-container"
echo "Test 2 Passed."

# Reset mocks
MOCK_DOCKER_CALLS=()

# Test 3: Invalid resource type
echo "Running Test 3: Invalid resource type"
output=$(bash "$SCRIPT_TO_TEST" "test-container-exists" "memory" "100" "10" 2>&1 || true)
assert_contains "$output" "Error: Invalid resource type. Must be 'cpu' or 'io'."
echo "Test 3 Passed."

# Reset mocks
MOCK_DOCKER_CALLS=()

# Test 4: Invalid value (non-integer)
echo "Running Test 4: Invalid value (non-integer)"
output=$(bash "$SCRIPT_TO_TEST" "test-container-exists" "cpu" "abc" "10" 2>&1 || true)
assert_contains "$output" "Error: Value must be a positive integer."
echo "Test 4 Passed."

# Reset mocks
MOCK_DOCKER_CALLS=()

# Test 5: Invalid duration (non-integer)
echo "Running Test 5: Invalid duration (non-integer)"
output=$(bash "$SCRIPT_TO_TEST" "test-container-exists" "cpu" "100" "xyz" 2>&1 || true)
assert_contains "$output" "Error: Duration must be a positive integer in seconds."
echo "Test 5 Passed."

# Reset mocks
MOCK_DOCKER_CALLS=()

# Test 6: CPU throttling and restore
echo "Running Test 6: CPU throttling and restore"
output=$(bash "$SCRIPT_TO_TEST" "test-container-exists" "cpu" "100" "1" 2>&1)

assert_contains "$output" "Applying compression..."
assert_contains "$output" "CPU shares set to 100 for test-container-exists."
assert_contains "$output" "MOCK: Sleeping for 1 seconds..."
assert_contains "$output" "Releasing compression..."
assert_contains "$output" "CPU shares restored to 1024 for test-container-exists."

# Verify docker calls
assert_contains "${MOCK_DOCKER_CALLS[*]}" "inspect test-container-exists --format '{{.HostConfig.CpuShares}}'"
assert_contains "${MOCK_DOCKER_CALLS[*]}" "update --cpu-shares 100 test-container-exists"
assert_contains "${MOCK_DOCKER_CALLS[*]}" "update --cpu-shares 1024 test-container-exists"
echo "Test 6 Passed."

# Reset mocks
MOCK_DOCKER_CALLS=()

# Test 7: I/O throttling and restore
echo "Running Test 7: I/O throttling and restore"
output=$(bash "$SCRIPT_TO_TEST" "test-container-exists" "io" "100" "1" 2>&1)

assert_contains "$output" "Applying compression..."
assert_contains "$output" "Block I/O weight set to 100 for test-container-exists."
assert_contains "$output" "MOCK: Sleeping for 1 seconds..."
assert_contains "$output" "Releasing compression..."
assert_contains "$output" "Block I/O weight restored to 500 for test-container-exists."

# Verify docker calls
assert_contains "${MOCK_DOCKER_CALLS[*]}" "inspect test-container-exists --format '{{.HostConfig.BlkioWeight}}'"
assert_contains "${MOCK_DOCKER_CALLS[*]}" "update --blkio-weight 100 test-container-exists"
assert_contains "${MOCK_DOCKER_CALLS[*]}" "update --blkio-weight 500 test-container-exists"
echo "Test 7 Passed."

echo "All tests passed!"
