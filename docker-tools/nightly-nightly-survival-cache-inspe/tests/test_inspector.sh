#!/bin/bash

set -euo pipefail

IMAGE_NAME="nightly-survival-cache-inspector-test"
TEST_DIR="$(mktemp -d)"

cleanup() {
    echo "Cleaning up..."
    rm -rf "$TEST_DIR"
    docker rmi "$IMAGE_NAME" || true # Ignore error if image wasn't built
}

trap cleanup EXIT

echo "Building Docker image..."
docker build -t "$IMAGE_NAME" . > /dev/null

# Mock rationale: Create dummy archive files locally to serve as deterministic inputs for the containerized utility.

# --- Test Case 1: Tar GZ archive ---
echo "\n--- Running Test Case 1: Tar GZ archive ---"

# Create a dummy tar.gz file
cd "$TEST_DIR"
mkdir -p "tar_cache"
echo "Hello from tar!" > "tar_cache/file1.txt"
echo "Another file." > "tar_cache/subdir/file2.log"
mkdir -p "tar_cache/subdir"
tar -czf "test_cache.tar.gz" -C "tar_cache" .

ARCHIVE_PATH="$TEST_DIR/test_cache.tar.gz"

# Get expected SHA256 sum of the dummy archive
EXPECTED_SHA256_TAR=$(sha256sum "$ARCHIVE_PATH" | awk '{print $1}')

OUTPUT_TAR=$(docker run --rm -v "$ARCHIVE_PATH":/mnt/cache/test_cache.tar.gz "$IMAGE_NAME" /mnt/cache/test_cache.tar.gz)

if echo "$OUTPUT_TAR" | grep -q "$EXPECTED_SHA256_TAR" && \
   echo "$OUTPUT_TAR" | grep -q "file1.txt" && \
   echo "$OUTPUT_TAR" | grep -q "subdir/file2.log"; then
    echo "Test Case 1 (Tar GZ) PASSED."
else
    echo "Test Case 1 (Tar GZ) FAILED."
    echo "Output:"
    echo "$OUTPUT_TAR"
    exit 1
fi

# --- Test Case 2: Zip archive ---
echo "\n--- Running Test Case 2: Zip archive ---"

# Create a dummy zip file
rm -rf "tar_cache" # Clean up previous dummy files
mkdir -p "zip_cache"
echo "Hello from zip!" > "zip_cache/document.txt"
echo "Secret data." > "zip_cache/secret.dat"
zip -j "test_cache.zip" "zip_cache/document.txt" "zip_cache/secret.dat" > /dev/null

ARCHIVE_PATH="$TEST_DIR/test_cache.zip"

# Get expected SHA256 sum of the dummy archive
EXPECTED_SHA256_ZIP=$(sha256sum "$ARCHIVE_PATH" | awk '{print $1}')

OUTPUT_ZIP=$(docker run --rm -v "$ARCHIVE_PATH":/mnt/cache/test_cache.zip "$IMAGE_NAME" /mnt/cache/test_cache.zip)

if echo "$OUTPUT_ZIP" | grep -q "$EXPECTED_SHA256_ZIP" && \
   echo "$OUTPUT_ZIP" | grep -q "document.txt" && \
   echo "$OUTPUT_ZIP" | grep -q "secret.dat"; then
    echo "Test Case 2 (Zip) PASSED."
else
    echo "Test Case 2 (Zip) FAILED."
    echo "Output:"
    echo "$OUTPUT_ZIP"
    exit 1
fi

# --- Test Case 3: Non-existent archive ---
echo "\n--- Running Test Case 3: Non-existent archive ---"

NON_EXISTENT_PATH="$TEST_DIR/non_existent.tar.gz"
OUTPUT_NON_EXISTENT=$(docker run --rm -v "$NON_EXISTENT_PATH":/mnt/cache/non_existent.tar.gz "$IMAGE_NAME" /mnt/cache/non_existent.tar.gz 2>&1 || true)

if echo "$OUTPUT_NON_EXISTENT" | grep -q "Error: Archive not found at '/mnt/cache/non_existent.tar.gz'"; then
    echo "Test Case 3 (Non-existent archive) PASSED."
else
    echo "Test Case 3 (Non-existent archive) FAILED."
    echo "Output:"
    echo "$OUTPUT_NON_EXISTENT"
    exit 1
fi

echo "\nAll tests completed successfully!"
