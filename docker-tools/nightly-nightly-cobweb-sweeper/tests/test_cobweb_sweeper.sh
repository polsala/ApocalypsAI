#!/bin/bash

set -euo pipefail

IMAGE_NAME="nightly-cobweb-sweeper-test"
TEST_DIR="temp_cobweb_test_dir"
REPORT_FILE="cobweb_report.txt"

# Mock rationale: We are testing the Docker image and its scanner script.
# The "mocking" is done by creating a controlled, deterministic filesystem
# within a temporary directory that the Docker container will scan.
# Docker commands (build, run) are the core functionality being tested,
# so they are executed directly.

cleanup() {
    echo "Cleaning up..."
    docker rmi "$IMAGE_NAME" || true
    rm -rf "$TEST_DIR"
    rm -f "$REPORT_FILE"
}

trap cleanup EXIT

echo "--- Starting Cobweb Sweeper Tests ---"

# 1. Build the Docker image
echo "Building Docker image: $IMAGE_NAME"
docker build -t "$IMAGE_NAME" . > /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Docker image build failed."
    exit 1
fi
echo "Docker image built successfully."

# 2. Create a temporary test directory with various "cobwebs"
echo "Creating test directory: $TEST_DIR"
mkdir -p "$TEST_DIR/subdir1"
mkdir -p "$TEST_DIR/subdir2/empty"
touch "$TEST_DIR/file.txt"
touch "$TEST_DIR/temp_file.tmp"
touch "$TEST_DIR/backup_file.bak"
touch "$TEST_DIR/emacs_backup~"
touch "$TEST_DIR/.#vim_swap_file"
touch "$TEST_DIR/empty_file.log" # Empty file
echo "some content" > "$TEST_DIR/legit_file.md"
echo "API_KEY=supersecret" > "$TEST_DIR/.env"
touch "$TEST_DIR/id_rsa"

# Create a large file (15MB)
dd if=/dev/zero of="$TEST_DIR/large_artifact.bin" bs=1M count=15 > /dev/null 2>&1

# Create an empty directory
mkdir "$TEST_DIR/empty_dir"

echo "Test directory populated."

# 3. Run the container and capture output
echo "Running cobweb sweeper container..."
docker run --rm -v "$(pwd)/$TEST_DIR:/scan_target" "$IMAGE_NAME" > "$REPORT_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Docker container run failed."
    cat "$REPORT_FILE"
    exit 1
fi
echo "Container run complete. Report saved to $REPORT_FILE."

# 4. Assert findings
echo "Asserting findings..."

# Expected cobwebs
EXPECTED_COBWEBS=(
    "TEMP: /scan_target/temp_file.tmp"
    "TEMP: /scan_target/backup_file.bak"
    "TEMP: /scan_target/emacs_backup~"
    "TEMP: /scan_target/.#vim_swap_file"
    "EMPTY: /scan_target/empty_file.log"
    "EMPTY_DIR: /scan_target/empty_dir"
    "EMPTY_DIR: /scan_target/subdir2/empty"
    "LARGE: /scan_target/large_artifact.bin (15.00 MB)"
    "SENSITIVE: /scan_target/.env"
    "SENSITIVE: /scan_target/id_rsa"
)

for cobweb in "${EXPECTED_COBWEBS[@]}"; do
    if ! grep -qF "$cobweb" "$REPORT_FILE"; then
        echo "FAIL: Expected cobweb not found: '$cobweb'"
        cat "$REPORT_FILE"
        exit 1
    fi
    echo "PASS: Found expected cobweb: '$cobweb'"
done

# Ensure legitimate files are NOT flagged
UNEXPECTED_FINDINGS=(
    "TEMP: /scan_target/file.txt"
    "TEMP: /scan_target/legit_file.md"
    "EMPTY: /scan_target/file.txt"
    "LARGE: /scan_target/file.txt"
    "SENSITIVE: /scan_target/file.txt"
    "SENSITIVE: /scan_target/legit_file.md"
)

for finding in "${UNEXPECTED_FINDINGS[@]}"; do
    if grep -qF "$finding" "$REPORT_FILE"; then
        echo "FAIL: Unexpected finding flagged: '$finding'"
        cat "$REPORT_FILE"
        exit 1
    fi
    echo "PASS: Did not flag unexpected finding: '$finding'"
done

# Test with MAX_FILE_SIZE_MB environment variable
echo "Testing MAX_FILE_SIZE_MB environment variable..."
docker run --rm -e MAX_FILE_SIZE_MB=20 -v "$(pwd)/$TEST_DIR:/scan_target" "$IMAGE_NAME" > "$REPORT_FILE" 2>&1
if grep -qF "LARGE: /scan_target/large_artifact.bin" "$REPORT_FILE"; then
    echo "FAIL: Large file flagged when it shouldn't be with MAX_FILE_SIZE_MB=20."
    cat "$REPORT_FILE"
    exit 1
fi
echo "PASS: Large file not flagged with MAX_FILE_SIZE_MB=20."

# Test with EXCLUDE_PATTERNS environment variable
echo "Testing EXCLUDE_PATTERNS environment variable..."
docker run --rm -e EXCLUDE_PATTERNS="/scan_target/temp_file.tmp,/scan_target/large_artifact.bin" -v "$(pwd)/$TEST_DIR:/scan_target" "$IMAGE_NAME" > "$REPORT_FILE" 2>&1

# Check that excluded items are NOT found
if grep -qF "TEMP: /scan_target/temp_file.tmp" "$REPORT_FILE"; then
    echo "FAIL: Excluded temp_file.tmp was still flagged."
    cat "$REPORT_FILE"
    exit 1
fi
echo "PASS: Excluded temp_file.tmp was not flagged."

if grep -qF "LARGE: /scan_target/large_artifact.bin" "$REPORT_FILE"; then
    echo "FAIL: Excluded large_artifact.bin was still flagged."
    cat "$REPORT_FILE"
    exit 1
fi
echo "PASS: Excluded large_artifact.bin was not flagged."

# Check that a non-excluded item IS found
if ! grep -qF "TEMP: /scan_target/backup_file.bak" "$REPORT_FILE"; then
    echo "FAIL: Non-excluded backup_file.bak was not flagged."
    cat "$REPORT_FILE"
    exit 1
fi
echo "PASS: Non-excluded backup_file.bak was flagged."


echo "All assertions passed!"
echo "--- Cobweb Sweeper Tests Complete ---"
