#!/bin/bash

# Test suite for Nightly Temporal File Sweeper

# --- Test Setup ---
TEST_DIR=$(mktemp -d)
SCRIPT_PATH="$(dirname "$0")"/../src/temporal_sweeper.sh
ARCHIVE_DIR_NAME="chrono_vault" # Must match the script's internal config

# Ensure the script is executable
chmod +x "$SCRIPT_PATH"

# Function to clean up test environment
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Helper function to create a file with a specific modification date
create_test_file() {
    local filename="$1"
    local date_str="$2" # e.g., "2 days ago", "2023-01-01"
    touch -d "$date_str" "$TEST_DIR/$filename"
}

# Helper function to assert output contains a string
assert_output_contains() {
    local output="$1"
    local expected_string="$2"
    if ! echo "$output" | grep -qF "$expected_string"; then
        echo "❌ Test Failed: Expected output to contain '$expected_string'"
        echo "--- Actual Output ---"
        echo "$output"
        echo "---------------------"
        return 1
    fi
    return 0
}

# Helper function to assert output does NOT contain a string
assert_output_not_contains() {
    local output="$1"
    local unexpected_string="$2"
    if echo "$output" | grep -qF "$unexpected_string"; then
        echo "❌ Test Failed: Expected output NOT to contain '$unexpected_string'"
        echo "--- Actual Output ---"
        echo "$output"
        echo "---------------------"
        return 1
    fi
    return 0
}

# --- Test Cases ---

# Test 1: No arguments provided
echo "Running Test 1: No arguments"
output=$("$SCRIPT_PATH" 2>&1)
assert_output_contains "$output" "Usage: $SCRIPT_PATH <directory_to_scan> <age_in_days>" || exit 1
echo "✅ Test 1 Passed"
echo ""

# Test 2: Invalid directory
echo "Running Test 2: Invalid directory"
output=$("$SCRIPT_PATH" "/non/existent/dir" 10 2>&1)
assert_output_contains "$output" "Error: Directory '/non/existent/dir' not found." || exit 1
echo "✅ Test 2 Passed"
echo ""

# Test 3: Invalid age (non-numeric)
echo "Running Test 3: Invalid age (non-numeric)"
output=$("$SCRIPT_PATH" "$TEST_DIR" "abc" 2>&1)
assert_output_contains "$output" "Error: Age in days must be a positive integer." || exit 1
echo "✅ Test 3 Passed"
echo ""

# Test 4: Invalid age (zero)
echo "Running Test 4: Invalid age (zero)"
output=$("$SCRIPT_PATH" "$TEST_DIR" 0 2>&1)
assert_output_contains "$output" "Error: Age in days must be a positive integer." || exit 1
echo "✅ Test 4 Passed"
echo ""

# Test 5: Files older than age are detected
echo "Running Test 5: Files older than age are detected"
create_test_file "old_file.txt" "2 days ago" # Should be detected if age is 1
create_test_file "very_old_report.pdf" "30 days ago" # Should be detected if age is 10
create_test_file "recent_doc.md" "now" # Should NOT be detected

# Mock rationale: We use 'touch -d' to set specific modification times for test files.
# The 'find -mtime' command in the script will then deterministically identify files
# based on these controlled timestamps relative to the current execution time.
# No external network or dynamic system state is involved beyond the local filesystem.
output=$("$SCRIPT_PATH" "$TEST_DIR" 1 2>&1) # Scan for files older than 1 day
assert_output_contains "$output" "Temporal Echo Detected: \"$TEST_DIR/old_file.txt\"" || exit 1
assert_output_contains "$output" "Temporal Echo Detected: \"$TEST_DIR/very_old_report.pdf\"" || exit 1
assert_output_not_contains "$output" "Temporal Echo Detected: \"$TEST_DIR/recent_doc.md\"" || exit 1
assert_output_contains "$output" "Archive to the Chrono-Vault: mkdir -p \"$TEST_DIR/$ARCHIVE_DIR_NAME\" && mv \"$TEST_DIR/old_file.txt\" \"$TEST_DIR/$ARCHIVE_DIR_NAME/\"" || exit 1
assert_output_contains "$output" "Vanish into the Aether: rm \"$TEST_DIR/old_file.txt\"" || exit 1
assert_output_contains "$output" "Re-energize for the Present: touch \"$TEST_DIR/old_file.txt\"" || exit 1
echo "✅ Test 5 Passed"
echo ""

# Test 6: Files with spaces in names
echo "Running Test 6: Files with spaces in names"
create_test_file "file with spaces.txt" "5 days ago"
output=$("$SCRIPT_PATH" "$TEST_DIR" 1 2>&1)
assert_output_contains "$output" "Temporal Echo Detected: \"$TEST_DIR/file with spaces.txt\"" || exit 1
assert_output_contains "$output" "Archive to the Chrono-Vault: mkdir -p \"$TEST_DIR/$ARCHIVE_DIR_NAME\" && mv \"$TEST_DIR/file with spaces.txt\" \"$TEST_DIR/$ARCHIVE_DIR_NAME/\"" || exit 1
echo "✅ Test 6 Passed"
echo ""

# Test 7: No old files found
echo "Running Test 7: No old files found"
# Clean up previous files for this test
rm -f "$TEST_DIR"/*
create_test_file "new_file_1.txt" "now"
create_test_file "new_file_2.txt" "now"
output=$("$SCRIPT_PATH" "$TEST_DIR" 1 2>&1) # Scan for files older than 1 day
assert_output_not_contains "$output" "Temporal Echo Detected:" || exit 1
assert_output_contains "$output" "Temporal Echo Scan Complete! May your digital space be ever harmonious." || exit 1
echo "✅ Test 7 Passed"
echo ""

echo "All tests completed."
