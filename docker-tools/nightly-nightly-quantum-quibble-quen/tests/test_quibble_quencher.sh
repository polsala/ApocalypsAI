#!/bin/bash

set -euo pipefail

# Mock rationale: We need to test the script's logic (argument parsing, output formatting, exit code handling)
# without actually requiring a Docker daemon or building/running real containers, which would make tests non-deterministic
# and slow. By mocking the 'docker' command, we can simulate its behavior and verify the script's responses.

# --- MOCK DOCKER COMMAND --- START
MOCKED_DOCKER_OUTPUT=""
MOCKED_DOCKER_EXIT_CODE=0
MOCKED_DOCKER_COMMAND_CALLED=""
MOCKED_DOCKER_BUILD_CALLED=false
MOCKED_DOCKER_IMAGE_EXISTS=false

docker() {
    MOCKED_DOCKER_COMMAND_CALLED="$*"
    case "$1" in
        "image")
            if [ "$2" = "inspect" ]; then
                if "$MOCKED_DOCKER_IMAGE_EXISTS"; then
                    echo "Mocked: Image exists" >&2 # Output to stderr to not interfere with script's stdout capture
                    return 0
                else
                    echo "Mocked: Image does not exist" >&2
                    return 1
                fi
            fi
            ;;
        "build")
            MOCKED_DOCKER_BUILD_CALLED=true
            echo "Mocked: Docker build command: $*" >&2
            return 0
            ;;
        "run")
            echo "Mocked: Docker run command: $*" >&2
            # Simulate output to stdout and stderr as the real docker run would
            echo -e "$MOCKED_DOCKER_OUTPUT"
            return "$MOCKED_DOCKER_EXIT_CODE"
            ;;
        "rm")
            echo "Mocked: Docker rm command: $*" >&2
            return 0
            ;;
        *)
            echo "Mocked: Unknown docker command: $*" >&2
            return 1
            ;;
    esac
}
# --- MOCK DOCKER COMMAND --- END

SCRIPT_PATH="$(dirname "$0")"/../src/quibble_quencher.sh

# Helper function to run a test
run_test() {
    local test_name="$1"
    local expected_exit_code="$2"
    local expected_output_contains="$3"
    shift 3
    local command_args=($@)

    echo "--- Running Test: $test_name ---"

    # Reset mocks
    MOCKED_DOCKER_OUTPUT=""
    MOCKED_DOCKER_EXIT_CODE=0
    MOCKED_DOCKER_COMMAND_CALLED=""
    MOCKED_DOCKER_BUILD_CALLED=false
    MOCKED_DOCKER_IMAGE_EXISTS=true # Assume image exists by default for most tests

    # Set specific mock behaviors for this test
    if [ "${#command_args[@]}" -gt 0 ]; then
        case "${command_args[0]}" in
            "echo")
                MOCKED_DOCKER_OUTPUT="${command_args[@]:1}"
                ;;
            "sh")
                if [[ "${command_args[@]}" =~ "exit 1" ]]; then
                    MOCKED_DOCKER_EXIT_CODE=1
                    MOCKED_DOCKER_OUTPUT="Error output from script"
                elif [[ "${command_args[@]}" =~ "exit 0" ]]; then
                    MOCKED_DOCKER_EXIT_CODE=0
                    MOCKED_DOCKER_OUTPUT="Success output from script"
                fi
                ;;
            "nonexistent_command")
                MOCKED_DOCKER_EXIT_CODE=127 # Command not found exit code
                MOCKED_DOCKER_OUTPUT="sh: nonexistent_command: not found"
                ;;
        esac
    fi

    # Run the script with the mocked docker command
    # We need to capture stderr as well, as the script prints status messages there.
    # Using a temporary file for output capture.
    local temp_output_file=$(mktemp)
    local actual_exit_code
    if ! "$SCRIPT_PATH" "${command_args[@]}" > "$temp_output_file" 2>&1; then
        actual_exit_code=$?
    else
        actual_exit_code=0
    fi
    local actual_output=$(cat "$temp_output_file")
    rm "$temp_output_file"

    # Assertions
    if [ "$actual_exit_code" -ne "$expected_exit_code" ]; then
        echo "FAIL: $test_name - Expected exit code $expected_exit_code, got $actual_exit_code"
        echo "Output:" "$actual_output"
        exit 1
    fi

    if ! echo "$actual_output" | grep -qF "$expected_output_contains"; then # Use -qF for fixed string search
        echo "FAIL: $test_name - Expected output to contain '$expected_output_contains', but it didn't."
        echo "Output:" "$actual_output"
        exit 1
    fi

    echo "PASS: $test_name"
    echo ""
}

# --- Test Cases ---

# Test 1: Successful command execution
run_test "Successful command" 0 "Quibble successfully quenched" echo "Hello World"

# Test 2: Command with non-zero exit code
run_test "Command with error" 1 "Quibble detected!" sh -c 'exit 1'

# Test 3: Command with output
run_test "Command with output" 0 "Success output from script" sh -c 'echo "Success output from script"; exit 0'

# Test 4: Command with stderr output and error exit code
run_test "Command with stderr and error" 1 "Error output from script" sh -c 'echo "Error output from script" >&2; exit 1'

# Test 5: No arguments provided (should show usage and exit 1)
run_test "No arguments" 1 "Usage: $(basename "$SCRIPT_PATH") <command_to_execute>"

# Test 6: Image build on first run (mocked image does not exist)
MOCKED_DOCKER_IMAGE_EXISTS=false
run_test "Image build on first run" 0 "Building Docker image 'quibble-quencher-runtime'" echo "Initial build test"
if ! "$MOCKED_DOCKER_BUILD_CALLED"; then
    echo "FAIL: Image build on first run - Docker build was not called."
    exit 1
fi
echo "PASS: Image build on first run - Docker build was called."
MOCKED_DOCKER_IMAGE_EXISTS=true # Reset for subsequent tests

# Test 7: Image not rebuilt on subsequent runs
MOCKED_DOCKER_BUILD_CALLED=false # Reset
run_test "Image not rebuilt on subsequent runs" 0 "Quibble successfully quenched" echo "Subsequent run test"
if "$MOCKED_DOCKER_BUILD_CALLED"; then
    echo "FAIL: Image not rebuilt on subsequent runs - Docker build was called unexpectedly."
    exit 1
fi
echo "PASS: Image not rebuilt on subsequent runs - Docker build was NOT called."

echo "All tests passed!"
