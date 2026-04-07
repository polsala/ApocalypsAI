#!/bin/bash
set -euo pipefail # Exit on error, unset variables, and pipefail

# Test script for nightly-data-echo-locator

# Set up a temporary directory for testing
TEST_DIR=$(mktemp -d)
SCRIPT_PATH="$(dirname "$0")"/../src/echo_locator.sh

# Ensure cleanup on exit
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

echo "Running tests for nightly-data-echo-locator..."

# Test Case 1: No duplicates
echo "Test Case 1: No duplicates"
mkdir -p "$TEST_DIR/no_dupes"
echo "content1" > "$TEST_DIR/no_dupes/file1.txt"
echo "content2" > "$TEST_DIR/no_dupes/file2.txt"
echo "content3" > "$TEST_DIR/no_dupes/file3.txt"

OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR/no_dupes" 2>&1 | grep -v "Initiating Temporal Data Echo Scan" | grep -v "---")
if [ -z "$OUTPUT" ]; then
    echo "PASS: No duplicates found as expected."
else
    echo "FAIL: Duplicates found when none expected."
    echo "Output: $OUTPUT"
    exit 1
fi

# Test Case 2: With duplicates
echo "Test Case 2: With duplicates"
mkdir -p "$TEST_DIR/with_dupes/subdir" # Ensure subdir exists before cp
echo "duplicate_content" > "$TEST_DIR/with_dupes/fileA.txt"
cp "$TEST_DIR/with_dupes/fileA.txt" "$TEST_DIR/with_dupes/fileB.txt"
echo "unique_content" > "$TEST_DIR/with_dupes/fileC.txt"
cp "$TEST_DIR/with_dupes/fileA.txt" "$TEST_DIR/with_dupes/subdir/fileD.txt"

# Mock rationale: File system operations (mkdir, echo, cp) are deterministic and offline.
# md5sum is a standard utility and its output for a given file is deterministic and offline.

OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR/with_dupes" 2>&1 | grep -v "Initiating Temporal Data Echo Scan" | grep -v "---")

# Expected MD5 hash for "duplicate_content\n"
EXPECTED_MD5="92955523a1059434857500196235123d"

# Check if the output contains the expected duplicate group
if echo "$OUTPUT" | grep -q "$EXPECTED_MD5"; then
    # Further check if all duplicate files are listed and unique file is not
    if echo "$OUTPUT" | grep -q "$TEST_DIR/with_dupes/fileA.txt" && \
       echo "$OUTPUT" | grep -q "$TEST_DIR/with_dupes/fileB.txt" && \
       echo "$OUTPUT" | grep -q "$TEST_DIR/with_dupes/subdir/fileD.txt" && \
       ! echo "$OUTPUT" | grep -q "$TEST_DIR/with_dupes/fileC.txt"; then
        echo "PASS: Duplicates found and reported correctly."
    else
        echo "FAIL: Duplicates reported incorrectly or missing files."
        echo "Output: $OUTPUT"
        exit 1
    fi
else
    echo "FAIL: Expected duplicate MD5 hash not found in output."
    echo "Output: $OUTPUT"
    exit 1
fi

# Test Case 3: Empty directory
echo "Test Case 3: Empty directory"
mkdir -p "$TEST_DIR/empty_dir"
OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR/empty_dir" 2>&1 | grep -v "Initiating Temporal Data Echo Scan" | grep -v "---")
if [ -z "$OUTPUT" ]; then
    echo "PASS: Empty directory handled correctly (no output)."
else
    echo "FAIL: Output found for empty directory."
    echo "Output: $OUTPUT"
    exit 1
fi

# Test Case 4: Invalid directory
echo "Test Case 4: Invalid directory"
OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR/non_existent_dir" 2>&1)
if echo "$OUTPUT" | grep -q "Error: Directory '$TEST_DIR/non_existent_dir' not found."; then
    echo "PASS: Invalid directory handled correctly."
else
    echo "FAIL: Invalid directory not handled as expected."
    echo "Output: $OUTPUT"
    exit 1
fi

echo "All tests completed."
