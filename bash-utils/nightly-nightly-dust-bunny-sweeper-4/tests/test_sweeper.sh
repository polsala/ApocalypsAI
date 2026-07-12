#!/bin/bash

# --- Setup ---
TEST_DIR=$(mktemp -d)

# Create test files/directories (these are for actual filesystem checks if mocks were not used,
# but with mocks, they serve as conceptual targets for the mocked 'find' output)
mkdir -p "$TEST_DIR/old_dir" "$TEST_DIR/empty_dir" "$TEST_DIR/recent_dir"
touch -t $(date -v-3d +%Y%m%d%H%M.%S 2>/dev/null || date -d "3 days ago" +%Y%m%d%H%M.%S) "$TEST_DIR/old_file.log" # Old file (3 days ago)
touch -t $(date -v-3d +%Y%m%d%H%M.%S 2>/dev/null || date -d "3 days ago" +%Y%m%d%H%M.%S) "$TEST_DIR/old_dir/another_old_file.tmp"
touch "$TEST_DIR/recent_file.txt" # Recent file

# --- Mocks ---
MOCKED_FIND_OUTPUT=""
MOCKED_RM_CALLS=""

find() {
    # Mock rationale: We control the output of 'find' to ensure deterministic test results
    # without relying on actual filesystem timestamps or complex 'find' arguments.
    # Output null-terminated strings as expected by the main script's 'read -d '''
    echo -ne "$MOCKED_FIND_OUTPUT"
}

rm() {
    # Mock rationale: We prevent actual file deletion during tests and record 'rm' calls
    # to verify the script's behavior without side effects.
    MOCKED_RM_CALLS+="rm $@\n"
    # Simulate success
    return 0
}

# --- Test Cases ---

# Test 1: Dry run - should report old files/empty dirs
# Null-terminated strings for find output
MOCKED_FIND_OUTPUT="${TEST_DIR}/old_file.log\0${TEST_DIR}/old_dir\0${TEST_DIR}/empty_dir\0"
MOCKED_RM_CALLS="" # Reset for this test

OUTPUT=$(bash src/dust_bunny_sweeper.sh "$TEST_DIR" 2 dry-run)

if echo "$OUTPUT" | grep -q "Found 3 digital dust bunnies"; then
    echo "Test 1 (Dry run count) PASSED"
else
    echo "Test 1 (Dry run count) FAILED"
    echo "Output: $OUTPUT"
    exit 1
fi

if echo "$OUTPUT" | grep -q "${TEST_DIR}/old_file.log (DRY RUN)"; then
    echo "Test 1 (Dry run file report) PASSED"
else
    echo "Test 1 (Dry run file report) FAILED"
    echo "Output: $OUTPUT"
    exit 1
fi

if [ -n "$MOCKED_RM_CALLS" ]; then
    echo "Test 1 (Dry run - no rm calls) FAILED: rm was called."
    echo "RM calls: $MOCKED_RM_CALLS"
    exit 1
else
    echo "Test 1 (Dry run - no rm calls) PASSED"
fi

# Test 2: Cleanup run - should call rm for old files/empty dirs
MOCKED_FIND_OUTPUT="${TEST_DIR}/old_file.log\0${TEST_DIR}/old_dir\0${TEST_DIR}/empty_dir\0"
MOCKED_RM_CALLS="" # Reset for this test

OUTPUT=$(bash src/dust_bunny_sweeper.sh "$TEST_DIR" 2 cleanup)

if echo "$OUTPUT" | grep -q "Swept away 3 digital dust bunnies"; then
    echo "Test 2 (Cleanup count) PASSED"
else
    echo "Test 2 (Cleanup count) FAILED"
    echo "Output: $OUTPUT"
    exit 1
fi

if echo "$OUTPUT" | grep -q "${TEST_DIR}/old_file.log (CLEANED)"; then
    echo "Test 2 (Cleanup file report) PASSED"
else
    echo "Test 2 (Cleanup file report) FAILED"
    echo "Output: $OUTPUT"
    exit 1
fi

# Verify rm calls for each item
if echo "$MOCKED_RM_CALLS" | grep -q "rm -rf \"${TEST_DIR}/old_file.log\""; then
    echo "Test 2 (Cleanup - rm old_file) PASSED"
else
    echo "Test 2 (Cleanup - rm old_file) FAILED: rm for old_file.log not found."
    echo "RM calls: $MOCKED_RM_CALLS"
    exit 1
fi

if echo "$MOCKED_RM_CALLS" | grep -q "rm -rf \"${TEST_DIR}/old_dir\""; then
    echo "Test 2 (Cleanup - rm old_dir) PASSED"
else
    echo "Test 2 (Cleanup - rm old_dir) FAILED: rm for old_dir not found."
    echo "RM calls: $MOCKED_RM_CALLS"
    exit 1
fi

if echo "$MOCKED_RM_CALLS" | grep -q "rm -rf \"${TEST_DIR}/empty_dir\""; then
    echo "Test 2 (Cleanup - rm empty_dir) PASSED"
else
    echo "Test 2 (Cleanup - rm empty_dir) FAILED: rm for empty_dir not found."
    echo "RM calls: $MOCKED_RM_CALLS"
    exit 1
fi


# Test 3: No dust bunnies found
MOCKED_FIND_OUTPUT="" # No files found
MOCKED_RM_CALLS="" # Reset for this test

OUTPUT=$(bash src/dust_bunny_sweeper.sh "$TEST_DIR" 2 dry-run)

if echo "$OUTPUT" | grep -q "No digital dust bunnies found"; then
    echo "Test 3 (No dust bunnies) PASSED"
else
    echo "Test 3 (No dust bunnies) FAILED"
    echo "Output: $OUTPUT"
    exit 1
fi

# Test 4: Invalid directory
MOCKED_FIND_OUTPUT=""
MOCKED_RM_CALLS=""

OUTPUT=$(bash src/dust_bunny_sweeper.sh "/non/existent/path" 2 dry-run 2>&1) # Redirect stderr to stdout

if echo "$OUTPUT" | grep -q "Error: Directory '/non/existent/path' not found."; then
    echo "Test 4 (Invalid directory) PASSED"
else
    echo "Test 4 (Invalid directory) FAILED"
    echo "Output: $OUTPUT"
    exit 1
fi

# Test 5: Invalid mode
MOCKED_FIND_OUTPUT=""
MOCKED_RM_CALLS=""

OUTPUT=$(bash src/dust_bunny_sweeper.sh "$TEST_DIR" 2 invalid-mode 2>&1) # Redirect stderr to stdout

if echo "$OUTPUT" | grep -q "Error: Invalid mode 'invalid-mode'. Use 'dry-run' or 'cleanup'."; then
    echo "Test 5 (Invalid mode) PASSED"
else
    echo "Test 5 (Invalid mode) FAILED"
    echo "Output: $OUTPUT"
    exit 1
fi


# --- Teardown ---
rm -rf "$TEST_DIR"
echo "All tests completed."
