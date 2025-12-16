#!/bin/bash

# Test suite for Nightly Digital Dust Bunny Sweeper

SCRIPT_PATH="./src/dust_bunny_sweeper.sh"
TEST_DIR="test_temp_dir"

# --- Helper functions ---

# Create a temporary test directory and files
setup_test_environment() {
    mkdir -p "$TEST_DIR/subdir1" "$TEST_DIR/subdir2"
    # Create a recent file (not a dust bunny)
    touch "$TEST_DIR/recent_file.txt"
    touch "$TEST_DIR/subdir1/recent_sub_file.log"

    # Create old files (dust bunnies) - set to a date far in the past
    # Mock rationale: Using 'touch -t' with a fixed historical date (e.g., 202301010000)
    # ensures that these files are consistently older than any reasonable 'AGE_DAYS'
    # threshold (like the default 90 days), making the tests deterministic regardless
    # of the current system date when the tests are run.
    touch -t 202301010000 "$TEST_DIR/old_file_1.txt"
    touch -t 202301010000 "$TEST_DIR/old_file_2.log"
    touch -t 202301010000 "$TEST_DIR/subdir2/ancient_data.bak"
}

# Clean up the test environment
cleanup_test_environment() {
    rm -rf "$TEST_DIR"
}

# Assert function
assert_contains() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if echo "$actual" | grep -qF "$expected"; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  Expected to contain: '$expected'"
        echo "  Actual output: '$actual'"
        exit 1
    fi
}

assert_not_contains() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if ! echo "$actual" | grep -qF "$expected"; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  Expected NOT to contain: '$expected'"
        echo "  Actual output: '$actual'"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    local message="$2"
    if [ -e "$file" ]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  File not found: '$file'"
        exit 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    local message="$2"
    if [ ! -e "$file" ]; then
        echo "✅ PASS: $message"
    else
        echo "❌ FAIL: $message"
        echo "  File unexpectedly found: '$file'"
        exit 1
    fi
}

# --- Test Cases ---

echo "--- Running Nightly Digital Dust Bunny Sweeper Tests ---"

# Test 1: No arguments - should show usage
echo "Test 1: No arguments (should show usage)"
OUTPUT=$("$SCRIPT_PATH" 2>&1)
assert_contains "Usage: $0 [OPTIONS] <directory>" "$OUTPUT" "Usage message displayed"
assert_contains "Error: No target directory specified." "$OUTPUT" "Error for missing directory"
echo ""

# Test 2: Invalid directory
echo "Test 2: Invalid directory"
OUTPUT=$("$SCRIPT_PATH" /non_existent_dir 2>&1)
assert_contains "Error: Target directory '/non_existent_dir' does not exist or is not a directory." "$OUTPUT" "Error for invalid directory"
echo ""

# Test 3: Report mode, default age (90 days), dry-run
echo "Test 3: Report mode, default age (90 days), dry-run"
cleanup_test_environment
setup_test_environment
OUTPUT=$("$SCRIPT_PATH" -d "$TEST_DIR" 2>&1)
assert_contains "old_file_1.txt" "$OUTPUT" "old_file_1.txt reported"
assert_contains "old_file_2.log" "$OUTPUT" "old_file_2.log reported"
assert_contains "ancient_data.bak" "$OUTPUT" "ancient_data.bak reported"
assert_not_contains "recent_file.txt" "$OUTPUT" "recent_file.txt not reported"
assert_contains "Dry Run: Yes" "$OUTPUT" "Dry run indicated"
assert_file_exists "$TEST_DIR/old_file_1.txt" "old_file_1.txt still exists after dry-run report"
cleanup_test_environment
echo ""

# Test 4: Report mode, custom age (110 days), dry-run
echo "Test 4: Report mode, custom age (110 days), dry-run"
cleanup_test_environment
setup_test_environment
# For files from 2023-01-01, 110 days means files older than 2023-04-21.
# All test files are from 2023-01-01, so they should all be reported.
OUTPUT=$("$SCRIPT_PATH" -a 110 -d "$TEST_DIR" 2>&1)
assert_contains "old_file_1.txt" "$OUTPUT" "old_file_1.txt reported (older than 110 days)"
assert_contains "old_file_2.log" "$OUTPUT" "old_file_2.log reported (older than 110 days)"
assert_contains "ancient_data.bak" "$OUTPUT" "ancient_data.bak reported (older than 110 days)"
assert_contains "Dry Run: Yes" "$OUTPUT" "Dry run indicated"
cleanup_test_environment
echo ""

# Test 5: Archive mode, dry-run
echo "Test 5: Archive mode, dry-run"
cleanup_test_environment
setup_test_environment
OUTPUT=$("$SCRIPT_PATH" -m archive -d "$TEST_DIR" 2>&1)
assert_contains "Would move to: $TEST_DIR/.dust_bunnies_archive/" "$OUTPUT" "Archive dry-run message for root file"
assert_contains "Would move to: $TEST_DIR/subdir2/.dust_bunnies_archive/" "$OUTPUT" "Archive dry-run message for sub-directory file"
assert_file_exists "$TEST_DIR/old_file_1.txt" "old_file_1.txt still exists after dry-run archive"
assert_file_not_exists "$TEST_DIR/.dust_bunnies_archive" "Archive dir not created in dry-run"
cleanup_test_environment
echo ""

# Test 6: Delete mode, dry-run
echo "Test 6: Delete mode, dry-run"
cleanup_test_environment
setup_test_environment
OUTPUT=$("$SCRIPT_PATH" -m delete -d "$TEST_DIR" 2>&1)
assert_contains "Would delete: $TEST_DIR/old_file_1.txt" "$OUTPUT" "Delete dry-run message for old_file_1.txt"
assert_contains "Would delete: $TEST_DIR/old_file_2.log" "$OUTPUT" "Delete dry-run message for old_file_2.log"
assert_file_exists "$TEST_DIR/old_file_1.txt" "old_file_1.txt still exists after dry-run delete"
cleanup_test_environment
echo ""

# Test 7: Archive mode (actual action)
echo "Test 7: Archive mode (actual action)"
cleanup_test_environment
setup_test_environment

# Mock rationale: Override 'mkdir' and 'mv' to simulate their behavior without
# actually modifying the filesystem. This allows us to verify that the correct
# commands *would have been called* and that the script's logic for constructing
# paths and commands is sound.
# We capture the commands into a log file.
MOCKED_COMMANDS_LOG="mocked_commands.log"

# Mock mkdir and mv functions
mkdir() {
    echo "MOCK_MKDIR $@" >> "$MOCKED_COMMANDS_LOG"
    # Simulate success
    return 0
}
mv() {
    echo "MOCK_MV $@" >> "$MOCKED_COMMANDS_LOG"
    # Simulate success
    return 0
}

# Run the script with actual archive mode
OUTPUT=$("$SCRIPT_PATH" -m archive "$TEST_DIR" 2>&1)

assert_contains "Archived to: $TEST_DIR/.dust_bunnies_archive/old_file_1.txt" "$OUTPUT" "Archive success message for old_file_1.txt"
assert_contains "Archived to: $TEST_DIR/subdir2/.dust_bunnies_archive/ancient_data.bak" "$OUTPUT" "Archive success message for ancient_data.bak"

# Verify mock calls
assert_file_exists "$MOCKED_COMMANDS_LOG" "Mock commands log exists"
MOCKED_OUTPUT=$(cat "$MOCKED_COMMANDS_LOG")
assert_contains "MOCK_MKDIR -p $TEST_DIR/.dust_bunnies_archive" "$MOCKED_OUTPUT" "mkdir called for root archive"
assert_contains "MOCK_MV $TEST_DIR/old_file_1.txt $TEST_DIR/.dust_bunnies_archive/" "$MOCKED_OUTPUT" "mv called for old_file_1.txt"
assert_contains "MOCK_MKDIR -p $TEST_DIR/subdir2/.dust_bunnies_archive" "$MOCKED_OUTPUT" "mkdir called for subdir2 archive"
assert_contains "MOCK_MV $TEST_DIR/subdir2/ancient_data.bak $TEST_DIR/subdir2/.dust_bunnies_archive/" "$MOCKED_OUTPUT" "mv called for ancient_data.bak"

# Clean up mock log
rm "$MOCKED_COMMANDS_LOG"
cleanup_test_environment
echo ""

# Test 8: Delete mode (actual action)
echo "Test 8: Delete mode (actual action)"
cleanup_test_environment
setup_test_environment

# Mock rationale: Override 'rm' to simulate its behavior without
# actually modifying the filesystem. This allows us to verify that the correct
# commands *would have been called*.
MOCKED_COMMANDS_LOG="mocked_commands.log"

# Mock rm function
rm() {
    echo "MOCK_RM $@" >> "$MOCKED_COMMANDS_LOG"
    # Simulate success
    return 0
}

# Run the script with actual delete mode
OUTPUT=$("$SCRIPT_PATH" -m delete "$TEST_DIR" 2>&1)

assert_contains "Evicted: $TEST_DIR/old_file_1.txt" "$OUTPUT" "Delete success message for old_file_1.txt"
assert_contains "Evicted: $TEST_DIR/old_file_2.log" "$OUTPUT" "Delete success message for old_file_2.log"
assert_contains "Evicted: $TEST_DIR/subdir2/ancient_data.bak" "$OUTPUT" "Delete success message for ancient_data.bak"

# Verify mock calls
assert_file_exists "$MOCKED_COMMANDS_LOG" "Mock commands log exists"
MOCKED_OUTPUT=$(cat "$MOCKED_COMMANDS_LOG")
assert_contains "MOCK_RM $TEST_DIR/old_file_1.txt" "$MOCKED_OUTPUT" "rm called for old_file_1.txt"
assert_contains "MOCK_RM $TEST_DIR/old_file_2.log" "$MOCKED_OUTPUT" "rm called for old_file_2.log"
assert_contains "MOCK_RM $TEST_DIR/subdir2/ancient_data.bak" "$MOCKED_OUTPUT" "rm called for ancient_data.bak"

# Clean up mock log
rm "$MOCKED_COMMANDS_LOG"
cleanup_test_environment
echo ""

# Test 9: No dust bunnies found
echo "Test 9: No dust bunnies found"
cleanup_test_environment
mkdir -p "$TEST_DIR"
touch "$TEST_DIR/recent_file.txt"
OUTPUT=$("$SCRIPT_PATH" "$TEST_DIR" 2>&1)
assert_contains "Hooray! No digital dust bunnies found." "$OUTPUT" "Message for no dust bunnies"
cleanup_test_environment
echo ""

echo "--- All tests completed ---"
