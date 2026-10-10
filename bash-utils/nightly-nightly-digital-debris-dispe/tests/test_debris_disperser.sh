#!/bin/bash

# Test setup
TEST_DIR=$(mktemp -d)
SCRIPT_PATH="../src/debris_disperser.sh"
ARCHIVE_DIR=".digital_debris_archive"

# Mock rationale: The 'find' command's output depends on the filesystem state and current time,
# which are non-deterministic. Mocking it allows for consistent test results by simulating
# specific file lists and ages without actually creating files with old timestamps.
# This also prevents accidental modification of real files during tests.
MOCKED_FIND_FILES_OUTPUT=""
MOCKED_FIND_EMPTY_DIRS_OUTPUT=""

find() {
    local path="$1"
    local type_arg="$2"
    local type_val="$3"
    local empty_arg="$4" # This will be -empty for empty dirs, or -mtime for files

    if [[ "$type_arg" == "-type" && "$type_val" == "f" ]]; then
        echo "$MOCKED_FIND_FILES_OUTPUT"
    elif [[ "$type_arg" == "-type" && "$type_val" == "d" && "$empty_arg" == "-empty" ]]; then
        echo "$MOCKED_FIND_EMPTY_DIRS_OUTPUT"
    else
        # Fallback for unexpected find calls
        echo ""
    fi
}

# Override mv and rmdir for testing to prevent actual file system changes
mv() {
    echo "MOCKED_MV: $@"
}
rmdir() {
    echo "MOCKED_RMDIR: $@"
}
mkdir() {
    # Allow mkdir to function normally for the archive directory within the test dir
    if [[ "$1" == *"$ARCHIVE_DIR"* ]]; then
        command mkdir "$@"
    else
        echo "MOCKED_MKDIR: $@"
    fi
}

cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Helper function for assertions
assert_contains() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if echo "$actual" | grep -qF "$expected"; then
        echo "PASS: $message"
    else
        echo "FAIL: $message (Expected to contain: '$expected', Actual: '$actual')"
        exit 1
    fi
}

assert_not_contains() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: $message (Expected NOT to contain: '$expected', Actual: '$actual')"
        exit 1
    fi
}

echo "Running tests for Nightly Digital Debris Disperser..."

# Test 1: No debris found
echo "--- Test 1: No debris found ---"
MOCKED_FIND_FILES_OUTPUT=""
MOCKED_FIND_EMPTY_DIRS_OUTPUT=""
OUTPUT=$(cd "$TEST_DIR" && "$SCRIPT_PATH" -p . -a 1)
assert_contains "No ancient digital debris found" "$OUTPUT" "Should report no debris when find is empty"

# Test 2: List mode - files and empty directories
echo "--- Test 2: List mode - files and empty directories ---"
MOCKED_FIND_FILES_OUTPUT="./old_file.txt\n./another_old_file.log"
MOCKED_FIND_EMPTY_DIRS_OUTPUT="./old_dir/empty_dir"
OUTPUT=$(cd "$TEST_DIR" && "$SCRIPT_PATH" -p . -a 30 -m list)
assert_contains "Whispers from the past (files):" "$OUTPUT" "Should list files section"
assert_contains "  - ./old_file.txt" "$OUTPUT" "Should list old_file.txt"
assert_contains "  - ./another_old_file.log" "$OUTPUT" "Should list another_old_file.log"
assert_contains "Echoes of forgotten spaces (empty directories):" "$OUTPUT" "Should list empty dirs section"
assert_contains "  - ./old_dir/empty_dir" "$OUTPUT" "Should list old_dir/empty_dir"
assert_contains "Consider running with '-m move'" "$OUTPUT" "Should suggest move mode"

# Test 3: List mode - only files
echo "--- Test 3: List mode - only files ---"
MOCKED_FIND_FILES_OUTPUT="./only_file.txt"
MOCKED_FIND_EMPTY_DIRS_OUTPUT=""
OUTPUT=$(cd "$TEST_DIR" && "$SCRIPT_PATH" -p . -a 10 -m list)
assert_contains "  - ./only_file.txt" "$OUTPUT" "Should list only_file.txt"
assert_contains "(None)" "$OUTPUT" "Should indicate no empty directories"

# Test 4: List mode - only empty directories
echo "--- Test 4: List mode - only empty directories ---"
MOCKED_FIND_FILES_OUTPUT=""
MOCKED_FIND_EMPTY_DIRS_OUTPUT="./only_empty_dir"
OUTPUT=$(cd "$TEST_DIR" && "$SCRIPT_PATH" -p . -a 5 -m list)
assert_contains "(None)" "$OUTPUT" "Should indicate no files"
assert_contains "  - ./only_empty_dir" "$OUTPUT" "Should list only_empty_dir"

# Test 5: Move mode - files and empty directories
echo "--- Test 5: Move mode - files and empty directories ---"
# Create actual files/dirs for mv/rmdir to operate on (even if mocked, script checks existence)
mkdir -p "$TEST_DIR/old_dir/empty_dir"
touch "$TEST_DIR/old_file.txt"
touch "$TEST_DIR/another_old_file.log"

MOCKED_FIND_FILES_OUTPUT="$TEST_DIR/old_file.txt\n$TEST_DIR/another_old_file.log"
MOCKED_FIND_EMPTY_DIRS_OUTPUT="$TEST_DIR/old_dir/empty_dir"

OUTPUT=$(cd "$TEST_DIR" && "$SCRIPT_PATH" -p . -a 1 -m move)

assert_contains "Preparing the temporal attic at: ./$ARCHIVE_DIR" "$OUTPUT" "Should indicate archive path"
assert_contains "Relocating ancient files to the temporal attic..." "$OUTPUT" "Should indicate file relocation"
assert_contains "MOCKED_MV: $TEST_DIR/old_file.txt $TEST_DIR/$ARCHIVE_DIR/" "$OUTPUT" "Should mock move old_file.txt"
assert_contains "MOCKED_MV: $TEST_DIR/another_old_file.log $TEST_DIR/$ARCHIVE_DIR/" "$OUTPUT" "Should mock move another_old_file.log"
assert_contains "Sweeping away forgotten empty spaces..." "$OUTPUT" "Should indicate empty dir removal"
assert_contains "MOCKED_RMDIR: $TEST_DIR/old_dir/empty_dir" "$OUTPUT" "Should mock rmdir empty_dir"
assert_contains "Digital debris dispersed!" "$OUTPUT" "Should confirm dispersal"

# Clean up files created for Test 5
rm -f "$TEST_DIR/old_file.txt" "$TEST_DIR/another_old_file.log"
rm -rf "$TEST_DIR/old_dir"
rm -rf "$TEST_DIR/$ARCHIVE_DIR" # Remove the archive dir created by mkdir mock

# Test 6: Invalid mode
echo "--- Test 6: Invalid mode ---"
OUTPUT=$(cd "$TEST_DIR" && "$SCRIPT_PATH" -p . -m invalid_mode 2>&1)
assert_contains "Error: Invalid mode 'invalid_mode'. Must be 'list' or 'move'." "$OUTPUT" "Should error on invalid mode"
assert_contains "Usage: $0" "$OUTPUT" "Should show usage on invalid mode"

echo "All tests passed!"
