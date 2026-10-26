#!/bin/bash

# Test suite for Nightly Temporal Cache Sweeper

# Source the main script
SCRIPT_PATH="../src/temporal_cache_sweeper.sh"

# --- Test Utilities ---
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Expected: '$expected'"
        echo "   Actual:   '$actual'"
        exit 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if echo "$haystack" | grep -qF "$needle"; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Haystack: '$haystack'"
        echo "   Did not contain: '$needle'"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if ! echo "$haystack" | grep -qF "$needle"; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   Haystack: '$haystack'"
        echo "   Contained: '$needle'"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    local message="$2"
    if [[ -f "$file" ]]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   File '$file' does not exist."
        exit 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    local message="$2"
    if [[ ! -f "$file" ]]; then
        echo "✅ Test Passed: $message"
    else
        echo "❌ Test Failed: $message"
        echo "   File '$file' unexpectedly exists."
        exit 1
    fi
}

# Function to get a past date in YYYYMMDDhhmm format
get_past_date() {
    local days_ago="$1"
    if [[ "$(uname)" == "Darwin" ]]; then
        # macOS (BSD date)
        date -v -"${days_ago}d" +%Y%m%d%H%M # Mock rationale: Setting specific file modification times for deterministic test results across OS.
    else
        # Linux (GNU date)
        date -d "${days_ago} days ago" +%Y%m%d%H%M # Mock rationale: Setting specific file modification times for deterministic test results across OS.
    fi
}

# --- Setup and Teardown ---
TEST_DIR=""

setup() {
    TEST_DIR=$(mktemp -d -t temporal-sweeper-test-XXXXXXXX)
    echo "Created test directory: $TEST_DIR"
}

teardown() {
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
        echo "Cleaned up test directory: $TEST_DIR"
    fi
}

# --- Test Cases ---

# Test 1: No ancient files
test_no_ancient_files() {
    setup
    local current_time=$(date +%Y%m%d%H%M)
    touch -t "$current_time" "$TEST_DIR/recent_file.txt" # Mock rationale: Setting specific file modification times for deterministic test results.
    
    local output=$("$SCRIPT_PATH" "$TEST_DIR" 1)
    assert_contains "$output" "No ancient detritus found!" "Should report no ancient files"
    assert_file_exists "$TEST_DIR/recent_file.txt" "Recent file should still exist"
    teardown
}

# Test 2: List ancient files (default mode)
test_list_ancient_files() {
    setup
    local current_time=$(date +%Y%m%d%H%M)
    local one_day_ago=$(get_past_date 1)
    local ten_days_ago=$(get_past_date 10)

    touch -t "$current_time" "$TEST_DIR/recent_file.txt"
    touch -t "$one_day_ago" "$TEST_DIR/old_but_not_ancient.txt"
    touch -t "$ten_days_ago" "$TEST_DIR/ancient_scroll.txt"
    touch -t "$ten_days_ago" "$TEST_DIR/another_ancient_relic.log"

    local output=$("$SCRIPT_PATH" "$TEST_DIR" 5) # Look for files older than 5 days
    assert_contains "$output" "ancient_scroll.txt" "Should list ancient_scroll.txt"
    assert_contains "$output" "another_ancient_relic.log" "Should list another_ancient_relic.log"
    assert_not_contains "$output" "recent_file.txt" "Should not list recent_file.txt"
    assert_not_contains "$output" "old_but_not_ancient.txt" "Should not list old_but_not_ancient.txt"
    assert_contains "$output" "To purge this temporal detritus" "Should suggest --sweep"

    assert_file_exists "$TEST_DIR/recent_file.txt" "Recent file should still exist"
    assert_file_exists "$TEST_DIR/old_but_not_ancient.txt" "Old but not ancient file should still exist"
    assert_file_exists "$TEST_DIR/ancient_scroll.txt" "Ancient file should still exist in list mode"
    assert_file_exists "$TEST_DIR/another_ancient_relic.log" "Another ancient file should still exist in list mode"
    teardown
}

# Test 3: Sweep ancient files
test_sweep_ancient_files() {
    setup
    local current_time=$(date +%Y%m%d%H%M)
    local ten_days_ago=$(get_past_date 10)

    touch -t "$current_time" "$TEST_DIR/recent_file.txt"
    touch -t "$ten_days_ago" "$TEST_DIR/ancient_scroll.txt"
    touch -t "$ten_days_ago" "$TEST_DIR/another_ancient_relic.log"

    local output=$("$SCRIPT_PATH" "$TEST_DIR" 5 --sweep) # Look for files older than 5 days and sweep
    assert_contains "$output" "Initiating temporal sweep protocol..." "Should indicate sweep mode"
    assert_contains "$output" "Temporal detritus successfully purged!" "Should confirm purge"
    assert_not_contains "$output" "To purge this temporal detritus" "Should not suggest --sweep in sweep mode"

    assert_file_exists "$TEST_DIR/recent_file.txt" "Recent file should still exist after sweep"
    assert_file_not_exists "$TEST_DIR/ancient_scroll.txt" "Ancient file should be deleted after sweep"
    assert_file_not_exists "$TEST_DIR/another_ancient_relic.log" "Another ancient file should be deleted after sweep"
    teardown
}

# Test 4: Invalid directory
test_invalid_directory() {
    local output=$("$SCRIPT_PATH" "/non/existent/path" 1 2>&1) # Redirect stderr to stdout
    assert_contains "$output" "Error: Directory '/non/existent/path' not found or is not a directory." "Should report invalid directory error"
    assert_equals "1" "$?" "Should exit with error code 1"
}

# Test 5: Default age
test_default_age() {
    setup
    local current_time=$(date +%Y%m%d%H%M)
    local six_days_ago=$(get_past_date 6)
    local eight_days_ago=$(get_past_date 8)

    touch -t "$current_time" "$TEST_DIR/recent.txt"
    touch -t "$six_days_ago" "$TEST_DIR/just_old.txt"
    touch -t "$eight_days_ago" "$TEST_DIR/very_old.txt"

    local output=$("$SCRIPT_PATH" "$TEST_DIR") # No age specified, should use default 7 days
    assert_not_contains "$output" "recent.txt" "Should not list recent.txt"
    assert_not_contains "$output" "just_old.txt" "Should not list just_old.txt (6 days old, default is >7)"
    assert_contains "$output" "very_old.txt" "Should list very_old.txt (8 days old, default is >7)"
    teardown
}

# Test 6: Files with spaces in names
test_files_with_spaces() {
    setup
    local ten_days_ago=$(get_past_date 10)
    touch -t "$ten_days_ago" "$TEST_DIR/file with spaces.txt"
    touch -t "$ten_days_ago" "$TEST_DIR/another file with spaces.log"

    local output=$("$SCRIPT_PATH" "$TEST_DIR" 5)
    assert_contains "$output" "file with spaces.txt" "Should list file with spaces"
    assert_contains "$output" "another file with spaces.log" "Should list another file with spaces"

    local sweep_output=$("$SCRIPT_PATH" "$TEST_DIR" 5 --sweep)
    assert_contains "$sweep_output" "Temporal detritus successfully purged!" "Should confirm purge for files with spaces"
    assert_file_not_exists "$TEST_DIR/file with spaces.txt" "File with spaces should be deleted"
    assert_file_not_exists "$TEST_DIR/another file with spaces.log" "Another file with spaces should be deleted"
    teardown
}

# Run all tests
echo "Running Nightly Temporal Cache Sweeper Tests..."
test_no_ancient_files
test_list_ancient_files
test_sweep_ancient_files
test_invalid_directory
test_default_age
test_files_with_spaces
echo "All tests completed successfully!"
