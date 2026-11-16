#!/bin/bash

# Test suite for Nightly Dust Bunny Sweeper

SCRIPT_PATH="./src/dust_bunny_sweeper.sh"
TEST_DIR="test_temp_dir"

# --- Helper functions for tests ---

setup_test_env() {
    rm -rf "$TEST_DIR"
    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR" || exit 1
    chmod +x "$SCRIPT_PATH" # Ensure script is executable for tests
}

cleanup_test_env() {
    cd - > /dev/null || exit 1 # Go back to original directory
    rm -rf "$TEST_DIR"
}

assert_contains() {
    local expected="$1"
    local actual="$2"
    if ! echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: Expected '$actual' to contain '$expected'"
        exit 1
    fi
}

assert_not_contains() {
    local expected="$1"
    local actual="$2"
    if echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: Expected '$actual' NOT to contain '$expected'"
        exit 1
    fi
}

assert_file_exists() {
    local file="$1"
    if [[ ! -e "$file" ]]; then
        echo "FAIL: Expected file '$file' to exist."
        exit 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    if [[ -e "$file" ]]; then
        echo "FAIL: Expected file '$file' NOT to exist."
        exit 1
    fi
}

# --- Test Cases ---

test_help_message() {
    setup_test_env
    echo "Running test: help message"
    output=$("$SCRIPT_PATH" --help)
    assert_contains "Usage: $0 [OPTIONS] [TARGET_DIRECTORY]" "$output"
    assert_contains "Find files not accessed in <days> days." "$output"
    cleanup_test_env
    echo "PASS: help message"
}

test_default_old_files_dry_run() {
    setup_test_env
    echo "Running test: default old files dry run"

    # Mock rationale: Create files with specific access times for deterministic testing.
    touch -a -d "2 days ago" old_file_recent.txt
    touch -a -d "31 days ago" old_file_ancient.txt
    mkdir -p sub_dir
    touch -a -d "32 days ago" sub_dir/another_ancient.log

    output=$("$SCRIPT_PATH" -a 30 .)
    assert_contains "Found 2 digital dust bunnies:" "$output"
    assert_contains "old_file_ancient.txt" "$output"
    assert_contains "sub_dir/another_ancient.log" "$output"
    assert_not_contains "old_file_recent.txt" "$output"
    assert_contains "Dry run complete. No changes were made." "$output"

    assert_file_exists "old_file_recent.txt"
    assert_file_exists "old_file_ancient.txt"
    assert_file_exists "sub_dir/another_ancient.log"

    cleanup_test_env
    echo "PASS: default old files dry run"
}

test_delete_old_files() {
    setup_test_env
    echo "Running test: delete old files"

    # Mock rationale: Create files with specific access times for deterministic testing.
    touch -a -d "2 days ago" keep_file.txt
    touch -a -d "31 days ago" delete_me.txt
    mkdir -p sub_dir
    touch -a -d "32 days ago" sub_dir/delete_me_too.log

    output=$("$SCRIPT_PATH" -a 30 -d .)
    assert_contains "Deleted: delete_me.txt" "$output"
    assert_contains "Deleted: sub_dir/delete_me_too.log" "$output"
    assert_not_contains "keep_file.txt" "$output"
    assert_contains "Cleanup complete." "$output"

    assert_file_exists "keep_file.txt"
    assert_file_not_exists "delete_me.txt"
    assert_file_not_exists "sub_dir/delete_me_too.log"

    cleanup_test_env
    echo "PASS: delete old files"
}

test_empty_directories_dry_run() {
    setup_test_env
    echo "Running test: empty directories dry run"

    mkdir -p empty_dir
    mkdir -p non_empty_dir
    touch non_empty_dir/file.txt
    mkdir -p nested_empty/another_empty

    output=$("$SCRIPT_PATH" -e .)
    assert_contains "Found 3 digital dust bunnies:" "$output"
    assert_contains "empty_dir" "$output"
    assert_contains "nested_empty" "$output"
    assert_contains "nested_empty/another_empty" "$output"
    assert_not_contains "non_empty_dir" "$output"
    assert_contains "Dry run complete. No changes were made." "$output"

    assert_file_exists "empty_dir"
    assert_file_exists "non_empty_dir"
    assert_file_exists "nested_empty/another_empty"

    cleanup_test_env
    echo "PASS: empty directories dry run"
}

test_delete_empty_directories() {
    setup_test_env
    echo "Running test: delete empty directories"

    mkdir -p empty_dir
    mkdir -p non_empty_dir
    touch non_empty_dir/file.txt
    mkdir -p nested_empty/another_empty

    output=$("$SCRIPT_PATH" -e -d .)
    assert_contains "Deleted: empty_dir" "$output"
    assert_contains "Deleted: nested_empty/another_empty" "$output"
    assert_contains "Deleted: nested_empty" "$output" # Parent empty dir should be deleted after child
    assert_not_contains "non_empty_dir" "$output"
    assert_contains "Cleanup complete." "$output"

    assert_file_not_exists "empty_dir"
    assert_file_exists "non_empty_dir"
    assert_file_not_exists "nested_empty/another_empty"
    assert_file_not_exists "nested_empty"

    cleanup_test_env
    echo "PASS: delete empty directories"
}

test_broken_symlinks_dry_run() {
    setup_test_env
    echo "Running test: broken symlinks dry run"

    touch existing_file.txt
    ln -s existing_file.txt good_link.txt
    ln -s non_existent_target.txt broken_link.txt
    mkdir -p sub_dir
    ln -s ../another_non_existent.txt sub_dir/another_broken_link.txt

    output=$("$SCRIPT_PATH" -b .)
    assert_contains "Found 2 digital dust bunnies:" "$output"
    assert_contains "broken_link.txt" "$output"
    assert_contains "sub_dir/another_broken_link.txt" "$output"
    assert_not_contains "good_link.txt" "$output"
    assert_contains "Dry run complete. No changes were made." "$output"

    assert_file_exists "broken_link.txt"
    assert_file_exists "sub_dir/another_broken_link.txt"

    cleanup_test_env
    echo "PASS: broken symlinks dry run"
}

test_delete_broken_symlinks() {
    setup_test_env
    echo "Running test: delete broken symlinks"

    touch existing_file.txt
    ln -s existing_file.txt good_link.txt
    ln -s non_existent_target.txt broken_link.txt
    mkdir -p sub_dir
    ln -s ../another_non_existent.txt sub_dir/another_broken_link.txt

    output=$("$SCRIPT_PATH" -b -d .)
    assert_contains "Deleted: broken_link.txt" "$output"
    assert_contains "Deleted: sub_dir/another_broken_link.txt" "$output"
    assert_not_contains "good_link.txt" "$output"
    assert_contains "Cleanup complete." "$output"

    assert_file_not_exists "broken_link.txt"
    assert_file_not_exists "sub_dir/another_broken_link.txt"
    assert_file_exists "good_link.txt" # Good link should remain

    cleanup_test_env
    echo "PASS: delete broken symlinks"
}

test_combined_dry_run() {
    setup_test_env
    echo "Running test: combined dry run"

    # Old file
    touch -a -d "31 days ago" old_file.txt
    # Empty dir
    mkdir -p empty_dir
    # Broken link
    ln -s non_existent.txt broken_link.txt
    # Keep file
    touch -a -d "1 day ago" recent_file.txt
    # Non-empty dir
    mkdir -p non_empty_dir
    touch non_empty_dir/file.txt
    # Good link
    ln -s recent_file.txt good_link.txt

    output=$("$SCRIPT_PATH" -a 30 -e -b .)
    assert_contains "Found 3 digital dust bunnies:" "$output"
    assert_contains "old_file.txt" "$output"
    assert_contains "empty_dir" "$output"
    assert_contains "broken_link.txt" "$output"
    assert_not_contains "recent_file.txt" "$output"
    assert_not_contains "non_empty_dir" "$output"
    assert_not_contains "good_link.txt" "$output"
    assert_contains "Dry run complete. No changes were made." "$output"

    assert_file_exists "old_file.txt"
    assert_file_exists "empty_dir"
    assert_file_exists "broken_link.txt"

    cleanup_test_env
    echo "PASS: combined dry run"
}

test_combined_delete() {
    setup_test_env
    echo "Running test: combined delete"

    # Old file
    touch -a -d "31 days ago" old_file.txt
    # Empty dir
    mkdir -p empty_dir
    # Broken link
    ln -s non_existent.txt broken_link.txt
    # Keep file
    touch -a -d "1 day ago" recent_file.txt
    # Non-empty dir
    mkdir -p non_empty_dir
    touch non_empty_dir/file.txt
    # Good link
    ln -s recent_file.txt good_link.txt

    output=$("$SCRIPT_PATH" -a 30 -e -b -d .)
    assert_contains "Deleted: old_file.txt" "$output"
    assert_contains "Deleted: empty_dir" "$output"
    assert_contains "Deleted: broken_link.txt" "$output"
    assert_contains "Cleanup complete." "$output"

    assert_file_not_exists "old_file.txt"
    assert_file_not_exists "empty_dir"
    assert_file_not_exists "broken_link.txt"
    assert_file_exists "recent_file.txt"
    assert_file_exists "non_empty_dir"
    assert_file_exists "good_link.txt"

    cleanup_test_env
    echo "PASS: combined delete"
}

test_interactive_delete() {
    setup_test_env
    echo "Running test: interactive delete (simulated input)"

    touch -a -d "31 days ago" old_file_interactive.txt
    mkdir -p empty_dir_interactive

    # Mock rationale: Simulate user input for interactive mode using a here-string.
    # 'y' for the first item, 'n' for the second.
    output=$(echo -e "y\nn" | "$SCRIPT_PATH" -a 30 -e -d -i .)

    assert_contains "Delete 'old_file_interactive.txt'? (y/N)" "$output"
    assert_contains "Deleted: old_file_interactive.txt" "$output"
    assert_contains "Delete 'empty_dir_interactive'? (y/N)" "$output"
    assert_contains "Skipped: empty_dir_interactive" "$output"

    assert_file_not_exists "old_file_interactive.txt"
    assert_file_exists "empty_dir_interactive"

    cleanup_test_env
    echo "PASS: interactive delete"
}

test_no_findings() {
    setup_test_env
    echo "Running test: no findings"

    touch -a -d "1 day ago" recent_file.txt
    mkdir -p non_empty_dir
    touch non_empty_dir/file.txt
    ln -s recent_file.txt good_link.txt

    output=$("$SCRIPT_PATH" -a 30 -e -b .)
    assert_contains "No digital dust bunnies found. Your digital space is sparkling clean!" "$output"
    assert_not_contains "Found" "$output"

    cleanup_test_env
    echo "PASS: no findings"
}

# --- Run all tests ---
echo "--- Starting Nightly Dust Bunny Sweeper Tests ---"
test_help_message
test_default_old_files_dry_run
test_delete_old_files
test_empty_directories_dry_run
test_delete_empty_directories
test_broken_symlinks_dry_run
test_delete_broken_symlinks
test_combined_dry_run
test_combined_delete
test_interactive_delete
test_no_findings
echo "--- All tests passed! ---"
