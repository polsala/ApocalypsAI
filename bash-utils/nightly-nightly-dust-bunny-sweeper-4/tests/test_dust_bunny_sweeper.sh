#!/bin/bash

# Test script for nightly-dust-bunny-sweeper

# Source the main script
SCRIPT_PATH="./src/dust_bunny_sweeper.sh"

# --- Test Utilities ---
# Function to run a test
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_output_regex="$3"
    local expected_exit_code="$4"
    local description="$5"

    echo "--- Running Test: $test_name ---"
    echo "Description: $description"

    # Execute the command and capture output and exit code
    output=$($command 2>&1)
    exit_code=$?

    # Check exit code
    if [ "$exit_code" -eq "$expected_exit_code" ]; then
        echo "PASS: Exit code is $exit_code as expected."
    else
        echo "FAIL: Expected exit code $expected_exit_code, got $exit_code."
        echo "Output: $output"
        return 1
    fi

    # Check output using regex
    if [[ "$output" =~ $expected_output_regex ]]; then
        echo "PASS: Output matches expected pattern."
    else
        echo "FAIL: Output does not match expected pattern."
        echo "Expected pattern: $expected_output_regex"
        echo "Actual output: $output"
        return 1
    fi
    echo ""
    return 0
}

# Function to create a file with a specific modification time
create_aged_file() {
    local dir="$1"
    local filename="$2"
    local days_ago="$3"
    local timestamp

    # Mock rationale: Using `touch -t` to set specific modification times for files and directories.
    # This allows deterministic testing of `find -mtime` logic without relying on real-time system clock.
    # The `date` command is used to calculate the past timestamp.
    if date -v-1d >/dev/null 2>&1; then # Check for BSD/macOS date syntax
        timestamp=$(date -v-"$days_ago"d +"%Y%m%d%H%M.%S")
    else # Fallback for GNU date (Linux)
        timestamp=$(date -d "$days_ago days ago" +"%Y%m%d%H%M.%S")
    fi
    touch -t "$timestamp" "$dir/$filename"
    echo "Created $dir/$filename aged $days_ago days."
}

# Function to create an aged directory
create_aged_dir() {
    local parent_dir="$1"
    local dirname="$2"
    local days_ago="$3"
    mkdir -p "$parent_dir/$dirname"
    local timestamp

    # Mock rationale: Similar to create_aged_file, this sets specific modification times for directories.
    if date -v-1d >/dev/null 2>&1; then # Check for BSD/macOS date syntax
        timestamp=$(date -v-"$days_ago"d +"%Y%m%d%H%M.%S")
    else # Fallback for GNU date (Linux)
        timestamp=$(date -d "$days_ago days ago" +"%Y%m%d%H%M.%S")
    fi
    touch -t "$timestamp" "$parent_dir/$dirname"
    echo "Created directory $parent_dir/$dirname aged $days_ago days."
}

# --- Setup ---
# Create a temporary directory for tests
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
echo "Test directory: $TEST_DIR"

# Ensure cleanup on exit
cleanup() {
    echo "Cleaning up test directory: $TEST_DIR"
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# --- Tests ---

# Test 1: No arguments
run_test "No Arguments" \
    "$SCRIPT_PATH" \
    "Usage: .* <target_directory> <age_in_days>" \
    1 \
    "Should display usage and exit with error if no arguments are provided."

# Test 2: One argument
run_test "One Argument" \
    "$SCRIPT_PATH $TEST_DIR" \
    "Usage: .* <target_directory> <age_in_days>" \
    1 \
    "Should display usage and exit with error if only one argument is provided."

# Test 3: Invalid target directory
run_test "Invalid Target Directory" \
    "$SCRIPT_PATH /nonexistent/path 7" \
    "Oh dear! The 'temporal vortex' at '/nonexistent/path' does not exist or is not a directory. Cannot sweep!" \
    1 \
    "Should exit with error if target directory does not exist."

# Test 4: Invalid age (non-numeric)
run_test "Invalid Age - Non-numeric" \
    "$SCRIPT_PATH $TEST_DIR abc" \
    "The 'temporal age' must be a non-negative number of days. How old are these dust bunnies, really?" \
    1 \
    "Should exit with error if age is not a number."

# Test 5: Invalid age (negative)
run_test "Invalid Age - Negative" \
    "$SCRIPT_PATH $TEST_DIR -5" \
    "The 'temporal age' must be a non-negative number of days. How old are these dust bunnies, really?" \
    1 \
    "Should exit with error if age is negative."

# Test 6: No old files found
# Create a file that is not old enough
create_aged_file "$TEST_DIR" "fresh_bunny.txt" 1
create_aged_dir "$TEST_DIR" "fresh_burrow" 1

run_test "No Old Files Found" \
    "$SCRIPT_PATH $TEST_DIR 7" \
    "Phew! No temporal dust bunnies found older than 7 days in '$TEST_DIR'. All clear!" \
    0 \
    "Should report no old files if none match the criteria."

# Verify files are still there
if [ -f "$TEST_DIR/fresh_bunny.txt" ] && [ -d "$TEST_DIR/fresh_burrow" ]; then
    echo "PASS: fresh_bunny.txt and fresh_burrow still exist."
else
    echo "FAIL: fresh_bunny.txt or fresh_burrow were unexpectedly removed."
    exit 1
fi
echo ""

# Test 7: Old files found and deleted
# Create old files and directories
create_aged_file "$TEST_DIR" "old_bunny.log" 10
create_aged_dir "$TEST_DIR" "old_burrow" 12
create_aged_file "$TEST_DIR/old_burrow" "nested_old_bunny.txt" 15 # Should not be deleted by -maxdepth 1

run_test "Old Files Found and Deleted" \
    "$SCRIPT_PATH $TEST_DIR 7" \
    "Aha! Detected some ancient temporal dust bunnies.*Sweeping away: '$TEST_DIR/old_bunny.log'.*Sweeping away: '$TEST_DIR/old_burrow'.*Temporal Dust Bunny Sweeper Protocol complete!" \
    0 \
    "Should find and delete old files/directories."

# Verify old files are gone, and fresh ones remain
if [ ! -f "$TEST_DIR/old_bunny.log" ] && [ ! -d "$TEST_DIR/old_burrow" ]; then
    echo "PASS: old_bunny.log and old_burrow were removed as expected."
else
    echo "FAIL: old_bunny.log or old_burrow were NOT removed."
    ls -la "$TEST_DIR"
    exit 1
fi

if [ -f "$TEST_DIR/fresh_bunny.txt" ] && [ -d "$TEST_DIR/fresh_burrow" ]; then
    echo "PASS: fresh_bunny.txt and fresh_burrow still exist."
else
    echo "FAIL: fresh_bunny.txt or fresh_burrow were unexpectedly removed."
    exit 1
}
echo ""

# Test 8: No files to delete, but some exist (just not old enough)
# Re-create fresh files for this test
rm -rf "$TEST_DIR"/* # Clear previous test artifacts
create_aged_file "$TEST_DIR" "another_fresh_bunny.txt" 2
create_aged_dir "$TEST_DIR" "another_fresh_burrow" 3

run_test "No Deletion Needed" \
    "$SCRIPT_PATH $TEST_DIR 5" \
    "Phew! No temporal dust bunnies found older than 5 days in '$TEST_DIR'. All clear!" \
    0 \
    "Should report no old files if none match the criteria, even if some exist."

if [ -f "$TEST_DIR/another_fresh_bunny.txt" ] && [ -d "$TEST_DIR/another_fresh_burrow" ]; then
    echo "PASS: another_fresh_bunny.txt and another_fresh_burrow still exist."
else
    echo "FAIL: another_fresh_bunny.txt or another_fresh_burrow were unexpectedly removed."
    exit 1
fi
echo ""

echo "All tests completed."
