#!/bin/bash

# Test setup
TEST_DIR=$(mktemp -d)
SCRIPT_PATH="./src/temporal_debris_sweep.sh"
MOCKED_FIND_OUTPUT=""
MOCKED_RM_CALLS=""

# Mock rationale: We need to control the output of 'find' and capture calls to 'rm'
# without actually touching the filesystem for deterministic, offline tests.
find() {
    echo -n "$MOCKED_FIND_OUTPUT"
}

rm() {
    MOCKED_RM_CALLS+="rm $*;"
}

# Helper function to run the script and capture output
run_script() {
    bash "${SCRIPT_PATH}" "$@"
}

# Test 1: Dry run - no files found
test_dry_run_no_files() {
    echo "Running Test 1: Dry run - no files found"
    MOCKED_FIND_OUTPUT=""
    MOCKED_RM_CALLS=""
    OUTPUT=$(run_script -d "${TEST_DIR}" -a 1)
    if echo "$OUTPUT" | grep -q "No significant temporal debris detected"; then
        echo "  PASS: Correctly reported no debris."
    else
        echo "  FAIL: Did not report no debris."
        echo "Output: $OUTPUT"
        exit 1
    fi
    if [ -n "$MOCKED_RM_CALLS" ]; then
        echo "  FAIL: rm was called in dry run."
        exit 1
    else
        echo "  PASS: rm was not called in dry run."
    fi
}

# Test 2: Dry run - files found
test_dry_run_files_found() {
    echo "Running Test 2: Dry run - files found"
    MOCKED_FIND_OUTPUT="${TEST_DIR}/old_file1.log\0${TEST_DIR}/old_file2.txt\0"
    MOCKED_RM_CALLS=""
    OUTPUT=$(run_script -d "${TEST_DIR}" -a 1)
    if echo "$OUTPUT" | grep -q "Detected temporal debris:"; then
        echo "  PASS: Correctly reported debris."
    else
        echo "  FAIL: Did not report debris."
        echo "Output: $OUTPUT"
        exit 1
    fi
    if echo "$OUTPUT" | grep -q "This was a dry run"; then
        echo "  PASS: Correctly indicated dry run."
    else
        echo "  FAIL: Did not indicate dry run."
        echo "Output: $OUTPUT"
        exit 1
    fi
    if [ -n "$MOCKED_RM_CALLS" ]; then
        echo "  FAIL: rm was called in dry run."
        exit 1
    else
        echo "  PASS: rm was not called in dry run."
    fi
}

# Test 3: Commit run - files found
test_commit_run_files_found() {
    echo "Running Test 3: Commit run - files found"
    MOCKED_FIND_OUTPUT="${TEST_DIR}/old_file1.log\0${TEST_DIR}/old_file2.txt\0"
    MOCKED_RM_CALLS=""
    OUTPUT=$(run_script -d "${TEST_DIR}" -a 1 -c)
    if echo "$OUTPUT" | grep -q "Initiating temporal debris purge..."; then
        echo "  PASS: Correctly indicated purge."
    else
        echo "  FAIL: Did not indicate purge."
        echo "Output: $OUTPUT"
        exit 1
    fi
    # xargs -0 rm -f will call rm once for each file
    EXPECTED_RM_CALLS="rm -f ${TEST_DIR}/old_file1.log;rm -f ${TEST_DIR}/old_file2.txt;"
    if [ "$MOCKED_RM_CALLS" = "$EXPECTED_RM_CALLS" ]; then
        echo "  PASS: rm was called with correct arguments."
    else
        echo "  FAIL: rm was not called correctly."
        echo "Expected: '$EXPECTED_RM_CALLS'"
        echo "Actual:   '$MOCKED_RM_CALLS'"
        exit 1
    fi
}

# Test 4: Invalid directory
test_invalid_directory() {
    echo "Running Test 4: Invalid directory"
    OUTPUT=$(run_script -d "/non/existent/path" 2>&1) # Redirect stderr to stdout
    if echo "$OUTPUT" | grep -q "Error: Target directory '/non/existent/path' does not exist or is not a directory."; then
        echo "  PASS: Correctly reported invalid directory."
    else
        echo "  FAIL: Did not report invalid directory."
        echo "Output: $OUTPUT"
        exit 1
    fi
}

# Run all tests
test_dry_run_no_files
test_dry_run_files_found
test_commit_run_files_found
test_invalid_directory

echo "All tests passed!"

# Cleanup
rm -rf "${TEST_DIR}"
