#!/bin/bash

set -euo pipefail

# --- Test Setup ---

# Mock rationale: We need to test the script's logic (parsing arguments,
# generating Dockerfiles, calling docker commands) without actually
# performing Docker builds or runs, which would be slow, require a
# Docker daemon, and not be deterministic.
# This mock captures the arguments passed to 'docker' and simulates
# success or specific outputs. It also allows us to inspect the generated
# Dockerfile content without actually building an image.

MOCK_DOCKER_LOG="$(mktemp)"
MOCK_CHAMBER_DIR="$(mktemp -d)"
export HOME="$MOCK_CHAMBER_DIR" # Redirect chamber config to mock home

# Override the docker command with our mock function
docker() {
    echo "MOCK_DOCKER_CALL: $@" >> "$MOCK_DOCKER_LOG"
    case "$1" in
        build)
            # Simulate successful build
            echo "Successfully built image nightly-temporal-dev-chamber-$3" >&2
            return 0
            ;;
        run)
            # Simulate successful run
            echo "Container nightly-temporal-dev-chamber-$3 started." >&2
            return 0
            ;;
        *)
            echo "MOCK_DOCKER: Unknown command: $@" >&2
            return 1
            ;;
    esac
}

# Path to the script under test
SCRIPT_PATH="$(dirname "$0")"/../src/temporal_chamber.sh

# --- Helper Functions ---

assert_contains() {
    local expected="$1"
    local actual="$2"
    if ! echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: Expected '$actual' to contain '$expected'"
        exit 1
    fi
}

assert_not_contains() {
    local expected="$1"
    local actual="$2"
    if echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: Expected '$actual' NOT to contain '$expected'"
        exit 1
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    if [ "$expected" != "$actual" ]; then
        echo "FAIL: Expected '$expected', got '$actual'"
        exit 1
    fi
}

assert_exit_code() {
    local expected_code="$1"
    local actual_code="$2"
    if [ "$expected_code" -ne "$actual_code" ]; then
        echo "FAIL: Expected exit code $expected_code, got $actual_code"
        exit 1
    fi
}

run_test() {
    local test_name="$1"
    echo "Running test: $test_name"
    # Clear mock log and config before each test
    > "$MOCK_DOCKER_LOG"
    rm -f "$MOCK_CHAMBER_DIR/.nightly-temporal-dev-chamber/chambers.conf"
    mkdir -p "$MOCK_CHAMBER_DIR/.nightly-temporal-dev-chamber"
    touch "$MOCK_CHAMBER_DIR/.nightly-temporal-dev-chamber/chambers.conf"

    # Execute the test function
    "$test_name"
    echo "PASS: $test_name"
}

# --- Test Cases ---

test_build_chamber_basic() {
    local chamber_name="test-basic"
    local base_image="ubuntu:20.04"
    local output
    output=$("$SCRIPT_PATH" build "$chamber_name" "$base_image" 2>&1)
    local exit_code=$?

    assert_exit_code 0 "$exit_code"
    assert_contains "Building temporal chamber 'test-basic'" "$output"
    assert_contains "MOCK_DOCKER_CALL: build -t nightly-temporal-dev-chamber-test-basic" "$(cat "$MOCK_DOCKER_LOG")"
    assert_contains "FROM ubuntu:20.04" "$output" # Check Dockerfile content in output
    assert_not_contains "RUN" "$output" # No setup commands
    assert_contains "${chamber_name}:${base_image}:" "$(cat "$MOCK_CHAMBER_DIR/.nightly-temporal-dev-chamber/chambers.conf")"
}

test_build_chamber_with_setup() {
    local chamber_name="test-setup"
    local base_image="python:3.9-slim"
    local setup_commands="pip install requests"
    local output
    output=$("$SCRIPT_PATH" build "$chamber_name" "$base_image" "$setup_commands" 2>&1)
    local exit_code=$?

    assert_exit_code 0 "$exit_code"
    assert_contains "Building temporal chamber 'test-setup'" "$output"
    assert_contains "MOCK_DOCKER_CALL: build -t nightly-temporal-dev-chamber-test-setup" "$(cat "$MOCK_DOCKER_LOG")"
    assert_contains "FROM python:3.9-slim" "$output"
    assert_contains "RUN pip install requests" "$output" # Check setup commands
    assert_contains "${chamber_name}:${base_image}:${setup_commands}" "$(cat "$MOCK_CHAMBER_DIR/.nightly-temporal-dev-chamber/chambers.conf")"
}

test_build_chamber_already_exists() {
    local chamber_name="test-exists"
    local base_image="alpine"
    # First build (mocked)
    "$SCRIPT_PATH" build "$chamber_name" "$base_image" > /dev/null 2>&1

    # Second build, should fail
    local output
    output=$("$SCRIPT_PATH" build "$chamber_name" "$base_image" 2>&1)
    local exit_code=$?

    assert_exit_code 1 "$exit_code"
    assert_contains "Error: Chamber 'test-exists' already exists." "$output"
}

test_run_chamber_basic() {
    local chamber_name="test-run"
    local base_image="debian"
    # Build the chamber first (mocked)
    "$SCRIPT_PATH" build "$chamber_name" "$base_image" > /dev/null 2>&1

    local output
    output=$("$SCRIPT_PATH" run "$chamber_name" 2>&1)
    local exit_code=$?

    assert_exit_code 0 "$exit_code"
    assert_contains "Running temporal chamber 'test-run' with command: 'bash'" "$output"
    assert_contains "MOCK_DOCKER_CALL: run -it --rm -v $(pwd):/app -w /app nightly-temporal-dev-chamber-test-run bash" "$(cat "$MOCK_DOCKER_LOG")"
}

test_run_chamber_with_command() {
    local chamber_name="test-run-cmd"
    local base_image="fedora"
    local custom_command="ls -la"
    # Build the chamber first (mocked)
    "$SCRIPT_PATH" build "$chamber_name" "$base_image" > /dev/null 2>&1

    local output
    output=$("$SCRIPT_PATH" run "$chamber_name" "$custom_command" 2>&1)
    local exit_code=$?

    assert_exit_code 0 "$exit_code"
    assert_contains "Running temporal chamber 'test-run-cmd' with command: 'ls -la'" "$output"
    assert_contains "MOCK_DOCKER_CALL: run -it --rm -v $(pwd):/app -w /app nightly-temporal-dev-chamber-test-run-cmd ls -la" "$(cat "$MOCK_DOCKER_LOG")"
}

test_run_chamber_not_found() {
    local chamber_name="non-existent-chamber"
    local output
    output=$("$SCRIPT_PATH" run "$chamber_name" 2>&1)
    local exit_code=$?

    assert_exit_code 1 "$exit_code"
    assert_contains "Error: Chamber 'non-existent-chamber' not found." "$output"
}

test_list_chambers_empty() {
    local output
    output=$("$SCRIPT_PATH" list 2>&1)
    local exit_code=$?

    assert_exit_code 0 "$exit_code"
    assert_contains "No chambers configured yet." "$output"
}

test_list_chambers_populated() {
    local chamber1_name="chamber-one"
    local chamber1_image="alpine"
    local chamber1_setup="apk add git"
    local chamber2_name="chamber-two"
    local chamber2_image="centos"

    "$SCRIPT_PATH" build "$chamber1_name" "$chamber1_image" "$chamber1_setup" > /dev/null 2>&1
    "$SCRIPT_PATH" build "$chamber2_name" "$chamber2_image" > /dev/null 2>&1

    local output
    output=$("$SCRIPT_PATH" list 2>&1)
    local exit_code=$?

    assert_exit_code 0 "$exit_code"
    assert_contains "Name: chamber-one" "$output"
    assert_contains "Base Image: alpine" "$output"
    assert_contains "Setup Commands: apk add git" "$output"
    assert_contains "Name: chamber-two" "$output"
    assert_contains "Base Image: centos" "$output"
    assert_not_contains "Setup Commands:" "$output" # For chamber-two
}

test_invalid_command() {
    local output
    output=$("$SCRIPT_PATH" invalid-cmd 2>&1)
    local exit_code=$?

    assert_exit_code 1 "$exit_code"
    assert_contains "Error: Unknown command: invalid-cmd. Usage: $0 {build|run|list}" "$output"
}

test_build_missing_args() {
    local output
    output=$("$SCRIPT_PATH" build test-name 2>&1)
    local exit_code=$?

    assert_exit_code 1 "$exit_code"
    assert_contains "Error: Usage: $0 build <chamber_name> <base_image> [setup_commands]" "$output"
}

test_run_missing_args() {
    local output
    output=$("$SCRIPT_PATH" run 2>&1)
    local exit_code=$?

    assert_exit_code 1 "$exit_code"
    assert_contains "Error: Usage: $0 run <chamber_name> [command]" "$output"
}

# --- Run all tests ---

run_test test_build_chamber_basic
run_test test_build_chamber_with_setup
run_test test_build_chamber_already_exists
run_test test_run_chamber_basic
run_test test_run_chamber_with_command
run_test test_run_chamber_not_found
run_test test_list_chambers_empty
run_test test_list_chambers_populated
run_test test_invalid_command
run_test test_build_missing_args
run_test test_run_missing_args

# --- Cleanup ---
rm -f "$MOCK_DOCKER_LOG"
rm -rf "$MOCK_CHAMBER_DIR"

echo "All tests passed!"
