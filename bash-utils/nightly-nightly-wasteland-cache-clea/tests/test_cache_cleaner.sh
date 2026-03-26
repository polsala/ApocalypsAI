#!/bin/bash

# Mock rationale:
# - Using mktemp -d to create a temporary, isolated test directory.
# - Using touch -t to set specific modification times for files, simulating age.
# - Using dd if=/dev/zero of=... bs=... count=... to create files of specific sizes.
# - Redirecting script output to a temporary file for assertion.
# - Using grep and wc -l to count and verify expected output.
# - Using test -f to verify file existence after operations.

TEST_DIR=$(mktemp -d)
SCRIPT_PATH="./src/cache_cleaner.sh"
OUTPUT_FILE=$(mktemp)

cleanup() {
    rm -rf "$TEST_DIR"
    rm -f "$OUTPUT_FILE"
}
trap cleanup EXIT

echo "Running tests for Wasteland Cache Cleaner..."

# Test 1: No files found (empty directory)
echo "Test 1: Empty directory"
"$SCRIPT_PATH" "$TEST_DIR" > "$OUTPUT_FILE"
if grep -q "No forgotten relics or resource hogs found" "$OUTPUT_FILE"; then
    echo "  PASS: Empty directory correctly reported no files."
else
    echo "  FAIL: Empty directory test failed."
    cat "$OUTPUT_FILE"
    exit 1
fi

# Create mock files for further tests
# File 1: Old, small
touch -t 202301010000 "$TEST_DIR/old_small_relic.txt"
echo "small content" > "$TEST_DIR/old_small_relic.txt" # Ensure it's not empty
# File 2: Old, large (150MB)
touch -t 202301010000 "$TEST_DIR/old_large_hog.bin"
dd if=/dev/zero of="$TEST_DIR/old_large_hog.bin" bs=1M count=150 2>/dev/null
# File 3: Recent, small
touch -t 202406010000 "$TEST_DIR/recent_small_item.txt"
echo "recent content" > "$TEST_DIR/recent_small_item.txt"
# File 4: Recent, large (50MB)
touch -t 202406010000 "$TEST_DIR/recent_large_data.bin"
dd if=/dev/zero of="$TEST_DIR/recent_large_data.bin" bs=1M count=50 2>/dev/null

# Test 2: List old files (default threshold 30d)
echo "Test 2: List old files (default threshold)"
"$SCRIPT_PATH" "$TEST_DIR" --mode old > "$OUTPUT_FILE"
if grep -q "old_small_relic.txt" "$OUTPUT_FILE" && \
   grep -q "old_large_hog.bin" "$OUTPUT_FILE" && \
   ! grep -q "recent_small_item.txt" "$OUTPUT_FILE" && \
   ! grep -q "recent_large_data.bin" "$OUTPUT_FILE" && \
   grep -q "Found 2 items" "$OUTPUT_FILE"; then
    echo "  PASS: Listed correct old files with default threshold."
else
    echo "  FAIL: Listing old files (default threshold) failed."
    cat "$OUTPUT_FILE"
    exit 1
fi

# Test 3: List large files (default threshold 100M)
echo "Test 3: List large files (default threshold)"
"$SCRIPT_PATH" "$TEST_DIR" --mode large > "$OUTPUT_FILE"
if grep -q "old_large_hog.bin" "$OUTPUT_FILE" && \
   ! grep -q "old_small_relic.txt" "$OUTPUT_FILE" && \
   ! grep -q "recent_small_item.txt" "$OUTPUT_FILE" && \
   ! grep -q "recent_large_data.bin" "$OUTPUT_FILE" && \
   grep -q "Found 1 items" "$OUTPUT_FILE"; then
    echo "  PASS: Listed correct large files with default threshold."
else
    echo "  FAIL: Listing large files (default threshold) failed."
    cat "$OUTPUT_FILE"
    exit 1
fi

# Test 4: List old files with custom threshold (e.g., 1000d, should find nothing recent)
echo "Test 4: List old files with custom threshold (1000d)"
"$SCRIPT_PATH" "$TEST_DIR" --mode old --threshold 1000d > "$OUTPUT_FILE"
if grep -q "No forgotten relics or resource hogs found" "$OUTPUT_FILE"; then
    echo "  PASS: Listed no files with a very high age threshold."
else
    echo "  FAIL: Listing old files with custom threshold failed."
    cat "$OUTPUT_FILE"
    exit 1
fi

# Test 5: List large files with custom threshold (e.g., 20M, should find both large files)
echo "Test 5: List large files with custom threshold (20M)"
"$SCRIPT_PATH" "$TEST_DIR" --mode large --threshold 20M > "$OUTPUT_FILE"
if grep -q "old_large_hog.bin" "$OUTPUT_FILE" && \
   grep -q "recent_large_data.bin" "$OUTPUT_FILE" && \
   grep -q "Found 2 items" "$OUTPUT_FILE"; then
    echo "  PASS: Listed correct large files with custom threshold."
else
    echo "  FAIL: Listing large files with custom threshold failed."
    cat "$OUTPUT_FILE"
    exit 1
fi

# Test 6: Delete old files
echo "Test 6: Delete old files"
"$SCRIPT_PATH" "$TEST_DIR" --mode old --threshold 30d --action delete > "$OUTPUT_FILE"
if grep -q "Purged 2 items" "$OUTPUT_FILE" && \
   ! test -f "$TEST_DIR/old_small_relic.txt" && \
   ! test -f "$TEST_DIR/old_large_hog.bin" && \
   test -f "$TEST_DIR/recent_small_item.txt" && \
   test -f "$TEST_DIR/recent_large_data.bin"; then
    echo "  PASS: Deleted old files correctly."
else
    echo "  FAIL: Deleting old files failed."
    cat "$OUTPUT_FILE"
    ls -l "$TEST_DIR"
    exit 1
fi

# Re-create old files for next delete test
touch -t 202301010000 "$TEST_DIR/old_small_relic.txt"
echo "small content" > "$TEST_DIR/old_small_relic.txt"
touch -t 202301010000 "$TEST_DIR/old_large_hog.bin"
dd if=/dev/zero of="$TEST_DIR/old_large_hog.bin" bs=1M count=150 2>/dev/null

# Test 7: Delete large files
echo "Test 7: Delete large files"
"$SCRIPT_PATH" "$TEST_DIR" --mode large --threshold 20M --action delete > "$OUTPUT_FILE"
if grep -q "Purged 3 items" "$OUTPUT_FILE" && \
   ! test -f "$TEST_DIR/old_small_relic.txt" && \
   ! test -f "$TEST_DIR/old_large_hog.bin" && \
   ! test -f "$TEST_DIR/recent_large_data.bin" && \
   test -f "$TEST_DIR/recent_small_item.txt"; then
    echo "  PASS: Deleted large files correctly."
else
    echo "  FAIL: Deleting large files failed."
    cat "$OUTPUT_FILE"
    ls -l "$TEST_DIR"
    exit 1
fi

echo "All tests completed."
