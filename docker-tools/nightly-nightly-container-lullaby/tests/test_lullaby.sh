#!/bin/bash

# Mock rationale: We need to simulate Docker daemon interactions without actually running Docker commands
# or requiring a Docker daemon to be present. This allows for deterministic and offline testing.

# --- Mock Docker Command --- 
# These variables control the behavior of the mocked 'docker' function.
MOCKED_DOCKER_COMMAND="" # Stores the last command received by the mock.
MOCKED_DOCKER_PS_OUTPUT="" # Controls the output of 'docker ps'.
MOCKED_DOCKER_STOP_SUCCESS=0 # Controls the exit code of 'docker stop'.
MOCKED_DOCKER_PAUSE_SUCCESS=0 # Controls the exit code of 'docker pause'.

docker() {
    MOCKED_DOCKER_COMMAND="$@"
    case "$1" in
        ps)
            if [[ "$@" == "ps -a --format {{.Names}}" ]]; then
                echo -e "$MOCKED_DOCKER_PS_OUTPUT"
                return 0
            fi
            ;;
        stop)
            # Simulate success only if the container is in our mocked ps output
            if echo -e "$MOCKED_DOCKER_PS_OUTPUT" | grep -q "^$2$"; then
                return $MOCKED_DOCKER_STOP_SUCCESS
            else
                return 1 # Simulate container not found for stop
            fi
            ;;
        pause)
            # Simulate success only if the container is in our mocked ps output
            if echo -e "$MOCKED_DOCKER_PS_OUTPUT" | grep -q "^$2$"; then
                return $MOCKED_DOCKER_PAUSE_SUCCESS
            else
                return 1 # Simulate container not found for pause
            fi
            ;;
    esac
    return 1 # Default to failure for unhandled commands
}

# --- Test Helper Function ---
run_test() {
    local test_name="$1"
    local expected_exit_code="$2"
    local script_args="${@:3}"
    local output

    echo "--- Running Test: $test_name ---"

    # Reset mocks for each test to ensure isolation
    MOCKED_DOCKER_COMMAND=""
    MOCKED_DOCKER_PS_OUTPUT=""
    MOCKED_DOCKER_STOP_SUCCESS=0
    MOCKED_DOCKER_PAUSE_SUCCESS=0

    # Run the script and capture its output and exit code
    output=$(bash src/lullaby.sh $script_args 2>&1)
    local actual_exit_code=$?

    if [ "$actual_exit_code" -eq "$expected_exit_code" ]; then
        echo "PASS: $test_name (Exit code: $actual_exit_code)"
    else
        echo "FAIL: $test_name (Expected exit code: $expected_exit_code, Got: $actual_exit_code)"
        echo "Output:"
        echo "$output"
        exit 1 # Exit on first failure to prevent cascading errors
    fi
    echo ""
}

# --- Tests ---

# Test 1: No arguments provided to the script
run_test "No arguments" 1

# Test 2: Invalid operation specified
run_test "Invalid operation" 1 "invalid_op"

# Test 3: Valid operation but no containers specified (should exit 0, as nothing to do)
run_test "No containers for stop" 0 "stop"
run_test "No containers for pause" 0 "pause"

# Test 4: Stop a single existing container successfully
MOCKED_DOCKER_PS_OUTPUT="container-alpha\ncontainer-beta"
MOCKED_DOCKER_STOP_SUCCESS=0
run_test "Stop single existing container" 0 "stop" "container-alpha"

# Test 5: Pause a single existing container successfully
MOCKED_DOCKER_PS_OUTPUT="container-alpha\ncontainer-beta"
MOCKED_DOCKER_PAUSE_SUCCESS=0
run_test "Pause single existing container" 0 "pause" "container-beta"

# Test 6: Stop multiple existing containers successfully
MOCKED_DOCKER_PS_OUTPUT="container-alpha\ncontainer-beta\ncontainer-gamma"
MOCKED_DOCKER_STOP_SUCCESS=0
run_test "Stop multiple existing containers" 0 "stop" "container-alpha" "container-beta"

# Test 7: Pause multiple existing containers successfully
MOCKED_DOCKER_PS_OUTPUT="container-alpha\ncontainer-beta\ncontainer-gamma"
MOCKED_DOCKER_PAUSE_SUCCESS=0
run_test "Pause multiple existing containers" 0 "pause" "container-beta" "container-gamma"

# Test 8: Attempt to stop a non-existent container (should fail overall)
MOCKED_DOCKER_PS_OUTPUT="container-alpha"
run_test "Stop non-existent container" 1 "stop" "container-nonexistent"

# Test 9: Attempt to pause a non-existent container (should fail overall)
MOCKED_DOCKER_PS_OUTPUT="container-alpha"
run_test "Pause non-existent container" 1 "pause" "container-nonexistent"

# Test 10: Mixed success/failure for stop (one exists, one doesn't) - should fail overall
MOCKED_DOCKER_PS_OUTPUT="container-alpha\ncontainer-beta"
MOCKED_DOCKER_STOP_SUCCESS=0
run_test "Mixed stop success/failure" 1 "stop" "container-alpha" "container-nonexistent"

# Test 11: Mixed success/failure for pause (one exists, one doesn't) - should fail overall
MOCKED_DOCKER_PS_OUTPUT="container-alpha\ncontainer-beta"
MOCKED_DOCKER_PAUSE_SUCCESS=0
run_test "Mixed pause success/failure" 1 "pause" "container-beta" "container-nonexistent"

# Test 12: Docker 'stop' command itself fails for an existing container (e.g., permissions, container stuck)
MOCKED_DOCKER_PS_OUTPUT="container-alpha"
MOCKED_DOCKER_STOP_SUCCESS=1 # Simulate docker stop failing
run_test "Docker stop command fails" 1 "stop" "container-alpha"

# Test 13: Docker 'pause' command itself fails for an existing container
MOCKED_DOCKER_PS_OUTPUT="container-alpha"
MOCKED_DOCKER_PAUSE_SUCCESS=1 # Simulate docker pause failing
run_test "Docker pause command fails" 1 "pause" "container-alpha"

echo "All tests completed successfully!"
