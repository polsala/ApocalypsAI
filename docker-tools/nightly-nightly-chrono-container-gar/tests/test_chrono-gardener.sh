#!/bin/bash

set -euo pipefail

# --- Test Setup ---

TEST_DIR=$(mktemp -d)
COMPOSE_FILE="$TEST_DIR/docker-compose.yml"
NGINX_CONF="$TEST_DIR/nginx.conf"
SCRIPT_PATH="$(dirname "$0")"/../src/chrono-gardener.sh

# Mock rationale: Prevent actual Docker operations and time delays during testing.
# Instead, we record calls and simulate outcomes.

MOCKED_DOCKER_COMPOSE_CALLS=()
MOCKED_SLEEP_CALLS=()
MOCKED_EXIT_CODE=0

# Override docker-compose and sleep functions for testing
docker-compose() {
    MOCKED_DOCKER_COMPOSE_CALLS+=("$@")
    echo "MOCK: docker-compose $@"
    return $MOCKED_EXIT_CODE
}

sleep() {
    MOCKED_SLEEP_CALLS+=("$@")
    echo "MOCK: sleep $@"
    return $MOCKED_EXIT_CODE
}

# Helper function to reset mocks and state for each test
reset_mocks() {
    MOCKED_DOCKER_COMPOSE_CALLS=()
    MOCKED_SLEEP_CALLS=()
    MOCKED_EXIT_CODE=0
    rm -f "$COMPOSE_FILE"
    rm -f "$NGINX_CONF"
    # Create a dummy compose file for tests
    cat > "$COMPOSE_FILE" <<EOF
version: '3.8'
services:
  test-service:
    image: alpine:latest
    command: echo "Hello from test container"
EOF
    cat > "$NGINX_CONF" <<EOF
events {}
http {
  server {
    listen 80;
    location / {
      return 200 'Hello from Nginx in Chrono-Container Garden!';
    }
  }
}
EOF
    # Ensure docker-compose mock is reset to default behavior
    unset -f docker-compose || true # Unset if it was temporarily redefined
    docker-compose() {
        MOCKED_DOCKER_COMPOSE_CALLS+=("$@")
        echo "MOCK: docker-compose $@"
        return $MOCKED_EXIT_CODE
    }
}

# Helper for assertions
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message (Expected: '$expected', Actual: '$actual')"
        exit 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" =~ "$needle" ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message (Expected to contain: '$needle', Actual: '$haystack')"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ ! "$haystack" =~ "$needle" ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message (Expected NOT to contain: '$needle', Actual: '$haystack')"
        exit 1
    fi
}

# --- Test Cases ---

# Test 1: Basic run with default project name
test_basic_run_default_project_name() {
    echo "\n--- Running Test 1: Basic run with default project name ---"
    reset_mocks

    local output
    output=$("$SCRIPT_PATH" --compose-file "$COMPOSE_FILE" --duration 1 2>&1)
    local exit_code=$?

    assert_equals 0 "$exit_code" "Script should exit successfully"
    assert_contains "$output" "MOCK: docker-compose -f $COMPOSE_FILE -p $(basename "$TEST_DIR")-\\d+ up -d" "docker-compose up -d should be called with default project name"
    assert_contains "$output" "MOCK: sleep 60" "sleep should be called with 60 seconds"
    assert_contains "$output" "MOCK: docker-compose -f $COMPOSE_FILE -p $(basename "$TEST_DIR")-\\d+ down" "docker-compose down should be called with default project name"
    assert_contains "$output" "No project name provided. Using generated name: $(basename "$TEST_DIR")-" "Should indicate default project name generation"
}

# Test 2: Basic run with custom project name
test_basic_run_custom_project_name() {
    echo "\n--- Running Test 2: Basic run with custom project name ---"
    reset_mocks

    local custom_project="my-custom-garden"
    local output
    output=$("$SCRIPT_PATH" --compose-file "$COMPOSE_FILE" --duration 2 --project-name "$custom_project" 2>&1)
    local exit_code=$?

    assert_equals 0 "$exit_code" "Script should exit successfully"
    assert_contains "$output" "MOCK: docker-compose -f $COMPOSE_FILE -p $custom_project up -d" "docker-compose up -d should be called with custom project name"
    assert_contains "$output" "MOCK: sleep 120" "sleep should be called with 120 seconds"
    assert_contains "$output" "MOCK: docker-compose -f $COMPOSE_FILE -p $custom_project down" "docker-compose down should be called with custom project name"
    assert_not_contains "$output" "No project name provided." "Should not indicate default project name generation"
}

# Test 3: Missing --compose-file argument
test_missing_compose_file() {
    echo "\n--- Running Test 3: Missing --compose-file argument ---"
    reset_mocks

    local output
    output=$("$SCRIPT_PATH" --duration 1 2>&1 || true)
    local exit_code=$?

    assert_equals 1 "$exit_code" "Script should exit with error"
    assert_contains "$output" "Error: --compose-file and a positive --duration are required." "Should show error for missing compose file"
    assert_equals 0 "${#MOCKED_DOCKER_COMPOSE_CALLS[@]}" "No docker-compose commands should be called"
}

# Test 4: Missing --duration argument
test_missing_duration() {
    echo "\n--- Running Test 4: Missing --duration argument ---"
    reset_mocks

    local output
    output=$("$SCRIPT_PATH" --compose-file "$COMPOSE_FILE" 2>&1 || true)
    local exit_code=$?

    assert_equals 1 "$exit_code" "Script should exit with error"
    assert_contains "$output" "Error: --compose-file and a positive --duration are required." "Should show error for missing duration"
    assert_equals 0 "${#MOCKED_DOCKER_COMPOSE_CALLS[@]}" "No docker-compose commands should be called"
}

# Test 5: Invalid duration (zero)
test_invalid_duration_zero() {
    echo "\n--- Running Test 5: Invalid duration (zero) ---"
    reset_mocks

    local output
    output=$("$SCRIPT_PATH" --compose-file "$COMPOSE_FILE" --duration 0 2>&1 || true)
    local exit_code=$?

    assert_equals 1 "$exit_code" "Script should exit with error"
    assert_contains "$output" "Error: --compose-file and a positive --duration are required." "Should show error for zero duration"
    assert_equals 0 "${#MOCKED_DOCKER_COMPOSE_CALLS[@]}" "No docker-compose commands should be called"
}

# Test 6: Invalid duration (negative)
test_invalid_duration_negative() {
    echo "\n--- Running Test 6: Invalid duration (negative) ---"
    reset_mocks

    local output
    output=$("$SCRIPT_PATH" --compose-file "$COMPOSE_FILE" --duration -5 2>&1 || true)
    local exit_code=$?

    assert_equals 1 "$exit_code" "Script should exit with error"
    assert_contains "$output" "Error: --compose-file and a positive --duration are required." "Should show error for negative duration"
    assert_equals 0 "${#MOCKED_DOCKER_COMPOSE_CALLS[@]}" "No docker-compose commands should be called"
}

# Test 7: Compose file not found
test_compose_file_not_found() {
    echo "\n--- Running Test 7: Compose file not found ---"
    reset_mocks
    rm "$COMPOSE_FILE" # Ensure file does not exist

    local output
    output=$("$SCRIPT_PATH" --compose-file "$COMPOSE_FILE" --duration 1 2>&1 || true)
    local exit_code=$?

    assert_equals 1 "$exit_code" "Script should exit with error"
    assert_contains "$output" "Error: Docker Compose file not found at '$COMPOSE_FILE'." "Should show error for non-existent compose file"
    assert_equals 0 "${#MOCKED_DOCKER_COMPOSE_CALLS[@]}" "No docker-compose commands should be called"
}

# Test 8: docker-compose up fails
test_docker_compose_up_fails() {
    echo "\n--- Running Test 8: docker-compose up fails ---"
    reset_mocks
    MOCKED_EXIT_CODE=1 # Simulate failure for docker-compose

    local output
    output=$("$SCRIPT_PATH" --compose-file "$COMPOSE_FILE" --duration 1 2>&1 || true)
    local exit_code=$?

    assert_equals 1 "$exit_code" "Script should exit with error"
    assert_contains "$output" "Failed to plant the garden." "Should report failure to plant garden"
    assert_contains "$output" "MOCK: docker-compose -f $COMPOSE_FILE -p $(basename "$TEST_DIR")-\\d+ up -d" "docker-compose up -d should be attempted"
    assert_equals 1 "${#MOCKED_DOCKER_COMPOSE_CALLS[@]}" "Only docker-compose up should be called"
    assert_equals 0 "${#MOCKED_SLEEP_CALLS[@]}" "sleep should not be called"
}

# Test 9: docker-compose down fails
test_docker_compose_down_fails() {
    echo "\n--- Running Test 9: docker-compose down fails ---"
    reset_mocks

    # Temporarily redefine docker-compose mock to simulate specific failure
    local docker_compose_call_count=0
    docker-compose() {
        docker_compose_call_count=$((docker_compose_call_count + 1))
        MOCKED_DOCKER_COMPOSE_CALLS+=("$@")
        echo "MOCK: docker-compose $@ (call $docker_compose_call_count)"
        if [[ "$docker_compose_call_count" -eq 2 ]]; then
            return 1 # Simulate failure for 'down' command
        else
            return 0 # Simulate success for 'up' command
        fi
    }

    local output
    output=$("$SCRIPT_PATH" --compose-file "$COMPOSE_FILE" --duration 1 2>&1 || true)
    local exit_code=$?

    assert_equals 1 "$exit_code" "Script should exit with error if down fails"
    assert_contains "$output" "Failed to prune the garden." "Should report failure to prune garden"
    assert_contains "$output" "MOCK: docker-compose -f $COMPOSE_FILE -p $(basename "$TEST_DIR")-\\d+ up -d" "docker-compose up -d should be attempted"
    assert_contains "$output" "MOCK: docker-compose -f $COMPOSE_FILE -p $(basename "$TEST_DIR")-\\d+ down" "docker-compose down should be attempted"
    assert_equals 2 "${#MOCKED_DOCKER_COMPOSE_CALLS[@]}" "Both docker-compose up and down should be called"
    assert_equals 1 "${#MOCKED_SLEEP_CALLS[@]}" "sleep should be called once"

    # Reset docker-compose mock for subsequent tests by calling reset_mocks again
    reset_mocks
}

# --- Run all tests ---

test_basic_run_default_project_name
test_basic_run_custom_project_name
test_missing_compose_file
test_missing_duration
test_invalid_duration_zero
test_invalid_duration_negative
test_compose_file_not_found
test_docker_compose_up_fails
test_docker_compose_down_fails

# --- Cleanup ---
rm -rf "$TEST_DIR"

echo "\nAll tests completed!"
