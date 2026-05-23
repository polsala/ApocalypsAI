#!/bin/bash

# Test suite for Nightly Digital Dust Bunny Collector

# --- Test Setup ---
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
ARCHIVE_TEST_DIR=$(mktemp -d -t dust-bunny-archive-XXXXXX)
SCRIPT_PATH="./src/dust_bunny_collector.sh"

# Mock rationale: We create a controlled temporary file system environment
# to simulate various scenarios for the script. This allows deterministic
# and offline testing without affecting the actual system.
# `mkdir`, `touch`, `dd`, `rm`, `tar`, `find`, `grep`, `wc`, `diff` are
# standard shell utilities used to set up the test environment and verify
# the script's output and side effects.

# Ensure the script is executable
chmod +x "$SCRIPT_PATH"

# Function to clean up test environment
cleanup() {
    echo "Cleaning up test environment..."
    rm -rf "$TEST_DIR" "$ARCHIVE_TEST_DIR"
}

# Register cleanup function to run on exit
trap cleanup EXIT

# Function to create a dummy file with specific size and age
create_dummy_file() {
    local path="$1"
    local size_mb="$2"
    local age_days="$3"

    # Create a file of specified size
    dd if=/dev/zero of="$path" bs=1M count="$size_mb" 2>/dev/null

    # Set modification time to simulate age
    # Using `date` command to calculate past date
    local past_date=$(date -d "$age_days days ago" +%Y%m%d%H%M.%S)
    touch -m -t "$past_date" "$path"
}

# --- Test Cases ---

echo "Starting tests for Nightly Digital Dust Bunny Collector..."

# Test 1: No dust bunnies found
echo -e "\n--- Test 1: No dust bunnies found ---"
OUTPUT=$( "$SCRIPT_PATH" "$TEST_DIR" 1 1 report )
if echo "$OUTPUT" | grep -q "No digital dust bunnies found"; then
    echo "Test 1 PASSED: Correctly reported no dust bunnies."
else
    echo "Test 1 FAILED: Expected 'No digital dust bunnies found', got:"
    echo "$OUTPUT"
    exit 1
fi

# Test 2: Report action - find old, large files
echo -e "\n--- Test 2: Report action - find old, large files ---"
create_dummy_file "$TEST_DIR/old_large_file_1.log" 5 30 # 5MB, 30 days old
create_dummy_file "$TEST_DIR/old_large_file_2.tmp" 10 45 # 10MB, 45 days old
create_dummy_file "$TEST_DIR/old_small_file.txt" 1 30   # 1MB, 30 days old (should be ignored by size)
create_dummy_file "$TEST_DIR/new_large_file.data" 20 1  # 20MB, 1 day old (should be ignored by age)

OUTPUT=$( "$SCRIPT_PATH" "$TEST_DIR" 15 3 report ) # Older than 15 days, larger than 3MB
if echo "$OUTPUT" | grep -q "old_large_file_1.log" && \
   echo "$OUTPUT" | grep -q "old_large_file_2.tmp" && \
   ! echo "$OUTPUT" | grep -q "old_small_file.txt" && \
   ! echo "$OUTPUT" | grep -q "new_large_file.data"; then
    echo "Test 2 PASSED: Correctly identified and reported relevant dust bunnies."
else
    echo "Test 2 FAILED: Incorrectly reported files. Output:"
    echo "$OUTPUT"
    exit 1
fi

# Test 3: Delete action - remove old, large files
echo -e "\n--- Test 3: Delete action - remove old, large files ---"
# Create new set of files for deletion test
rm -f "$TEST_DIR"/* # Clean up previous test files
create_dummy_file "$TEST_DIR/to_delete_1.bak" 7 20
create_dummy_file "$TEST_DIR/to_delete_2.log" 12 25
create_dummy_file "$TEST_DIR/keep_small.txt" 2 20
create_dummy_file "$TEST_DIR/keep_new.data" 15 5

"$SCRIPT_PATH" "$TEST_DIR" 10 5 delete # Older than 10 days, larger than 5MB

if [ ! -f "$TEST_DIR/to_delete_1.bak" ] && \
   [ ! -f "$TEST_DIR/to_delete_2.log" ] && \
   [ -f "$TEST_DIR/keep_small.txt" ] && \
   [ -f "$TEST_DIR/keep_new.data" ]; then
    echo "Test 3 PASSED: Correctly deleted specified dust bunnies and kept others."
else
    echo "Test 3 FAILED: Deletion was incorrect. Files remaining:"
    ls -l "$TEST_DIR"
    exit 1
fi

# Test 4: Archive action - archive old, large files
echo -e "\n--- Test 4: Archive action - archive old, large files ---"
# Create new set of files for archiving test
rm -f "$TEST_DIR"/* # Clean up previous test files
create_dummy_file "$TEST_DIR/to_archive_1.old" 8 40
create_dummy_file "$TEST_DIR/to_archive_2.dump" 11 35
create_dummy_file "$TEST_DIR/keep_small_archive.txt" 3 40
create_dummy_file "$TEST_DIR/keep_new_archive.data" 10 2

"$SCRIPT_PATH" "$TEST_DIR" 30 5 archive "$ARCHIVE_TEST_DIR" # Older than 30 days, larger than 5MB

# Check if archive file was created
ARCHIVE_FILE=$(find "$ARCHIVE_TEST_DIR" -name "dust_bunnies_*.tar.gz" | head -n 1)
if [ -f "$ARCHIVE_FILE" ]; then
    echo "Archive file created: $ARCHIVE_FILE"
    # Check if original files were deleted
    if [ ! -f "$TEST_DIR/to_archive_1.old" ] && \
       [ ! -f "$TEST_DIR/to_archive_2.dump" ] && \
       [ -f "$TEST_DIR/keep_small_archive.txt" ] && \
       [ -f "$TEST_DIR/keep_new_archive.data" ]; then
        echo "Test 4 PASSED: Correctly archived specified dust bunnies and deleted originals."
    else
        echo "Test 4 FAILED: Original files not deleted correctly after archiving. Files remaining:"
        ls -l "$TEST_DIR"
        exit 1
    fi
    # Optionally, check archive content (more complex for bash, but possible)
    # tar -tf "$ARCHIVE_FILE" | grep -q "to_archive_1.old" && tar -tf "$ARCHIVE_FILE" | grep -q "to_archive_2.dump"
else
    echo "Test 4 FAILED: Archive file not created."
    exit 1
fi

# Test 5: Invalid directory
echo -e "\n--- Test 5: Invalid directory ---"
OUTPUT=$( "$SCRIPT_PATH" "/non/existent/dir" 1 1 report 2>&1 )
if echo "$OUTPUT" | grep -q "Error: Directory '/non/existent/dir' not found"; then
    echo "Test 5 PASSED: Correctly handled invalid directory."
else
    echo "Test 5 FAILED: Did not handle invalid directory correctly. Output:"
    echo "$OUTPUT"
    exit 1
fi

# Test 6: Invalid action
echo -e "\n--- Test 6: Invalid action ---"
OUTPUT=$( "$SCRIPT_PATH" "$TEST_DIR" 1 1 invalid_action 2>&1 )
if echo "$OUTPUT" | grep -q "Error: Invalid action 'invalid_action'"; then
    echo "Test 6 PASSED: Correctly handled invalid action."
else
    echo "Test 6 FAILED: Did not handle invalid action correctly. Output:"
    echo "$OUTPUT"
    exit 1
fi

echo -e "\nAll tests completed."
