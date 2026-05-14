#!/bin/bash

# Source the main script to test its functions or just run it
SCRIPT_TO_TEST="../src/dust_bunny_hunt.sh"

# Setup a temporary directory for testing
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
if [ ! -d "$TEST_DIR" ]; then
    echo "Failed to create test directory." >&2
    exit 1
fi

# Mock rationale: We are creating a controlled, deterministic file system environment
# within a temporary directory. By using 'touch -d' with specific timestamps relative
# to the current execution time, we ensure that the 'find' command (used by the main
# script) will produce consistent results regardless of when the tests are run. This
# avoids relying on the actual system's file modification times or complex 'find' command mocking.

# Test counter
TEST_COUNT=0
PASS_COUNT=0

# Helper function to run a test
run_test() {
    TEST_COUNT=$((TEST_COUNT + 1))
    local name="$1"
    local command="$2"
    local expected_output_regex="$3"
    local actual_output

    echo "Running test: $name"

    # Cleanup existing test files for this run_test call
    rm -rf "$TEST_DIR"/*
    
    # Create directories first, then touch them to set specific mtimes
    mkdir -p "$TEST_DIR/subdir"
    mkdir -p "$TEST_DIR/medium_dir"
    mkdir -p "$TEST_DIR/new_dir"

    # Create files and set their mtimes relative to 'now'
    # Older than 30 days (e.g., 31 days ago)
    touch -d "$(date -d '31 days ago' +%Y-%m-%d) 10:00" "$TEST_DIR/old_file_1.txt"
    touch -d "$(date -d '31 days ago' +%Y-%m-%d) 11:00" "$TEST_DIR/subdir/old_file_2.log"
    touch -d "$(date -d '31 days ago' +%Y-%m-%d) 09:00" "$TEST_DIR/subdir" # Set mtime for subdir itself

    # Older than 10 days but not 30 (e.g., 15 days ago)
    touch -d "$(date -d '15 days ago' +%Y-%m-%d) 10:00" "$TEST_DIR/medium_file.json"
    touch -d "$(date -d '15 days ago' +%Y-%m-%d) 11:00" "$TEST_DIR/medium_dir/another_file.tmp"
    touch -d "$(date -d '15 days ago' +%Y-%m-%d) 09:00" "$TEST_DIR/medium_dir" # Set mtime for medium_dir itself

    # Newer than 10 days (e.g., 5 days ago)
    touch -d "$(date -d '5 days ago' +%Y-%m-%d) 10:00" "$TEST_DIR/new_file.txt"
    touch -d "$(date -d '5 days ago' +%Y-%m-%d) 09:00" "$TEST_DIR/new_dir" # Set mtime for new_dir itself

    actual_output=$(eval "$command" 2>&1)

    if echo "$actual_output" | grep -Eq "$expected_output_regex"; then
        echo "  PASS: $name"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo "  FAIL: $name"
        echo "    Expected regex: $expected_output_regex"
        echo "    Actual output:"
        echo "$actual_output"
    fi
    echo "---"
}

# --- Test Cases ---

# Test 1: Default behavior (files older than 30 days)
run_test "Default search for files (30 days)" \
    "$SCRIPT_TO_TEST -p $TEST_DIR -a 30" \
    "Found a dusty relic: $TEST_DIR/old_file_1.txt.*Found a dusty relic: $TEST_DIR/subdir/old_file_2.log"

# Test 2: Search for directories older than 10 days
run_test "Search for directories (10 days)" \
    "$SCRIPT_TO_TEST -p $TEST_DIR -a 10 -t d" \
    "Found a dusty relic: $TEST_DIR/subdir.*Found a dusty relic: $TEST_DIR/medium_dir"

# Test 3: Search for all (files and directories) older than 5 days
run_test "Search for all (5 days)" \
    "$SCRIPT_TO_TEST -p $TEST_DIR -a 5 -t a" \
    "Found a dusty relic: $TEST_DIR/old_file_1.txt.*Found a dusty relic: $TEST_DIR/subdir/old_file_2.log.*Found a dusty relic: $TEST_DIR/subdir.*Found a dusty relic: $TEST_DIR/medium_file.json.*Found a dusty relic: $TEST_DIR/medium_dir/another_file.tmp.*Found a dusty relic: $TEST_DIR/medium_dir"

# Test 4: Invalid age argument
run_test "Invalid age argument" \
    "$SCRIPT_TO_TEST -a abc" \
    "Error: Age must be a positive integer."

# Test 5: Invalid type argument
run_test "Invalid type argument" \
    "$SCRIPT_TO_TEST -t x" \
    "Error: Invalid search type. Use 'f' for files, 'd' for directories, or 'a' for all."

# Test 6: No matches found for a very high age (e.g., 365 days)
run_test "No matches found for a very high age" \
    "$SCRIPT_TO_TEST -p $TEST_DIR -a 365 -t a" \
    "Digital Dust Bunny Hunt Complete! May your storage be ever clean."

# Test 7: Search for files older than 10 days
run_test "Search for files (10 days)" \
    "$SCRIPT_TO_TEST -p $TEST_DIR -a 10 -t f" \
    "Found a dusty relic: $TEST_DIR/old_file_1.txt.*Found a dusty relic: $TEST_DIR/subdir/old_file_2.log.*Found a dusty relic: $TEST_DIR/medium_file.json.*Found a dusty relic: $TEST_DIR/medium_dir/another_file.tmp"

# --- Summary ---
echo "========================================="
echo "Test Summary: $PASS_COUNT / $TEST_COUNT tests passed."
echo "========================================="

# Cleanup
rm -rf "$TEST_DIR"

if [ "$PASS_COUNT" -eq "$TEST_COUNT" ]; then
    exit 0
else
    exit 1
fi
