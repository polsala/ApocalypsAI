#!/bin/bash

# Test suite for Nightly Container Compost Heap

# Mock rationale: We need to prevent actual docker commands from running during tests.
# This mock function will capture calls to 'docker' and allow us to assert arguments.
MOCKED_DOCKER_CALLS=""
docker() {
    MOCKED_DOCKER_CALLS+="docker $@\n"
    # Simulate success for prune command
    # The arguments passed to docker are split by bash, so "until=24h" will be one argument.
    if [[ "$1" == "system" && "$2" == "prune" && "$3" == "--force" && "$4" == "--all" && "$5" == "--volumes" && "$6" == "--filter" && "$7" == "until=24h" ]]; then
        echo "Total reclaimed space: 123.4MB"
        return 0
    fi
    # Simulate other docker commands if needed, or fail by default
    echo "Mocked docker command: $@" >&2
    return 0
}

# Source the script to be tested
SCRIPT_TO_TEST="../src/compost_heap.sh"

# Test function for dry-run
test_dry_run() {
    echo "Running test_dry_run..."
    MOCKED_DOCKER_CALLS="" # Reset mock calls

    OUTPUT=$(bash "$SCRIPT_TO_TEST" --dry-run)
    EXIT_CODE=$?

    if [ "$EXIT_CODE" -ne 0 ]; then
        echo "FAIL: test_dry_run - Script exited with non-zero code: $EXIT_CODE"
        echo "Output: $OUTPUT"
        return 1
    fi

    if ! echo "$OUTPUT" | grep -q "Digital Compost Report (Dry Run)"; then
        echo "FAIL: test_dry_run - Output missing 'Digital Compost Report (Dry Run)'"
        echo "Output: $OUTPUT"
        return 1
    fi

    if ! echo "$OUTPUT" | grep -q "To actually prune these, run with '--prune'."; then
        echo "FAIL: test_dry_run - Output missing dry-run instruction"
        echo "Output: $OUTPUT"
        return 1
    fi

    if [ -n "$MOCKED_DOCKER_CALLS" ]; then
        echo "FAIL: test_dry_run - Docker command was called during dry-run: $MOCKED_DOCKER_CALLS"
        return 1
    fi

    echo "PASS: test_dry_run"
    return 0
}

# Test function for prune
test_prune() {
    echo "Running test_prune..."
    MOCKED_DOCKER_CALLS="" # Reset mock calls

    OUTPUT=$(bash "$SCRIPT_TO_TEST" --prune)
    EXIT_CODE=$?

    if [ "$EXIT_CODE" -ne 0 ]; then
        echo "FAIL: test_prune - Script exited with non-zero code: $EXIT_CODE"
        echo "Output: $OUTPUT"
        return 1
    fi

    # Check if the specific docker prune command was called
    EXPECTED_DOCKER_CALL_PATTERN="docker system prune --force --all --volumes --filter until=24h"
    if ! echo "$MOCKED_DOCKER_CALLS" | grep -qF "$EXPECTED_DOCKER_CALL_PATTERN"; then
        echo "FAIL: test_prune - Expected docker prune command not called."
        echo "Expected pattern: '$EXPECTED_DOCKER_CALL_PATTERN'"
        echo "Actual calls: '$MOCKED_DOCKER_CALLS'"
        return 1
    fi

    if ! echo "$OUTPUT" | grep -q "Digital compost created!"; then
        echo "FAIL: test_prune - Output missing success message"
        echo "Output: $OUTPUT"
        return 1
    fi

    echo "PASS: test_prune"
    return 0
}

# Test function for invalid argument
test_invalid_arg() {
    echo "Running test_invalid_arg..."
    MOCKED_DOCKER_CALLS="" # Reset mock calls

    OUTPUT=$(bash "$SCRIPT_TO_TEST" --invalid-arg 2>&1) # Redirect stderr to stdout
    EXIT_CODE=$?

    if [ "$EXIT_CODE" -eq 0 ]; then
        echo "FAIL: test_invalid_arg - Script exited with zero code for invalid arg"
        echo "Output: $OUTPUT"
        return 1
    fi

    if ! echo "$OUTPUT" | grep -q "Error: Unknown option '--invalid-arg'"; then
        echo "FAIL: test_invalid_arg - Output missing error message for invalid arg"
        echo "Output: $OUTPUT"
        return 1
    fi

    echo "PASS: test_invalid_arg"
    return 0
}

# Test function for help message
test_help_message() {
    echo "Running test_help_message..."
    MOCKED_DOCKER_CALLS="" # Reset mock calls

    OUTPUT=$(bash "$SCRIPT_TO_TEST" --help)
    EXIT_CODE=$?

    if [ "$EXIT_CODE" -ne 0 ]; then
        echo "FAIL: test_help_message - Script exited with non-zero code for help"
        echo "Output: $OUTPUT"
        return 1
    fi

    if ! echo "$OUTPUT" | grep -q "Usage: $0 [--dry-run | --prune]"; then
        echo "FAIL: test_help_message - Output missing usage message"
        echo "Output: $OUTPUT"
        return 1
    fi

    echo "PASS: test_help_message"
    return 0
}

# Run all tests
echo "--- Starting Nightly Container Compost Heap Tests ---"
test_dry_run
test_prune
test_invalid_arg
test_help_message
echo "--- All tests completed ---"
