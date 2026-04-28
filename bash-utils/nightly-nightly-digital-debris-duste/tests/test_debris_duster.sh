#!/bin/bash

# Mock rationale: To ensure deterministic and offline testing,
# the 'rm' command is mocked to log its calls instead of performing actual deletions,
# and the 'read' command is mocked to provide predefined user input.

# Test setup
TEST_DIR=$(mktemp -d -t debris-duster-test-XXXX)
MOCKED_RM_LOG="$TEST_DIR/mock_rm.log"
MOCKED_READ_INPUT=""

# Mock functions
# Override system 'rm' for testing
rm() {
    echo "MOCKED_RM_CALL: $*" >> "$MOCKED_RM_LOG"
    # echo "MOCKED RM: $*" # Debugging
}

# Override system 'read' for testing
read() {
    REPLY="$MOCKED_READ_INPUT"
    # echo "MOCKED READ: $REPLY" # Debugging
}

# Helper function to create a file with specific mtime and size
create_test_file() {
    local path="$1"
    local mtime_days_ago="$2"
    local size_kb="$3"
    dd if=/dev/zero of="$path" bs=1K count="$size_kb" 2>/dev/null
    touch -d "$mtime_days_ago days ago" "$path"
}

# Helper function to run the script and capture output
run_script() {
    local args="$*"
    # Clear mocks for each run
    > "$MOCKED_RM_LOG" # Clear log file
    MOCKED_READ_INPUT=""
    # Run the script by sourcing it, so mocks are effective
    # Redirect stdout and stderr to a temporary file for capture
    local temp_output_file=$(mktemp)
    (source ../src/debris_duster.sh "$@") > "$temp_output_file" 2>&1
    local output=$(cat "$temp_output_file")
    /bin/rm "$temp_output_file"
    echo "$output"
}

# --- Test Cases ---

# Test 1: No debris found
test_no_debris() {
    echo "Running Test 1: No debris found"
    local output=$(run_script "$TEST_DIR" 1 1)
    if echo "$output" | grep -q "No significant digital debris found"; then
        echo "Test 1 PASSED"
    else
        echo "Test 1 FAILED: Expected 'No significant digital debris found', got:\n$output"
        exit 1
    fi
}

# Test 2: Debris found, user declines deletion
test_decline_deletion() {
    echo "Running Test 2: Debris found, user declines deletion"
    create_test_file "$TEST_DIR/old_large_file.txt" 100 2 # 100 days old, 2KB
    MOCKED_READ_INPUT="n" # User declines
    local output=$(run_script "$TEST_DIR" 30 1) # Find files older than 30 days, larger than 1KB
    local rm_calls=$(cat "$MOCKED_RM_LOG")
    if echo "$output" | grep -q "Digital debris left untouched" && [[ -z "$rm_calls" ]]; then
        echo "Test 2 PASSED"
    else
        echo "Test 2 FAILED: Expected 'Digital debris left untouched' and no rm calls, got:\n$output\nRM Calls:\n$rm_calls"
        exit 1
    fi
    /bin/rm "$TEST_DIR/old_large_file.txt" # Clean up test file (using actual rm for cleanup)
}

# Test 3: Debris found, user accepts deletion
test_accept_deletion() {
    echo "Running Test 3: Debris found, user accepts deletion"
    create_test_file "$TEST_DIR/another_old_large_file.log" 60 5 # 60 days old, 5KB
    MOCKED_READ_INPUT="y" # User accepts
    local output=$(run_script "$TEST_DIR" 30 1) # Find files older than 30 days, larger than 1KB
    local rm_calls=$(cat "$MOCKED_RM_LOG")
    if echo "$output" | grep -q "Digital debris scavenged" && echo "$rm_calls" | grep -q "MOCKED_RM_CALL: -v $TEST_DIR/another_old_large_file.log"; then
        echo "Test 3 PASSED"
    else
        echo "Test 3 FAILED: Expected 'Digital debris scavenged' and rm call, got:\n$output\nRM Calls:\n$rm_calls"
        exit 1
    fi
    /bin/rm "$TEST_DIR/another_old_large_file.log" # Clean up test file
}

# Test 4: File too new
test_file_too_new() {
    echo "Running Test 4: File too new"
    create_test_file "$TEST_DIR/new_file.txt" 10 2 # 10 days old, 2KB
    local output=$(run_script "$TEST_DIR" 30 1)
    if echo "$output" | grep -q "No significant digital debris found"; then
        echo "Test 4 PASSED"
    else
        echo "Test 4 FAILED: Expected 'No significant digital debris found', got:\n$output"
        exit 1
    fi
    /bin/rm "$TEST_DIR/new_file.txt" # Clean up
}

# Test 5: File too small
test_file_too_small() {
    echo "Running Test 5: File too small"
    create_test_file "$TEST_DIR/small_old_file.txt" 100 0 # 100 days old, 0KB (less than 1KB)
    local output=$(run_script "$TEST_DIR" 30 1)
    if echo "$output" | grep -q "No significant digital debris found"; then
        echo "Test 5 PASSED"
    else
        echo "Test 5 FAILED: Expected 'No significant digital debris found', got:\n$output"
        exit 1
    fi
    /bin/rm "$TEST_DIR/small_old_file.txt" # Clean up
}

# Test 6: Invalid directory
test_invalid_directory() {
    echo "Running Test 6: Invalid directory"
    local output=$(run_script "$TEST_DIR/non_existent_dir" 30 1)
    if echo "$output" | grep -q "Error: Target directory '$TEST_DIR/non_existent_dir' does not exist."; then
        echo "Test 6 PASSED"
    else
        echo "Test 6 FAILED: Expected error for invalid directory, got:\n$output"
        exit 1
    fi
}

# Run all tests
test_no_debris
test_decline_deletion
test_accept_deletion
test_file_too_new
test_file_too_small
test_invalid_directory

# Cleanup
# Use the actual system rm for cleanup
/bin/rm -rf "$TEST_DIR"
echo "All tests completed."
