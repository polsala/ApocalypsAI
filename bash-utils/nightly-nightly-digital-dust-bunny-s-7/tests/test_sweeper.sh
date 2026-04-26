#!/bin/bash

# Automated tests for nightly-digital-dust-bunny-sweeper

# Mock rationale: These tests create actual temporary files and directories
# with specific timestamps using `mktemp` and `touch -d`. This provides a
# deterministic and offline environment for `find` to operate, effectively
# mocking the real filesystem state without needing complex `find` command mocking.

SCRIPT_PATH="$(dirname "$0")"/../src/dust_bunny_sweeper.sh

# Function to run a test
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_output_regex="$3"
    local unexpected_output_regex="$4"
    local temp_dir="$5"

    echo "Running test: $test_name"
    output=$(eval "$command" 2>&1)
    exit_code=$?

    if [[ $exit_code -ne 0 ]]; then
        echo "FAIL: $test_name - Script exited with error code $exit_code."
        echo "Output:" >&2
        echo "$output" >&2
        return 1
    fi

    if [[ "$output" =~ $expected_output_regex ]]; then
        echo "  PASS: Expected output found."
    else
        echo "FAIL: $test_name - Expected output not found."
        echo "  Expected regex: '$expected_output_regex'"
        echo "  Actual output: '$output'"
        return 1
    fi

    if [[ -n "$unexpected_output_regex" && "$output" =~ $unexpected_output_regex ]]; then
        echo "FAIL: $test_name - Unexpected output found."
        echo "  Unexpected regex: '$unexpected_output_regex'"
        echo "  Actual output: '$output'"
        return 1
    else
        echo "  PASS: Unexpected output not found (or not specified)."
    fi
    return 0
}

# --- Test Cases ---

# Test 1: Basic scan, find old file and directory
TEMP_DIR_1=$(mktemp -d)
OLD_FILE_1="$TEMP_DIR_1/old_file.txt"
OLD_DIR_1="$TEMP_DIR_1/old_dir"
NEW_FILE_1="$TEMP_DIR_1/new_file.txt"
NEW_DIR_1="$TEMP_DIR_1/new_dir"

# Create old items (100 days old)
touch -d "100 days ago" "$OLD_FILE_1"
mkdir "$OLD_DIR_1"
touch -d "100 days ago" "$OLD_DIR_1"

# Create new items (1 day old)
touch -d "1 day ago" "$NEW_FILE_1"
mkdir "$NEW_DIR_1"
touch -d "1 day ago" "$NEW_DIR_1"

TEST_COMMAND_1="$SCRIPT_PATH --path $TEMP_DIR_1 --age-days 90"
EXPECTED_REGEX_1=".*Digital Dust Bunnies.*$OLD_FILE_1.*Forgotten Cobwebs.*$OLD_DIR_1.*"
UNEXPECTED_REGEX_1=".*new_file.txt.*|.*new_dir.*"

run_test "Basic scan for old items" "$TEST_COMMAND_1" "$EXPECTED_REGEX_1" "$UNEXPECTED_REGEX_1"
RESULT_1=$?

# Test 2: No old items found
TEMP_DIR_2=$(mktemp -d)
NEW_FILE_2="$TEMP_DIR_2/new_file_2.txt"
NEW_DIR_2="$TEMP_DIR_2/new_dir_2"

touch -d "1 day ago" "$NEW_FILE_2"
mkdir "$NEW_DIR_2"
touch -d "1 day ago" "$NEW_DIR_2"

TEST_COMMAND_2="$SCRIPT_PATH --path $TEMP_DIR_2 --age-days 90"
EXPECTED_REGEX_2=".*Your digital space is sparkling clean! No dust bunnies or cobwebs found.*"
UNEXPECTED_REGEX_2=".*Digital Dust Bunnies.*|.*Forgotten Cobwebs.*"

run_test "No old items found" "$TEST_COMMAND_2" "$EXPECTED_REGEX_2" "$UNEXPECTED_REGEX_2"
RESULT_2=$?

# Test 3: Exclude pattern works
TEMP_DIR_3=$(mktemp -d)
OLD_FILE_3="$TEMP_DIR_3/old_file_3.txt"
EXCLUDED_DIR_3="$TEMP_DIR_3/node_modules"
EXCLUDED_FILE_3="$EXCLUDED_DIR_3/old_excluded.js"

touch -d "100 days ago" "$OLD_FILE_3"
mkdir "$EXCLUDED_DIR_3"
touch -d "100 days ago" "$EXCLUDED_DIR_3"
touch -d "100 days ago" "$EXCLUDED_FILE_3"

TEST_COMMAND_3="$SCRIPT_PATH --path $TEMP_DIR_3 --age-days 90 --exclude node_modules"
EXPECTED_REGEX_3=".*Digital Dust Bunnies.*$OLD_FILE_3.*"
UNEXPECTED_REGEX_3=".*node_modules.*"

run_test "Exclude pattern works" "$TEST_COMMAND_3" "$EXPECTED_REGEX_3" "$UNEXPECTED_REGEX_3"
RESULT_3=$?

# Test 4: Suggest commands output
TEMP_DIR_4=$(mktemp -d)
OLD_FILE_4="$TEMP_DIR_4/old_file_4.txt"
OLD_DIR_4="$TEMP_DIR_4/old_dir_4"

touch -d "100 days ago" "$OLD_FILE_4"
mkdir "$OLD_DIR_4"
touch -d "100 days ago" "$OLD_DIR_4"

TEST_COMMAND_4="$SCRIPT_PATH --path $TEMP_DIR_4 --age-days 90 --suggest-commands"
EXPECTED_REGEX_4=".*Suggested command: rm -f '$OLD_FILE_4'.*Suggested command: rm -rf '$OLD_DIR_4'.*"
UNEXPECTED_REGEX_4=""

run_test "Suggest commands output" "$TEST_COMMAND_4" "$EXPECTED_REGEX_4" "$UNEXPECTED_REGEX_4"
RESULT_4=$?

# Test 5: Invalid age-days input
TEMP_DIR_5=$(mktemp -d)
TEST_COMMAND_5="$SCRIPT_PATH --path $TEMP_DIR_5 --age-days abc"
EXPECTED_REGEX_5=".*Error: --age-days must be a positive integer.*"

# This test expects an error, so we need to check stderr and exit code
output=$(eval "$TEST_COMMAND_5" 2>&1)
exit_code=$?

if [[ $exit_code -ne 0 && "$output" =~ $EXPECTED_REGEX_5 ]]; then
    echo "Running test: Invalid age-days input"
    echo "  PASS: Script exited with error and correct message."
    RESULT_5=0
else
    echo "Running test: Invalid age-days input"
    echo "FAIL: Expected script to exit with error and message, but got:"
    echo "  Exit code: $exit_code"
    echo "  Output: '$output'"
    RESULT_5=1
fi

# Test 6: Invalid path input
TEMP_DIR_6=$(mktemp -d)
TEST_COMMAND_6="$SCRIPT_PATH --path $TEMP_DIR_6/non_existent_dir --age-days 90"
EXPECTED_REGEX_6=".*Error: Scan path '$TEMP_DIR_6/non_existent_dir' is not a valid directory.*"

# This test expects an error, so we need to check stderr and exit code
output=$(eval "$TEST_COMMAND_6" 2>&1)
exit_code=$?

if [[ $exit_code -ne 0 && "$output" =~ $EXPECTED_REGEX_6 ]]; then
    echo "Running test: Invalid path input"
    echo "  PASS: Script exited with error and correct message."
    RESULT_6=0
else
    echo "Running test: Invalid path input"
    echo "FAIL: Expected script to exit with error and message, but got:"
    echo "  Exit code: $exit_code"
    echo "  Output: '$output'"
    RESULT_6=1
fi

# Clean up temporary directories
rm -rf "$TEMP_DIR_1" "$TEMP_DIR_2" "$TEMP_DIR_3" "$TEMP_DIR_4" "$TEMP_DIR_5" "$TEMP_DIR_6"

# Final summary
TOTAL_FAILURES=0
(( RESULT_1 != 0 )) && (( TOTAL_FAILURES++ ))
(( RESULT_2 != 0 )) && (( TOTAL_FAILURES++ ))
(( RESULT_3 != 0 )) && (( TOTAL_FAILURES++ ))
(( RESULT_4 != 0 )) && (( TOTAL_FAILURES++ ))
(( RESULT_5 != 0 )) && (( TOTAL_FAILURES++ ))
(( RESULT_6 != 0 )) && (( TOTAL_FAILURES++ ))

if [[ $TOTAL_FAILURES -eq 0 ]]; then
    echo "\nAll tests passed! 🎉"
    exit 0
else
    echo "\n$TOTAL_FAILURES test(s) failed. 🧹"
    exit 1
fi
