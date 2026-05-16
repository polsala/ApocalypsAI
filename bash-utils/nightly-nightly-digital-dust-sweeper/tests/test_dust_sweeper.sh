#!/bin/bash

# Test suite for nightly-digital-dust-sweeper

SCRIPT_PATH="../src/dust_sweeper.sh"
TEST_DIR=$(mktemp -d)

# Mock rationale:
# We need to create temporary files and directories with specific properties (size, age)
# to simulate a real filesystem for testing the 'find' and 'du' commands.
# This ensures the script's logic for identifying "dust bunnies" works correctly
# without relying on the actual system's file state.

setup_test_environment() {
    echo "Setting up test environment in $TEST_DIR..."
    cd "$TEST_DIR" || exit 1

    # Create a large, old file (should be detected)
    dd if=/dev/zero of=old_large_file.bin bs=1M count=150 > /dev/null 2>&1 # 150MB
    touch -d "2 years ago" old_large_file.bin

    # Create a large, new file (should NOT be detected by age)
    dd if=/dev/zero of=new_large_file.bin bs=1M count=150 > /dev/null 2>&1 # 150MB
    touch -d "1 day ago" new_large_file.bin

    # Create a small, old file (should NOT be detected by size)
    echo "small old content" > old_small_file.txt
    touch -d "2 years ago" old_small_file.txt

    # Create a large, old directory with content (should be detected)
    mkdir -p old_large_dir/subdir
    dd if=/dev/zero of=old_large_dir/file1.bin bs=1M count=60 > /dev/null 2>&1
    dd if=/dev/zero of=old_large_dir/subdir/file2.bin bs=1M count=70 > /dev/null 2>&1
    touch -d "2 years ago" old_large_dir # Set dir modification time
    touch -d "2 years ago" old_large_dir/file1.bin
    touch -d "2 years ago" old_large_dir/subdir/file2.bin

    # Create a large, new directory (should NOT be detected by age)
    mkdir -p new_large_dir/subdir
    dd if=/dev/zero of=new_large_dir/file1.bin bs=1M count=60 > /dev/null 2>&1
    dd if=/dev/zero of=new_large_dir/subdir/file2.bin bs=1M count=70 > /dev/null 2>&1
    touch -d "1 day ago" new_large_dir
    touch -d "1 day ago" new_large_dir/file1.bin
    touch -d "1 day ago" new_large_dir/subdir/file2.bin

    # Create a small, old directory (should NOT be detected by size)
    mkdir -p old_small_dir
    echo "small content" > old_small_dir/file.txt
    touch -d "2 years ago" old_small_dir
    touch -d "2 years ago" old_small_dir/file.txt

    echo "Test environment setup complete."
}

cleanup_test_environment() {
    echo "Cleaning up test environment..."
    cd - > /dev/null || exit 1 # Go back to original directory
    rm -rf "$TEST_DIR"
    echo "Test environment cleaned."
}

# --- Test Cases ---

test_help_message() {
    echo "Running test: Help message"
    output=$("$SCRIPT_PATH" -h)
    if echo "$output" | grep -q "Usage: $SCRIPT_PATH"; then
        echo "PASS: Help message displayed correctly."
    else
        echo "FAIL: Help message not displayed."
        echo "Output: $output"
        exit 1
    fi
}

test_detects_old_large_file() {
    echo "Running test: Detects old large file"
    output=$("$SCRIPT_PATH" -p "$TEST_DIR" -a 365 -s 100)
    if echo "$output" | grep -q "old_large_file.bin"; then
        echo "PASS: Old large file detected."
    else
        echo "FAIL: Old large file not detected."
        echo "Output: $output"
        exit 1
    fi
}

test_detects_old_large_directory() {
    echo "Running test: Detects old large directory"
    output=$("$SCRIPT_PATH" -p "$TEST_DIR" -a 365 -s 100)
    if echo "$output" | grep -q "old_large_dir"; then
        echo "PASS: Old large directory detected."
    else
        echo "FAIL: Old large directory not detected."
        echo "Output: $output"
        exit 1
    fi
}

test_ignores_new_large_file() {
    echo "Running test: Ignores new large file"
    output=$("$SCRIPT_PATH" -p "$TEST_DIR" -a 365 -s 100)
    if echo "$output" | grep -q "new_large_file.bin"; then
        echo "FAIL: New large file detected (should be ignored)."
        echo "Output: $output"
        exit 1
    else
        echo "PASS: New large file ignored."
    fi
}

test_ignores_small_old_file() {
    echo "Running test: Ignores small old file"
    output=$("$SCRIPT_PATH" -p "$TEST_DIR" -a 365 -s 100)
    if echo "$output" | grep -q "old_small_file.txt"; then
        echo "FAIL: Small old file detected (should be ignored)."
        echo "Output: $output"
        exit 1
    else
        echo "PASS: Small old file ignored."
    fi
}

test_ignores_new_large_directory() {
    echo "Running test: Ignores new large directory"
    output=$("$SCRIPT_PATH" -p "$TEST_DIR" -a 365 -s 100)
    if echo "$output" | grep -q "new_large_dir"; then
        echo "FAIL: New large directory detected (should be ignored)."
        echo "Output: $output"
        exit 1
    else
        echo "PASS: New large directory ignored."
    fi
}

test_ignores_small_old_directory() {
    echo "Running test: Ignores small old directory"
    output=$("$SCRIPT_PATH" -p "$TEST_DIR" -a 365 -s 100)
    if echo "$output" | grep -q "old_small_dir"; then
        echo "FAIL: Small old directory detected (should be ignored)."
        echo "Output: $output"
        exit 1
    else
        echo "PASS: Small old directory ignored."
    fi
}

test_no_dust_message() {
    echo "Running test: No dust message when nothing found"
    # Create a temporary directory with no dust bunnies
    NO_DUST_DIR=$(mktemp -d)
    output=$("$SCRIPT_PATH" -p "$NO_DUST_DIR" -a 1 -s 1) # Very strict criteria
    if echo "$output" | grep -q "no significant dust bunnies found"; then
        echo "PASS: 'No dust' message displayed."
    else
        echo "FAIL: 'No dust' message not displayed."
        echo "Output: $output"
        exit 1
    fi
    rm -rf "$NO_DUST_DIR"
}

test_custom_age_and_size() {
    echo "Running test: Custom age and size parameters"
    # Create a file that is 6 months old and 60MB
    dd if=/dev/zero of="$TEST_DIR/medium_old_file.bin" bs=1M count=60 > /dev/null 2>&1
    touch -d "6 months ago" "$TEST_DIR/medium_old_file.bin"

    # Test with default (age 365, size 100) - should NOT find
    output_default=$("$SCRIPT_PATH" -p "$TEST_DIR")
    if echo "$output_default" | grep -q "medium_old_file.bin"; then
        echo "FAIL: medium_old_file.bin detected with default settings (should not be)."
        echo "Output: $output_default"
        exit 1
    else
        echo "PASS: medium_old_file.bin ignored by default settings."
    fi

    # Test with custom (age 90, size 50) - should find
    output_custom=$("$SCRIPT_PATH" -p "$TEST_DIR" -a 90 -s 50)
    if echo "$output_custom" | grep -q "medium_old_file.bin"; then
        echo "PASS: medium_old_file.bin detected with custom settings."
    else
        echo "FAIL: medium_old_file.bin not detected with custom settings."
        echo "Output: $output_custom"
        exit 1
    fi
    rm "$TEST_DIR/medium_old_file.bin"
}


# --- Main Test Runner ---
main() {
    setup_test_environment

    test_help_message
    test_detects_old_large_file
    test_detects_old_large_directory
    test_ignores_new_large_file
    test_ignores_small_old_file
    test_ignores_new_large_directory
    test_ignores_small_old_directory
    test_no_dust_message
    test_custom_age_and_size

    cleanup_test_environment
    echo "All tests passed!"
}

main
