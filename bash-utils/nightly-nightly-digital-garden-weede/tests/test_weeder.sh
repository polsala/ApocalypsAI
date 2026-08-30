#!/bin/bash

# Test script for Nightly Digital Garden Weeder

# Set up a temporary test directory
TEST_DIR=$(mktemp -d -t weeder-test-XXXXXX)
WEEDER_SCRIPT="../src/weeder.sh"

# Mock rationale:
# We mock 'find' and 'rm' to ensure tests are deterministic,
# run offline, and do not modify the actual filesystem.
# This allows us to control the exact input 'find' would produce
# and verify the exact arguments 'rm' would receive, without
# relying on system state or actual file operations.

# --- MOCK FUNCTIONS ---
MOCKED_FIND_OUTPUT=""
MOCKED_RM_CALLS=""
MOCKED_RM_EXIT_CODE=0

find() {
    # Mock rationale: Simulate the output of the 'find' command
    # based on predefined test scenarios.
    echo -e "$MOCKED_FIND_OUTPUT"
    return 0
}

rm() {
    # Mock rationale: Record calls to 'rm' and its arguments
    # instead of actually deleting files. This allows verification
    # of what *would* be deleted.
    MOCKED_RM_CALLS+="$*\n"
    return "$MOCKED_RM_EXIT_CODE"
}

# --- HELPER FUNCTIONS ---
cleanup() {
    /bin/rm -rf "$TEST_DIR" # Use absolute path to avoid mocking rm during cleanup
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    if ! echo "$haystack" | grep -qF "$needle"; then
        echo "FAIL: Expected '$haystack' to contain '$needle'"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    if echo "$haystack" | grep -qF "$needle"; then
        echo "FAIL: Expected '$haystack' NOT to contain '$needle'"
        exit 1
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    if [ "$expected" != "$actual" ]; then
        echo "FAIL: Expected '$expected', got '$actual'"
        exit 1
    fi
}

# --- TEST CASES ---

# Test 1: Dry run with no weeds
test_dry_run_no_weeds() {
    echo "Running Test 1: Dry run with no weeds"
    MOCKED_FIND_OUTPUT="" # Simulate no files/dirs found
    MOCKED_RM_CALLS=""
    MOCKED_RM_EXIT_CODE=0

    output=$("$WEEDER_SCRIPT" --path "$TEST_DIR" --age 1 --dry-run)
    exit_code=$?

    assert_equals 0 "$exit_code"
    assert_contains "$output" "Your digital garden is already pristine!"
    assert_equals "" "$MOCKED_RM_CALLS" # No rm calls in dry run
    echo "Test 1 Passed."
}

# Test 2: Dry run with old files and empty directories
test_dry_run_with_weeds() {
    echo "Running Test 2: Dry run with old files and empty directories"
    MOCKED_FIND_OUTPUT="${TEST_DIR}/old_file.txt\n${TEST_DIR}/empty_dir" # Simulate some weeds
    MOCKED_RM_CALLS=""
    MOCKED_RM_EXIT_CODE=0

    output=$("$WEEDER_SCRIPT" --path "$TEST_DIR" --age 1 --dry-run)
    exit_code=$?

    assert_equals 0 "$exit_code"
    assert_contains "$output" "Found these ancient digital weeds"
    assert_contains "$output" "${TEST_DIR}/old_file.txt"
    assert_contains "$output" "Found these desolate empty plots"
    assert_contains "$output" "${TEST_DIR}/empty_dir"
    assert_contains "$output" "Digital Garden Weeding complete (Dry Run)"
    assert_equals "" "$MOCKED_RM_CALLS" # No rm calls in dry run
    echo "Test 2 Passed."
}

# Test 3: Actual deletion with confirmation (mock user input)
test_actual_deletion_with_confirm() {
    echo "Running Test 3: Actual deletion with confirmation"
    MOCKED_FIND_OUTPUT="${TEST_DIR}/old_file.txt\n${TEST_DIR}/empty_dir"
    MOCKED_RM_CALLS=""
    MOCKED_RM_EXIT_CODE=0

    # Simulate user typing 'y' and Enter
    output=$(echo "y" | "$WEEDER_SCRIPT" --path "$TEST_DIR" --age 1)
    exit_code=$?

    assert_equals 0 "$exit_code"
    assert_contains "$output" "Proceed with recycling these withered data leaves"
    assert_contains "$output" "Digital Garden Weeding complete!"
    assert_contains "$MOCKED_RM_CALLS" "rm -v ${TEST_DIR}/old_file.txt"
    assert_contains "$MOCKED_RM_CALLS" "rm -rv ${TEST_DIR}/empty_dir"
    echo "Test 3 Passed."
}

# Test 4: Actual deletion with auto-confirm
test_actual_deletion_auto_confirm() {
    echo "Running Test 4: Actual deletion with auto-confirm"
    MOCKED_FIND_OUTPUT="${TEST_DIR}/another_old_file.log\n${TEST_DIR}/another_empty_dir"
    MOCKED_RM_CALLS=""
    MOCKED_RM_EXIT_CODE=0

    output=$("$WEEDER_SCRIPT" --path "$TEST_DIR" --age 1 --confirm)
    exit_code=$?

    assert_equals 0 "$exit_code"
    assert_contains "$output" "Digital Garden Weeding complete!"
    assert_contains "$MOCKED_RM_CALLS" "rm -v ${TEST_DIR}/another_old_file.log"
    assert_contains "$MOCKED_RM_CALLS" "rm -rv ${TEST_DIR}/another_empty_dir"
    echo "Test 4 Passed."
}

# Test 5: Deletion cancelled by user
test_deletion_cancelled() {
    echo "Running Test 5: Deletion cancelled by user"
    MOCKED_FIND_OUTPUT="${TEST_DIR}/cancel_file.tmp"
    MOCKED_RM_CALLS=""
    MOCKED_RM_EXIT_CODE=0

    # Simulate user typing 'n' and Enter
    output=$(echo "n" | "$WEEDER_SCRIPT" --path "$TEST_DIR" --age 1)
    exit_code=$?

    assert_equals 1 "$exit_code" # Script should exit with 1 on cancellation
    assert_contains "$output" "Weeding cancelled. Your digital garden remains as is."
    assert_equals "" "$MOCKED_RM_CALLS" # No rm calls
    echo "Test 5 Passed."
}

# Test 6: No candidates found, even without dry-run
test_no_candidates_no_dry_run() {
    echo "Running Test 6: No candidates found, even without dry-run"
    MOCKED_FIND_OUTPUT=""
    MOCKED_RM_CALLS=""
    MOCKED_RM_EXIT_CODE=0

    output=$("$WEEDER_SCRIPT" --path "$TEST_DIR" --age 1)
    exit_code=$?

    assert_equals 0 "$exit_code"
    assert_contains "$output" "Your digital garden is already pristine!"
    assert_equals "" "$MOCKED_RM_CALLS"
    echo "Test 6 Passed."
}

# Test 7: Error during rm operation
test_rm_error() {
    echo "Running Test 7: Error during rm operation"
    MOCKED_FIND_OUTPUT="${TEST_DIR}/problem_file.txt"
    MOCKED_RM_CALLS=""
    MOCKED_RM_EXIT_CODE=1 # Simulate rm failing

    output=$("$WEEDER_SCRIPT" --path "$TEST_DIR" --age 1 --confirm)
    exit_code=$?

    assert_equals 1 "$exit_code" # Script should exit with 1 on error
    assert_contains "$output" "A thorny issue encountered during weeding."
    assert_contains "$MOCKED_RM_CALLS" "rm -v ${TEST_DIR}/problem_file.txt"
    echo "Test 7 Passed."
}


# Run all tests
main() {
    cleanup # Ensure a clean slate before starting
    test_dry_run_no_weeds
    test_dry_run_with_weeds
    test_actual_deletion_with_confirm
    test_actual_deletion_auto_confirm
    test_deletion_cancelled
    test_no_candidates_no_dry_run
    test_rm_error
    cleanup # Clean up after all tests
    echo "All tests completed successfully!"
}

main
