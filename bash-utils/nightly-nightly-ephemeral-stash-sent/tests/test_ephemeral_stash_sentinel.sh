#!/bin/bash

# Test setup
TEST_DIR=$(mktemp -d -t ephemeral-stash-XXXXXX)
STASH_LOG="$TEST_DIR/stash_actions.log"
REMINDER_LOG="$TEST_DIR/reminders.log"

# Mock rationale:
# We are mocking filesystem operations (mkdir, rm) and time-based delays (sleep)
# to ensure tests are deterministic, fast, and do not modify the actual filesystem
# or introduce real delays. `_notify_send` is mocked to prevent GUI pop-ups
# and capture notification content for verification.

# Source the script under test (will be done in subshells for isolation)
SCRIPT_TO_TEST="../src/ephemeral_stash_sentinel.sh"

# Helper to run the script with mocks in a subshell
run_script() {
    ( # Start a subshell
        # Override functions within this subshell
        _mkdir() { echo "MOCK: mkdir $@" >> "$STASH_LOG"; /bin/mkdir "$@"; }
        _rm() { echo "MOCK: rm $@" >> "$STASH_LOG"; /bin/rm "$@"; }
        _sleep() { echo "MOCK: sleep $@" >> "$STASH_LOG"; }
        _notify_send() { echo "MOCK: notify-send $@" >> "$REMINDER_LOG"; }
        
        # Source the script to make its functions available in this subshell
        # and ensure our mocks are used. The 'main' function will then be called.
        source "$SCRIPT_TO_TEST"
        main "$@" # Call the main function directly with provided arguments
    )
}

# Test cases
test_parse_duration() {
    local test_name="test_parse_duration"
    echo "Running $test_name..."

    # Source the script to get access to parse_duration for direct testing
    source "$SCRIPT_TO_TEST"

    if [ "$(parse_duration "10s")" -eq 10 ] && \
       [ "$(parse_duration "2m")" -eq 120 ] && \
       [ "$(parse_duration "1h")" -eq 3600 ] && \
       [ "$(parse_duration "1d")" -eq 86400 ] && \
       [ "$(parse_duration "0s")" -eq 0 ] && \
       [ "$(parse_duration "invalid")" -eq 0 ] && \
       [ "$(parse_duration "10x")" -eq 0 ] && \
       [ "$(parse_duration "s")" -eq 0 ] && \
       [ "$(parse_duration "-5s")" -eq 0 ]; then
        echo "PASS: $test_name - parse_duration works correctly."
    else
        echo "FAIL: $test_name - parse_duration failed."
        exit 1
    }
}

test_create_stash() {
    local test_name="test_create_stash"
    local stash="my_test_stash"
    echo "Running $test_name..."
    
    cd "$TEST_DIR"
    run_script "$stash" > /dev/null 2>&1
    
    if grep -q "MOCK: mkdir $stash" "$STASH_LOG" && [ -d "$stash" ]; then
        echo "PASS: $test_name - Stash created and mkdir mocked."
    else
        echo "FAIL: $test_name - Stash not created or mkdir not mocked."
        cat "$STASH_LOG"
        exit 1
    fi
    cd - > /dev/null
    /bin/rm -rf "$TEST_DIR/$stash" # Clean up
    > "$STASH_LOG" # Clear log for next test
}

test_create_stash_with_deletion() {
    local test_name="test_create_stash_with_deletion"
    local stash="delete_stash"
    local duration="1s"
    echo "Running $test_name..."

    cd "$TEST_DIR"
    run_script "$stash" -d "$duration" > /dev/null 2>&1

    if grep -q "MOCK: mkdir $stash" "$STASH_LOG" && \
       grep -q "MOCK: sleep 1" "$STASH_LOG" && \
       grep -q "Stash '$stash' scheduled for self-destruction in $duration." "$STASH_LOG" && \
       [ -d "$stash" ]; then
        echo "PASS: $test_name - Stash created and deletion scheduled."
    else
        echo "FAIL: $test_name - Stash not created or deletion not scheduled."
        cat "$STASH_LOG"
        exit 1
    fi
    cd - > /dev/null
    /bin/rm -rf "$TEST_DIR/$stash" # Clean up
    > "$STASH_LOG" # Clear log for next test
}

test_create_stash_with_reminder() {
    local test_name="test_create_stash_with_reminder"
    local stash="reminder_stash"
    local duration="1m"
    echo "Running $test_name..."

    cd "$TEST_DIR"
    run_script "$stash" -r "$duration" > /dev/null 2>&1

    if grep -q "MOCK: mkdir $stash" "$STASH_LOG" && \
       grep -q "MOCK: sleep 60" "$STASH_LOG" && \
       grep -q "Check-in reminder for '$stash' scheduled in $duration." "$STASH_LOG" && \
       [ -d "$stash" ]; then
        echo "PASS: $test_name - Stash created and reminder scheduled."
    else
        echo "FAIL: $test_name - Stash not created or reminder not scheduled."
        cat "$STASH_LOG"
        exit 1
    fi
    cd - > /dev/null
    /bin/rm -rf "$TEST_DIR/$stash" # Clean up
    > "$STASH_LOG" # Clear log for next test
}

test_create_stash_with_both() {
    local test_name="test_create_stash_with_both"
    local stash="both_stash"
    local delete_duration="2s"
    local reminder_duration="1s"
    echo "Running $test_name..."

    cd "$TEST_DIR"
    run_script "$stash" -d "$delete_duration" -r "$reminder_duration" > /dev/null 2>&1

    if grep -q "MOCK: mkdir $stash" "$STASH_LOG" && \
       grep -q "MOCK: sleep 2" "$STASH_LOG" && \
       grep -q "MOCK: sleep 1" "$STASH_LOG" && \
       grep -q "Stash '$stash' scheduled for self-destruction in $delete_duration." "$STASH_LOG" && \
       grep -q "Check-in reminder for '$stash' scheduled in $reminder_duration." "$STASH_LOG" && \
       [ -d "$stash" ]; then
        echo "PASS: $test_name - Stash created with both deletion and reminder."
    else
        echo "FAIL: $test_name - Stash not created or both not scheduled."
        cat "$STASH_LOG"
        exit 1
    fi
    cd - > /dev/null
    /bin/rm -rf "$TEST_DIR/$stash" # Clean up
    > "$STASH_LOG" # Clear log for next test
}

test_invalid_stash_name() {
    local test_name="test_invalid_stash_name"
    echo "Running $test_name..."

    cd "$TEST_DIR"
    output=$(run_script "" 2>&1)
    
    if echo "$output" | grep -q "Error: Stash name is required."; then
        echo "PASS: $test_name - Correctly handled missing stash name."
    else
        echo "FAIL: $test_name - Did not handle missing stash name."
        echo "$output"
        exit 1
    fi
    cd - > /dev/null
    > "$STASH_LOG" # Clear log for next test
}

test_existing_stash_name() {
    local test_name="test_existing_stash_name"
    local stash="existing_stash"
    echo "Running $test_name..."

    cd "$TEST_DIR"
    /bin/mkdir "$stash" # Create it manually for the test
    output=$(run_script "$stash" 2>&1)
    
    if echo "$output" | grep -q "Error: Directory '$stash' already exists."; then
        echo "PASS: $test_name - Correctly handled existing stash name."
    else
        echo "FAIL: $test_name - Did not handle existing stash name."
        echo "$output"
        exit 1
    fi
    cd - > /dev/null
    /bin/rm -rf "$TEST_DIR/$stash" # Clean up
    > "$STASH_LOG" # Clear log for next test
}

test_invalid_duration_format() {
    local test_name="test_invalid_duration_format"
    local stash="bad_duration_stash"
    echo "Running $test_name..."

    cd "$TEST_DIR"
    output=$(run_script "$stash" -d "10x" 2>&1)
    
    if echo "$output" | grep -q "Error: Invalid delete duration format: 10x"; then
        echo "PASS: $test_name - Correctly handled invalid delete duration."
    else
        echo "FAIL: $test_name - Did not handle invalid delete duration."
        echo "$output"
        exit 1
    fi

    output=$(run_script "$stash" -r "5y" 2>&1)
    if echo "$output" | grep -q "Error: Invalid reminder duration format: 5y"; then
        echo "PASS: $test_name - Correctly handled invalid reminder duration."
    else
        echo "FAIL: $test_name - Did not handle invalid reminder duration."
        echo "$output"
        exit 1
    fi
    cd - > /dev/null
    /bin/rm -rf "$TEST_DIR/$stash" # Clean up if it was created before error
    > "$STASH_LOG" # Clear log for next test
}

# Run all tests
echo "Starting Ephemeral Stash Sentinel tests..."

test_parse_duration
test_create_stash
test_create_stash_with_deletion
test_create_stash_with_reminder
test_create_stash_with_both
test_invalid_stash_name
test_existing_stash_name
test_invalid_duration_format

echo "All tests completed."

# Cleanup
/bin/rm -rf "$TEST_DIR"
