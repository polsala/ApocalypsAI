#!/bin/bash

set -euo pipefail

# --- Test Setup ---

# Mock rationale: We want to test the shell script's logic for constructing docker commands,
# not actually run Docker. We'll replace the 'docker' command with a mock function
# that prints its arguments and simulates success/failure.

mock_docker_output=""
mock_docker_exit_code=0

docker() {
    mock_docker_output="MOCK_DOCKER_CALL: $@"
    case "$1" in
        "build")
            if [[ "$2" == "-t" && "$3" == *":latest" ]]; then
                echo "Successfully built $3"
                mock_docker_exit_code=0
            else
                mock_docker_exit_code=1
            fi
            ;;
        "run")
            if [[ "$2" == "--rm" && "$3" == *":latest" ]]; then
                echo "MOCK_OUTPUT: Running command in $3"
                mock_docker_exit_code=0
            else
                mock_docker_exit_code=1
            fi
            ;;
        "images")
            echo "REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE"
            echo "test-chamber        latest              abcdef123456        2 minutes ago       100MB"
            echo "another-chamber     latest              fedcba654321        5 minutes ago       200MB"
            mock_docker_exit_code=0
            ;;
        "rmi")
            if [[ "$2" == *":latest" ]]; then
                echo "Deleted $2"
                mock_docker_exit_code=0
            else
                mock_docker_exit_code=1
            fi
            ;;
        *)
            mock_docker_exit_code=1
            ;;
    esac
    return ${mock_docker_exit_code}
}

# Redirect stdout/stderr to /dev/null for cleaner test output, capture for assertions
exec 3>&1 # Save stdout
exec 4>&2 # Save stderr

# --- Test Helper Functions ---

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "${expected}" == "${actual}" ]]; then
        echo "✓ ${message}"
    else
        echo "✗ ${message}"
        echo "  Expected: '${expected}'"
        echo "  Actual:   '${actual}'"
        exit 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "${haystack}" == *"${needle}"* ]]; then
        echo "✓ ${message}"
    else
        echo "✗ ${message}"
        echo "  Expected to contain: '${needle}'"
        echo "  Actual:              '${haystack}'"
        exit 1
    fi
}

# --- Tests ---

TEST_DIR="$(dirname "$0")"
SRC_DIR="${TEST_DIR}/../src"
CHAMBER_MANAGER_SCRIPT="${SRC_DIR}/chamber_manager.sh"

# Create a dummy Dockerfile for testing build command
TEST_DOCKERFILE="${TEST_DIR}/TestDockerfile"
echo "FROM alpine" > "${TEST_DOCKERFILE}"

# Test 1: build_chamber with valid arguments
run_test_build_valid() {
    echo "\n--- Running Test: build_chamber with valid arguments ---"
    output=$(bash "${CHAMBER_MANAGER_SCRIPT}" build test-chamber "${TEST_DOCKERFILE}" --build-arg TEST_VAR=value 2>&1)
    assert_contains "${output}" "MOCK_DOCKER_CALL: build -t test-chamber:latest -f ${TEST_DOCKERFILE} --build-arg TEST_VAR=value ${TEST_DIR}" "build_chamber calls docker build correctly"
    assert_contains "${output}" "Chamber 'test-chamber' built successfully." "build_chamber reports success"
}

# Test 2: build_chamber with missing Dockerfile
run_test_build_missing_dockerfile() {
    echo "\n--- Running Test: build_chamber with missing Dockerfile ---"
    output=$(bash "${CHAMBER_MANAGER_SCRIPT}" build missing-chamber "${TEST_DIR}/NonExistentDockerfile" 2>&1 || true)
    assert_contains "${output}" "Dockerfile not found at: ${TEST_DIR}/NonExistentDockerfile" "build_chamber handles missing Dockerfile"
    assert_contains "${output}" "[ERROR]" "build_chamber outputs error for missing Dockerfile"
}

# Test 3: run_chamber with valid arguments
run_test_run_valid() {
    echo "\n--- Running Test: run_chamber with valid arguments ---"
    output=$(bash "${CHAMBER_MANAGER_SCRIPT}" run test-chamber "echo Hello" 2>&1)
    assert_contains "${output}" "MOCK_DOCKER_CALL: run --rm test-chamber:latest bash -c echo Hello" "run_chamber calls docker run correctly"
    assert_contains "${output}" "MOCK_OUTPUT: Running command in test-chamber" "run_chamber reports command execution"
}

# Test 4: enter_chamber with valid arguments
run_test_enter_valid() {
    echo "\n--- Running Test: enter_chamber with valid arguments ---"
    output=$(bash "${CHAMBER_MANAGER_SCRIPT}" enter test-chamber 2>&1)
    assert_contains "${output}" "MOCK_DOCKER_CALL: run -it --rm test-chamber:latest" "enter_chamber calls docker run -it correctly"
    assert_contains "${output}" "Entering temporal chamber: test-chamber" "enter_chamber reports entering chamber"
}

# Test 5: list_chambers
run_test_list_chambers() {
    echo "\n--- Running Test: list_chambers ---"
    output=$(bash "${CHAMBER_MANAGER_SCRIPT}" list 2>&1)
    assert_contains "${output}" "MOCK_DOCKER_CALL: images --filter label=description=Temporal Development Chamber Base Image --format {{.Repository}}	{{.Tag}}" "list_chambers calls docker images correctly"
    assert_contains "${output}" "test-chamber\tlatest" "list_chambers shows test-chamber"
    assert_contains "${output}" "another-chamber\tlatest" "list_chambers shows another-chamber"
}

# Test 6: clean_chamber with valid arguments
run_test_clean_valid() {
    echo "\n--- Running Test: clean_chamber with valid arguments ---"
    output=$(bash "${CHAMBER_MANAGER_SCRIPT}" clean test-chamber 2>&1)
    assert_contains "${output}" "MOCK_DOCKER_CALL: rmi test-chamber:latest" "clean_chamber calls docker rmi correctly"
    assert_contains "${output}" "Chamber 'test-chamber' removed." "clean_chamber reports removal"
}

# Test 7: No command provided
run_test_no_command() {
    echo "\n--- Running Test: No command provided ---"
    output=$(bash "${CHAMBER_MANAGER_SCRIPT}" 2>&1 || true)
    assert_contains "${output}" "[ERROR] No command provided." "Script exits with error if no command"
    assert_contains "${output}" "Usage: $0 <command> [args...]" "Script shows usage on no command"
}

# Test 8: Unknown command
run_test_unknown_command() {
    echo "\n--- Running Test: Unknown command ---"
    output=$(bash "${CHAMBER_MANAGER_SCRIPT}" foobar 2>&1 || true)
    assert_contains "${output}" "[ERROR] Unknown command: foobar" "Script exits with error on unknown command"
    assert_contains "${output}" "Usage: $0 <command> [args...]" "Script shows usage on unknown command"
}

# Run all tests
run_test_build_valid
run_test_build_missing_dockerfile
run_test_run_valid
run_test_enter_valid
run_test_list_chambers
run_test_clean_valid
run_test_no_command
run_test_unknown_command

# Cleanup dummy Dockerfile
rm -f "${TEST_DOCKERFILE}"

echo "\nAll tests passed!"
