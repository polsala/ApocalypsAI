#!/bin/bash

# Test script for nightly-temporal-debris-sweeper

# Source the main script
SCRIPT_PATH="./src/sweep_debris.sh"

# Ensure the script is executable for tests
chmod +x "$SCRIPT_PATH"

# --- Global variables for testing ---
TEST_DIR=""

# --- Helper functions ---
create_test_dir() {
    TEST_DIR=$(mktemp -d -t debris-test-XXXXXX)
    echo "Created test directory: $TEST_DIR"
}

cleanup_test_dir() {
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
        echo "Cleaned up test directory: $TEST_DIR"
        TEST_DIR="" # Reset for next test
    fi
}

# Create a file with a specific timestamp
# Usage: create_file <filename> <relative_days_ago>
create_file() {
    local filename="$1"
    local days_ago="$2"
    local timestamp
    # Mock rationale: Using 'date -d' for deterministic past dates, assuming a Linux-like environment for testing.
    # This ensures files are created with consistent 'old' timestamps relative to test execution.
    if [[ "$days_ago" -eq 0 ]]; then
        timestamp=$(date +%Y%m%d%H%M.%S)
    else
        timestamp=$(date -d "$days_ago days ago" +%Y%m%d%H%M.%S)
    fi
    touch -t "$timestamp" "$TEST_DIR/$filename"
    echo "Created file: $TEST_DIR/$filename with timestamp $timestamp"
}

# --- Test Cases ---

# Test 1: No debris found
test_no_debris() {
    echo "\n--- Running Test 1: No debris found ---"
    create_test_dir

    # Create a recent file
    create_file "recent_file.txt" 0

    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 1)
    if echo "$OUTPUT" | grep -q "No temporal debris detected"; then
        echo "Test 1 Passed: Correctly reported no debris."
    else
        echo "Test 1 Failed: Expected 'No temporal debris detected', got:\n$OUTPUT"
        cleanup_test_dir
        exit 1
    fi
    cleanup_test_dir
}

# Test 2: Debris found (dry run)
test_dry_run() {
    echo "\n--- Running Test 2: Debris found (dry run) ---"
    create_test_dir

    # Create an old file (3 days ago)
    create_file "old_file.log" 3
    # Create a recent file
    create_file "recent_file.txt" 0

    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 2 --dry-run)

    if echo "$OUTPUT" | grep -q "DRY RUN" && \
       echo "$OUTPUT" | grep -q "old_file.log" && \
       ! echo "$OUTPUT" | grep -q "recent_file.txt"; then
        echo "Test 2 Passed: Correctly identified old file in dry run."
    else
        echo "Test 2 Failed: Dry run output incorrect. Got:\n$OUTPUT"
        cleanup_test_dir
        exit 1
    fi

    if [[ -f "$TEST_DIR/old_file.log" ]]; then
        echo "Test 2 Passed: File was not deleted in dry run."
    else
        echo "Test 2 Failed: File was deleted in dry run."
        cleanup_test_dir
        exit 1
    fi
    cleanup_test_dir
}

# Test 3: Debris found and purged (force)
test_force_purge() {
    echo "\n--- Running Test 3: Debris found and purged (force) ---"
    create_test_dir

    # Create an old file (3 days ago)
    create_file "ancient_data.bak" 3
    # Create a recent file
    create_file "new_report.txt" 0

    # Redirect stdout to /dev/null to avoid cluttering test output, but capture stderr if any
    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 2 --force 2>&1)

    if [[ ! -f "$TEST_DIR/ancient_data.bak" ]] && [[ -f "$TEST_DIR/new_report.txt" ]]; then
        echo "Test 3 Passed: Old file purged, recent file retained."
    else
        echo "Test 3 Failed: Purge operation incorrect. Files remaining:\n$(ls -l "$TEST_DIR")\nOutput:\n$OUTPUT"
        cleanup_test_dir
        exit 1
    fi
    cleanup_test_dir
}

# Test 4: Debris found, user confirms purge
test_interactive_purge() {
    echo "\n--- Running Test 4: Debris found, user confirms purge ---"
    create_test_dir

    # Create an old file (3 days ago)
    create_file "temp_log_old.txt" 3

    # Pipe 'y' to stdin for confirmation
    OUTPUT=$(echo "y" | "$SCRIPT_PATH" -d "$TEST_DIR" -a 2)

    if echo "$OUTPUT" | grep -q "Purge sequence complete" && ! [[ -f "$TEST_DIR/temp_log_old.txt" ]]; then
        echo "Test 4 Passed: Interactive purge successful."
    else
        echo "Test 4 Failed: Interactive purge incorrect. Output:\n$OUTPUT\nFiles remaining:\n$(ls -l "$TEST_DIR")"
        cleanup_test_dir
        exit 1
    fi
    cleanup_test_dir
}

# Test 5: Invalid directory
test_invalid_directory() {
    echo "\n--- Running Test 5: Invalid directory ---"
    OUTPUT=$("$SCRIPT_PATH" -d "/non/existent/path/to/debris" 2>&1)
    if echo "$OUTPUT" | grep -q "Error: Target directory"; then
        echo "Test 5 Passed: Correctly handled invalid directory."
    else
        echo "Test 5 Failed: Did not report error for invalid directory. Got:\n$OUTPUT"
        exit 1
    fi
}

# Test 6: User aborts purge
test_abort_purge() {
    echo "\n--- Running Test 6: User aborts purge ---"
    create_test_dir

    # Create an old file (3 days ago)
    create_file "abort_me.tmp" 3

    # Pipe 'n' to stdin for abortion
    OUTPUT=$(echo "n" | "$SCRIPT_PATH" -d "$TEST_DIR" -a 2)

    if echo "$OUTPUT" | grep -q "Purge sequence aborted" && [[ -f "$TEST_DIR/abort_me.tmp" ]]; then
        echo "Test 6 Passed: User abortion successful, file retained."
    else
        echo "Test 6 Failed: Abortion logic incorrect. Output:\n$OUTPUT\nFiles remaining:\n$(ls -l "$TEST_DIR")"
        cleanup_test_dir
        exit 1
    fi
    cleanup_test_dir
}

# Run all tests
test_no_debris
test_dry_run
test_force_purge
test_interactive_purge
test_invalid_directory
test_abort_purge

echo "\nAll tests completed."
