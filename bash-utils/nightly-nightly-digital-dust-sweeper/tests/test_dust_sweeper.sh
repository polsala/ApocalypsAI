#!/bin/bash

# Mock rationale:
# We need to test the script's logic without actually modifying the user's filesystem.
# We create a temporary test environment with specific files and directories.
# We then run the script against this controlled environment and assert its output
# and the state of the temporary filesystem.
# 'find', 'mkdir', 'mv', 'rmdir' are standard commands whose behavior is predictable
# within a controlled environment, so they don't need explicit mocking beyond
# operating on temporary paths.

set -euo pipefail

TEST_DIR=$(mktemp -d -t dust-sweeper-test-XXXXXX)
SCRIPT_PATH="$(dirname "$0")"/../src/dust_sweeper.sh

cleanup() {
    echo "Cleaning up test directory: $TEST_DIR"
    rm -rf "$TEST_DIR"
}

trap cleanup EXIT

echo "Running tests in $TEST_DIR"

# Test 1: Dry run - find old files and empty directories
echo "--- Test 1: Dry run, find old files and empty directories ---"
TEST_ROOT="$TEST_DIR/test1"
mkdir -p "$TEST_ROOT/sub/empty_dir"
mkdir -p "$TEST_ROOT/sub/another_empty"
echo "old content" > "$TEST_ROOT/old_file.log"
echo "recent content" > "$TEST_ROOT/recent_file.txt"
echo "another old" > "$TEST_ROOT/sub/another_old.tmp"

# Set modification times using GNU date syntax
touch -d "91 days ago" "$TEST_ROOT/old_file.log"
touch -d "91 days ago" "$TEST_ROOT/sub/another_old.tmp"
touch -d "10 days ago" "$TEST_ROOT/recent_file.txt"

OUTPUT=$(bash "$SCRIPT_PATH" -d "$TEST_ROOT" -a 90)

if echo "$OUTPUT" | grep -q "Found: $TEST_ROOT/old_file.log" && \
   echo "$OUTPUT" | grep -q "Found: $TEST_ROOT/sub/another_old.tmp" && \
   ! echo "$OUTPUT" | grep -q "Found: $TEST_ROOT/recent_file.txt" && \
   echo "$OUTPUT" | grep -q "Found: $TEST_ROOT/sub/empty_dir" && \
   echo "$OUTPUT" | grep -q "Found: $TEST_ROOT/sub/another_empty" && \
   echo "$OUTPUT" | grep -q "Mode: Dry Run"; then
    echo "Test 1 PASSED: Correctly identified old files and empty directories in dry run."
else
    echo "Test 1 FAILED: Dry run did not identify files/dirs correctly."
    echo "Output:"
    echo "$OUTPUT"
    exit 1
fi

# Test 2: Sweep mode - move old files and remove empty directories
echo "--- Test 2: Sweep mode, move old files and remove empty directories ---"
TEST_ROOT="$TEST_DIR/test2"
COMPOST_HEAP="$TEST_ROOT/digital_compost_heap"
mkdir -p "$TEST_ROOT/sub/empty_dir"
mkdir -p "$TEST_ROOT/sub/another_empty"
echo "old content" > "$TEST_ROOT/old_file.log"
echo "recent content" > "$TEST_ROOT/recent_file.txt"
echo "another old" > "$TEST_ROOT/sub/another_old.tmp"

touch -d "91 days ago" "$TEST_ROOT/old_file.log"
touch -d "91 days ago" "$TEST_ROOT/sub/another_old.tmp"
touch -d "10 days ago" "$TEST_ROOT/recent_file.txt"

OUTPUT=$(bash "$SCRIPT_PATH" -d "$TEST_ROOT" -a 90 -s -c "$COMPOST_HEAP")

if echo "$OUTPUT" | grep -q "Mode: SWEEPING!" && \
   [ ! -f "$TEST_ROOT/old_file.log" ] && \
   [ ! -f "$TEST_ROOT/sub/another_old.tmp" ] && \
   [ -f "$TEST_ROOT/recent_file.txt" ] && \
   [ -f "$COMPOST_HEAP/old_file.log" ] && \
   [ -f "$COMPOST_HEAP/sub/another_old.tmp" ] && \
   [ ! -d "$TEST_ROOT/sub/empty_dir" ] && \
   [ ! -d "$TEST_ROOT/sub/another_empty" ]; then
    echo "Test 2 PASSED: Correctly moved old files and removed empty directories in sweep mode."
else
    echo "Test 2 FAILED: Sweep mode did not function correctly."
    echo "Output:"
    echo "$OUTPUT"
    ls -R "$TEST_ROOT"
    exit 1
fi

# Test 3: No old files or empty directories
echo "--- Test 3: No old files or empty directories ---"
TEST_ROOT="$TEST_DIR/test3"
mkdir -p "$TEST_ROOT/sub/not_empty"
echo "content" > "$TEST_ROOT/sub/not_empty/file.txt"
echo "recent content" > "$TEST_ROOT/recent_file.txt"

touch -d "10 days ago" "$TEST_ROOT/recent_file.txt"
touch -d "10 days ago" "$TEST_ROOT/sub/not_empty/file.txt"

OUTPUT=$(bash "$SCRIPT_PATH" -d "$TEST_ROOT" -a 90)

if echo "$OUTPUT" | grep -q "No ancient scrolls found" && \
   echo "$OUTPUT" | grep -q "No forgotten chambers found"; then
    echo "Test 3 PASSED: Correctly reported no dust bunnies."
else
    echo "Test 3 FAILED: Did not correctly report no dust bunnies."
    echo "Output:"
    echo "$OUTPUT"
    exit 1
fi

# Test 4: Invalid target directory
echo "--- Test 4: Invalid target directory ---"
OUTPUT=$(bash "$SCRIPT_PATH" -d "$TEST_DIR/non_existent_dir" 2>&1 || true) # Capture stderr and prevent script exit

if echo "$OUTPUT" | grep -q "Error: Target directory '$TEST_DIR/non_existent_dir' does not exist."; then
    echo "Test 4 PASSED: Handled invalid target directory gracefully."
else
    echo "Test 4 FAILED: Did not handle invalid target directory."
    echo "Output:"
    echo "$OUTPUT"
    exit 1
fi

echo "All tests passed!"
