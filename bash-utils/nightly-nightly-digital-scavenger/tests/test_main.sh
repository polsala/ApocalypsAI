#!/bin/bash

# Source the main script
SCRIPT_TO_TEST="../src/main.sh"

# Create a temporary directory for testing
TEST_DIR=$(mktemp -d)
echo "Using temporary test directory: $TEST_DIR"

# Ensure cleanup on exit
cleanup() {
    echo "Cleaning up $TEST_DIR"
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Test 1: No files found
echo "--- Test 1: No stale files found ---"
OUTPUT=$(bash "$SCRIPT_TO_TEST" -d "$TEST_DIR" --dry-run)
if echo "$OUTPUT" | grep -q "No ancient digital artifacts found"; then
    echo "Test 1 Passed: Correctly reported no files."
else
    echo "Test 1 FAILED: Expected 'No ancient digital artifacts found', got:"
    echo "$OUTPUT"
    exit 1
fi

# Create some files for testing
touch "$TEST_DIR/new_file.txt" # Current time
touch -d "2 days ago" "$TEST_DIR/recent_file.log"
touch -d "40 days ago" "$TEST_DIR/old_file_1.dat"
touch -d "45 days ago" "$TEST_DIR/old_file_2.tmp"
mkdir "$TEST_DIR/subdir"
touch -d "50 days ago" "$TEST_DIR/subdir/old_nested_file.txt"

# Test 2: Dry run - should list old files but not delete
echo "--- Test 2: Dry run - list old files ---"
OUTPUT=$(bash "$SCRIPT_TO_TEST" -d "$TEST_DIR" -a 30 --dry-run)

if echo "$OUTPUT" | grep -q "Found 3 potential relics" && \
   echo "$OUTPUT" | grep -q "old_file_1.dat" && \
   echo "$OUTPUT" | grep -q "old_file_2.tmp" && \
   echo "$OUTPUT" | grep -q "old_nested_file.txt" && \
   echo "$OUTPUT" | grep -q "DRY RUN COMPLETE"; then
    echo "Test 2 Passed: Correctly listed old files in dry run."
else
    echo "Test 2 FAILED: Dry run output incorrect."
    echo "$OUTPUT"
    exit 1
fi

# Verify files still exist after dry run
if [ -f "$TEST_DIR/old_file_1.dat" ] && [ -f "$TEST_DIR/old_file_2.tmp" ] && [ -f "$TEST_DIR/subdir/old_nested_file.txt" ]; then
    echo "Test 2 Passed: Files still exist after dry run."
else
    echo "Test 2 FAILED: Files were unexpectedly deleted during dry run."
    ls -l "$TEST_DIR"
    exit 1
fi

# Test 3: Actual deletion with --force
echo "--- Test 3: Actual deletion with --force ---"
# Mock rationale: For `read` command, we can pipe 'y' to stdin for confirmation.
# However, using `--force` bypasses `read` entirely, making the test deterministic.
OUTPUT=$(bash "$SCRIPT_TO_TEST" -d "$TEST_DIR" -a 30 --force)

if echo "$OUTPUT" | grep -q "Salvage complete! 3 digital relics reclaimed"; then
    echo "Test 3 Passed: Correctly reported deletion."
else
    echo "Test 3 FAILED: Deletion output incorrect."
    echo "$OUTPUT"
    exit 1
fi

# Verify old files are deleted and new/recent ones remain
if [ ! -f "$TEST_DIR/old_file_1.dat" ] && \
   [ ! -f "$TEST_DIR/old_file_2.tmp" ] && \
   [ ! -f "$TEST_DIR/subdir/old_nested_file.txt" ] && \
   [ -f "$TEST_DIR/new_file.txt" ] && \
   [ -f "$TEST_DIR/recent_file.log" ]; then
    echo "Test 3 Passed: Old files deleted, new/recent files remain."
else
    echo "Test 3 FAILED: File deletion verification failed."
    ls -l "$TEST_DIR"
    exit 1
fi

# Test 4: Deletion without --force, user input 'N'
echo "--- Test 4: Deletion without --force, user input 'N' ---"
# Recreate old files
touch -d "40 days ago" "$TEST_DIR/old_file_3.dat"
touch -d "45 days ago" "$TEST_DIR/old_file_4.tmp"

# Mock rationale: Pipe 'N' to stdin to simulate user declining deletion.
OUTPUT=$(echo "N" | bash "$SCRIPT_TO_TEST" -d "$TEST_DIR" -a 30)

if echo "$OUTPUT" | grep -q "Salvage aborted. The relics remain, for now."; then
    echo "Test 4 Passed: Correctly aborted deletion."
else
    echo "Test 4 FAILED: Abort output incorrect."
    echo "$OUTPUT"
    exit 1
fi

# Verify files still exist
if [ -f "$TEST_DIR/old_file_3.dat" ] && [ -f "$TEST_DIR/old_file_4.tmp" ]; then
    echo "Test 4 Passed: Files still exist after abort."
else
    echo "Test 4 FAILED: Files were unexpectedly deleted after abort."
    ls -l "$TEST_DIR"
    exit 1
fi

echo "All tests completed successfully!"
