#!/bin/bash

set -euo pipefail

# Mock the actionlint command
# This mock simulates actionlint returning success (exit code 0)
mock_actionlint_success() {
    echo "Mock actionlint: $1"
    return 0
}

# This mock simulates actionlint returning failure (exit code 1)
mock_actionlint_failure() {
    echo "Mock actionlint: $1"
    echo "::error file=$1::Mock linting error."
    return 1
}

# Mock the find command to return specific files
mock_find() {
    echo "Mock find: $1"
    if [[ "$1" == *'.github/workflows/*.yml'* ]]; then
        echo "./.github/workflows/main.yml"
        echo "./.github/workflows/deploy.yml"
    fi
    return 0
}

# Mock the command -v command to always find actionlint
mock_command_v() {
    echo "Mock command -v: $1"
    if [ "$1" == "actionlint" ]; then
        return 0
    fi
    return 1
}

# --- Test Cases ---

# Test 1: All workflows lint successfully
test_all_success() {
    echo "--- Running Test 1: All workflows lint successfully ---"

    # Override commands with mocks
    local original_actionlint=$(declare -f actionlint)
    local original_find=$(declare -f find)
    local original_command_v=$(declare -f command)

    actionlint() { mock_actionlint_success "$@"; }
    find() { mock_find "$@"; }
    command() { mock_command_v "$@"; }

    # Execute the script
    if bash src/main.sh; then
        echo "Test 1 Passed: All workflows linted successfully."
    else
        echo "Test 1 Failed: Script exited with non-zero status."
    fi

    # Restore original commands
    eval "$original_actionlint"
    eval "$original_find"
    eval "$original_command_v"
}

# Test 2: One workflow fails linting
test_one_failure() {
    echo "--- Running Test 2: One workflow fails linting ---"

    local original_actionlint=$(declare -f actionlint)
    local original_find=$(declare -f find)
    local original_command_v=$(declare -f command)

    # Mock actionlint to fail for one specific file
    actionlint() {
        if [[ "$1" == "./.github/workflows/deploy.yml" ]]; then
            mock_actionlint_failure "$@"
        else
            mock_actionlint_success "$@"
        fi
    }
    find() { mock_find "$@"; }
    command() { mock_command_v "$@"; }

    # Execute the script - expect it to fail
    if ! bash src/main.sh; then
        echo "Test 2 Passed: Script correctly failed due to linting error."
    else
        echo "Test 2 Failed: Script did not fail when a linting error was present."
    fi

    # Restore original commands
    eval "$original_actionlint"
    eval "$original_find"
    eval "$original_command_v"
}

# Test 3: No workflow files found
test_no_files() {
    echo "--- Running Test 3: No workflow files found ---"

    local original_actionlint=$(declare -f actionlint)
    local original_find=$(declare -f find)
    local original_command_v=$(declare -f command)

    # Mock find to return nothing
    find() {
        echo "Mock find: $1"
        return 0 # Return success, but no output
    }
    actionlint() { mock_actionlint_success "$@"; }
    command() { mock_command_v "$@"; }

    # Execute the script - expect it to succeed and report no files found
    if bash src/main.sh; then
        echo "Test 3 Passed: Script handled no workflow files gracefully."
    else
        echo "Test 3 Failed: Script exited with non-zero status when no files were found."
    fi

    # Restore original commands
    eval "$original_actionlint"
    eval "$original_find"
    eval "$original_command_v"
}

# Test 4: Custom workflow path
test_custom_path() {
    echo "--- Running Test 4: Custom workflow path ---"

    local original_actionlint=$(declare -f actionlint)
    local original_find=$(declare -f find)
    local original_command_v=$(declare -f command)

    # Mock find to only return a specific file
    find() {
        echo "Mock find: $1"
        if [[ "$1" == *'my_specific_workflow.yml'* ]]; then
            echo "./.github/workflows/my_specific_workflow.yml"
        fi
        return 0
    }
    actionlint() { mock_actionlint_success "$@"; }
    command() { mock_command_v "$@"; }

    # Execute the script with a custom path
    if INPUT_WORKFLOW_PATH='.github/workflows/my_specific_workflow.yml' bash src/main.sh; then
        echo "Test 4 Passed: Custom workflow path handled correctly."
    else
        echo "Test 4 Failed: Script did not handle custom path correctly."
    fi

    # Restore original commands
    eval "$original_actionlint"
    eval "$original_find"
    eval "$original_command_v"
}

# --- Run Tests ---

test_all_success
test_one_failure
test_no_files
test_custom_path

echo "All tests completed."
