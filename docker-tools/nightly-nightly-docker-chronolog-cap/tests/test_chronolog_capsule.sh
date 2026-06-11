#!/bin/bash

set -euo pipefail

# --- Test Setup ---

# Mock rationale: Simulate docker commands for isolated testing without a real Docker daemon.
# This allows deterministic and offline execution of tests.

DOCKER_MOCK_CONTAINER_NAME="mock_app_container"
DOCKER_MOCK_LOG_CONTENT="Mock log line 1\nMock log line 2\nMock error line 1"
DOCKER_MOCK_ETC_CONTENT="mock_config_file_content_etc"
DOCKER_MOCK_VAR_LOG_CONTENT="mock_log_file_content_var_log"
DOCKER_MOCK_APP_CONFIG_CONTENT="mock_app_config_content"
DOCKER_MOCK_CUSTOM_PATH_CONTENT="mock_custom_file_content"

# Function to simulate the 'docker' command
docker() {
    local cmd="$1"
    shift

    case "$cmd" in
        "logs")
            local container_name="$1"
            if [[ "$container_name" == "$DOCKER_MOCK_CONTAINER_NAME" ]]; then
                echo -e "$DOCKER_MOCK_LOG_CONTENT"
                return 0
            else
                echo "Error: No such container: $container_name" >&2
                return 1
            fi
            ;;
        "cp")
            local src="$1"
            local dest="$2"
            local container_name=$(echo "$src" | cut -d':' -f1)
            local container_path=$(echo "$src" | cut -d':' -f2-)

            if [[ "$container_name" != "$DOCKER_MOCK_CONTAINER_NAME" ]]; then
                echo "Error: No such container: $container_name" >&2
                return 1
            fi

            # Simulate copying content based on container_path
            # docker cp copies the content *into* the destination directory if it exists
            # or creates the file/directory at the destination if it doesn't.
            # We need to simulate this behavior for the test.
            
            # Ensure the destination directory exists for docker cp to place content into
            mkdir -p "$dest"

            case "$container_path" in
                "/etc")
                    mkdir -p "$dest/etc"
                    echo "$DOCKER_MOCK_ETC_CONTENT" > "$dest/etc/mock_config.conf"
                    ;;
                "/var/log")
                    mkdir -p "$dest/var/log"
                    echo "$DOCKER_MOCK_VAR_LOG_CONTENT" > "$dest/var/log/app.log"
                    ;;
                "/app/config")
                    mkdir -p "$dest/app/config"
                    echo "$DOCKER_MOCK_APP_CONFIG_CONTENT" > "$dest/app/config/settings.ini"
                    ;;
                "/custom/path/file.txt")
                    mkdir -p "$dest/custom/path"
                    echo "$DOCKER_MOCK_CUSTOM_PATH_CONTENT" > "$dest/custom/path/file.txt"
                    ;;
                *) # For paths not explicitly mocked, simulate an empty copy or a warning
                    echo "Warning: Mock 'docker cp' for path '$container_path' not explicitly implemented." >&2
                    ;;
            esac
            return 0
            ;;
        *) # For any other docker command, simulate failure or not found
            echo "Error: Mock 'docker $cmd' not implemented or unexpected." >&2
            return 1
            ;;
    esac
}

# Path to the script under test
SCRIPT_PATH="$(dirname "$0")"/../src/chronolog_capsule.sh

# Temporary directory for test outputs
TEST_OUTPUT_DIR="$(mktemp -d -t chronolog_test_output_XXXXXX)"

# --- Test Functions ---

assert_contains() {
    local file="$1"
    local expected_content="$2"
    if ! grep -qF "$expected_content" "$file"; then
        echo "FAIL: File '$file' does not contain expected content: '$expected_content'"
        cat "$file"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo "FAIL: Expected file '$file' does not exist."
        exit 1
    fi
}

assert_dir_exists() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "FAIL: Expected directory '$dir' does not exist."
        exit 1
    fi
}

run_test() {
    local test_name="$1"
    local test_func="$2"
    echo "Running test: $test_name..."
    if "$test_func"; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        exit 1
    fi
}

# --- Test Cases ---

test_basic_capture() {
    local output_archive_path
    
    # Run the script with default paths
    "$SCRIPT_PATH" "$DOCKER_MOCK_CONTAINER_NAME" "$TEST_OUTPUT_DIR"

    # Find the generated archive (it will have a timestamp)
    output_archive_path=$(find "$TEST_OUTPUT_DIR" -name "${DOCKER_MOCK_CONTAINER_NAME}_chronolog_capsule_*.tar.gz" | head -n 1)
    assert_file_exists "$output_archive_path"

    # Extract the archive to inspect its contents
    local extract_dir="$(mktemp -d -t chronolog_extract_XXXXXX)"
    tar -xzf "$output_archive_path" -C "$extract_dir"

    # Verify logs.txt
    assert_file_exists "$extract_dir/logs.txt"
    assert_contains "$extract_dir/logs.txt" "Mock log line 1"
    assert_contains "$extract_dir/logs.txt" "Mock error line 1"

    # Verify default config paths
    assert_file_exists "$extract_dir/etc/mock_config.conf"
    assert_contains "$extract_dir/etc/mock_config.conf" "$DOCKER_MOCK_ETC_CONTENT"

    assert_file_exists "$extract_dir/var/log/app.log"
    assert_contains "$extract_dir/var/log/app.log" "$DOCKER_MOCK_VAR_LOG_CONTENT"

    assert_file_exists "$extract_dir/app/config/settings.ini"
    assert_contains "$extract_dir/app/config/settings.ini" "$DOCKER_MOCK_APP_CONFIG_CONTENT"

    # Clean up extracted files
    rm -rf "$extract_dir"
}

test_custom_paths() {
    local output_archive_path
    local custom_path="/custom/path/file.txt"

    # Run the script with custom paths
    "$SCRIPT_PATH" "$DOCKER_MOCK_CONTAINER_NAME" "$TEST_OUTPUT_DIR" "$custom_path"

    output_archive_path=$(find "$TEST_OUTPUT_DIR" -name "${DOCKER_MOCK_CONTAINER_NAME}_chronolog_capsule_*.tar.gz" | head -n 1)
    assert_file_exists "$output_archive_path"

    local extract_dir="$(mktemp -d -t chronolog_extract_XXXXXX)"
    tar -xzf "$output_archive_path" -C "$extract_dir"

    # Verify custom path content
    assert_file_exists "$extract_dir/custom/path/file.txt"
    assert_contains "$extract_dir/custom/path/file.txt" "$DOCKER_MOCK_CUSTOM_PATH_CONTENT"

    # Also verify default paths are still included
    assert_file_exists "$extract_dir/etc/mock_config.conf"

    rm -rf "$extract_dir"
}

test_missing_container_logs_fail() {
    # Expect the script to exit with an error if logs cannot be retrieved
    if "$SCRIPT_PATH" "non_existent_container" "$TEST_OUTPUT_DIR"; then
        echo "FAIL: Script did not exit on missing container logs."
        exit 1
    fi
    # Check that no archive was created
    if find "$TEST_OUTPUT_DIR" -name "non_existent_container_chronolog_capsule_*.tar.gz" | grep -q .; then
        echo "FAIL: Archive was created despite log capture failure."
        exit 1
    fi
}

# --- Run Tests ---

run_test "Basic capture with default paths" test_basic_capture
run_test "Capture with custom paths" test_custom_paths
run_test "Script exits on missing container for logs" test_missing_container_logs_fail

# --- Cleanup ---

rm -rf "$TEST_OUTPUT_DIR"
echo "All tests passed!"
