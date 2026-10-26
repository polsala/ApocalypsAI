#!/bin/bash

# Mock rationale: We cannot run actual docker commands in an offline, deterministic test.
# Mocking the `docker` command allows us to verify that the `compost_bin.sh` script
# attempts to execute the correct `docker` subcommands with the expected arguments,
# without needing a live Docker daemon.

# Store expected calls
declare -a MOCKED_CALLS

# Mock docker command
docker() {
    local cmd="$1"
    shift
    local args="$@"
    local full_command="docker $cmd $args"
    echo "MOCK: $full_command" >&2 # Log mock calls for debugging
    MOCKED_CALLS+=("$full_command")
    return 0 # Always succeed for mock
}

# Helper function to assert a command was called
assert_called() {
    local expected_command="$1"
    local found=0
    for call in "${MOCKED_CALLS[@]}"; do
        if [[ "$call" == "$expected_command" ]]; then
            found=1
            break
        fi
    done

    if [ "$found" -eq 1 ]; then
        echo "PASS: Expected command '$expected_command' was called."
    else
        echo "FAIL: Expected command '$expected_command' was NOT called."
        exit 1
    fi
}

# Helper function to reset mocks
reset_mocks() {
    MOCKED_CALLS=()
}

echo "Running tests for compost_bin.sh"
echo "---"

# Test Case 1: Default pruning (7 days)
echo "Test Case 1: Default pruning (7 days)"
reset_mocks
COMPOST_DAYS_OLD= ./src/compost_bin.sh # Run with default
assert_called "docker container prune --force --filter until=168h"
assert_called "docker image prune --force --filter dangling=true"
assert_called "docker image prune --force --filter until=168h"
assert_called "docker volume prune --force --filter until=168h"
echo "---"

# Test Case 2: Custom pruning age (1 day)
echo "Test Case 2: Custom pruning age (1 day)"
reset_mocks
COMPOST_DAYS_OLD=1 ./src/compost_bin.sh
assert_called "docker container prune --force --filter until=24h"
assert_called "docker image prune --force --filter dangling=true"
assert_called "docker image prune --force --filter until=24h"
assert_called "docker volume prune --force --filter until=24h"
echo "---"

# Test Case 3: Custom pruning age (0 days - effectively immediate)
echo "Test Case 3: Custom pruning age (0 days)"
reset_mocks
COMPOST_DAYS_OLD=0 ./src/compost_bin.sh
assert_called "docker container prune --force --filter until=0h"
assert_called "docker image prune --force --filter dangling=true"
assert_called "docker image prune --force --filter until=0h"
assert_called "docker volume prune --force --filter until=0h"
echo "---"

echo "All tests passed!"
