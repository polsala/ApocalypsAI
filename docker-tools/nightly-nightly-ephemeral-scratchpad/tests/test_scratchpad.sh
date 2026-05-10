#!/bin/bash

# Mock rationale: We cannot reliably run actual Docker commands in a CI/CD environment
# without Docker daemon access, which is often restricted or unavailable. Mocks allow
# us to test the script's logic, command parsing, and error handling deterministically
# and offline, ensuring the script behaves as expected under various simulated Docker outcomes.

# --- Test Setup ---
# Global variables to capture mocked command calls and control exit codes
MOCKED_DOCKER_COMMAND=""
MOCKED_DOCKER_BUILD_EXIT_CODE=0
MOCKED_DOCKER_RUN_EXIT_CODE=0
MOCKED_DOCKER_IMAGES_OUTPUT=""
MOCKED_DOCKER_IMAGES_EXIT_CODE=0
MOCKED_RM_COMMAND=""

# Define the temporary directory prefix used by the script
TEMP_DIR_PREFIX="apocalypsai_scratchpad_"
MOCKED_MKTEMP_DIR="/tmp/mock_apocalypsai_scratchpad_123456"

# Override docker command for testing
docker() {
    MOCKED_DOCKER_COMMAND="$@"
    case "$1" in
        "build")
            return $MOCKED_DOCKER_BUILD_EXIT_CODE
            ;;
        "run")
            return $MOCKED_DOCKER_RUN_EXIT_CODE
            ;;
        "images")
            echo "$MOCKED_DOCKER_IMAGES_OUTPUT"
            return $MOCKED_DOCKER_IMAGES_EXIT_CODE
            ;;
        *)
            echo "Unknown mocked docker command: $@" >&2
            return 1
            ;;
    esac
}

# Override mktemp for deterministic temporary directory creation
mktemp() {
    if [[ "$@" == *"${TEMP_DIR_PREFIX}"* ]]; then
        echo "$MOCKED_MKTEMP_DIR"
        mkdir -p "$MOCKED_MKTEMP_DIR" # Simulate creation
        return 0
    else
        /usr/bin/mktemp "$@" # Fallback to real mktemp if not our prefix
    fi
}

# Override rm for deterministic cleanup check
rm() {
    MOCKED_RM_COMMAND="$@"
    # Do not actually remove in test, just capture the call
    return 0
}

# Helper function to run the script in a subshell and capture output/exit code
run_script() {
    ( # Start a subshell to isolate environment changes
        # Reset mocks for each test run within the subshell
        MOCKED_DOCKER_COMMAND=""
        MOCKED_DOCKER_BUILD_EXIT_CODE=0
        MOCKED_DOCKER_RUN_EXIT_CODE=0
        MOCKED_DOCKER_IMAGES_OUTPUT=""
        MOCKED_DOCKER_IMAGES_EXIT_CODE=0
        MOCKED_RM_COMMAND=""
        
        # Redefine mocks within the subshell to ensure they are used by the sourced script
        docker() { MOCKED_DOCKER_COMMAND="$@"; case "$1" in "build") return $MOCKED_DOCKER_BUILD_EXIT_CODE;; "run") return $MOCKED_DOCKER_RUN_EXIT_CODE;; "images") echo "$MOCKED_DOCKER_IMAGES_OUTPUT"; return $MOCKED_DOCKER_IMAGES_EXIT_CODE;; *) echo "Unknown mocked docker command: $@" >&2; return 1;; esac; }
        mktemp() { if [[ "$@" == *"${TEMP_DIR_PREFIX}"* ]]; then echo "$MOCKED_MKTEMP_DIR"; mkdir -p "$MOCKED_MKTEMP_DIR"; return 0; else /usr/bin/mktemp "$@"; fi; }
        rm() { MOCKED_RM_COMMAND="$@"; return 0; }

        # Execute the script directly. The `trap cleanup EXIT` in run.sh will ensure `rm` is called.
        bash ../src/run.sh "$@"
    )
    return $?
}

# --- Test Cases ---

# Test 1: Docker not installed
test_docker_not_installed() {
    echo "Running Test 1: Docker not installed"
    # Mock rationale: To simulate Docker not being installed, we temporarily remove
    # common Docker binary paths from the PATH environment variable. This allows
    # `command -v docker` within the script to fail, mimicking a system without Docker.
    local PATH_BAK=$PATH
    PATH=$(echo $PATH | sed 's/:\/usr\/bin//g' | sed 's/:\/usr\/local\/bin//g') # Remove common docker paths
    
    local output=$(run_script 2>&1)
    local exit_code=$?
    
    PATH=$PATH_BAK # Restore PATH

    if [ $exit_code -ne 1 ]; then
        echo "FAIL: Expected exit code 1, got $exit_code"
        echo "$output"
        return 1
    fi
    if ! echo "$output" | grep -q "ERROR: Docker is not installed"; then
        echo "FAIL: Expected 'Docker is not installed' error message"
        echo "$output"
        return 1
    fi
    echo "PASS: Docker not installed handled correctly."
    return 0
}

# Test 2: Image build success and container run success
test_full_success() {
    echo "Running Test 2: Full success scenario"
    MOCKED_DOCKER_IMAGES_OUTPUT="" # Simulate image not existing
    MOCKED_DOCKER_BUILD_EXIT_CODE=0
    MOCKED_DOCKER_RUN_EXIT_CODE=0

    local output=$(run_script 2>&1)
    local exit_code=$?

    if [ $exit_code -ne 0 ]; then
        echo "FAIL: Expected exit code 0, got $exit_code"
        echo "$output"
        return 1
    fi
    if ! echo "$MOCKED_DOCKER_COMMAND" | grep -q "build -t apocalypsai/ephemeral-scratchpad ."; then
        echo "FAIL: Expected docker build command not found or incorrect."
        echo "Mocked Docker Command: $MOCKED_DOCKER_COMMAND"
        return 1
    fi
    if ! echo "$MOCKED_DOCKER_COMMAND" | grep -q "run --name apocalypsai-scratchpad-.* -it --rm -v .*:/scratchpad/current_dir:ro -v $MOCKED_MKTEMP_DIR:/scratchpad/host_mount apocalypsai/ephemeral-scratchpad"; then
        echo "FAIL: Expected docker run command not found or incorrect."
        echo "Mocked Docker Command: $MOCKED_DOCKER_COMMAND"
        return 1
    fi
    if ! echo "$MOCKED_RM_COMMAND" | grep -q "rm -rf $MOCKED_MKTEMP_DIR"; then
        echo "FAIL: Expected temporary directory cleanup command not found or incorrect."
        echo "Mocked RM Command: $MOCKED_RM_COMMAND"
        return 1
    fi
    echo "PASS: Full success scenario handled correctly."
    return 0
}

# Test 3: Image build failure
test_build_failure() {
    echo "Running Test 3: Image build failure"
    MOCKED_DOCKER_IMAGES_OUTPUT="" # Simulate image not existing
    MOCKED_DOCKER_BUILD_EXIT_CODE=1 # Simulate build failure
    MOCKED_DOCKER_RUN_EXIT_CODE=0 # This shouldn't be reached

    local output=$(run_script 2>&1)
    local exit_code=$?

    if [ $exit_code -ne 1 ]; then
        echo "FAIL: Expected exit code 1, got $exit_code"
        echo "$output"
        return 1
    fi
    if ! echo "$output" | grep -q "ERROR: Failed to build Docker image"; then
        echo "FAIL: Expected 'Failed to build Docker image' error message."
        echo "$output"
        return 1
    }
    # Ensure no container run command was attempted
    if echo "$MOCKED_DOCKER_COMMAND" | grep -q "run"; then
        echo "FAIL: Docker run command should not have been called after build failure."
        echo "Mocked Docker Command: $MOCKED_DOCKER_COMMAND"
        return 1
    fi
    echo "PASS: Image build failure handled correctly."
    return 0
}

# Test 4: Container run failure
test_run_failure() {
    echo "Running Test 4: Container run failure"
    MOCKED_DOCKER_IMAGES_OUTPUT="apocalypsai/ephemeral-scratchpad latest 1234567890ab 2 hours ago 100MB" # Simulate image existing
    MOCKED_DOCKER_BUILD_EXIT_CODE=0 # No build needed
    MOCKED_DOCKER_RUN_EXIT_CODE=1 # Simulate run failure

    local output=$(run_script 2>&1)
    local exit_code=$?

    if [ $exit_code -ne 1 ]; then
        echo "FAIL: Expected exit code 1, got $exit_code"
        echo "$output"
        return 1
    fi
    if ! echo "$output" | grep -q "ERROR: Container exited with an error."; then
        echo "FAIL: Expected 'Container exited with an error' message."
        echo "$output"
        return 1
    fi
    if ! echo "$MOCKED_RM_COMMAND" | grep -q "rm -rf $MOCKED_MKTEMP_DIR"; then
        echo "FAIL: Expected temporary directory cleanup command even after run failure."
        echo "Mocked RM Command: $MOCKED_RM_COMMAND"
        return 1
    fi
    echo "PASS: Container run failure handled correctly."
    return 0
}

# Test 5: Image already exists, no build needed
test_image_exists() {
    echo "Running Test 5: Image already exists"
    MOCKED_DOCKER_IMAGES_OUTPUT="apocalypsai/ephemeral-scratchpad latest 1234567890ab 2 hours ago 100MB" # Simulate image existing
    MOCKED_DOCKER_BUILD_EXIT_CODE=0 # Should not be called
    MOCKED_DOCKER_RUN_EXIT_CODE=0

    local output=$(run_script 2>&1)
    local exit_code=$?

    if [ $exit_code -ne 0 ]; then
        echo "FAIL: Expected exit code 0, got $exit_code"
        echo "$output"
        return 1
    fi
    if echo "$MOCKED_DOCKER_COMMAND" | grep -q "build"; then
        echo "FAIL: Docker build command should not have been called when image exists."
        echo "Mocked Docker Command: $MOCKED_DOCKER_COMMAND"
        return 1
    fi
    if ! echo "$MOCKED_DOCKER_COMMAND" | grep -q "run"; then
        echo "FAIL: Docker run command should have been called."
        echo "Mocked Docker Command: $MOCKED_DOCKER_COMMAND"
        return 1
    fi
    echo "PASS: Image already exists scenario handled correctly."
    return 0
}

# --- Run all tests ---
ALL_TESTS_PASSED=0

test_docker_not_installed || ALL_TESTS_PASSED=1
test_full_success || ALL_TESTS_PASSED=1
test_build_failure || ALL_TESTS_PASSED=1
test_run_failure || ALL_TESTS_PASSED=1
test_image_exists || ALL_TESTS_PASSED=1

if [ $ALL_TESTS_PASSED -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed!"
    exit 1
fi
