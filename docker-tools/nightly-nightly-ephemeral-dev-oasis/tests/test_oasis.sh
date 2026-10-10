#!/bin/bash

set -euo pipefail

# --- Test Setup --- #
TEST_DIR="$(dirname \"$0\")"
UTIL_DIR="$TEST_DIR/../src"
MOCK_LOG="$TEST_DIR/mock_docker_compose.log"

# Mock rationale: We don't want to actually run Docker commands during unit tests,
# as it would be slow, require Docker daemon, and not be deterministic.
# We mock docker-compose and docker commands to verify that the correct commands are invoked.

# Global variable to simulate docker-compose ps output
MOCK_PS_RUNNING="false"

mock_docker_compose() {
    echo "MOCKED docker-compose $*" >> "$MOCK_LOG"
    case "$1" in
        "build")
            # Simulate build success
            ;;
        "up")
            if [[ "$2" == "-d" ]]; then
                MOCK_PS_RUNNING="true"
            fi
            ;;
        "down")
            MOCK_PS_RUNNING="false"
            ;;
        "ps")
            if [[ "$MOCK_PS_RUNNING" == "true" ]]; then
                echo "nightly-oasis-shell"
            else
                echo ""
            fi
            ;;
        *) # Catch-all for unexpected commands
            echo "Unknown docker-compose command: $*" >> "$MOCK_LOG"
            return 1
            ;;
    esac
    return 0
}

mock_docker() {
    echo "MOCKED docker $*" >> "$MOCK_LOG"
    case "$1" in
        "exec")
            # Simulate exec success
            ;;
        *) # Catch-all for unexpected commands
            echo "Unknown docker command: $*" >> "$MOCK_LOG"
            return 1
            ;;
    esac
    return 0
}

# Override the real docker-compose and docker with our mocks for testing
export DOCKER_COMPOSE_CMD="$(command -v bash) -c 'mock_docker_compose' --"
export docker="$(command -v bash) -c 'mock_docker' --"

# Function to run the oasis.sh script with mocks
run_oasis_script() {
    bash "$UTIL_DIR/oasis.sh" "$@"
}

# --- Test Cases --- #

# Test 1: `create` command
test_create_command() {
    echo "Running test_create_command..."
    rm -f "$MOCK_LOG"
    MOCK_PS_RUNNING="false"

    # Ensure work directory doesn't exist initially for this test
    rm -rf "$UTIL_DIR/work"

    run_oasis_script create > /dev/null 2>&1

    grep -q "MOCKED docker-compose -f $UTIL_DIR/docker-compose.yml build" "$MOCK_LOG"
    assert_equals $? 0 "Expected 'docker-compose build' call"

    grep -q "MOCKED docker-compose -f $UTIL_DIR/docker-compose.yml up -d" "$MOCK_LOG"
    assert_equals $? 0 "Expected 'docker-compose up -d' call"

    # Verify work directory was created
    test -d "$UTIL_DIR/work"
    assert_equals $? 0 "Expected 'src/work' directory to be created"

    echo "test_create_command PASSED"
}

# Test 2: `enter` command when oasis is running
test_enter_command_running() {
    echo "Running test_enter_command_running..."
    rm -f "$MOCK_LOG"
    MOCK_PS_RUNNING="true" # Simulate container already running

    run_oasis_script enter > /dev/null 2>&1

    grep -q "MOCKED docker-compose -f $UTIL_DIR/docker-compose.yml ps --services --filter status=running" "$MOCK_LOG"
    assert_equals $? 0 "Expected 'docker-compose ps' call"

    grep -q "MOCKED docker exec -it nightly-oasis-shell bash" "$MOCK_LOG"
    assert_equals $? 0 "Expected 'docker exec' call"

    echo "test_enter_command_running PASSED"
}

# Test 3: `enter` command when oasis is NOT running
test_enter_command_not_running() {
    echo "Running test_enter_command_not_running..."
    rm -f "$MOCK_LOG"
    MOCK_PS_RUNNING="false" # Simulate container not running

    # Expect an error, so capture stderr and check exit code
    output=$(run_oasis_script enter 2>&1 || true)
    assert_contains "Error: Oasis 'nightly-oasis-shell' is not running." "$output" "Expected error message for not running oasis"
    assert_equals $? 0 "Expected 'enter' to fail when oasis is not running"

    # Ensure docker exec was NOT called
    ! grep -q "MOCKED docker exec" "$MOCK_LOG"
    assert_equals $? 0 "Expected 'docker exec' NOT to be called"

    echo "test_enter_command_not_running PASSED"
}

# Test 4: `destroy` command
test_destroy_command() {
    echo "Running test_destroy_command..."
    rm -f "$MOCK_LOG"
    MOCK_PS_RUNNING="true" # Simulate container running before destroy

    run_oasis_script destroy > /dev/null 2>&1

    grep -q "MOCKED docker-compose -f $UTIL_DIR/docker-compose.yml down" "$MOCK_LOG"
    assert_equals $? 0 "Expected 'docker-compose down' call"

    echo "test_destroy_command PASSED"
}

# Test 5: `list` command
test_list_command() {
    echo "Running test_list_command..."
    rm -f "$MOCK_LOG"
    MOCK_PS_RUNNING="true" # Simulate container running for list

    output=$(run_oasis_script list)

    grep -q "MOCKED docker-compose -f $UTIL_DIR/docker-compose.yml ps" "$MOCK_LOG"
    assert_equals $? 0 "Expected 'docker-compose ps' call"

    assert_contains "nightly-oasis-shell" "$output" "Expected 'nightly-oasis-shell' in list output"

    echo "test_list_command PASSED"
}

# Test 6: `list` command when no oasis is running
test_list_command_no_oasis() {
    echo "Running test_list_command_no_oasis..."
    rm -f "$MOCK_LOG"
    MOCK_PS_RUNNING="false" # Simulate no container running for list

    output=$(run_oasis_script list)

    grep -q "MOCKED docker-compose -f $UTIL_DIR/docker-compose.yml ps" "$MOCK_LOG"
    assert_equals $? 0 "Expected 'docker-compose ps' call"

    ! assert_contains "nightly-oasis-shell" "$output" "Expected 'nightly-oasis-shell' NOT in list output"

    echo "test_list_command_no_oasis PASSED"
}

# Test 7: Invalid command
test_invalid_command() {
    echo "Running test_invalid_command..."
    rm -f "$MOCK_LOG"

    output=$(run_oasis_script invalid_cmd 2>&1 || true)
    assert_contains "Usage: $UTIL_DIR/oasis.sh {create|enter|destroy|list}" "$output" "Expected usage message for invalid command"
    assert_equals $? 0 "Expected 'invalid_cmd' to fail"

    echo "test_invalid_command PASSED"
}

# --- Assertion Helpers --- #
assert_equals() {
    if [ "$1" -ne "$2" ]; then
        echo "FAIL: $3 (Expected: $1, Got: $2)"
        exit 1
    fi
}

assert_contains() {
    if ! echo "$2" | grep -qF "$1"; then
        echo "FAIL: $3 (Expected to contain: '$1', Got: '$2')"
        exit 1
    fi
}

# --- Run Tests --- #
cleanup() {
    rm -f "$MOCK_LOG"
    rm -rf "$UTIL_DIR/work" # Clean up work directory created by tests
}
trap cleanup EXIT

cleanup # Initial cleanup

test_create_command
test_enter_command_running
test_enter_command_not_running
test_destroy_command
test_list_command
test_list_command_no_oasis
test_invalid_command

echo "All tests PASSED!"
