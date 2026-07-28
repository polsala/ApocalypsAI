#!/bin/bash

# --- Test Setup ---
TEST_DIR=$(mktemp -d -t digital-dust-sweeper-test-XXXXXX)
DUSTBIN_DIR=$(mktemp -d -t digital-dustbin-test-XXXXXX)
SCRIPT_PATH="$(dirname "$0")"/../src/digital-dust-bunny-sweeper.sh

# Mock rationale: Prevent actual filesystem scans, provide controlled output.
MOCKED_FIND_OUTPUT=""
find() {
    echo -e "$MOCKED_FIND_OUTPUT"
}

# Mock rationale: Prevent actual file deletion, record calls.
MOCKED_RM_CALLS=""
rm() {
    MOCKED_RM_CALLS+="rm $*"$'
'
    return 0 # Simulate success
}

# Mock rationale: Prevent actual file movement, record calls.
MOCKED_MV_CALLS=""
mv() {
    MOCKED_MV_CALLS+="mv $*"$'
'
    return 0 # Simulate success
}

# Mock rationale: Prevent actual directory creation during tests, except for the designated test dustbin.
mkdir() {
    if [[ "$1" == "-p" ]]; then
        # Only allow creation of our test dustbin, otherwise mock
        if [[ "$2" == "$DUSTBIN_DIR" ]]; then
            command mkdir -p "$2"
        else
            echo "MOCKED mkdir -p $2"
        fi
    else
        echo "MOCKED mkdir $*"
    fi
    return 0
}


# Helper for assertions
assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if ! echo "$haystack" | grep -qF "$needle"; then
        echo "❌ FAIL: $message"
        echo "  Expected to contain: '$needle'"
        echo "  Actual output:"
        echo "$haystack"
        exit 1
    else
        echo "✅ PASS: $message"
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if echo "$haystack" | grep -qF "$needle"; then
        echo "❌ FAIL: $message"
        echo "  Expected NOT to contain: '$needle'"
        echo "  Actual output:"
        echo "$haystack"
        exit 1
    else
        echo "✅ PASS: $message"
    fi
}

assert_equals() {
    local actual="$1"
    local expected="$2"
    local message="$3"
    if [[ "$actual" != "$expected" ]]; then
        echo "❌ FAIL: $message"
        echo "  Expected: '$expected'"
        echo "  Actual:   '$actual'"
        exit 1
    else
        echo "✅ PASS: $message"
    fi
}

# --- Test Cases ---

echo "Running tests for Digital Dust Bunny Sweeper..."

# Test 1: Help message
echo "--- Test 1: Display help message ---"
output=$("$SCRIPT_PATH" --help)
assert_contains "$output" "Usage: digital-dust-bunny-sweeper.sh [OPTIONS]" "Help message should be displayed"

# Test 2: Report mode - no files found
echo "--- Test 2: Report mode - no files found ---"
MOCKED_FIND_OUTPUT="" # No files
output=$("$SCRIPT_PATH" --dir "$TEST_DIR" --report)
assert_contains "$output" "Your digital space is sparkling clean! No dust bunnies detected." "Should report no dust bunnies"
assert_not_contains "$output" "Sweep Mode Activated!" "Should not activate sweep mode"

# Test 3: Report mode - old files found
echo "--- Test 3: Report mode - old files found ---"
MOCKED_FIND_OUTPUT="$TEST_DIR/old_file_1.txt"$'
'"$TEST_DIR/old_file_2.log"
output=$("$SCRIPT_PATH" --dir "$TEST_DIR" --age 10 --report)
assert_contains "$output" "Ancient Artifacts (Files older than 10 days):" "Should list ancient artifacts header"
assert_contains "$output" "$TEST_DIR/old_file_1.txt" "Should list old_file_1.txt"
assert_contains "$output" "$TEST_DIR/old_file_2.log" "Should list old_file_2.log"
assert_contains "$output" "Total Digital Dust Bunnies identified: 2 files." "Should count 2 files"
assert_contains "$output" "Report Mode: These files would be acted upon" "Should indicate report mode"
assert_not_contains "$output" "Sweep Mode Activated!" "Should not activate sweep mode"

# Test 4: Report mode - temp pattern files found
echo "--- Test 4: Report mode - temp pattern files found ---"
MOCKED_FIND_OUTPUT="$TEST_DIR/temp.tmp"$'
'"$TEST_DIR/backup~"
output=$("$SCRIPT_PATH" --dir "$TEST_DIR" --report) # Default age 30, but find is mocked
assert_contains "$output" "Ephemeral Remnants (Temporary pattern files):" "Should list ephemeral remnants header"
assert_contains "$output" "$TEST_DIR/temp.tmp" "Should list temp.tmp"
assert_contains "$output" "$TEST_DIR/backup~" "Should list backup~"
assert_contains "$output" "Total Digital Dust Bunnies identified: 2 files." "Should count 2 files"
assert_contains "$output" "Report Mode: These files would be acted upon" "Should indicate report mode"

# Test 5: Sweep mode - delete action
echo "--- Test 5: Sweep mode - delete action ---"
MOCKED_FIND_OUTPUT="$TEST_DIR/delete_me.txt"$'
'"$TEST_DIR/another_delete.log"
MOCKED_RM_CALLS="" # Reset mock calls
output=$("$SCRIPT_PATH" --dir "$TEST_DIR" --sweep --delete)
assert_contains "$output" "Sweep Mode Activated!" "Should activate sweep mode"
assert_contains "$output" "Permanently deleting identified digital dust bunnies..." "Should indicate deletion"
assert_contains "$output" "Digital dust bunnies have been vanquished!" "Should confirm vanquishing"
assert_contains "$MOCKED_RM_CALLS" "rm -f $TEST_DIR/delete_me.txt" "rm should be called for delete_me.txt"
assert_contains "$MOCKED_RM_CALLS" "rm -f $TEST_DIR/another_delete.log" "rm should be called for another_delete.log"
assert_equals "$(echo -e "$MOCKED_RM_CALLS" | grep -c 'rm -f')" "2" "rm should be called exactly twice"

# Test 6: Sweep mode - move to dustbin action
echo "--- Test 6: Sweep mode - move to dustbin action ---"
MOCKED_FIND_OUTPUT="$TEST_DIR/move_me.txt"$'
'"$TEST_DIR/another_move.log"
MOCKED_MV_CALLS="" # Reset mock calls
output=$("$SCRIPT_PATH" --dir "$TEST_DIR" --sweep --dustbin "$DUSTBIN_DIR")
assert_contains "$output" "Sweep Mode Activated!" "Should activate sweep mode"
assert_contains "$output" "Moving identified digital dust bunnies to the digital dustbin: '$DUSTBIN_DIR'..." "Should indicate moving"
assert_contains "$output" "Digital dust bunnies have been safely quarantined in the dustbin!" "Should confirm quarantine"
assert_contains "$MOCKED_MV_CALLS" "mv $TEST_DIR/move_me.txt $DUSTBIN_DIR/" "mv should be called for move_me.txt"
assert_contains "$MOCKED_MV_CALLS" "mv $TEST_DIR/another_move.log $DUSTBIN_DIR/" "mv should be called for another_move.log"
assert_equals "$(echo -e "$MOCKED_MV_CALLS" | grep -c 'mv')" "2" "mv should be called exactly twice"

# Test 7: Sweep mode - no dustbin/delete specified, defaults to delete
echo "--- Test 7: Sweep mode - default to delete if no action specified ---"
MOCKED_FIND_OUTPUT="$TEST_DIR/default_delete.txt"
MOCKED_RM_CALLS="" # Reset mock calls
output=$("$SCRIPT_PATH" --dir "$TEST_DIR" --sweep)
assert_contains "$output" "Warning: --sweep was used without --dustbin or --delete. Defaulting to --delete." "Should warn about default delete"
assert_contains "$output" "Permanently deleting identified digital dust bunnies..." "Should indicate deletion"
assert_contains "$MOCKED_RM_CALLS" "rm -f $TEST_DIR/default_delete.txt" "rm should be called for default_delete.txt"

# Test 8: Invalid age
echo "--- Test 8: Invalid age parameter ---"
output=$("$SCRIPT_PATH" --age abc 2>&1)
assert_contains "$output" "Error: --age must be a positive integer." "Should error on invalid age"

# Test 9: Non-existent target directory
echo "--- Test 9: Non-existent target directory ---"
output=$("$SCRIPT_PATH" --dir /non/existent/path 2>&1)
assert_contains "$output" "Error: Target directory '/non/existent/path' does not exist or is not a directory." "Should error on non-existent directory"

# Test 10: Combined old and temp files, deduplication
echo "--- Test 10: Combined old and temp files, deduplication ---"
MOCKED_FIND_OUTPUT="$TEST_DIR/file_a.tmp"$'
'"$TEST_DIR/file_b.log"$'
'"$TEST_DIR/file_a.tmp" # file_a.tmp is listed twice to test deduplication
output=$("$SCRIPT_PATH" --dir "$TEST_DIR" --age 1 --report)
assert_contains "$output" "Ancient Artifacts" "Should list ancient artifacts header"
assert_contains "$output" "Ephemeral Remnants" "Should list ephemeral remnants header"
assert_contains "$output" "$TEST_DIR/file_a.tmp" "Should list file_a.tmp"
assert_contains "$output" "$TEST_DIR/file_b.log" "Should list file_b.log"
assert_equals "$(echo -e "$output" | grep -E "$TEST_DIR/(file_a.tmp|file_b.log)" | sort -u | wc -l)" "2" "Should list only 2 unique files"
assert_contains "$output" "Total Digital Dust Bunnies identified: 2 files." "Should count 2 unique files"

# --- Cleanup ---
rm -rf "$TEST_DIR" "$DUSTBIN_DIR"
echo "All tests completed."
