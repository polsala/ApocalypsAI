#!/bin/bash

# Test script for nightly-dust-bunny-sweeper

# Set -e to exit immediately if a command exits with a non-zero status.
set -e

# Define the path to the script
SCRIPT_PATH="./src/dust_bunny_sweeper.sh"

# Global array to track mocked deletions
MOCKED_DELETED_FILES=()

# --- Test Utilities ---
# Function to create a temporary directory and clean it up on exit
setup_test_env() {
    TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
    export TEST_DIR # Make it available to subshells/mocks
    echo "Created test environment: $TEST_DIR"
    cd "$TEST_DIR"
}

cleanup_test_env() {
    cd - > /dev/null # Go back to original directory
    rm -rf "$TEST_DIR"
    echo "Cleaned up test environment: $TEST_DIR"
}

# Mock commands
# Mock rationale: Prevents actual file system changes and allows controlled output for 'find', 'rm', 'du', 'numfmt'.
mock_find() {
    local dir="$1"
    local type="$2"
    local mtime="$3"
    local print0="$4"
    # Simulate find output based on predefined test files
    if [[ "$dir" == "./test_dir_1" && "$mtime" == "+7" ]]; then
        echo -ne "./test_dir_1/old_file_1.txt\0./test_dir_1/old_file_2.log\0"
    elif [[ "$dir" == "./test_dir_2" && "$mtime" == "+7" ]]; then
        echo -ne "./test_dir_2/ancient_data.bak\0"
    elif [[ "$dir" == "." && "$mtime" == "+7" ]]; then
        echo -ne "./old_file_in_cwd.tmp\0"
    else
        echo -n ""
    fi
}

mock_rm() {
    # Simulate rm by just printing what would be deleted
    # In a real test, you'd check if the file exists before/after
    # echo "MOCK_RM: Deleting $1"
    # For testing purposes, we'll track "deleted" files in a global array
    MOCKED_DELETED_FILES+=("$1")
    return 0 # Always succeed for mock
}

mock_du() {
    # Simulate du -b to return a fixed size for testing
    # Mock rationale: Provides deterministic file sizes for calculation.
    echo "1024\t$1" # All files are 1KB for simplicity in tests
}

mock_numfmt() {
    # Mock rationale: Provides deterministic formatted output for file sizes.
    local size="$1"
    local to="$2"
    local suffix="$3"
    local format="$4"
    # Based on mock_du returning 1024 bytes
    echo "1.0KiB"
}

# Override commands for testing
export -f find=mock_find
export -f rm=mock_rm
export -f du=mock_du
export -f numfmt=mock_numfmt

# --- Test Cases ---

# Test 1: Dry run with specified directories
test_dry_run_multiple_dirs() {
    echo "--- Running Test 1: Dry run with multiple directories ---"
    setup_test_env

    mkdir -p test_dir_1 test_dir_2
    touch test_dir_1/old_file_1.txt test_dir_1/old_file_2.log
    touch test_dir_2/ancient_data.bak
    touch test_dir_1/new_file.txt # This should not be found by mock_find

    # Run the script in dry-run mode
    OUTPUT=$("$SCRIPT_PATH" 7 ./test_dir_1 ./test_dir_2 --dry-run)

    # Assertions
    echo "$OUTPUT" | grep -q "--- DRY RUN MODE: No files will be deleted. ---"
    echo "$OUTPUT" | grep -q "Found a dusty relic: ./test_dir_1/old_file_1.txt"
    echo "$OUTPUT" | grep -q "Found a dusty relic: ./test_dir_1/old_file_2.log"
    echo "$OUTPUT" | grep -q "Found a dusty relic: ./test_dir_2/ancient_data.bak"
    echo "$OUTPUT" | grep -q "Total digital dust bunnies swept across all realms: 0" # Dry run doesn't increment this
    echo "$OUTPUT" | grep -q "Total digital fluff (disk space) reclaimed: 0.0B" # Dry run doesn't reclaim

    # Ensure no actual deletion happened (via mock, MOCKED_DELETED_FILES should be empty)
    if [[ "${#MOCKED_DELETED_FILES[@]}" -ne 0 ]]; then
        echo "FAIL: Files were unexpectedly marked for deletion in dry run."
        cleanup_test_env
        exit 1
    fi

    echo "Test 1 Passed."
    cleanup_test_env
}

# Test 2: Actual run with specified directories
test_actual_run_multiple_dirs() {
    echo "--- Running Test 2: Actual run with multiple directories ---"
    setup_test_env

    mkdir -p test_dir_1 test_dir_2
    touch test_dir_1/old_file_1.txt test_dir_1/old_file_2.log
    touch test_dir_2/ancient_data.bak

    MOCKED_DELETED_FILES=() # Reset for this test

    # Run the script in actual deletion mode
    OUTPUT=$("$SCRIPT_PATH" 7 ./test_dir_1 ./test_dir_2)

    # Assertions
    echo "$OUTPUT" | grep -q "Gently ushered into the void. ✨"
    echo "$OUTPUT" | grep -q "Total digital dust bunnies swept across all realms: 3"
    echo "$OUTPUT" | grep -q "Total digital fluff (disk space) reclaimed: 3.0KiB"

    # Ensure mock_rm was called for the correct files
    if [[ "${#MOCKED_DELETED_FILES[@]}" -ne 3 ]]; then
        echo "FAIL: Expected 3 files to be marked for deletion, but got ${#MOCKED_DELETED_FILES[@]}.
Files: ${MOCKED_DELETED_FILES[*]}"
        cleanup_test_env
        exit 1
    fi
    echo "MOCKED_DELETED_FILES: ${MOCKED_DELETED_FILES[*]}"
    echo "${MOCKED_DELETED_FILES[*]}" | grep -q "./test_dir_1/old_file_1.txt"
    echo "${MOCKED_DELETED_FILES[*]}" | grep -q "./test_dir_1/old_file_2.log"
    echo "${MOCKED_DELETED_FILES[*]}" | grep -q "./test_dir_2/ancient_data.bak"

    echo "Test 2 Passed."
    cleanup_test_env
}

# Test 3: No directories specified (should use current directory)
test_no_dirs_specified() {
    echo "--- Running Test 3: No directories specified (uses CWD) ---"
    setup_test_env

    touch old_file_in_cwd.tmp
    touch new_file_in_cwd.txt # This should not be found by mock_find

    MOCKED_DELETED_FILES=() # Reset for this test

    # Run the script without specifying directories
    OUTPUT=$("$SCRIPT_PATH" 7)

    # Assertions
    echo "$OUTPUT" | grep -q "Sweeping through the digital corners of: ."
    echo "$OUTPUT" | grep -q "Found a dusty relic: ./old_file_in_cwd.tmp"
    echo "$OUTPUT" | grep -q "Total digital dust bunnies swept across all realms: 1"
    echo "$OUTPUT" | grep -q "Total digital fluff (disk space) reclaimed: 1.0KiB"

    if [[ "${#MOCKED_DELETED_FILES[@]}" -ne 1 ]]; then
        echo "FAIL: Expected 1 file to be marked for deletion, but got ${#MOCKED_DELETED_FILES[@]}.
Files: ${MOCKED_DELETED_FILES[*]}"
        cleanup_test_env
        exit 1
    fi
    echo "${MOCKED_DELETED_FILES[*]}" | grep -q "./old_file_in_cwd.tmp"

    echo "Test 3 Passed."
    cleanup_test_env
}

# Test 4: Invalid age argument
test_invalid_age() {
    echo "--- Running Test 4: Invalid age argument ---"
    setup_test_env # Setup to ensure cleanup runs

    # Expect script to exit with error
    if ! "$SCRIPT_PATH" "abc" 2>&1 | grep -q "Error: <age_in_days> must be a positive integer."; then
        echo "FAIL: Script did not handle invalid age argument correctly."
        cleanup_test_env
        exit 1
    fi
    echo "Test 4 Passed."
    cleanup_test_env
}

# Test 5: Non-existent directory
test_non_existent_dir() {
    echo "--- Running Test 5: Non-existent directory ---"
    setup_test_env

    # Expect script to warn about non-existent directory but continue
    OUTPUT=$("$SCRIPT_PATH" 7 ./non_existent_dir 2>&1)

    echo "$OUTPUT" | grep -q "Warning: Directory './non_existent_dir' does not exist or is not a directory. Skipping."
    echo "$OUTPUT" | grep -q "No ancient digital dust bunnies found here. All clear! 🌟" # Since no valid dirs, it will sweep CWD by default, which is empty in this mock setup.
    echo "$OUTPUT" | grep -q "Total digital dust bunnies swept across all realms: 0"
    echo "Test 5 Passed."
    cleanup_test_env
}

# Run all tests
test_dry_run_multiple_dirs
test_actual_run_multiple_dirs
test_no_dirs_specified
test_invalid_age
test_non_existent_dir

echo ""
echo "All Nightly Digital Dust Bunny Sweeper tests passed successfully! 🎉"
