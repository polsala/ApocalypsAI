#!/bin/bash

# Mock rationale: We are creating a temporary directory and files with specific modification times
# and content to simulate a real filesystem. This makes the tests deterministic and offline
# without needing to mock system commands like 'find' or 'grep', as their behavior on a controlled
# filesystem is predictable.

SCRIPT_PATH="../src/nightly-chrono-compass.sh"
TEST_DIR="temp_test_dir"
EXIT_CODE=0

# Helper function for assertions
assert_contains() {
    local output="$1"
    local expected="$2"
    local test_name="$3"
    if echo "$output" | grep -q "$expected"; then
        echo "✅ PASS: $test_name (contains '$expected')"
    else
        echo "❌ FAIL: $test_name (expected to contain '$expected', but did not)"
        echo "--- Output ---"
        echo "$output"
        echo "--------------"
        EXIT_CODE=1
    fi
}

assert_not_contains() {
    local output="$1"
    local unexpected="$2"
    local test_name="$3"
    if ! echo "$output" | grep -q "$unexpected"; then
        echo "✅ PASS: $test_name (does not contain '$unexpected')"
    else
        echo "❌ FAIL: $test_name (expected not to contain '$unexpected', but did)"
        echo "--- Output ---"
        echo "$output"
        echo "--------------"
        EXIT_CODE=1
    fi
}

# Setup: Create test directory and files
setup() {
    rm -rf "$TEST_DIR"
    mkdir -p "$TEST_DIR"

    # File modified 2 days ago
    # Using 'touch -d' for broader compatibility than 'date -v' or specific stat commands.
    # This assumes a GNU-like 'touch' which is common in most Linux environments and via coreutils on macOS.
    touch -d "2 days ago" "$TEST_DIR/file_old.txt"
    echo "This is an old file." > "$TEST_DIR/file_old.txt"

    # File modified recently (0 days ago)
    touch -d "now" "$TEST_DIR/file_recent_no_keyword.txt"
    echo "This is a recent file without special keywords." > "$TEST_DIR/file_recent_no_keyword.txt"

    # File modified recently with a keyword
    touch -d "now" "$TEST_DIR/file_recent_with_keyword.txt"
    echo "This file contains an URGENT task." > "$TEST_DIR/file_recent_with_keyword.txt"

    # File modified recently with another keyword
    touch -d "now" "$TEST_DIR/file_recent_with_another_keyword.txt"
    echo "This file has a DEADLINE approaching." > "$TEST_DIR/file_recent_with_another_keyword.txt"

    # File modified recently with mixed case keyword
    touch -d "now" "$TEST_DIR/file_recent_mixed_case.txt"
    echo "This file has a todo item." > "$TEST_DIR/file_recent_mixed_case.txt"
}

# Teardown: Clean up test directory
teardown() {
    rm -rf "$TEST_DIR"
}

# --- Test Cases ---

echo "Running Chrono-Compass Tests..."

# Test 1: Default scan (current directory, 1 day, no keywords)
setup
OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR" 1)
assert_contains "$OUTPUT" "file_recent_no_keyword.txt" "Test 1.1: Default scan finds recent file (no keyword)"
assert_contains "$OUTPUT" "file_recent_with_keyword.txt" "Test 1.2: Default scan finds recent file (with keyword)"
assert_contains "$OUTPUT" "file_recent_with_another_keyword.txt" "Test 1.3: Default scan finds another recent file"
assert_contains "$OUTPUT" "file_recent_mixed_case.txt" "Test 1.4: Default scan finds mixed case file"
assert_not_contains "$OUTPUT" "file_old.txt" "Test 1.5: Default scan does not find old file"
assert_contains "$OUTPUT" "No specific whispers detected within this echo." "Test 1.6: Default scan indicates no whispers when no keywords are searched"
teardown

# Test 2: Scan with keyword
setup
OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR" 1 URGENT)
assert_contains "$OUTPUT" "file_recent_with_keyword.txt" "Test 2.1: Keyword scan finds file with keyword"
assert_contains "$OUTPUT" "URGENT task" "Test 2.2: Keyword scan shows line with keyword"
assert_not_contains "$OUTPUT" "file_recent_no_keyword.txt" "Test 2.3: Keyword scan does not show file without keyword"
assert_not_contains "$OUTPUT" "file_old.txt" "Test 2.4: Keyword scan does not show old file"
teardown

# Test 3: Scan with multiple keywords
setup
OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR" 1 URGENT DEADLINE)
assert_contains "$OUTPUT" "file_recent_with_keyword.txt" "Test 3.1: Multi-keyword scan finds first keyword file"
assert_contains "$OUTPUT" "URGENT task" "Test 3.2: Multi-keyword scan shows line for first keyword"
assert_contains "$OUTPUT" "file_recent_with_another_keyword.txt" "Test 3.3: Multi-keyword scan finds second keyword file"
assert_contains "$OUTPUT" "DEADLINE approaching" "Test 3.4: Multi-keyword scan shows line for second keyword"
assert_not_contains "$OUTPUT" "file_recent_no_keyword.txt" "Test 3.5: Multi-keyword scan does not show file without keywords"
teardown

# Test 4: Scan for more days (should include old file)
setup
OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR" 2)
assert_contains "$OUTPUT" "file_old.txt" "Test 4.1: Scan for 2 days finds old file"
assert_contains "$OUTPUT" "file_recent_no_keyword.txt" "Test 4.2: Scan for 2 days finds recent file"
teardown

# Test 5: Scan with mixed case keyword (should be case-insensitive)
setup
OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR" 1 todo)
assert_contains "$OUTPUT" "file_recent_mixed_case.txt" "Test 5.1: Mixed case keyword scan finds file"
assert_contains "$OUTPUT" "todo item" "Test 5.2: Mixed case keyword scan shows line with keyword"
teardown

# Test 6: Non-existent directory
OUTPUT=$(bash "$SCRIPT_PATH" "non_existent_dir" 2>&1)
assert_contains "$OUTPUT" "Error: Directory 'non_existent_dir' not found." "Test 6.1: Non-existent directory reports error"
assert_contains "$OUTPUT" "Usage: $SCRIPT_PATH" "Test 6.2: Non-existent directory shows usage"

echo ""
if [ "$EXIT_CODE" -eq 0 ]; then
    echo "All Chrono-Compass tests passed!"
else
    echo "Some Chrono-Compass tests failed!"
fi

exit "$EXIT_CODE"
