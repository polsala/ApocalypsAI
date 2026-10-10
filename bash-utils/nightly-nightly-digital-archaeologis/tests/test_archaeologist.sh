#!/bin/bash

# Mock rationale: We need to create a controlled environment with specific file ages and sizes
# to test the script's filtering logic without relying on the actual filesystem state.
# This involves creating temporary files and directories, and setting their modification times.

set -euo pipefail

SCRIPT_PATH="./src/archaeologist.sh"
TEST_DIR="test_artifacts"
REPORT_FILE="archaeology_report.txt"

# Cleanup function
cleanup() {
    rm -rf "$TEST_DIR" "$REPORT_FILE"
}

# Ensure cleanup runs on exit
trap cleanup EXIT

echo "Running tests for Nightly Digital Archaeologist..."

# Test 1: No artifacts found
echo "Test 1: No artifacts found (empty directory)"
cleanup
mkdir -p "$TEST_DIR"
"$SCRIPT_PATH" -d "$TEST_DIR" -a 0 -s 0 > "$REPORT_FILE"
if grep -q "ARTIFACT FOUND" "$REPORT_FILE"; then
    echo "FAIL: Test 1 - Found artifacts in empty directory."
    cat "$REPORT_FILE"
    exit 1
fi
echo "PASS: Test 1"

# Test 2: Find an old, large artifact
echo "Test 2: Find an old, large artifact"
cleanup
mkdir -p "$TEST_DIR"
# Create a file that is 2 days old and 150MB
# Attempt macOS specific date command first (BSD date)
if ! touch -t "$(date -v-2d +%Y%m%d%H%M.%S)" "$TEST_DIR/ancient_scroll.log" 2>/dev/null; then
    # Fallback to GNU/Linux specific date command
    touch -d "2 days ago" "$TEST_DIR/ancient_scroll.log"
fi
truncate -s 150M "$TEST_DIR/ancient_scroll.log"

# Create a recent, small file (should not be found)
touch "$TEST_DIR/recent_note.txt"
truncate -s 10K "$TEST_DIR/recent_note.txt"

# Run with criteria: older than 1 day, larger than 100MB
"$SCRIPT_PATH" -d "$TEST_DIR" -a 1 -s 100 > "$REPORT_FILE"

if ! grep -q "ARTIFACT FOUND.*ancient_scroll.log" "$REPORT_FILE"; then
    echo "FAIL: Test 2 - Did not find expected ancient_scroll.log."
    cat "$REPORT_FILE"
    exit 1
fi
if grep -q "ARTIFACT FOUND.*recent_note.txt" "$REPORT_FILE"; then
    echo "FAIL: Test 2 - Found unexpected recent_note.txt."
    cat "$REPORT_FILE"
    exit 1
fi
echo "PASS: Test 2"

# Test 3: Find multiple artifacts
echo "Test 3: Find multiple artifacts"
cleanup
mkdir -p "$TEST_DIR/sub_dir"
# Artifact 1: 3 days old, 200MB
if ! touch -t "$(date -v-3d +%Y%m%d%H%M.%S)" "$TEST_DIR/old_data.bak" 2>/dev/null; then
    touch -d "3 days ago" "$TEST_DIR/old_data.bak"
fi
truncate -s 200M "$TEST_DIR/old_data.bak"

# Artifact 2: 2 days old, 120MB in a subdir
if ! touch -t "$(date -v-2d +%Y%m%d%H%M.%S)" "$TEST_DIR/sub_dir/forgotten_cache.zip" 2>/dev/null; then
    touch -d "2 days ago" "$TEST_DIR/sub_dir/forgotten_cache.zip"
fi
truncate -s 120M "$TEST_DIR/sub_dir/forgotten_cache.zip"

# Recent, large file (should not be found by age)
touch "$TEST_DIR/new_large_file.iso"
truncate -s 500M "$TEST_DIR/new_large_file.iso"

# Old, small file (should not be found by size)
if ! touch -t "$(date -v-5d +%Y%m%d%H%M.%S)" "$TEST_DIR/tiny_log.txt" 2>/dev/null; then
    touch -d "5 days ago" "$TEST_DIR/tiny_log.txt"
fi
truncate -s 5M "$TEST_DIR/tiny_log.txt"

# Run with criteria: older than 1 day, larger than 100MB
"$SCRIPT_PATH" -d "$TEST_DIR" -a 1 -s 100 > "$REPORT_FILE"

if ! grep -q "ARTIFACT FOUND.*old_data.bak" "$REPORT_FILE"; then
    echo "FAIL: Test 3 - Did not find expected old_data.bak."
    cat "$REPORT_FILE"
    exit 1
fi
if ! grep -q "ARTIFACT FOUND.*forgotten_cache.zip" "$REPORT_FILE"; then
    echo "FAIL: Test 3 - Did not find expected forgotten_cache.zip."
    cat "$REPORT_FILE"
    exit 1
fi
if grep -q "ARTIFACT FOUND.*new_large_file.iso" "$REPORT_FILE"; then
    echo "FAIL: Test 3 - Found unexpected new_large_file.iso."
    cat "$REPORT_FILE"
    exit 1
fi
if grep -q "ARTIFACT FOUND.*tiny_log.txt" "$REPORT_FILE"; then
    echo "FAIL: Test 3 - Found unexpected tiny_log.txt."
    cat "$REPORT_FILE"
    exit 1
fi

# Check count of artifacts found
ARTIFACT_COUNT=$(grep -c "ARTIFACT FOUND" "$REPORT_FILE")
if [[ "$ARTIFACT_COUNT" -ne 2 ]]; then
    echo "FAIL: Test 3 - Expected 2 artifacts, found $ARTIFACT_COUNT."
    cat "$REPORT_FILE"
    exit 1
fi
echo "PASS: Test 3"

# Test 4: Invalid directory
echo "Test 4: Invalid directory"
cleanup
"$SCRIPT_PATH" -d "non_existent_dir" 2> "$REPORT_FILE"
if ! grep -q "Error: Directory 'non_existent_dir' not found." "$REPORT_FILE"; then
    echo "FAIL: Test 4 - Did not report error for invalid directory."
    cat "$REPORT_FILE"
    exit 1
fi
echo "PASS: Test 4"

# Test 5: Invalid age parameter
echo "Test 5: Invalid age parameter"
cleanup
mkdir -p "$TEST_DIR"
"$SCRIPT_PATH" -d "$TEST_DIR" -a "abc" 2> "$REPORT_FILE"
if ! grep -q "Error: Minimum age must be a non-negative integer." "$REPORT_FILE"; then
    echo "FAIL: Test 5 - Did not report error for invalid age."
    cat "$REPORT_FILE"
    exit 1
fi
echo "PASS: Test 5"

# Test 6: Invalid size parameter
echo "Test 6: Invalid size parameter"
cleanup
mkdir -p "$TEST_DIR"
"$SCRIPT_PATH" -d "$TEST_DIR" -s "xyz" 2> "$REPORT_FILE"
if ! grep -q "Error: Minimum size must be a non-negative integer." "$REPORT_FILE"; then
    echo "FAIL: Test 6 - Did not report error for invalid size."
    cat "$REPORT_FILE"
    exit 1
fi
echo "PASS: Test 6"

echo "All tests passed!"
