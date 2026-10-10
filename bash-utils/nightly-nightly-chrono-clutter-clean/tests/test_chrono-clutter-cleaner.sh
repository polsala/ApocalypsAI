#!/bin/bash

# Mock rationale: We need to test file operations without affecting the actual filesystem.
# Creating temporary directories and files allows for isolated, deterministic testing.
# Using `touch -t` allows precise control over file modification times.

set -euo pipefail

SCRIPT_PATH="../src/chrono-clutter-cleaner.sh"

# Function to create a file with a specific timestamp
create_file_with_timestamp() {
    local dir=$1
    local filename=$2
    local timestamp=$3 # YYYYMMDDhhmm
    touch -t "$timestamp" "$dir/$filename"
}

# Test 1: Dry run - should list old, matching files
test_dry_run() {
    echo "Running Test 1: Dry run - should list old, matching files"
    TEST_DIR=$(mktemp -d)
    
    # Create files:
    # Old and matching pattern
    create_file_with_timestamp "$TEST_DIR" "old_temp.tmp" "202301011200"
    create_file_with_timestamp "$TEST_DIR" "old_backup.bak" "202301011200"
    
    # Old but not matching pattern
    create_file_with_timestamp "$TEST_DIR" "old_regular.txt" "202301011200"
    
    # New and matching pattern
    create_file_with_timestamp "$TEST_DIR" "new_temp.tmp" "$(date +%Y%m%d%H%M)"
    
    # New and not matching pattern
    create_file_with_timestamp "$TEST_DIR" "new_regular.txt" "$(date +%Y%m%d%H%M)"

    # Run the script in dry-run mode (default)
    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 1)

    # Assertions
    if echo "$OUTPUT" | grep -q "old_temp.tmp" && \
       echo "$OUTPUT" | grep -q "old_backup.bak" && \
       ! echo "$OUTPUT" | grep -q "old_regular.txt" && \
       ! echo "$OUTPUT" | grep -q "new_temp.tmp" && \
       ! echo "$OUTPUT" | grep -q "new_regular.txt"; then
        echo "Test 1 Passed: Correct files listed in dry run."
    else
        echo "Test 1 Failed: Incorrect files listed in dry run."
        echo "Output:"
        echo "$OUTPUT"
        exit 1
    fi

    # Cleanup
    rm -rf "$TEST_DIR"
    echo ""
}

# Test 2: Cleanup run - should delete old, matching files
test_cleanup_run() {
    echo "Running Test 2: Cleanup run - should delete old, matching files"
    TEST_DIR=$(mktemp -d)
    
    # Create files:
    # Old and matching pattern (should be deleted)
    create_file_with_timestamp "$TEST_DIR" "delete_me.tmp" "202301011200"
    create_file_with_timestamp "$TEST_DIR" "also_delete.bak" "202301011200"
    
    # Old but not matching pattern (should remain)
    create_file_with_timestamp "$TEST_DIR" "keep_old.txt" "202301011200"
    
    # New and matching pattern (should remain)
    create_file_with_timestamp "$TEST_DIR" "keep_new.tmp" "$(date +%Y%m%d%H%M)"

    # Run the script in cleanup mode
    "$SCRIPT_PATH" -d "$TEST_DIR" -a 1 -c > /dev/null # Age 1 day, suppress output

    # Assertions
    if [ ! -f "$TEST_DIR/delete_me.tmp" ] && \
       [ ! -f "$TEST_DIR/also_delete.bak" ] && \
       [ -f "$TEST_DIR/keep_old.txt" ] && \
       [ -f "$TEST_DIR/keep_new.tmp" ]; then
        echo "Test 2 Passed: Correct files deleted in cleanup run."
    else
        echo "Test 2 Failed: Incorrect files deleted in cleanup run."
        ls -l "$TEST_DIR"
        exit 1
    fi

    # Cleanup
    rm -rf "$TEST_DIR"
    echo ""
}

# Test 3: Custom patterns
test_custom_patterns() {
    echo "Running Test 3: Custom patterns"
    TEST_DIR=$(mktemp -d)

    # Create files
    create_file_with_timestamp "$TEST_DIR" "log_file.log" "202301011200" # Should be picked up by custom pattern
    create_file_with_timestamp "$TEST_DIR" "temp_file.tmp" "202301011200" # Should not be picked up by custom pattern
    create_file_with_timestamp "$TEST_DIR" "important.txt" "202301011200" # Should not be picked up

    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 1 -p "*.log" )

    if echo "$OUTPUT" | grep -q "log_file.log" && \
       ! echo "$OUTPUT" | grep -q "temp_file.tmp" && \
       ! echo "$OUTPUT" | grep -q "important.txt"; then
        echo "Test 3 Passed: Custom patterns applied correctly."
    else
        echo "Test 3 Failed: Custom patterns not applied correctly."
        echo "Output:"
        echo "$OUTPUT"
        exit 1
    fi

    rm -rf "$TEST_DIR"
    echo ""
}

# Test 4: No clutter found
test_no_clutter() {
    echo "Running Test 4: No clutter found"
    TEST_DIR=$(mktemp -d)

    create_file_with_timestamp "$TEST_DIR" "new_file.tmp" "$(date +%Y%m%d%H%M)"
    create_file_with_timestamp "$TEST_DIR" "regular.txt" "202301011200"

    OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" -a 1)

    if echo "$OUTPUT" | grep -q "No chrono-clutter found matching criteria."; then
        echo "Test 4 Passed: Correctly reported no clutter."
    else
        echo "Test 4 Failed: Did not report no clutter."
        echo "Output:"
        echo "$OUTPUT"
        exit 1
    fi

    rm -rf "$TEST_DIR"
    echo ""
}

# Test 5: Invalid age argument
test_invalid_age() {
    echo "Running Test 5: Invalid age argument"
    OUTPUT=$("$SCRIPT_PATH" -a "abc" 2>&1 || true)
    if echo "$OUTPUT" | grep -q "Error: Age must be a positive integer."; then
        echo "Test 5 Passed: Handled invalid age argument correctly."
    else
        echo "Test 5 Failed: Did not handle invalid age argument."
        echo "Output:"
        echo "$OUTPUT"
        exit 1
    fi
    echo ""
}

# Run all tests
test_dry_run
test_cleanup_run
test_custom_patterns
test_no_clutter
test_invalid_age

echo "All tests passed!"
