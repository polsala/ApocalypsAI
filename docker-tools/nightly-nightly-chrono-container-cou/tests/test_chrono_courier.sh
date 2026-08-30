#!/bin/bash

# Automated tests for Nightly Chrono-Container Courier

set -euo pipefail

# --- Test Setup ---

# Define the path to the script under test
SCRIPT_PATH="$(dirname "$0")"/../src/chrono_courier.sh

# Create a temporary directory for test artifacts
TEST_DIR=$(mktemp -d)
CONFIG_FILE="$TEST_DIR/test_config.json"
OUTPUT_FILE="$TEST_DIR/test_output.log"

# Mock rationale: Avoid actual Docker operations for deterministic, offline testing.
# This mock simulates the behavior of 'docker pull' and 'docker run' commands.
# It captures arguments and provides predefined outputs/exit codes.
mocked_docker_output=""
mocked_docker_exit_code=0
mocked_docker_run_args=""

docker() {
    local cmd="$1"
    shift
    case "$cmd" in
        pull)
            echo "MOCK: docker pull $*"
            return 0 # Always succeed pull in mock
            ;;
        run)
            mocked_docker_run_args="$*"
            echo "MOCK: docker run $*" >&2 # Log to stderr to not interfere with stdout capture
            echo -e "$mocked_docker_output"
            return $mocked_docker_exit_code
            ;;
        *)
            echo "MOCK ERROR: Unknown docker command: $cmd $*" >&2
            return 1
            ;;
    esac
}

# Mock rationale: Avoid actual 'jq' execution for deterministic, offline testing.
# This mock simulates 'jq' parsing by returning predefined values based on the query.
mocked_jq_image=""
mocked_jq_commands_array=()
mocked_jq_output_file=""
mocked_jq_mount_path=""

jq() {
    local query="$1"
    local file="$2"
    # MOCK: Simulate jq parsing based on expected queries
    case "$query" in
        '.image')
            echo "$mocked_jq_image"
            ;;
        '.commands[]')
            for cmd in "${mocked_jq_commands_array[@]}"; do
                echo "$cmd"
            done
            ;;
        '.output_file // "chrono_courier_results.log"')
            echo "$mocked_jq_output_file"
            ;;
        '.mount_path // "/app"')
            echo "$mocked_jq_mount_path"
            ;;
        *)
            echo "MOCK ERROR: Unknown jq query: $query" >&2
            return 1
            ;;
    esac
}

# Mock rationale: Avoid actual 'command -v' checks for deterministic, offline testing.
# This mock ensures that 'docker' and 'jq' are always reported as found.
command() {
    if [[ "$1" == "-v" && ("$2" == "docker" || "$2" == "jq") ]]; then
        return 0 # command found
    else
        # Call actual command for other checks if needed, or fail
        builtin command "$@"
    fi
}

# --- Test Helper Functions ---

setup_test_config() {
    local image="$1"
    shift
    local commands_str="$1"
    local output_file="$2"
    local mount_path="$3"

    mocked_jq_image="$image"
    mocked_jq_commands_array=()
    IFS=$'\n' read -r -d '' -a mocked_jq_commands_array <<< "$commands_str"
    mocked_jq_output_file="$output_file"
    mocked_jq_mount_path="$mount_path"

    # Create a dummy config file for the script to find, though jq is mocked
    echo "{\"image\": \"$image\", \"commands\": [\"echo 'dummy'\"]}" > "$CONFIG_FILE"
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" != "$actual" ]]; then
        echo "FAIL: $message (Expected: '$expected', Actual: '$actual')" >&2
        exit 1
    else
        echo "PASS: $message"
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" != *"$needle"* ]]; then
        echo "FAIL: $message (Expected to contain: '$needle', Actual: '$haystack')" >&2
        exit 1
    else
        echo "PASS: $message"
    fi
}

# --- Test Cases ---

test_successful_execution() {
    echo "Running test_successful_execution..."
    setup_test_config "ubuntu:latest" "echo 'Hello'; echo 'World'" "$OUTPUT_FILE" "/app"
    mocked_docker_output="Hello\nWorld"
    mocked_docker_exit_code=0

    # Run the script
    if ! "$SCRIPT_PATH" "$CONFIG_FILE"; then
        echo "FAIL: Script exited with non-zero status for successful execution." >&2
        exit 1
    fi

    assert_equals "Hello\nWorld" "$(cat "$OUTPUT_FILE")" "Output should match expected content"
    assert_contains "$mocked_docker_run_args" "ubuntu:latest" "Docker run args should include image"
    assert_contains "$mocked_docker_run_args" "/bin/sh -c 'echo 'Hello' && echo 'World''" "Docker run args should include commands"
    echo "-----------------------------------------"
}

test_command_failure() {
    echo "Running test_command_failure..."
    setup_test_config "alpine:latest" "false; echo 'This should not run'" "$OUTPUT_FILE" "/mnt"
    mocked_docker_output="Error: Command failed inside container"
    mocked_docker_exit_code=1

    # Run the script, expecting a non-zero exit code
    if "$SCRIPT_PATH" "$CONFIG_FILE"; then
        echo "FAIL: Script exited with zero status for failed command." >&2
        exit 1
    fi

    assert_equals "Error: Command failed inside container" "$(cat "$OUTPUT_FILE")" "Output should reflect command failure"
    assert_contains "$mocked_docker_run_args" "alpine:latest" "Docker run args should include image for failure test"
    assert_contains "$mocked_docker_run_args" "/bin/sh -c 'false && echo 'This should not run''" "Docker run args should include commands for failure test"
    echo "-----------------------------------------"
}

test_default_output_file() {
    echo "Running test_default_output_file..."
    local default_output="$TEST_DIR/chrono_courier_results.log"
    setup_test_config "debian:latest" "echo 'Default output test'" "" "/app"
    mocked_docker_output="Default output test content"
    mocked_docker_exit_code=0

    # Run the script
    if ! "$SCRIPT_PATH" "$CONFIG_FILE"; then
        echo "FAIL: Script exited with non-zero status for default output file test." >&2
        exit 1
    fi

    assert_equals "Default output test content" "$(cat "$default_output")" "Output should be written to default file"
    rm -f "$default_output" # Clean up default output file
    echo "-----------------------------------------"
}

test_custom_mount_path() {
    echo "Running test_custom_mount_path..."
    setup_test_config "centos:latest" "ls /custom_mount" "$OUTPUT_FILE" "/custom_mount"
    mocked_docker_output="file_in_host_dir"
    mocked_docker_exit_code=0

    # Run the script
    if ! "$SCRIPT_PATH" "$CONFIG_FILE"; then
        echo "FAIL: Script exited with non-zero status for custom mount path test." >&2
        exit 1
    fi

    assert_contains "$mocked_docker_run_args" "-v $(pwd):/custom_mount" "Docker run args should include custom mount path"
    assert_equals "file_in_host_dir" "$(cat "$OUTPUT_FILE")" "Output should reflect command execution with custom mount"
    echo "-----------------------------------------"
}

# --- Run Tests ---

test_successful_execution
test_command_failure
test_default_output_file
test_custom_mount_path

# --- Cleanup ---

rm -rf "$TEST_DIR"

echo "All tests passed!"
