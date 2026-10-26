#!/bin/bash

# Automated tests for Nightly Dust Bunny Sweeper

# --- Test Setup ---

# Create a temporary directory for tests
TEST_DIR=$(mktemp -d -t dust-bunny-sweeper-test-XXXXXX)
MOCK_TRASH_DIR="${TEST_DIR}/mock_trash"
mkdir -p "${MOCK_TRASH_DIR}"

# Mock rationale:
# find: We simulate find's output by creating a temporary directory structure with touch to control modification times.
#       This avoids relying on the actual system's find behavior and allows precise control over test data.
# rm: We override the rm command within the test script to move files to a designated "mock_trash" directory instead of
#     permanently deleting them. This ensures tests are non-destructive, deterministic, and can be run offline.
# read: We mock 'read' to automatically provide 'y' or 'n' for confirmation prompts, making the tests non-interactive.

# Override 'rm' command for testing purposes
rm() {
    for arg in "$@"; do
        if [[ "$arg" != -* ]]; then # If it's not a flag (like -r, -f)
            # Check if the item actually exists before trying to move it
            if [[ -e "$arg" ]]; then
                mv "$arg" "${MOCK_TRASH_DIR}/" 2>/dev/null || true # Move to mock trash, ignore errors if already gone
                echo "MOCKED_RM: Moved '$arg' to mock trash." # Log for verification
            fi
        fi
    done
}

# Override 'read' command for testing purposes
# This makes tests non-interactive by always returning 'y' or 'n' based on a global variable.
TEST_READ_REPLY="y"
read() {
    if [[ "$1" == "-p"* ]]; then # If it's a prompt
        # Simulate user input based on TEST_READ_REPLY
        REPLY="${TEST_READ_REPLY}"
        echo "MOCKED_READ: Responded with '${REPLY}'"
    else
        # Fallback for other read usages if any, though unlikely in this script
        builtin read "$@"
    fi
}

# Helper function to create a file with a specific modification time
create_test_file() {
    local path="$1"
    local days_ago="$2"
    touch -t "$(date -d "${days_ago} days ago" +%Y%m%d%H%M)" "$path"
}

# Helper function to create an empty directory with a specific modification time
create_test_dir() {
    local path="$1"
    local days_ago="$2"
    mkdir -p "$path"
    touch -t "$(date -d "${days_ago} days ago" +%Y%m%d%H%M)" "$path"
}

# Source the script to be tested
SCRIPT_TO_TEST="$(dirname "$0")"/../src/dust_bunny_sweeper.sh

# --- Test Cases ---

# Test 1: Dry run - no deletion, correct items identified
test_dry_run() {
    echo "Running Test 1: Dry run - no deletion, correct items identified"
    local test_case_dir="${TEST_DIR}/test1"
    mkdir -p "${test_case_dir}"
    create_test_file "${test_case_dir}/old_file.txt" 10
    create_test_file "${test_case_dir}/new_file.txt" 1
    create_test_dir "${test_case_dir}/old_empty_dir" 10
    create_test_dir "${test_case_dir}/new_empty_dir" 1
    mkdir -p "${test_case_dir}/old_non_empty_dir"
    create_test_file "${test_case_dir}/old_non_empty_dir/file.txt" 10
    touch -t "$(date -d "10 days ago" +%Y%m%d%H%M)" "${test_case_dir}/old_non_empty_dir"

    output=$(bash "$SCRIPT_TO_TEST" "${test_case_dir}" 5 --dry-run)

    if echo "$output" | grep -q "old_file.txt" && \
       echo "$output" | grep -q "old_empty_dir" && \
       ! echo "$output" | grep -q "new_file.txt" && \
       ! echo "$output" | grep -q "new_empty_dir" && \
       ! echo "$output" | grep -q "old_non_empty_dir" && \
       echo "$output" | grep -q "This was a dry run. No dust bunnies were swept."; then
        echo "Test 1 PASSED"
    else
        echo "Test 1 FAILED"
        echo "Output:"
        echo "$output"
        exit 1
    fi
    rm -rf "${test_case_dir}" # Clean up test case directory
    rm -rf "${MOCK_TRASH_DIR}"/* # Clear mock trash
}

# Test 2: Actual deletion with confirmation (mocked 'y')
test_actual_deletion_confirm() {
    echo "Running Test 2: Actual deletion with confirmation (mocked 'y')"
    local test_case_dir="${TEST_DIR}/test2"
    mkdir -p "${test_case_dir}"
    create_test_file "${test_case_dir}/old_file_to_delete.txt" 10
    create_test_dir "${test_case_dir}/old_empty_dir_to_delete" 10
    create_test_file "${test_case_dir}/new_file_to_keep.txt" 1

    TEST_READ_REPLY="y" bash "$SCRIPT_TO_TEST" "${test_case_dir}" 5

    if [[ ! -f "${test_case_dir}/old_file_to_delete.txt" ]] && \
       [[ ! -d "${test_case_dir}/old_empty_dir_to_delete" ]] && \
       [[ -f "${test_case_dir}/new_file_to_keep.txt" ]] && \
       [[ -f "${MOCK_TRASH_DIR}/old_file_to_delete.txt" ]] && \
       [[ -d "${MOCK_TRASH_DIR}/old_empty_dir_to_delete" ]]; then
        echo "Test 2 PASSED"
    else
        echo "Test 2 FAILED"
        ls -lR "${test_case_dir}"
        ls -lR "${MOCK_TRASH_DIR}"
        exit 1
    fi
    rm -rf "${test_case_dir}" # Clean up test case directory
    rm -rf "${MOCK_TRASH_DIR}"/* # Clear mock trash
}

# Test 3: Actual deletion with no confirmation (--force)
test_actual_deletion_force() {
    echo "Running Test 3: Actual deletion with --force"
    local test_case_dir="${TEST_DIR}/test3"
    mkdir -p "${test_case_dir}"
    create_test_file "${test_case_dir}/force_old_file.txt" 10
    create_test_dir "${test_case_dir}/force_old_empty_dir" 10
    create_test_file "${test_case_dir}/force_new_file.txt" 1

    bash "$SCRIPT_TO_TEST" "${test_case_dir}" 5 --force

    if [[ ! -f "${test_case_dir}/force_old_file.txt" ]] && \
       [[ ! -d "${test_case_dir}/force_old_empty_dir" ]] && \
       [[ -f "${test_case_dir}/force_new_file.txt" ]] && \
       [[ -f "${MOCK_TRASH_DIR}/force_old_file.txt" ]] && \
       [[ -d "${MOCK_TRASH_DIR}/force_old_empty_dir" ]]; then
        echo "Test 3 PASSED"
    else
        echo "Test 3 FAILED"
        ls -lR "${test_case_dir}"
        ls -lR "${MOCK_TRASH_DIR}"
        exit 1
    fi
    rm -rf "${test_case_dir}" # Clean up test case directory
    rm -rf "${MOCK_TRASH_DIR}"/* # Clear mock trash
}

# Test 4: No dust bunnies found
test_no_dust_bunnies() {
    echo "Running Test 4: No dust bunnies found"
    local test_case_dir="${TEST_DIR}/test4"
    mkdir -p "${test_case_dir}"
    create_test_file "${test_case_dir}/recent_file.txt" 1
    create_test_dir "${test_case_dir}/recent_empty_dir" 1

    output=$(bash "$SCRIPT_TO_TEST" "${test_case_dir}" 5 --dry-run)

    if echo "$output" | grep -q "No digital dust bunnies found older than 5 days" && \
       echo "$output" | grep -q "Your digital space is sparkling clean!" && \
       [[ -f "${test_case_dir}/recent_file.txt" ]] && \
       [[ -d "${test_case_dir}/recent_empty_dir" ]]; then
        echo "Test 4 PASSED"
    else
        echo "Test 4 FAILED"
        echo "Output:"
        echo "$output"
        exit 1
    fi
    rm -rf "${test_case_dir}" # Clean up test case directory
    rm -rf "${MOCK_TRASH_DIR}"/* # Clear mock trash
}

# Test 5: Invalid directory
test_invalid_directory() {
    echo "Running Test 5: Invalid directory"
    local non_existent_dir="${TEST_DIR}/non_existent"
    output=$(bash "$SCRIPT_TO_TEST" "${non_existent_dir}" 10 2>&1)

    if echo "$output" | grep -q "ERROR: Target directory '${non_existent_dir}' does not exist or is not a directory."; then
        echo "Test 5 PASSED"
    else
        echo "Test 5 FAILED"
        echo "Output:"
        echo "$output"
        exit 1
    fi
    rm -rf "${MOCK_TRASH_DIR}"/* # Clear mock trash
}

# Test 6: Default age
test_default_age() {
    echo "Running Test 6: Default age"
    local test_case_dir="${TEST_DIR}/test6"
    mkdir -p "${test_case_dir}"
    create_test_file "${test_case_dir}/old_default.txt" 35 # Older than default 30
    create_test_file "${test_case_dir}/new_default.txt" 20 # Newer than default 30

    output=$(bash "$SCRIPT_TO_TEST" "${test_case_dir}" --dry-run)

    if echo "$output" | grep -q "No age specified. Defaulting to 30 days." && \
       echo "$output" | grep -q "old_default.txt" && \
       ! echo "$output" | grep -q "new_default.txt"; then
        echo "Test 6 PASSED"
    else
        echo "Test 6 FAILED"
        echo "Output:"
        echo "$output"
        exit 1
    fi
    rm -rf "${test_case_dir}" # Clean up test case directory
    rm -rf "${MOCK_TRASH_DIR}"/* # Clear mock trash
}

# Test 7: Confirmation denied (mocked 'n')
test_confirmation_denied() {
    echo "Running Test 7: Confirmation denied (mocked 'n')"
    local test_case_dir="${TEST_DIR}/test7"
    mkdir -p "${test_case_dir}"
    create_test_file "${test_case_dir}/old_file_to_deny.txt" 10

    TEST_READ_REPLY="n" output=$(bash "$SCRIPT_TO_TEST" "${test_case_dir}" 5)

    if echo "$output" | grep -q "Sweep cancelled. Digital dust bunnies live to see another day" && \
       [[ -f "${test_case_dir}/old_file_to_deny.txt" ]] && \
       [[ ! -f "${MOCK_TRASH_DIR}/old_file_to_deny.txt" ]]; then
        echo "Test 7 PASSED"
    else
        echo "Test 7 FAILED"
        echo "Output:"
        echo "$output"
        ls -lR "${test_case_dir}"
        ls -lR "${MOCK_TRASH_DIR}"
        exit 1
    fi
    rm -rf "${test_case_dir}" # Clean up test case directory
    rm -rf "${MOCK_TRASH_DIR}"/* # Clear mock trash
}

# --- Run Tests ---

test_dry_run
test_actual_deletion_confirm
test_actual_deletion_force
test_no_dust_bunnies
test_invalid_directory
test_default_age
test_confirmation_denied

# --- Cleanup ---
rm -rf "${TEST_DIR}"
echo "All tests completed. Temporary test directory '${TEST_DIR}' removed."
