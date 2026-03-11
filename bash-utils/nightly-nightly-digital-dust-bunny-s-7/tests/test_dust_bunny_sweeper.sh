#!/bin/bash

# Set up a temporary directory for tests
TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
MOCK_LOG="$TEST_DIR/mock_rm.log"
SCRIPT_PATH="$(dirname "$0")"/../src/dust_bunny_sweeper.sh

# Mock rationale: Overriding internal functions to control 'find' output and 'rm' behavior.
# This ensures tests are deterministic, don't touch the actual filesystem, and can simulate
# various scenarios (e.g., files found, no files found, deletion attempts).

# Override _find_old_files to return specific paths
_find_old_files() {
    local test_target_dir="$1"
    local test_age="$2"
    # Simulate finding files in the test directory based on arguments
    if [[ "$test_target_dir" == "$TEST_DIR/target1" && "$test_age" == "7" ]]; then
        echo "$TEST_DIR/target1/old_log.txt"
        echo "$TEST_DIR/target1/cache/old_data.tmp"
    elif [[ "$test_target_dir" == "$TEST_DIR/target2" && "$test_age" == "1" ]]; then
        echo "$TEST_DIR/target2/very_old_file.bak"
    else
        # No files found for other scenarios or ages
        :
    fi
}

# Override _delete_file to log deletion attempts instead of actual deletion
_delete_file() {
    echo "MOCKED_RM: $1" >> "$MOCK_LOG"
}

# Helper function to assert output
assert_output() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$actual" == *"$expected"* ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  Expected to contain: '$expected'"
        echo "  Actual output: '$actual'"
        exit 1
    fi
}

# Helper function to assert mock log content
assert_mock_log() {
    local expected="$1"
    local message="$2"
    if grep -q "$expected" "$MOCK_LOG"; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  Expected mock log to contain: '$expected'"
        echo "  Actual mock log content:"
        cat "$MOCK_LOG"
        exit 1
    fi
}

# Helper function to assert mock log is empty
assert_mock_log_empty() {
    local message="$1"
    if [[ ! -s "$MOCK_LOG" ]]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  Expected mock log to be empty, but it contains:"
        cat "$MOCK_LOG"
        exit 1
    fi
}

# --- Test Cases ---

echo "Running tests for Digital Dust Bunny Sweeper..."

# Create dummy directories for mocks to reference
mkdir -p "$TEST_DIR/target1/cache"
mkdir -p "$TEST_DIR/target2"

# Test 1: Dry run with default age and custom directory
echo "--- Test 1: Dry run, custom dir, default age ---"
rm -f "$MOCK_LOG" # Clear mock log
OUTPUT=$(DRY_RUN=true "$SCRIPT_PATH" -d "$TEST_DIR/target1" -a 7)
assert_output "DRY RUN (no files will be deleted)" "$OUTPUT" "Dry run mode indicated"
assert_output "DRY RUN: Would delete: $TEST_DIR/target1/old_log.txt" "$OUTPUT" "Dry run output for old_log.txt"
assert_output "DRY RUN: Would delete: $TEST_DIR/target1/cache/old_data.tmp" "$OUTPUT" "Dry run output for old_data.tmp"
assert_mock_log_empty "Mock log should be empty in dry run (no actual _delete_file calls)"

# Test 2: Real run with custom age and custom directory
echo "--- Test 2: Real run, custom dir, custom age ---"
rm -f "$MOCK_LOG" # Clear mock log
OUTPUT=$(DRY_RUN=false "$SCRIPT_PATH" -d "$TEST_DIR/target2" -a 1)
assert_output "REAL RUN (files will be deleted)" "$OUTPUT" "Real run mode indicated"
assert_output "Swept away 1 dust bunnies" "$OUTPUT" "Correct count for real run"
assert_mock_log "MOCKED_RM: $TEST_DIR/target2/very_old_file.bak" "Mock log shows deletion attempt for very_old_file.bak"

# Test 3: Real run with verbose output
echo "--- Test 3: Real run, verbose output ---"
rm -f "$MOCK_LOG" # Clear mock log
OUTPUT=$(DRY_RUN=false VERBOSE=true "$SCRIPT_PATH" -d "$TEST_DIR/target1" -a 7)
assert_output "Deleting: $TEST_DIR/target1/old_log.txt" "$OUTPUT" "Verbose output for old_log.txt"
assert_output "Deleting: $TEST_DIR/target1/cache/old_data.tmp" "$OUTPUT" "Verbose output for old_data.tmp"
assert_mock_log "MOCKED_RM: $TEST_DIR/target1/old_log.txt" "Mock log shows deletion attempt for old_log.txt (verbose)"
assert_mock_log "MOCKED_RM: $TEST_DIR/target1/cache/old_data.tmp" "Mock log shows deletion attempt for old_data.tmp (verbose)"
assert_output "Swept away 2 dust bunnies" "$OUTPUT" "Correct count for real run (verbose)"

# Test 4: No old files found
echo "--- Test 4: No old files found ---"
rm -f "$MOCK_LOG" # Clear mock log
# Override _find_old_files temporarily for this test to return nothing
_find_old_files_original=$(declare -f _find_old_files)
_find_old_files() { :; } # Mock to return nothing
OUTPUT=$(DRY_RUN=true "$SCRIPT_PATH" -d "$TEST_DIR/nonexistent" -a 10) # Use a non-existent dir to ensure no files are found
assert_output "No digital dust bunnies found" "$OUTPUT" "Message for no files found"
assert_mock_log_empty "Mock log should be empty when no files are found"
eval "$_find_old_files_original" # Restore original mock function

# Test 5: Usage message
echo "--- Test 5: Usage message ---"
OUTPUT=$("$SCRIPT_PATH" -h)
assert_output "Usage: $0" "$OUTPUT" "Usage message displayed"
assert_output "Add a directory to scan" "$OUTPUT" "Usage message contains directory option"

# Test 6: Environment variable configuration
echo "--- Test 6: Environment variable configuration ---"
rm -f "$MOCK_LOG" # Clear mock log
OUTPUT=$(DUST_BUNNY_DIRS="$TEST_DIR/target1" DUST_BUNNY_MAX_AGE=7 DUST_BUNNY_REAL_RUN=true "$SCRIPT_PATH")
assert_output "REAL RUN (files will be deleted)" "$OUTPUT" "Real run mode indicated by env var"
assert_output "Scanning directories: $TEST_DIR/target1" "$OUTPUT" "Directory set by env var"
assert_output "Files older than: 7 days" "$OUTPUT" "Age set by env var"
assert_mock_log "MOCKED_RM: $TEST_DIR/target1/old_log.txt" "Mock log shows deletion attempt for old_log.txt (env var)"
assert_mock_log "MOCKED_RM: $TEST_DIR/target1/cache/old_data.tmp" "Mock log shows deletion attempt for old_data.tmp (env var)"

echo "All tests passed!"

# Clean up
rm -rf "$TEST_DIR"
