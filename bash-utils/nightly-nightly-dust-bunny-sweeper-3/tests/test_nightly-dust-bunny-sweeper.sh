#!/bin/bash

SCRIPT_PATH="../src/nightly-dust-bunny-sweeper.sh"

# --- Test Helper Functions ---

TEST_DIR=""

# Mock rationale: `mktemp` is a standard utility and its behavior is deterministic.
# It creates a unique temporary directory, which is essential for isolated tests.
setup_test_env() {
    TEST_DIR=$(mktemp -d -t dust-bunny-test-XXXXXX)
    export HOME="$TEST_DIR" # Isolate HOME for .cache and .local/share/Trash
    mkdir -p "${HOME}/.cache"
    mkdir -p "${HOME}/.local/share/Trash/files"
    echo "Test environment setup in: $TEST_DIR"
}

cleanup_test_env() {
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
        echo "Test environment cleaned up: $TEST_DIR"
    fi
}

create_file() {
    local path="$1"
    local age_days="$2"
    mkdir -p "$(dirname "$path")"
    touch "$path"
    if [[ -n "$age_days" ]]; then
        # Mock rationale: `touch` is a standard utility and its behavior is deterministic.
        # It's used to set file modification times for testing age-based filtering.
        touch -d "$age_days days ago" "$path"
    fi
}

assert_output_contains() {
    local output="$1"
    local expected="$2"
    if ! echo "$output" | grep -qF "$expected"; then
        echo "FAIL: Expected output to contain '$expected', but it did not."
        echo "Output: $output"
        return 1
    fi
    return 0
}

assert_output_not_contains() {
    local output="$1"
    local unexpected="$2"
    if echo "$output" | grep -qF "$unexpected"; then
        echo "FAIL: Expected output NOT to contain '$unexpected', but it did."
        echo "Output: $output"
        return 1
    fi
    return 0
}

assert_file_exists() {
    local path="$1"
    if [[ ! -e "$path" ]]; then
        echo "FAIL: Expected file/directory to exist: $path"
        return 1
    fi
    return 0
}

assert_file_not_exists() {
    local path="$1"
    if [[ -e "$path" ]]; then
        echo "FAIL: Expected file/directory NOT to exist: $path"
        return 1
    fi
    return 0
}

run_test() {
    local test_name="$1"
    shift
    echo "--- Running Test: $test_name ---"
    setup_test_env
    if "$@"; then
        echo "PASS: $test_name"
        cleanup_test_env
        return 0
    else
        echo "FAIL: $test_name"
        cleanup_test_env
        return 1
    fi
}

# --- Test Cases ---

test_dry_run_default_paths_and_age() {
    create_file "${HOME}/.cache/old_cache_file.txt" 10
    create_file "${HOME}/.cache/new_cache_file.txt" 1
    create_file "${HOME}/.local/share/Trash/files/old_trash.log" 10
    create_file "${HOME}/.local/share/Trash/files/new_trash.log" 1
    mkdir -p "${HOME}/.cache/empty_dir"
    mkdir -p "${HOME}/.cache/non_empty_dir"
    create_file "${HOME}/.cache/non_empty_dir/file.txt" 1

    # Mock rationale: The script is executed in a controlled test environment.
    # Its output is captured and analyzed, making the test deterministic and offline.
    output=$("$SCRIPT_PATH" -p "${HOME}/.cache" -p "${HOME}/.local/share/Trash/files" -a 7)

    assert_output_contains "$output" "old_cache_file.txt" || return 1
    assert_output_not_contains "$output" "new_cache_file.txt" || return 1
    assert_output_contains "$output" "old_trash.log" || return 1
    assert_output_not_contains "$output" "new_trash.log" || return 1
    assert_output_contains "$output" "empty_dir (empty directory)" || return 1
    assert_output_not_contains "$output" "non_empty_dir" || return 1
    return 0
}

test_cleanup_mode_with_confirmation() {
    create_file "${HOME}/.cache/old_file_to_delete.txt" 10
    create_file "${HOME}/.cache/new_file_to_keep.txt" 1
    mkdir -p "${HOME}/.cache/empty_dir_to_delete"

    # Mock rationale: `echo "y"` pipes 'y' to stdin, simulating user confirmation.
    # This makes the interactive part of the script deterministic for testing.
    output=$(echo "y" | "$SCRIPT_PATH" -c -p "${HOME}/.cache" -a 7)

    assert_output_contains "$output" "Swept: ${HOME}/.cache/old_file_to_delete.txt" || return 1
    assert_output_contains "$output" "Swept: ${HOME}/.cache/empty_dir_to_delete" || return 1
    assert_output_not_contains "$output" "Swept: ${HOME}/.cache/new_file_to_keep.txt" || return 1

    assert_file_not_exists "${HOME}/.cache/old_file_to_delete.txt" || return 1
    assert_file_exists "${HOME}/.cache/new_file_to_keep.txt" || return 1
    assert_file_not_exists "${HOME}/.cache/empty_dir_to_delete" || return 1
    return 0
}

test_force_cleanup_mode() {
    create_file "${HOME}/.cache/old_file_to_force_delete.txt" 10
    mkdir -p "${HOME}/.cache/empty_dir_to_force_delete"

    # Mock rationale: Running with -f bypasses interactive confirmation, making the test deterministic.
    output=$("$SCRIPT_PATH" -f -p "${HOME}/.cache" -a 7)

    assert_output_contains "$output" "Swept: ${HOME}/.cache/old_file_to_force_delete.txt" || return 1
    assert_output_contains "$output" "Swept: ${HOME}/.cache/empty_dir_to_force_delete" || return 1

    assert_file_not_exists "${HOME}/.cache/old_file_to_force_delete.txt" || return 1
    assert_file_not_exists "${HOME}/.cache/empty_dir_to_force_delete" || return 1
    return 0
}

test_keep_empty_directories() {
    create_file "${HOME}/.cache/old_file_to_delete.txt" 10
    mkdir -p "${HOME}/.cache/empty_dir_to_keep"

    # Mock rationale: `echo "y"` pipes 'y' to stdin, simulating user confirmation.
    # This makes the interactive part of the script deterministic for testing.
    output=$(echo "y" | "$SCRIPT_PATH" -c -k -p "${HOME}/.cache" -a 7)

    assert_output_contains "$output" "Swept: ${HOME}/.cache/old_file_to_delete.txt" || return 1
    assert_output_not_contains "$output" "empty_dir_to_keep" || return 1 # Should not be listed for deletion

    assert_file_not_exists "${HOME}/.cache/old_file_to_delete.txt" || return 1
    assert_file_exists "${HOME}/.cache/empty_dir_to_keep" || return 1
    return 0
}

test_no_dust_bunnies_found() {
    create_file "${HOME}/.cache/new_file.txt" 1
    mkdir -p "${HOME}/.cache/non_empty_dir"
    create_file "${HOME}/.cache/non_empty_dir/file.txt" 1

    output=$("$SCRIPT_PATH" -p "${HOME}/.cache" -a 7)

    assert_output_contains "$output" "No dust bunnies found to sweep. Your digital space is sparkling!" || return 1
    assert_output_not_contains "$output" "Swept:" || return 1
    return 0
}

test_invalid_path_handling() {
    output=$("$SCRIPT_PATH" -p "/non/existent/path" -a 7)
    assert_output_contains "$output" "Path not found or not a directory, skipping: /non/existent/path" || return 1
    return 0
}

test_usage_message() {
    output=$("$SCRIPT_PATH" -h)
    assert_output_contains "$output" "Nightly Digital Dust Bunny Sweeper" || return 1
    assert_output_contains "$output" "Usage: $0 [OPTIONS]" || return 1
    return 0
}

# --- Run all tests ---
ALL_TESTS_PASSED=true

run_test "Dry Run Default Paths and Age" test_dry_run_default_paths_and_age || ALL_TESTS_PASSED=false
run_test "Cleanup Mode with Confirmation" test_cleanup_mode_with_confirmation || ALL_TESTS_PASSED=false
run_test "Force Cleanup Mode" test_force_cleanup_mode || ALL_TESTS_PASSED=false
run_test "Keep Empty Directories" test_keep_empty_directories || ALL_TESTS_PASSED=false
run_test "No Dust Bunnies Found" test_no_dust_bunnies_found || ALL_TESTS_PASSED=false
run_test "Invalid Path Handling" test_invalid_path_handling || ALL_TESTS_PASSED=false
run_test "Usage Message" test_usage_message || ALL_TESTS_PASSED=false

if $ALL_TESTS_PASSED; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
