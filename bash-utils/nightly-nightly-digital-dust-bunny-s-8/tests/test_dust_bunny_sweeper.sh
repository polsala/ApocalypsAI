#!/bin/bash

# Mock rationale:
# We create a temporary directory and populate it with files and directories
# with specific modification times. This allows us to test the script's
# file-finding and deletion logic in an isolated, deterministic, and offline
# manner without affecting the actual filesystem. `find`, `touch`, `rm`, `rmdir`,
# and `grep` commands operate only within this temporary test environment.

TEST_DIR=$(mktemp -d)
SCRIPT_PATH="../src/dust_bunny_sweeper.sh"

# Ensure cleanup on exit
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Create test files and directories with specific modification times
# File older than 30 days
touch -d "31 days ago" "$TEST_DIR/old_file.txt"
# File newer than 30 days
touch -d "10 days ago" "$TEST_DIR/new_file.txt"
# Another old file
touch -d "40 days ago" "$TEST_DIR/another_old_file.log"
# Empty directory older than 30 days
mkdir "$TEST_DIR/old_empty_dir"
touch -d "35 days ago" "$TEST_DIR/old_empty_dir" # Set mtime for dir
# Directory with a new file (should not be removed as it's not empty)
mkdir "$TEST_DIR/dir_with_new_file"
touch -d "5 days ago" "$TEST_DIR/dir_with_new_file/inside_new.txt"
# Directory with an old file (should not be removed as it's not empty)
mkdir "$TEST_DIR/dir_with_old_file"
touch -d "35 days ago" "$TEST_DIR/dir_with_old_file/inside_old.txt"

echo "--- Running Dry Run Test ---"
OUTPUT_DRY_RUN=$("$SCRIPT_PATH" "$TEST_DIR" 30 --dry-run)

# Check if the correct files/dirs are identified in dry run output
if echo "$OUTPUT_DRY_RUN" | grep -q "old_file.txt" && \
   echo "$OUTPUT_DRY_RUN" | grep -q "another_old_file.log" && \
   echo "$OUTPUT_DRY_RUN" | grep -q "old_empty_dir" && \
   ! echo "$OUTPUT_DRY_RUN" | grep -q "new_file.txt" && \
   ! echo "$OUTPUT_DRY_RUN" | grep -q "inside_new.txt" && \
   ! echo "$OUTPUT_DRY_RUN" | grep -q "dir_with_new_file" && \
   ! echo "$OUTPUT_DRY_RUN" | grep -q "inside_old.txt" && \
   ! echo "$OUTPUT_DRY_RUN" | grep -q "dir_with_old_file"; then
    echo "Dry run test PASSED: Correct files/dirs identified."
else
    echo "Dry run test FAILED: Incorrect files/dirs identified."
    echo "Output was:"
    echo "$OUTPUT_DRY_RUN"
    exit 1
fi

# Check if no files/dirs were actually deleted during dry run
if [[ -f "$TEST_DIR/old_file.txt" && -f "$TEST_DIR/new_file.txt" && -d "$TEST_DIR/old_empty_dir" ]]; then
    echo "Dry run test PASSED: No files/dirs deleted during dry run."
else
    echo "Dry run test FAILED: Files/dirs were deleted during dry run."
    exit 1
fi

echo "--- Running Actual Deletion Test ---"
# Run the script, piping 'y' for confirmation to proceed with deletion
OUTPUT_DELETE=$(echo "y" | "$SCRIPT_PATH" "$TEST_DIR" 30)

# Check if old files and empty directories were deleted
if ! [[ -f "$TEST_DIR/old_file.txt" || -f "$TEST_DIR/another_old_file.log" || -d "$TEST_DIR/old_empty_dir" ]]; then
    echo "Deletion test PASSED: Old files and empty dir were deleted."
else
    echo "Deletion test FAILED: Old files or empty dir were NOT deleted."
    ls -l "$TEST_DIR"
    exit 1
fi

# Check if new files and non-empty directories were preserved
if [[ -f "$TEST_DIR/new_file.txt" && -f "$TEST_DIR/dir_with_new_file/inside_new.txt" && -d "$TEST_DIR/dir_with_old_file" && -f "$TEST_DIR/dir_with_old_file/inside_old.txt" ]]; then
    echo "Deletion test PASSED: New files and non-empty dirs were preserved."
else
    echo "Deletion test FAILED: New files or non-empty dirs were NOT preserved."
    ls -l "$TEST_DIR"
    exit 1
fi

echo "All tests PASSED!"
