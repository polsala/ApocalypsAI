#!/bin/bash

# --- Test Setup ---
TEST_DIR=""
PRUNER_SCRIPT="../src/pruner.sh"

# Mock rationale: We create a temporary directory and files with specific access times
# to ensure deterministic and isolated testing of the pruner script's logic.
# This avoids relying on the actual system's filesystem state or real-time clock.
# The `find` and `rm` commands will operate on these controlled temporary files.

setup_test_env() {
    TEST_DIR=$(mktemp -d)
    if [ ! -d "$TEST_DIR" ]; then
        echo "Failed to create temporary directory." >&2
        exit 1
    fi
}

cleanup_test_env() {
    if [ -d "$TEST_DIR" ]; then
        rm -rf "$TEST_DIR"
    fi
}

# Ensure cleanup runs on exit
trap cleanup_test_env EXIT

# --- Helper Functions ---
create_test_files() {
    # Create a file accessed 2 days ago (using portable date calculation for touch -t)
    # YYYYMMDDhhmm.SS format for touch -t is POSIX compliant.
    # We'll try BSD date first, then GNU date.
    OLD_DATE_STR=$(date -v-2d +%Y%m%d%H%M.%S 2>/dev/null || date -d "2 days ago" +%Y%m%d%H%M.%S 2>/dev/null)
    if [ -z "$OLD_DATE_STR" ]; then
        echo "Warning: Could not determine '2 days ago' date string portably. Using a fallback." >&2
        # Fallback: create a file, then touch it with a fixed old date if date command fails
        touch "$TEST_DIR/old_file_1.log"
        touch "$TEST_DIR/old_file_2.txt"
        touch -a -t 202301010000.00 "$TEST_DIR/old_file_1.log"
        touch -a -t 202301010000.00 "$TEST_DIR/old_file_2.txt"
    else
        touch -a -t "$OLD_DATE_STR" "$TEST_DIR/old_file_1.log"
        touch -a -t "$OLD_DIR_STR" "$TEST_DIR/old_file_2.txt"
    fi

    # Create a file accessed now
    touch "$TEST_DIR/new_file.tmp"
}

# --- Test Cases ---

# Test 1: Dry run, files found
test_dry_run_files_found() {
    setup_test_env
    echo "Running test_dry_run_files_found..."
    create_test_files
    output=$(echo "N" | "$PRUNER_SCRIPT" -d "$TEST_DIR" -a 1 -n)
    if echo "$output" | grep -q "Found 2 withered digital leaves:" && \
       echo "$output" | grep -q "This was a dry run. No digital flora were pruned."; then
        echo "PASS: Dry run with files found."
    else
        echo "FAIL: Dry run with files found. Output: $output" >&2
        exit 1
    fi
    # Ensure files still exist
    if [ -f "$TEST_DIR/old_file_1.log" ] && [ -f "$TEST_DIR/old_file_2.txt" ] && [ -f "$TEST_DIR/new_file.tmp" ]; then
        echo "PASS: Files not deleted during dry run."
    else
        echo "FAIL: Files deleted during dry run." >&2
        ls -l "$TEST_DIR" >&2
        exit 1
    fi
    cleanup_test_env
}

# Test 2: Dry run, no files found
test_dry_run_no_files_found() {
    setup_test_env
    echo "Running test_dry_run_no_files_found..."
    # Create only new files, or no files that match the criteria
    touch "$TEST_DIR/new_file_1.tmp"
    output=$(echo "N" | "$PRUNER_SCRIPT" -d "$TEST_DIR" -a 1 -n)
    if echo "$output" | grep -q "No withered digital flora found. Your garden is pristine!"; then
        echo "PASS: Dry run with no files found."
    else
        echo "FAIL: Dry run with no files found. Output: $output" >&2
        exit 1
    fi
    cleanup_test_env
}

# Test 3: Actual pruning with confirmation (confirm 'y')
test_pruning_with_confirmation_yes() {
    setup_test_env
    echo "Running test_pruning_with_confirmation_yes..."
    create_test_files
    echo "y" | "$PRUNER_SCRIPT" -d "$TEST_DIR" -a 1
    if [ ! -f "$TEST_DIR/old_file_1.log" ] && [ ! -f "$TEST_DIR/old_file_2.txt" ] && \
       [ -f "$TEST_DIR/new_file.tmp" ]; then # New file should remain
        echo "PASS: Pruning with confirmation (y) successful."
    else
        echo "FAIL: Pruning with confirmation (y) failed. Files state incorrect." >&2
        ls -l "$TEST_DIR" >&2
        exit 1
    fi
    cleanup_test_env
}

# Test 4: Actual pruning with confirmation (confirm 'N')
test_pruning_with_confirmation_no() {
    setup_test_env
    echo "Running test_pruning_with_confirmation_no..."
    create_test_files
    output=$(echo "N" | "$PRUNER_SCRIPT" -d "$TEST_DIR" -a 1)
    if echo "$output" | grep -q "Pruning cancelled. The digital garden remains as is."; then
        echo "PASS: Pruning with confirmation (N) cancelled."
    else
        echo "FAIL: Pruning with confirmation (N) did not cancel. Output: $output" >&2
        exit 1
    fi
    if [ -f "$TEST_DIR/old_file_1.log" ] && [ -f "$TEST_DIR/old_file_2.txt" ] && [ -f "$TEST_DIR/new_file.tmp" ]; then
        echo "PASS: Files not deleted after cancellation."
    else
        echo "FAIL: Files deleted after cancellation." >&2
        exit 1
    fi
    cleanup_test_env
}

# Test 5: Force pruning without confirmation
test_force_pruning() {
    setup_test_env
    echo "Running test_force_pruning..."
    create_test_files
    "$PRUNER_SCRIPT" -d "$TEST_DIR" -a 1 -f
    if [ ! -f "$TEST_DIR/old_file_1.log" ] && [ ! -f "$TEST_DIR/old_file_2.txt" ] && \
       [ -f "$TEST_DIR/new_file.tmp" ]; then # New file should remain
        echo "PASS: Force pruning successful."
    else
        echo "FAIL: Force pruning failed. Files state incorrect." >&2
        ls -l "$TEST_DIR" >&2
        exit 1
    fi
    cleanup_test_env
}

# Test 6: Invalid directory
test_invalid_directory() {
    setup_test_env
    echo "Running test_invalid_directory..."
    output=$(bash "$PRUNER_SCRIPT" -d "/non/existent/path" -a 1 2>&1)
    if echo "$output" | grep -q "Error: Digital garden path '/non/existent/path' not found."; then
        echo "PASS: Invalid directory handled."
    else
        echo "FAIL: Invalid directory not handled. Output: $output" >&2
        exit 1
    fi
    cleanup_test_env
}

# Test 7: Invalid age
test_invalid_age() {
    setup_test_env
    echo "Running test_invalid_age..."
    output=$(bash "$PRUNER_SCRIPT" -d "$TEST_DIR" -a "abc" 2>&1)
    if echo "$output" | grep -q "Error: Age must be a non-negative integer."; then
        echo "PASS: Invalid age handled."
    else
        echo "FAIL: Invalid age not handled. Output: $output" >&2
        exit 1
    fi
    cleanup_test_env
}

# Test 8: Missing arguments
test_missing_arguments() {
    setup_test_env
    echo "Running test_missing_arguments..."
    output=$(bash "$PRUNER_SCRIPT" -d "$TEST_DIR" 2>&1)
    if echo "$output" | grep -q "Error: Both -d (directory) and -a (age) are required."; then
        echo "PASS: Missing age argument handled."
    else
        echo "FAIL: Missing age argument not handled. Output: $output" >&2
        exit 1
    fi
    output=$(bash "$PRUNER_SCRIPT" -a 1 2>&1)
    if echo "$output" | grep -q "Error: Both -d (directory) and -a (age) are required."; then
        echo "PASS: Missing directory argument handled."
    else
        echo "FAIL: Missing directory argument not handled. Output: $output" >&2
        exit 1
    fi
    cleanup_test_env
}

# Run all tests
test_dry_run_files_found
test_dry_run_no_files_found
test_pruning_with_confirmation_yes
test_pruning_with_confirmation_no
test_force_pruning
test_invalid_directory
test_invalid_age
test_missing_arguments

echo "All tests completed."
