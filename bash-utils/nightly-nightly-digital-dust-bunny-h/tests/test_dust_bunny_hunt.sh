#!/bin/bash

# Test setup
TEST_DIR=$(mktemp -d)
ARCHIVE_TEST_DIR=$(mktemp -d)
SCRIPT_PATH="$(dirname "$0")/../src/dust_bunny_hunt.sh"

# Mock command variables
MOCKED_FIND_OUTPUT=""
MOCKED_TOUCH_CALLS=()
MOCKED_MV_CALLS=()
MOCKED_MKDIR_CALLS=()

# Helper function to reset mocks
reset_mocks() {
    MOCKED_FIND_OUTPUT=""
    MOCKED_TOUCH_CALLS=()
    MOCKED_MV_CALLS=()
    MOCKED_MKDIR_CALLS=()
}

# Helper function to run the script with mocked commands
run_script() {
    # Create a temporary mock bin directory
    local MOCK_BIN=$(mktemp -d)
    export PATH="$MOCK_BIN:$PATH"

    # Create mock executables
    echo '#!/bin/bash' > "$MOCK_BIN/find"
    echo 'echo "$MOCKED_FIND_OUTPUT"' >> "$MOCK_BIN/find"
    chmod +x "$MOCK_BIN/find"
    # Mock rationale: `find` is mocked to return predefined output, avoiding actual filesystem traversal for deterministic tests.

    echo '#!/bin/bash' > "$MOCK_BIN/touch"
    echo 'MOCKED_TOUCH_CALLS+=("$@")' >> "$MOCK_BIN/touch"
    chmod +x "$MOCK_BIN/touch"
    # Mock rationale: `touch` is mocked to record its arguments, allowing verification of calls without modifying real timestamps.

    echo '#!/bin/bash' > "$MOCK_BIN/mv"
    echo 'MOCKED_MV_CALLS+=("$@")' >> "$MOCK_BIN/mv"
    chmod +x "$MOCK_BIN/mv"
    # Mock rationale: `mv` is mocked to record its arguments, allowing verification of calls without moving real files.

    echo '#!/bin/bash' > "$MOCK_BIN/mkdir"
    echo 'MOCKED_MKDIR_CALLS+=("$@")' >> "$MOCK_BIN/mkdir"
    chmod +x "$MOCK_BIN/mkdir"
    # Mock rationale: `mkdir` is mocked to record its arguments, allowing verification of calls without creating real directories.

    # Now run the actual script
    local output
    output=$("$SCRIPT_PATH" "$@" 2>&1)
    local status=$?

    # Clean up mock bin
    rm -rf "$MOCK_BIN"
    
    echo "$output"
    return $status
}

# Test cases

# Test 1: No arguments - should show usage and exit with error
test_no_args() {
    reset_mocks
    echo "Running test: No arguments"
    output=$(run_script)
    if [[ $? -eq 1 && "$output" == *"Usage: "* ]]; then
        echo "PASS: No arguments shows usage."
    else
        echo "FAIL: No arguments did not show usage or exit with error."
        echo "Output: $output"
        exit 1
    fi
}

# Test 2: Invalid action
test_invalid_action() {
    reset_mocks
    echo "Running test: Invalid action"
    output=$(run_script -x "invalid")
    if [[ $? -eq 1 && "$output" == *"Error: Invalid action"* ]]; then
        echo "PASS: Invalid action handled correctly."
    else
        echo "FAIL: Invalid action not handled."
        echo "Output: $output"
        exit 1
    fi
}

# Test 3: Report action - no files found
test_report_no_files() {
    reset_mocks
    echo "Running test: Report action - no files found"
    MOCKED_FIND_OUTPUT="" # No files
    output=$(run_script -d "$TEST_DIR" -a 10 -x "report")
    if [[ $? -eq 0 && "$output" == *"No digital dust bunnies found"* ]]; then
        echo "PASS: Report action with no files found."
    else
        echo "FAIL: Report action with no files found failed."
        echo "Output: $output"
        exit 1
    fi
}

# Test 4: Report action - files found
test_report_files_found() {
    reset_mocks
    echo "Running test: Report action - files found"
    file1="$TEST_DIR/old_file_1.txt"
    file2="$TEST_DIR/old_file_2.log"
    MOCKED_FIND_OUTPUT="$file1\n$file2" # Mock find output
    output=$(run_script -d "$TEST_DIR" -a 10 -x "report")
    if [[ $? -eq 0 && "$output" == *"$file1 (ready for inspection)"* && "$output" == *"$file2 (ready for inspection)"* ]]; then
        echo "PASS: Report action with files found."
    else
        echo "FAIL: Report action with files found failed."
        echo "Output: $output"
        exit 1
    fi
    if [[ ${#MOCKED_TOUCH_CALLS[@]} -ne 0 || ${#MOCKED_MV_CALLS[@]} -ne 0 ]]; then
        echo "FAIL: Report action should not call touch or mv."
        exit 1
    fi
}

# Test 5: Re-energize action
test_re_energize() {
    reset_mocks
    echo "Running test: Re-energize action"
    file1="$TEST_DIR/dusty_doc.txt"
    file2="$TEST_DIR/ancient_script.sh"
    MOCKED_FIND_OUTPUT="$file1\n$file2"
    output=$(run_script -d "$TEST_DIR" -a 5 -x "re-energize")
    if [[ $? -eq 0 && "$output" == *"$file1 (re-energized, timestamp updated!)"* && "$output" == *"$file2 (re-energized, timestamp updated!)"* ]]; then
        echo "PASS: Re-energize action successful."
    else
        echo "FAIL: Re-energize action failed."
        echo "Output: $output"
        exit 1
    fi
    if [[ ${#MOCKED_TOUCH_CALLS[@]} -ne 2 ]]; then
        echo "FAIL: Expected 2 touch calls, got ${#MOCKED_TOUCH_CALLS[@]} arguments."
        exit 1
    fi
    if [[ "${MOCKED_TOUCH_CALLS[0]}" != "$file1" || "${MOCKED_TOUCH_CALLS[1]}" != "$file2" ]]; then
        echo "FAIL: Touch calls arguments incorrect: ${MOCKED_TOUCH_CALLS[*]}"
        exit 1
    fi
    if [[ ${#MOCKED_MV_CALLS[@]} -ne 0 ]]; then
        echo "FAIL: Re-energize action should not call mv."
        exit 1
    fi
}

# Test 6: Archive action
test_archive() {
    reset_mocks
    echo "Running test: Archive action"
    file1="$TEST_DIR/forgotten_photo.jpg"
    file2="$TEST_DIR/old_config.ini"
    MOCKED_FIND_OUTPUT="$file1\n$file2"
    output=$(run_script -d "$TEST_DIR" -a 10 -x "archive" -o "$ARCHIVE_TEST_DIR")
    if [[ $? -eq 0 && "$output" == *"$file1 (archived to the void: $ARCHIVE_TEST_DIR)"* && "$output" == *"$file2 (archived to the void: $ARCHIVE_TEST_DIR)"* ]]; then
        echo "PASS: Archive action successful."
    else
        echo "FAIL: Archive action failed."
        echo "Output: $output"
        exit 1
    fi
    if [[ ${#MOCKED_MV_CALLS[@]} -ne 4 ]]; then # mv "$file" "$ARCHIVE_DIR/" means 2 args per call, 2 calls = 4 args
        echo "FAIL: Expected 2 mv calls (4 args), got ${#MOCKED_MV_CALLS[@]} arguments."
        exit 1
    fi
    if [[ "${MOCKED_MV_CALLS[0]}" != "$file1" || "${MOCKED_MV_CALLS[1]}" != "$ARCHIVE_TEST_DIR/" || \
          "${MOCKED_MV_CALLS[2]}" != "$file2" || "${MOCKED_MV_CALLS[3]}" != "$ARCHIVE_TEST_DIR/" ]]; then
        echo "FAIL: MV calls arguments incorrect: ${MOCKED_MV_CALLS[*]}"
        exit 1
    fi
    if [[ ${#MOCKED_TOUCH_CALLS[@]} -ne 0 ]]; then
        echo "FAIL: Archive action should not call touch."
        exit 1
    fi
    if [[ ${#MOCKED_MKDIR_CALLS[@]} -ne 2 ]]; then # mkdir -p "$ARCHIVE_TEST_DIR" means 2 args
        echo "FAIL: Expected 1 mkdir call (2 args), got ${#MOCKED_MKDIR_CALLS[@]} arguments."
        exit 1
    fi
    if [[ "${MOCKED_MKDIR_CALLS[0]}" != "-p" || "${MOCKED_MKDIR_CALLS[1]}" != "$ARCHIVE_TEST_DIR" ]]; then
        echo "FAIL: MKDIR calls arguments incorrect: ${MOCKED_MKDIR_CALLS[*]}"
        exit 1
    fi
}

# Test 7: Archive action without output directory
test_archive_no_output_dir() {
    reset_mocks
    echo "Running test: Archive action without output directory"
    output=$(run_script -d "$TEST_DIR" -a 10 -x "archive")
    if [[ $? -eq 1 && "$output" == *"Error: Archive directory (-o) is required"* ]]; then
        echo "PASS: Archive action without output directory handled."
    else
        echo "FAIL: Archive action without output directory failed."
        echo "Output: $output"
        exit 1
    fi
}

# Test 8: Invalid target directory
test_invalid_target_dir() {
    reset_mocks
    echo "Running test: Invalid target directory"
    output=$(run_script -d "/non/existent/path" -x "report")
    if [[ $? -eq 1 && "$output" == *"Error: Target directory"* ]]; then
        echo "PASS: Invalid target directory handled."
    else
        echo "FAIL: Invalid target directory failed."
        echo "Output: $output"
        exit 1
    fi
}

# Test 9: Invalid age days
test_invalid_age_days() {
    reset_mocks
    echo "Running test: Invalid age days (non-numeric)"
    output=$(run_script -d "$TEST_DIR" -a "abc" -x "report")
    if [[ $? -eq 1 && "$output" == *"Error: Age days must be a non-negative integer."* ]]; then
        echo "PASS: Invalid age days (non-numeric) handled."
    else
        echo "FAIL: Invalid age days (non-numeric) failed."
        echo "Output: $output"
        exit 1
    fi

    reset_mocks
    echo "Running test: Invalid age days (negative)"
    output=$(run_script -d "$TEST_DIR" -a "-5" -x "report")
    if [[ $? -eq 1 && "$output" == *"Error: Age days must be a non-negative integer."* ]]; then
        echo "PASS: Invalid age days (negative) handled."
    else
        echo "FAIL: Invalid age days (negative) failed."
        echo "Output: $output"
        exit 1
    fi
}

# Run all tests
test_no_args
test_invalid_action
test_report_no_files
test_report_files_found
test_re_energize
test_archive
test_archive_no_output_dir
test_invalid_target_dir
test_invalid_age_days

# Cleanup
rm -rf "$TEST_DIR" "$ARCHIVE_TEST_DIR"
echo "All tests completed successfully."
