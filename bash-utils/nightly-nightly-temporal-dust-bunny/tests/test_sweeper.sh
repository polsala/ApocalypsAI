#!/bin/bash

# Test script for nightly-temporal-dust-bunny-sweeper

SCRIPT_PATH="$(dirname "$0")"/../src/temporal_dust_bunny_sweeper.sh

# Setup a temporary test environment
setup_test_env() {
    TEST_DIR=$(mktemp -d -t dust-bunny-XXXXXX)
    export TEST_DIR # Make it available to subshells if needed
    echo "Created test directory: $TEST_DIR"

    # Create some files with different ages relative to now
    # Mock rationale: `touch -t` allows creating files with specific modification times,
    # making `find -mtime` behavior deterministic for testing purposes.
    touch -t $(date +%Y%m%d%H%M -d "90 days ago") "$TEST_DIR/old_file_1.txt" 
    touch -t $(date +%Y%m%d%H%M -d "91 days ago") "$TEST_DIR/old_file_2.log"
    touch -t $(date +%Y%m%d%H%M -d "45 days ago") "$TEST_DIR/medium_file.data"
    touch -t $(date +%Y%m%d%H%M -d "31 days ago") "$TEST_DIR/exactly_31_days_old.txt"
    touch -t $(date +%Y%m%d%H%M -d "29 days ago") "$TEST_DIR/exactly_29_days_old.txt"
    touch -t $(date +%Y%m%d%H%M -d "11 days ago") "$TEST_DIR/exactly_11_days_old.txt"
    touch -t $(date +%Y%m%d%H%M -d "9 days ago") "$TEST_DIR/exactly_9_days_old.txt"
    touch -t $(date +%Y%m%d%H%M -d "yesterday") "$TEST_DIR/recent_file.tmp"
    touch -t $(date +%Y%m%d%H%M) "$TEST_DIR/current_file.txt"

    # Create a subdirectory with files
    mkdir -p "$TEST_DIR/subdir"
    touch -t $(date +%Y%m%d%H%M -d "60 days ago") "$TEST_DIR/subdir/old_sub_file.txt"
    touch -t $(date +%Y%m%d%H%M -d "5 days ago") "$TEST_DIR/subdir/recent_sub_file.txt"
}

# Cleanup the temporary test environment
cleanup_test_env() {
    if [ -d "$TEST_DIR" ]; then
        echo "Cleaning up test directory: $TEST_DIR"
        rm -rf "$TEST_DIR"
    fi
}

# Run a test case
run_test() {
    local name="$1"
    local command="$2"
    local expected_exit_code="$3"
    local file_check_mode="$4" # "present" or "absent"
    shift 4 # Shift arguments to get remaining files for checking and output regexes

    local expected_output_regexes=()
    local files_to_check=()

    # Separate output regexes from files to check
    local parsing_files=false
    for arg in "$@"; do
        if [[ "$arg" == "--files-to-check" ]]; then
            parsing_files=true
            continue
        fi
        if "$parsing_files"; then
            files_to_check+=("$arg")
        else
            expected_output_regexes+=("$arg")
        fi
    done

    echo "--- Running Test: $name ---"
    output=$(eval "$command" 2>&1)
    exit_code=$?

    if [ "$exit_code" -ne "$expected_exit_code" ]; then
        echo "FAIL: $name - Expected exit code $expected_exit_code, got $exit_code"
        echo "Output: $output"
        ALL_TESTS_PASSED=false
        return 1
    fi

    for regex in "${expected_output_regexes[@]}"; do
        if [[ ! "$output" =~ $regex ]]; then
            echo "FAIL: $name - Output mismatch for regex: '$regex'"
            echo "Actual output: $output"
            ALL_TESTS_PASSED=false
            return 1
        fi
    done

    if [ -n "$file_check_mode" ]; then
        local file_status_ok=true
        for file_to_check in "${files_to_check[@]}"; do
            local full_path="$TEST_DIR/$file_to_check"
            if [ "$file_check_mode" = "absent" ]; then
                if [ -f "$full_path" ]; then
                    echo "FAIL: $name - File '$file_to_check' should be absent but is present."
                    file_status_ok=false
                fi
            elif [ "$file_check_mode" = "present" ]; then
                if [ ! -f "$full_path" ]; then
                    echo "FAIL: $name - File '$file_to_check' should be present but is absent."
                    file_status_ok=false
                fi
            fi
        done
        if ! "$file_status_ok"; then
            ALL_TESTS_PASSED=false
            return 1
        fi
    fi

    echo "PASS: $name"
    return 0
}

# --- Test Cases ---
ALL_TESTS_PASSED=true

# Test 1: No arguments, should show usage and exit 1
setup_test_env
run_test "No arguments (usage)" "$SCRIPT_PATH" 1 "" \
    "Usage: .*temporal_dust_bunny_sweeper.sh"
cleanup_test_env

# Test 2: Invalid directory, should exit 1
setup_test_env
run_test "Invalid directory" "$SCRIPT_PATH /nonexistent_dir" 1 "" \
    "Error: Directory '/nonexistent_dir' not found."
cleanup_test_env

# Test 3: Dry run, default 30 days, should find 5 old files
setup_test_env
run_test "Dry run, default 30 days" "$SCRIPT_PATH \"$TEST_DIR\"" 0 "present" \
    "Detected 5 temporal dust bunnies:" "This was a dry run" \
    "--files-to-check" "old_file_1.txt" "old_file_2.log" "medium_file.data" "exactly_31_days_old.txt" "exactly_29_days_old.txt" "exactly_11_days_old.txt" "exactly_9_days_old.txt" "recent_file.tmp" "current_file.txt" "subdir/old_sub_file.txt" "subdir/recent_sub_file.txt"
if [ $? -ne 0 ]; then ALL_TESTS_PASSED=false; fi
cleanup_test_env

# Test 4: Dry run, 10 days, should find 6 files
setup_test_env
run_test "Dry run, 10 days" "$SCRIPT_PATH -d 10 \"$TEST_DIR\"" 0 "present" \
    "Detected 6 temporal dust bunnies:" "This was a dry run" \
    "--files-to-check" "old_file_1.txt" "old_file_2.log" "medium_file.data" "exactly_31_days_old.txt" "exactly_29_days_old.txt" "exactly_11_days_old.txt" "exactly_9_days_old.txt" "recent_file.tmp" "current_file.txt" "subdir/old_sub_file.txt" "subdir/recent_sub_file.txt"
if [ $? -ne 0 ]; then ALL_TESTS_PASSED=false; fi
cleanup_test_env

# Test 5: Execute deletion, default 30 days
setup_test_env
run_test "Execute deletion, default 30 days" "$SCRIPT_PATH -x \"$TEST_DIR\"" 0 "absent" \
    "Sweeping away ancient digital detritus..." "Temporal dust bunnies successfully swept!" \
    "--files-to-check" "old_file_1.txt" "old_file_2.log" "medium_file.data" "exactly_31_days_old.txt" "subdir/old_sub_file.txt"
if [ $? -ne 0 ]; then ALL_TESTS_PASSED=false; fi
run_test "Verify remaining files after deletion" "true" 0 "present" \
    "--files-to-check" "exactly_29_days_old.txt" "exactly_11_days_old.txt" "exactly_9_days_old.txt" "recent_file.tmp" "current_file.txt" "subdir/recent_sub_file.txt"
if [ $? -ne 0 ]; then ALL_TESTS_PASSED=false; fi
cleanup_test_env

# Test 6: Verbose dry run, default 30 days, should list files
setup_test_env
run_test "Verbose dry run, default 30 days" "$SCRIPT_PATH -v \"$TEST_DIR\"" 0 "present" \
    "Detected 5 temporal dust bunnies:" "This was a dry run" \
    ".*old_file_1.txt" ".*old_file_2.log" ".*medium_file.data" ".*exactly_31_days_old.txt" ".*subdir/old_sub_file.txt" \
    "--files-to-check" "old_file_1.txt" "old_file_2.log" "medium_file.data" "exactly_31_days_old.txt" "exactly_29_days_old.txt" "exactly_11_days_old.txt" "exactly_9_days_old.txt" "recent_file.tmp" "current_file.txt" "subdir/old_sub_file.txt" "subdir/recent_sub_file.txt"
if [ $? -ne 0 ]; then ALL_TESTS_PASSED=false; fi
cleanup_test_env

# Test 7: No dust bunnies found (high age threshold)
setup_test_env
run_test "No dust bunnies found (high age)" "$SCRIPT_PATH -d 1000 \"$TEST_DIR\"" 0 "present" \
    "No temporal dust bunnies detected. Your digital realm is pristine!" \
    "--files-to-check" "old_file_1.txt" "old_file_2.log" "medium_file.data" "exactly_31_days_old.txt" "exactly_29_days_old.txt" "exactly_11_days_old.txt" "exactly_9_days_old.txt" "recent_file.tmp" "current_file.txt" "subdir/old_sub_file.txt" "subdir/recent_sub_file.txt"
if [ $? -ne 0 ]; then ALL_TESTS_PASSED=false; fi
cleanup_test_env

# Final result
if "$ALL_TESTS_PASSED"; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed!"
    exit 1
fi
