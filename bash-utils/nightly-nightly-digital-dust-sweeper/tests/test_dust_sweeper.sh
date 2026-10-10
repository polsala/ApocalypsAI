#!/bin/bash

# Test script for Nightly Digital Dust Bunny Sweeper

# --- Setup ---
TEST_DIR=$(mktemp -d)
SCRIPT_PATH="$(dirname "$0")"/../src/dust_sweeper.sh
MOCK_RM_LOG="$TEST_DIR/mock_rm.log"
MOCK_FIND_OUTPUT_FILE="$TEST_DIR/mock_find_output.txt"

# Mock rationale: We need to control the output of 'find' and prevent 'rm' from
# actually deleting files on the test system. 'read' is mocked to simulate user input.

# Override 'find' to read from a predefined file
find() {
    # Mock rationale: Instead of scanning the filesystem, 'find' will output
    # the contents of a controlled file, allowing deterministic tests.
    cat "$MOCK_FIND_OUTPUT_FILE"
}

# Override 'rm' to log what it would delete
rm() {
    # Mock rationale: Prevent actual file deletion during tests.
    # Instead, log the arguments passed to 'rm' to a file for verification.
    echo "MOCKED_RM_CALL: $*" >> "$MOCK_RM_LOG"
}

# Override 'read' to provide canned input
mock_read_input=""
read() {
    # Mock rationale: Simulate user input for confirmation prompts.
    # The global variable 'mock_read_input' will be used as the response.
    REPLY="$mock_read_input"
    # Suppress actual read prompt output
    if [[ "$1" == *"-p"* ]]; then
        # Simulate prompt, but don't print it
        :
    fi
}

# Helper function to run the script with mocks
run_sweeper() {
    # Clear mock logs before each run
    > "$MOCK_RM_LOG"
    > "$MOCK_FIND_OUTPUT_FILE"
    # Ensure mock_read_input is reset
    mock_read_input=""

    # Run the script, redirecting stdout and stderr
    bash "$SCRIPT_PATH" "$@"
}

# --- Test Cases ---

# Test 1: No dust bunnies found
test_no_dust_bunnies() {
    echo -n "" > "$MOCK_FIND_OUTPUT_FILE" # Empty find output
    output=$(run_sweeper "$TEST_DIR")
    if echo "$output" | grep -q "No digital dust bunnies found!"; then
        echo "Test 1 (No dust bunnies): PASSED"
    else
        echo "Test 1 (No dust bunnies): FAILED"
        echo "Output: $output"
        return 1
    fi
    return 0
}

# Test 2: Dust bunnies found, user declines deletion
test_decline_deletion() {
    echo "$TEST_DIR/old_file.log" > "$MOCK_FIND_OUTPUT_FILE"
    mock_read_input="n" # Simulate user declining
    output=$(run_sweeper "$TEST_DIR")
    if echo "$output" | grep -q "Digital dust bunnies spared for another cycle."; then
        if [ ! -s "$MOCK_RM_LOG" ]; then # Check if rm was NOT called
            echo "Test 2 (Decline deletion): PASSED"
        else
            echo "Test 2 (Decline deletion): FAILED - rm was called"
            cat "$MOCK_RM_LOG"
            return 1
        fi
    else
        echo "Test 2 (Decline deletion): FAILED - Incorrect output"
        echo "Output: $output"
        return 1
    fi
    return 0
}

# Test 3: Dust bunnies found, user accepts deletion
test_accept_deletion() {
    echo "$TEST_DIR/old_file.log" > "$MOCK_FIND_OUTPUT_FILE"
    echo "$TEST_DIR/empty_dir" >> "$MOCK_FIND_OUTPUT_FILE"
    mock_read_input="y" # Simulate user accepting
    output=$(run_sweeper "$TEST_DIR")
    if echo "$output" | grep -q "Digital dust bunnies successfully swept!"; then
        if grep -q "MOCKED_RM_CALL: -rf $TEST_DIR/old_file.log $TEST_DIR/empty_dir" "$MOCK_RM_LOG"; then
            echo "Test 3 (Accept deletion): PASSED"
        else
            echo "Test 3 (Accept deletion): FAILED - rm call mismatch"
            cat "$MOCK_RM_LOG"
            return 1
        fi
    else
        echo "Test 3 (Accept deletion): FAILED - Incorrect output"
        echo "Output: $output"
        return 1
    fi
    return 0
}

# Test 4: Dry run mode
test_dry_run() {
    echo "$TEST_DIR/temp_file.tmp" > "$MOCK_FIND_OUTPUT_FILE"
    output=$(run_sweeper -n "$TEST_DIR")
    if echo "$output" | grep -q "This was a dry run. No files were swept away."; then
        if [ ! -s "$MOCK_RM_LOG" ]; then # Check if rm was NOT called
            echo "Test 4 (Dry run): PASSED"
        else
            echo "Test 4 (Dry run): FAILED - rm was called in dry run"
            cat "$MOCK_RM_LOG"
            return 1
        fi
    else
        echo "Test 4 (Dry run): FAILED - Incorrect output"
        echo "Output: $output"
        return 1
    fi
    return 0
}

# Test 5: Auto-yes mode (-y)
test_auto_yes() {
    echo "$TEST_DIR/another_old_file.txt" > "$MOCK_FIND_OUTPUT_FILE"
    output=$(run_sweeper -y "$TEST_DIR")
    if echo "$output" | grep -q "Digital dust bunnies successfully swept!"; then
        if grep -q "MOCKED_RM_CALL: -rf $TEST_DIR/another_old_file.txt" "$MOCK_RM_LOG"; then
            echo "Test 5 (Auto-yes): PASSED"
        else
            echo "Test 5 (Auto-yes): FAILED - rm call mismatch for auto-yes"
            cat "$MOCK_RM_LOG"
            return 1
        fi
    else
        echo "Test 5 (Auto-yes): FAILED - Incorrect output for auto-yes"
        echo "Output: $output"
        return 1
    fi
    return 0
}

# Test 6: Invalid age argument
test_invalid_age() {
    output=$(run_sweeper -a "not_a_number" "$TEST_DIR" 2>&1) # Redirect stderr
    if echo "$output" | grep -q "Error: Age must be a positive integer."; then
        echo "Test 6 (Invalid age): PASSED"
    else
        echo "Test 6 (Invalid age): FAILED"
        echo "Output: $output"
        return 1
    fi
    return 0
}

# Test 7: Age argument missing value
test_missing_age_value() {
    output=$(run_sweeper -a "$TEST_DIR" 2>&1) # Redirect stderr, $TEST_DIR is treated as next arg
    if echo "$output" | grep -q "Error: --age requires a number of days."; then
        echo "Test 7 (Missing age value): PASSED"
    else
        echo "Test 7 (Missing age value): FAILED"
        echo "Output: $output"
        return 1
    fi
    return 0
}

# Test 8: Help message
test_help_message() {
    output=$(run_sweeper -h)
    if echo "$output" | grep -q "Nightly Digital Dust Bunny Sweeper" && \
       echo "$output" | grep -q "Usage: $0 [OPTIONS] [PATH]"; then
        echo "Test 8 (Help message): PASSED"
    else
        echo "Test 8 (Help message): FAILED"
        echo "Output: $output"
        return 1
    fi
    return 0
}

# Test 9: Exclude target directory itself
test_exclude_target_dir() {
    # Simulate find returning the target directory itself and another file
    echo "$TEST_DIR" > "$MOCK_FIND_OUTPUT_FILE"
    echo "$TEST_DIR/some_file.log" >> "$MOCK_FIND_OUTPUT_FILE"
    mock_read_input="y"
    output=$(run_sweeper "$TEST_DIR")
    if echo "$output" | grep -q "Digital dust bunnies successfully swept!"; then
        # rm should only be called for some_file.log, not TEST_DIR itself
        if grep -q "MOCKED_RM_CALL: -rf $TEST_DIR/some_file.log" "$MOCK_RM_LOG" && \
           ! grep -q "MOCKED_RM_CALL: -rf $TEST_DIR" "$MOCK_RM_LOG"; then
            echo "Test 9 (Exclude target directory): PASSED"
        else
            echo "Test 9 (Exclude target directory): FAILED - rm call mismatch"
            cat "$MOCK_RM_LOG"
            return 1
        fi
    else
        echo "Test 9 (Exclude target directory): FAILED - Incorrect output"
        echo "Output: $output"
        return 1
    fi
    return 0
}

# --- Run all tests ---
echo "Running tests for Nightly Digital Dust Bunny Sweeper..."
test_no_dust_bunnies
test_decline_deletion
test_accept_deletion
test_dry_run
test_auto_yes
test_invalid_age
test_missing_age_value
test_help_message
test_exclude_target_dir

# --- Cleanup ---
rm -rf "$TEST_DIR"
echo "Tests complete."
