#!/bin/bash

# Mock rationale: We cannot run actual docker commands in a self-contained test
# without a running Docker daemon, which would make the test non-deterministic
# and not offline. We mock the 'docker' command to verify its invocation.
# Similarly, 'sleep' is mocked to prevent infinite loops and control test duration.

# --- Test Setup ---
MOCKED_DOCKER_CALLS_FILE="/tmp/mocked_docker_calls.log"
MOCKED_SLEEP_CALLS_FILE="/tmp/mocked_sleep_calls.log"

# Mock the 'docker' command
docker() {
    echo "MOCKED_DOCKER_CALL: $@" >> "$MOCKED_DOCKER_CALLS_FILE"
    # Simulate success
    return 0
}

# Mock the 'sleep' command
sleep() {
    echo "MOCKED_SLEEP_CALL: $@" >> "$MOCKED_SLEEP_CALLS_FILE"
    # For testing, we only want one loop iteration, so we exit after the first sleep.
    # This makes the test deterministic and prevents infinite loops.
    exit 0 
}

# Clean up mock files before each test run
cleanup() {
    rm -f "$MOCKED_DOCKER_CALLS_FILE" "$MOCKED_SLEEP_CALLS_FILE"
}
trap cleanup EXIT

# --- Test Functions ---

test_default_prune_options() {
    cleanup
    echo "Running test_default_prune_options..."
    DOCKER_PRUNE_INTERVAL="1s" /bin/bash src/prune.sh > /dev/null 2>&1 & # Run in background
    PRUNE_PID=$!
    wait $PRUNE_PID # Wait for the script to exit (due to mocked sleep)

    if grep -q "MOCKED_DOCKER_CALL: system prune -f --volumes --all" "$MOCKED_DOCKER_CALLS_FILE"; then
        echo "PASS: Default prune options (--volumes --all) detected."
    else
        echo "FAIL: Default prune options not detected."
        cat "$MOCKED_DOCKER_CALLS_FILE"
        exit 1
    fi
    if grep -q "MOCKED_SLEEP_CALL: 1" "$MOCKED_SLEEP_CALLS_FILE"; then
        echo "PASS: Sleep interval of 1 second detected."
    else
        echo "FAIL: Sleep interval not detected correctly."
        cat "$MOCKED_SLEEP_CALLS_FILE"
        exit 1
    fi
}

test_custom_prune_options() {
    cleanup
    echo "Running test_custom_prune_options..."
    DOCKER_PRUNE_INTERVAL="1s" DOCKER_PRUNE_OPTIONS="--force" /bin/bash src/prune.sh > /dev/null 2>&1 & # Run in background
    PRUNE_PID=$!
    wait $PRUNE_PID

    if grep -q "MOCKED_DOCKER_CALL: system prune -f --force" "$MOCKED_DOCKER_CALLS_FILE"; then
        echo "PASS: Custom prune options (--force) detected."
    else
        echo "FAIL: Custom prune options not detected."
        cat "$MOCKED_DOCKER_CALLS_FILE"
        exit 1
    fi
}

test_custom_prune_interval() {
    cleanup
    echo "Running test_custom_prune_interval..."
    DOCKER_PRUNE_INTERVAL="5m" /bin/bash src/prune.sh > /dev/null 2>&1 & # Run in background
    PRUNE_PID=$!
    wait $PRUNE_PID

    if grep -q "MOCKED_SLEEP_CALL: 300" "$MOCKED_SLEEP_CALLS_FILE"; then # 5 minutes = 300 seconds
        echo "PASS: Custom sleep interval (5m -> 300s) detected."
    else
        echo "FAIL: Custom sleep interval not detected correctly."
        cat "$MOCKED_SLEEP_CALLS_FILE"
        exit 1
    fi
}

test_invalid_prune_interval_defaults_to_24h() {
    cleanup
    echo "Running test_invalid_prune_interval_defaults_to_24h..."
    # The script will print a warning and default to 24h (86400s)
    DOCKER_PRUNE_INTERVAL="invalid" /bin/bash src/prune.sh > /dev/null 2>&1 & # Run in background
    PRUNE_PID=$!
    wait $PRUNE_PID

    if grep -q "MOCKED_SLEEP_CALL: 86400" "$MOCKED_SLEEP_CALLS_FILE"; then
        echo "PASS: Invalid interval defaults to 24h (86400s).
        (Note: 'Warning: Unknown interval unit' message is expected in stderr)"
    else
        echo "FAIL: Invalid interval did not default to 24h."
        cat "$MOCKED_SLEEP_CALLS_FILE"
        exit 1
    fi
}

# --- Run Tests ---
test_default_prune_options
test_custom_prune_options
test_custom_prune_interval
test_invalid_prune_interval_defaults_to_24h

echo "All tests completed."
