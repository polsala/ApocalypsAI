#!/bin/bash

# Automated tests for nightly-digital-dust-bunny-sweeper

# Mock rationale: These tests create a temporary, isolated filesystem environment
# to simulate various file ages and sizes. This ensures deterministic results
# without affecting the actual system's /tmp or /var/log directories and provides
# a consistent state for testing the script's logic.

set -euo pipefail

TEST_DIR="$(mktemp -d)"
SCRIPT_PATH="$(dirname "$0")/../src/dust_bunny_sweeper.sh"

cleanup() {
    rm -rf "$TEST_DIR"
}

trap cleanup EXIT

echo "Running tests for dust_bunny_sweeper.sh..."

# Test 1: No dust bunnies found
TEST_NAME="No dust bunnies"
OUTPUT=$(DUST_BUNNY_AGE_DAYS=1 bash "$SCRIPT_PATH" "$TEST_DIR")
if echo "$OUTPUT" | grep -q "No digital dust bunnies found"; then
    echo "✅ $TEST_NAME passed."
else
    echo "❌ $TEST_NAME failed. Output:\n$OUTPUT"
    exit 1
fi

# Test 2: One dust bunny found
TEST_NAME="One dust bunny"
mkdir -p "$TEST_DIR/subdir1"
# Create a file older than 30 days
touch -d "35 days ago" "$TEST_DIR/subdir1/old_file.txt"
# Make it 100 bytes
echo "$(head /dev/urandom | tr -dc A-Za-z0-9_ | head -c 100)" > "$TEST_DIR/subdir1/old_file.txt"

OUTPUT=$(DUST_BUNNY_AGE_DAYS=30 bash "$SCRIPT_PATH" "$TEST_DIR")
if echo "$OUTPUT" | grep -q "Found a colony of 1 digital dust bunnies" && \
   echo "$OUTPUT" | grep -q "old_file.txt"; then
    echo "✅ $TEST_NAME passed."
else
    echo "❌ $TEST_NAME failed. Output:\n$OUTPUT"
    exit 1
fi

# Test 3: Multiple dust bunnies, different sizes and ages
TEST_NAME="Multiple dust bunnies"
mkdir -p "$TEST_DIR/subdir2"
# 100 bytes, 35 days old
touch -d "35 days ago" "$TEST_DIR/subdir2/old_file_small.log"
echo "$(head /dev/urandom | tr -dc A-Za-z-0-9_ | head -c 100)" > "$TEST_DIR/subdir2/old_file_small.log"

# 1000 bytes, 40 days old
touch -d "40 days ago" "$TEST_DIR/subdir2/old_file_medium.dat"
echo "$(head /dev/urandom | tr -dc A-Za-z-0-9_ | head -c 1000)" > "$TEST_DIR/subdir2/old_file_medium.dat"

# 50 bytes, 20 days old (should NOT be a dust bunny with DUST_BUNNY_AGE_DAYS=30)
touch -d "20 days ago" "$TEST_DIR/subdir2/recent_file.tmp"
echo "$(head /dev/urandom | tr -dc A-Za-z-0-9_ | head -c 50)" > "$TEST_DIR/subdir2/recent_file.tmp"

# 2000 bytes, 31 days old
touch -d "31 days ago" "$TEST_DIR/subdir2/old_file_large.bin"
echo "$(head /dev/urandom | tr -dc A-Za-z-0-9_ | head -c 2000)" > "$TEST_DIR/subdir2/old_file_large.bin"

OUTPUT=$(DUST_BUNNY_AGE_DAYS=30 bash "$SCRIPT_PATH" "$TEST_DIR")

# Check count (should be 3: small, medium, large)
if ! echo "$OUTPUT" | grep -q "Found a colony of 3 digital dust bunnies"; then
    echo "❌ $TEST_NAME failed: Incorrect count. Output:\n$OUTPUT"
    exit 1
fi

# Check total size (100 + 1000 + 2000 = 3100 bytes, ~3.0K)
if ! echo "$OUTPUT" | grep -q "weighing in at 3.0KB"; then # numfmt rounds to 1 decimal
    echo "❌ $TEST_NAME failed: Incorrect total size. Output:\n$OUTPUT"
    exit 1
fi

# Check that recent_file.tmp is NOT listed
if echo "$OUTPUT" | grep -q "recent_file.tmp"; then
    echo "❌ $TEST_NAME failed: Recent file incorrectly listed. Output:\n$OUTPUT"
    exit 1
fi

# Check order of top 5 (should be large, medium, small)
if ! echo "$OUTPUT" | grep -E -q ".*old_file_large.bin.*old_file_medium.dat.*old_file_small.log"; then
    echo "❌ $TEST_NAME failed: Incorrect order of top files. Output:\n$OUTPUT"
    exit 1
fi

echo "✅ $TEST_NAME passed."

# Test 4: Custom DUST_BUNNY_AGE_DAYS
TEST_NAME="Custom age threshold"
mkdir -p "$TEST_DIR/subdir3"
# 100 bytes, 5 days old (should be a dust bunny with DUST_BUNNY_AGE_DAYS=4)
touch -d "5 days ago" "$TEST_DIR/subdir3/young_but_stale.txt"
echo "$(head /dev/urandom | tr -dc A-Za-z-0-9_ | head -c 100)" > "$TEST_DIR/subdir3/young_but_stale.txt"

OUTPUT=$(DUST_BUNNY_AGE_DAYS=4 bash "$SCRIPT_PATH" "$TEST_DIR/subdir3")
if echo "$OUTPUT" | grep -q "Found a colony of 1 digital dust bunnies" && \
   echo "$OUTPUT" | grep -q "young_but_stale.txt"; then
    echo "✅ $TEST_NAME passed."
else
    echo "❌ $TEST_NAME failed. Output:\n$OUTPUT"
    exit 1
fi

# Test 5: Handling non-existent directories (should not error)
TEST_NAME="Non-existent directory handling"
OUTPUT=$(DUST_BUNNY_AGE_DAYS=30 bash "$SCRIPT_PATH" "$TEST_DIR/non_existent_dir")
if echo "$OUTPUT" | grep -q "No digital dust bunnies found"; then
    echo "✅ $TEST_NAME passed."
else
    echo "❌ $TEST_NAME failed. Output:\n$OUTPUT"
    exit 1
fi


echo "All tests completed."
