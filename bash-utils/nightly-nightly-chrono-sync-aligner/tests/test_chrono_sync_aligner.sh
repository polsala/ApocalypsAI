#!/bin/bash

# Automated tests for nightly-chrono-sync-aligner

set -euo pipefail

SCRIPT_PATH="$(dirname "$0")"/../src/chrono_sync_aligner.sh

# Create a temporary directory for tests
TEST_ROOT_DIR=$(mktemp -d -t chrono-sync-aligner-test-XXXXXX)

# Mock rationale: We are creating a controlled file system environment
# with specific modification times using 'touch -d' to ensure deterministic
# and offline testing of the script's logic without external dependencies.
# The 'stat' command used by the script will report these precisely set times.

cleanup() {
    echo "Cleaning up temporary directory: $TEST_ROOT_DIR"
    rm -rf "$TEST_ROOT_DIR"
}

trap cleanup EXIT

# Test function for single line output
run_single_line_test() {
    local test_name="$1"
    local expected_output_regex="$2"
    local source_dir="$3"
    local target_dir="$4"

    echo "--- Running Test: $test_name ---"
    output=$(bash "$SCRIPT_PATH" "$source_dir" "$target_dir" 2>&1)
    
    if echo "$output" | grep -Eq "$expected_output_regex"; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        echo "Expected regex: '$expected_output_regex'"
        echo "Actual output:\n$output"
        exit 1
    fi
    echo ""
}

# --- Test Scenarios ---

# Scenario 1: Identical files and times
TEST_DIR_A="$TEST_ROOT_DIR/dir_a_s1"
TEST_DIR_B="$TEST_ROOT_DIR/dir_b_s1"
mkdir -p "$TEST_DIR_A" "$TEST_DIR_B"

touch -d "2023-01-01 10:00:00 UTC" "$TEST_DIR_A/file1.txt"
touch -d "2023-01-01 10:00:00 UTC" "$TEST_DIR_B/file1.txt"

run_single_line_test \
    "Scenario 1: Identical files and times" \
    "^\[ALIGNED\] file1\.txt \(Source: 1672567200, Target: 1672567200\)$" \
    "$TEST_DIR_A" "$TEST_DIR_B"

# Scenario 2: Misaligned times
TEST_DIR_A="$TEST_ROOT_DIR/dir_a_s2"
TEST_DIR_B="$TEST_ROOT_DIR/dir_b_s2"
mkdir -p "$TEST_DIR_A" "$TEST_DIR_B"

touch -d "2023-01-01 10:00:00 UTC" "$TEST_DIR_A/file2.txt"
touch -d "2023-01-01 11:00:00 UTC" "$TEST_DIR_B/file2.txt"

run_single_line_test \
    "Scenario 2: Misaligned times" \
    "^\[MISALIGNED\] file2\.txt \(Source: 1672567200, Target: 1672570800\)$" \
    "$TEST_DIR_A" "$TEST_DIR_B"

# Scenario 3: File missing in target
TEST_DIR_A="$TEST_ROOT_DIR/dir_a_s3"
TEST_DIR_B="$TEST_ROOT_DIR/dir_b_s3"
mkdir -p "$TEST_DIR_A" "$TEST_DIR_B"

touch -d "2023-01-01 10:00:00 UTC" "$TEST_DIR_A/file3.txt"

run_single_line_test \
    "Scenario 3: File missing in target" \
    "^\[MISSING_TARGET\] file3\.txt \(Source: 1672567200\)$" \
    "$TEST_DIR_A" "$TEST_DIR_B"

# Scenario 4: File missing in source
TEST_DIR_A="$TEST_ROOT_DIR/dir_a_s4"
TEST_DIR_B="$TEST_ROOT_DIR/dir_b_s4"
mkdir -p "$TEST_DIR_A" "$TEST_DIR_B"

touch -d "2023-01-01 10:00:00 UTC" "$TEST_DIR_B/file4.txt"

run_single_line_test \
    "Scenario 4: File missing in source" \
    "^\[MISSING_SOURCE\] file4\.txt \(Target: 1672567200\)$" \
    "$TEST_DIR_A" "$TEST_DIR_B"

# Scenario 5: Mixed scenario with subdirectories and spaces in filenames
TEST_DIR_A="$TEST_ROOT_DIR/dir_a_s5"
TEST_DIR_B="$TEST_ROOT_DIR/dir_b_s5"
mkdir -p "$TEST_DIR_A/sub dir" "$TEST_DIR_B/sub dir"

touch -d "2023-01-01 10:00:00 UTC" "$TEST_DIR_A/sub dir/file with spaces.txt"
touch -d "2023-01-01 10:00:00 UTC" "$TEST_DIR_B/sub dir/file with spaces.txt"

touch -d "2023-01-02 10:00:00 UTC" "$TEST_DIR_A/another_file.log"
touch -d "2023-01-02 11:00:00 UTC" "$TEST_DIR_B/another_file.log"

touch -d "2023-01-03 10:00:00 UTC" "$TEST_DIR_A/only_in_a.conf"

touch -d "2023-01-04 10:00:00 UTC" "$TEST_DIR_B/only_in_b.data"

# Expected outputs for Scenario 5 (order might vary, so check for individual lines)
EXPECTED_S5_OUTPUTS=(
    "^\[ALIGNED\] sub dir/file with spaces\.txt \(Source: 1672567200, Target: 1672567200\)$"
    "^\[MISALIGNED\] another_file\.log \(Source: 1672653600, Target: 1672657200\)$"
    "^\[MISSING_TARGET\] only_in_a\.conf \(Source: 1672740000\)$"
    "^\[MISSING_SOURCE\] only_in_b\.data \(Target: 1672826400\)$"
)

echo "--- Running Test: Scenario 5: Mixed scenario with subdirectories and spaces in filenames ---"
MIXED_OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR_A" "$TEST_DIR_B" 2>&1)

ALL_PASS=true
for regex in "${EXPECTED_S5_OUTPUTS[@]}"; do
    if ! echo "$MIXED_OUTPUT" | grep -Eq "$regex"; then
        echo "FAIL: Scenario 5: Missing expected output for regex: '$regex'"
        echo "Actual output:\n$MIXED_OUTPUT"
        ALL_PASS=false
    fi
done

if $ALL_PASS; then
    echo "PASS: Scenario 5: Mixed scenario with subdirectories and spaces in filenames"
else
    exit 1
fi

echo "\nAll tests passed!"
