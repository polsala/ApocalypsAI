#!/bin/bash

# Automated tests for nightly-digital-detritus-duster

SCRIPT_PATH="$(dirname "$0")"/../src/detritus_duster.sh
TEST_DIR="$(mktemp -d)"

# --- Test Helpers ---

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "\033[0;32m[PASS]\033[0m $message"
    else
        echo "\033[0;31m[FAIL]\033[0m $message"
        echo "       Expected: '$expected'"
        echo "       Actual:   '$actual'"
        exit 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" == *"$needle"* ]]; then
        echo "\033[0;32m[PASS]\033[0m $message"
    else
        echo "\033[0;31m[FAIL]\033[0m $message"
        echo "       Expected to contain: '$needle'"
        echo "       Actual:              '$haystack'"
        exit 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    if [[ "$haystack" != *"$needle"* ]]; then
        echo "\033[0;32m[PASS]\033[0m $message"
    else
        echo "\033[0;31m[FAIL]\033[0m $message"
        echo "       Expected NOT to contain: '$needle'"
        echo "       Actual:                  '$haystack'"
        exit 1
    fi
}

# Function to set file modification time reliably across Linux/macOS
# Mock rationale: Ensures deterministic file ages for 'find -mtime' tests.
set_mtime() {
    local file="$1"
    local days_ago="$2"
    if command -v gdate &>/dev/null; then # GNU date (often on macOS with coreutils)
        gdate -s "${days_ago} days ago" "$file"
    elif command -v date &>/dev/null && date --version &>/dev/null; then # Linux date
        date -s "${days_ago} days ago" "$file"
    elif command -v date &>/dev/null; then # macOS date
        # macOS date -v-3d +%Y%m%d%H%M.%S is for current time. Need to calculate.
        # Fallback for macOS: create file, then touch with specific time.
        local timestamp
        timestamp=$(date -v-"${days_ago}"d +%Y%m%d%H%M.%S)
        touch -t "$timestamp" "$file"
    else
        echo "Warning: Could not set modification time for '$file'. Test might be unreliable." >&2
    fi
}

# --- Setup and Teardown ---

setup() {
    echo "\nSetting up test environment in $TEST_DIR..."
    mkdir -p "$TEST_DIR"

    # Create old files (older than DEFAULT_AGE_DAYS=3)
    touch "$TEST_DIR/ancient_scroll.txt"
    set_mtime "$TEST_DIR/ancient_scroll.txt" 4

    touch "$TEST_DIR/old_log.log"
    set_mtime "$TEST_DIR/old_log.log" 5

    # Create recent files (younger than DEFAULT_AGE_DAYS=3)
    touch "$TEST_DIR/recent_report.pdf"
    set_mtime "$TEST_DIR/recent_report.pdf" 1

    touch "$TEST_DIR/current_data.json"
    set_mtime "$TEST_DIR/current_data.json" 0

    # Create empty directories
    mkdir -p "$TEST_DIR/echoing_vault"
    mkdir -p "$TEST_DIR/nested/empty_chamber"

    # Create non-empty directories
    mkdir -p "$TEST_DIR/data_archive"
    touch "$TEST_DIR/data_archive/important_file.zip"

    mkdir -p "$TEST_DIR/logs"
    touch "$TEST_DIR/logs/access.log"

    chmod +x "$SCRIPT_PATH"
}

teardown() {
    echo "Cleaning up test environment..."
    rm -rf "$TEST_DIR"
}

# --- Test Cases ---

test_help_message() {
    local output
    output=$("$SCRIPT_PATH" -h)
    assert_contains "$output" "Usage: detritus_duster.sh" "Should display help message with -h"
    assert_contains "$output" "--age <days>" "Help message should contain --age option"
}

test_report_mode() {
    echo "\n--- Running test_report_mode ---"
    local output
    output=$("$SCRIPT_PATH" "$TEST_DIR" 2>&1)

    assert_contains "$output" "Ancient Scrolls identified: 2" "Report mode should identify 2 old files"
    assert_contains "$output" "Echoing Vaults identified: 2" "Report mode should identify 2 empty directories"
    assert_contains "$output" "Identified file: '$TEST_DIR/ancient_scroll.txt'" "Report should list ancient_scroll.txt"
    assert_contains "$output" "Identified dir: '$TEST_DIR/echoing_vault'" "Report should list echoing_vault"
    assert_not_contains "$output" "recent_report.pdf" "Report should NOT list recent_report.pdf"
    assert_not_contains "$output" "data_archive" "Report should NOT list non-empty data_archive"

    # Verify no files were moved/deleted
    assert_equals "true" "$(test -f "$TEST_DIR/ancient_scroll.txt" && echo true || echo false)" "ancient_scroll.txt should still exist"
    assert_equals "true" "$(test -d "$TEST_DIR/echoing_vault" && echo true || echo false)" "echoing_vault should still exist"
}

test_quarantine_mode() {
    echo "\n--- Running test_quarantine_mode ---"
    local output
    output=$("$SCRIPT_PATH" -q "$TEST_DIR" 2>&1)

    assert_contains "$output" "Ancient Scrolls identified: 2" "Quarantine mode should identify 2 old files"
    assert_contains "$output" "Echoing Vaults identified: 2" "Quarantine mode should identify 2 empty directories"
    assert_contains "$output" "Quarantined file 'ancient_scroll.txt'" "Quarantine should report ancient_scroll.txt moved"
    assert_contains "$output" "Quarantined dir 'echoing_vault'" "Quarantine should report echoing_vault moved"

    # Verify files were moved to quarantine
    assert_equals "false" "$(test -f "$TEST_DIR/ancient_scroll.txt" && echo true || echo false)" "ancient_scroll.txt should NOT exist in original location"
    assert_equals "true" "$(test -f "$TEST_DIR/.digital_detritus_quarantine/ancient_scroll.txt" && echo true || echo false)" "ancient_scroll.txt should be in quarantine"

    assert_equals "false" "$(test -d "$TEST_DIR/echoing_vault" && echo true || echo false)" "echoing_vault should NOT exist in original location"
    assert_equals "true" "$(test -d "$TEST_DIR/.digital_detritus_quarantine/echoing_vault" && echo true || echo false)" "echoing_vault should be in quarantine"

    assert_equals "true" "$(test -f "$TEST_DIR/recent_report.pdf" && echo true || echo false)" "recent_report.pdf should still exist"
}

test_delete_mode() {
    echo "\n--- Running test_delete_mode ---"
    # Re-setup for delete test as quarantine modified the state
    teardown
    setup

    local output
    output=$("$SCRIPT_PATH" -d "$TEST_DIR" 2>&1)

    assert_contains "$output" "Ancient Scrolls identified: 2" "Delete mode should identify 2 old files"
    assert_contains "$output" "Echoing Vaults identified: 2" "Delete mode should identify 2 empty directories"
    assert_contains "$output" "Purged file 'ancient_scroll.txt'" "Delete should report ancient_scroll.txt purged"
    assert_contains "$output" "Purged dir 'echoing_vault'" "Delete should report echoing_vault purged"

    # Verify files were deleted
    assert_equals "false" "$(test -f "$TEST_DIR/ancient_scroll.txt" && echo true || echo false)" "ancient_scroll.txt should be deleted"
    assert_equals "false" "$(test -d "$TEST_DIR/echoing_vault" && echo true || echo false)" "echoing_vault should be deleted"

    assert_equals "true" "$(test -f "$TEST_DIR/recent_report.pdf" && echo true || echo false)" "recent_report.pdf should still exist"
}

test_custom_age_threshold() {
    echo "\n--- Running test_custom_age_threshold ---"
    # Re-setup for this test
    teardown
    setup

    # Create a file that is 2 days old
    touch "$TEST_DIR/medium_age_file.tmp"
    set_mtime "$TEST_DIR/medium_age_file.tmp" 2

    local output
    # Scan for files older than 1 day. This should include ancient_scroll.txt, old_log.log, and medium_age_file.tmp
    output=$("$SCRIPT_PATH" -a 1 "$TEST_DIR" 2>&1)

    assert_contains "$output" "Ancient Scrolls identified: 3" "Custom age (1 day) should identify 3 old files"
    assert_contains "$output" "Identified file: '$TEST_DIR/medium_age_file.tmp'" "Custom age should list medium_age_file.tmp"
    assert_not_contains "$output" "recent_report.pdf" "Custom age should NOT list recent_report.pdf"
}

# --- Run Tests ---

main() {
    setup
    test_help_message
    test_report_mode
    test_quarantine_mode
    test_delete_mode
    test_custom_age_threshold
    teardown
    echo "\nAll tests passed!"
}

main
