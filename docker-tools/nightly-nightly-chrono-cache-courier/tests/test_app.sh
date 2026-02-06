#!/bin/bash

# Mock rationale: We need to control the environment for deterministic tests,
# especially file system interactions and time-based cleaning.
# We'll use a temporary directory for the cache and manually set file modification times.

# Source the script to test its functions directly
. src/app.sh

# Setup a temporary cache directory for tests
TEST_CACHE_DIR="/tmp/chrono_cache_test_$(date +%s%N)"
export CACHE_DIR="$TEST_CACHE_DIR" # Override CACHE_DIR for tests
export CHRONO_RETENTION_HOURS=1 # Set retention to 1 hour for easier testing

# Override mkdir -p to ensure it uses our test dir when app.sh is sourced
mkdir() {
    if [[ "$1" == "/cache/notes" ]]; then
        command mkdir -p "$TEST_CACHE_DIR"
    else
        command mkdir "$@"
    fi
}

# Test setup
setup() {
    rm -rf "$TEST_CACHE_DIR"
    mkdir -p "$TEST_CACHE_DIR"
    # Re-initialize CACHE_DIR in app.sh context after cleanup
    mkdir -p "$CACHE_DIR"
}

# Test teardown
teardown() {
    rm -rf "$TEST_CACHE_DIR"
}

# Test add_note
test_add_note() {
    add_note "testkey1" "testvalue1" > /dev/null
    assertTrue "Note file should exist" "[ -f \"${TEST_CACHE_DIR}/testkey1\" ]"
    assertEquals "Note content should be correct" "testvalue1" "$(cat \"${TEST_CACHE_DIR}/testkey1\")"
}

# Test get_note
test_get_note() {
    echo "testvalue2" > "${TEST_CACHE_DIR}/testkey2"
    assertEquals "Retrieved note content should be correct" "testvalue2" "$(get_note \"testkey2\")"
    assertFalse "Getting non-existent note should fail" "get_note \"nonexistent\" 2>/dev/null"
}

# Test list_notes
test_list_notes() {
    add_note "testkeyA" "valueA" > /dev/null
    add_note "testkeyB" "valueB" > /dev/null
    local output=$(list_notes)
    assertTrue "List should contain testkeyA" "echo \"$output\" | grep -q 'testkeyA'"
    assertTrue "List should contain testkeyB" "echo \"$output\" | grep -q 'testkeyB'"
    
    # Test empty list
    rm -rf "$TEST_CACHE_DIR"/*
    output=$(list_notes)
    assertTrue "Empty list should indicate no notes" "echo \"$output\" | grep -q 'No active Chrono-Cache notes.'"
}

# Test clean_notes
test_clean_notes() {
    # Create a note that should be cleaned (older than 1 hour, as CHRONO_RETENTION_HOURS=1)
    add_note "old_note" "old_value" > /dev/null
    # Mock rationale: Manually setting file modification time to simulate an old file.
    # This ensures determinism for time-based cleaning. Using `date -r @<timestamp>` for portability.
    local two_hours_ago_sec=$(($(date +%s) - (2 * 3600)))
    touch -t "$(date -r @$two_hours_ago_sec +%Y%m%d%H%M.%S)" "${TEST_CACHE_DIR}/old_note"

    # Create a note that should NOT be cleaned (recent)
    add_note "recent_note" "recent_value" > /dev/null
    # Mock rationale: Manually setting file modification time to simulate a recent file.
    # This ensures determinism for time-based cleaning. Using `date -r @<timestamp>` for portability.
    local ten_minutes_ago_sec=$(($(date +%s) - (10 * 60)))
    touch -t "$(date -r @$ten_minutes_ago_sec +%Y%m%d%H%M.%S)" "${TEST_CACHE_DIR}/recent_note"

    clean_notes > /dev/null

    assertFalse "Old note should be removed" "[ -f \"${TEST_CACHE_DIR}/old_note\" ]"
    assertTrue "Recent note should remain" "[ -f \"${TEST_CACHE_DIR}/recent_note\" ]"
}

# Test help_message
test_help_message() {
    local output=$(help_message)
    assertTrue "Help message should contain Usage" "echo \"$output\" | grep -q 'Usage: chrono-cache-courier <command> [args]'"
    assertTrue "Help message should contain add command" "echo \"$output\" | grep -q 'add <key> <value>'"
}

# Load shunit2
. shunit2
