#!/bin/bash

# Test script for Nightly Digital Dust Bunny Sweeper

# Define the path to the script
SCRIPT_PATH="./src/dust_bunny_sweeper.sh"

# Setup a temporary directory for tests
TEST_DIR=$(mktemp -d)
export TEST_DIR # Make it available to subshells/mocks

# Mock functions for deterministic testing
# Mock rationale: Prevents actual file system changes and allows control over `find` and `rm` behavior.

# Mock `find` to return predefined files
mock_find() {
    local dir=""
    local age_days=""
    local print0_requested=false
    local type_f_requested=false

    # Parse arguments passed to the mock find
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -type)
                if [[ "$2" == "f" ]]; then type_f_requested=true; fi
                shift
                ;;
            -mtime)
                age_days="$2"
                shift
                ;;
            -print0)
                print0_requested=true
                ;;
            *)
                if [[ -d "$1" ]]; then # Assume the first non-option is the directory
                    dir="$1"
                fi
                ;;
        esac
        shift
    done

    # Only proceed if -type f and -mtime +N are requested (as per script's usage)
    if [[ "$type_f_requested" == "false" || -z "$age_days" ]]; then
        return 0
    fi

    local files=()
    local age_num=${age_days#+} # Remove '+' prefix

    if [[ "$dir" == "${TEST_DIR}/dusty_dir" ]]; then
        if (( age_num <= 7 )); then # If looking for files older than 7 days, include medium_file
            files+=("${TEST_DIR}/dusty_dir/old_file_1.txt")
            files+=("${TEST_DIR}/dusty_dir/old_file_2.log")
            files+=("${TEST_DIR}/dusty_dir/medium_file.tmp")
        elif (( age_num <= 30 )); then # If looking for files older than 30 days
            files+=("${TEST_DIR}/dusty_dir/old_file_1.txt")
            files+=("${TEST_DIR}/dusty_dir/old_file_2.log")
        fi
    elif [[ "$dir" == "${TEST_DIR}/clean_dir" ]]; then
        : # No files
    elif [[ "$dir" == "${TEST_DIR}/mixed_dir" ]]; then
        if (( age_num <= 7 )); then
            files+=("${TEST_DIR}/mixed_dir/very_old.dat")
            files+=("${TEST_DIR}/mixed_dir/oldish.txt")
        elif (( age_num <= 30 )); then
            files+=("${TEST_DIR}/mixed_dir/very_old.dat")
        fi
    fi

    if [[ "$print0_requested" == "true" ]]; then
        for f in "${files[@]}"; do
            printf "%s\0" "$f"
        done
    else
        for f in "${files[@]}"; do
            echo "$f"
        done
    fi
}

# Mock `rm` to log deletions instead of performing them
mock_rm() {
    for file in "$@"; do
        echo "MOCK_RM: Deleted $file" >> "${TEST_DIR}/rm_log.txt"
    done
    return 0 # Always succeed for mock
}

# Override system commands with mocks for the test run
export -f find
export -f rm

# Helper function for assertions
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

assert_equals() {
    local expected="$1"
    local actual="$2"
    if [[ "$actual" != "$expected" ]]; then
        echo "FAIL: Expected '$expected', got '$actual'"
        exit 1
    fi
}

# Test cases
echo "Running tests..."

# Create dummy directories for mock_find to reference
mkdir -p "${TEST_DIR}/dusty_dir"
mkdir -p "${TEST_DIR}/clean_dir"
mkdir -p "${TEST_DIR}/mixed_dir"

# Test 1: Dry-run with default age (30 days)
echo "--- Test 1: Dry-run default age ---"
OUTPUT=$(bash "$SCRIPT_PATH" "${TEST_DIR}/dusty_dir" "${TEST_DIR}/clean_dir")
assert_contains "Running in DRY-RUN mode. No files will be deleted." "$OUTPUT"
assert_contains "Found 2 digital dust bunnies:" "$OUTPUT"
assert_contains "${TEST_DIR}/dusty_dir/old_file_1.txt" "$OUTPUT"
assert_contains "${TEST_DIR}/dusty_dir/old_file_2.log" "$OUTPUT"
assert_not_contains "${TEST_DIR}/dusty_dir/medium_file.tmp" "$OUTPUT" # Should not be found with +30
assert_contains "Dry-run complete. These files *would* have been swept away." "$OUTPUT"
assert_not_contains "MOCK_RM" "$(cat "${TEST_DIR}/rm_log.txt" 2>/dev/null || true)" # Ensure rm was not called
echo "Test 1 passed."

# Test 2: Dry-run with custom age (7 days)
echo "--- Test 2: Dry-run custom age ---"
OUTPUT=$(bash "$SCRIPT_PATH" -a 7 "${TEST_DIR}/dusty_dir" "${TEST_DIR}/mixed_dir")
assert_contains "Looking for files older than 7 days" "$OUTPUT"
assert_contains "Found 5 digital dust bunnies:" "$OUTPUT" # 3 from dusty_dir, 2 from mixed_dir
assert_contains "${TEST_DIR}/dusty_dir/old_file_1.txt" "$OUTPUT"
assert_contains "${TEST_DIR}/dusty_dir/old_file_2.log" "$OUTPUT"
assert_contains "${TEST_DIR}/dusty_dir/medium_file.tmp" "$OUTPUT"
assert_contains "${TEST_DIR}/mixed_dir/very_old.dat" "$OUTPUT"
assert_contains "${TEST_DIR}/mixed_dir/oldish.txt" "$OUTPUT"
echo "Test 2 passed."

# Test 3: Clean mode with user confirmation (simulated 'y')
echo "--- Test 3: Clean mode with user confirmation ---"
# Clear rm_log for this test
> "${TEST_DIR}/rm_log.txt"
OUTPUT=$(echo "y" | bash "$SCRIPT_PATH" -c "${TEST_DIR}/dusty_dir")
assert_not_contains "Running in DRY-RUN mode" "$OUTPUT"
assert_contains "Sweeping away the digital dust bunnies..." "$OUTPUT"
assert_contains "[SWEPT] ${TEST_DIR}/dusty_dir/old_file_1.txt" "$OUTPUT"
assert_contains "[SWEPT] ${TEST_DIR}/dusty_dir/old_file_2.log" "$OUTPUT"
assert_contains "Digital dust bunny sweeping complete!" "$OUTPUT"
assert_contains "MOCK_RM: Deleted ${TEST_DIR}/dusty_dir/old_file_1.txt" "$(cat "${TEST_DIR}/rm_log.txt")"
assert_contains "MOCK_RM: Deleted ${TEST_DIR}/dusty_dir/old_file_2.log" "$(cat "${TEST_DIR}/rm_log.txt")"
echo "Test 3 passed."

# Test 4: Clean mode with user confirmation (simulated 'n')
echo "--- Test 4: Clean mode with user confirmation (n) ---"
> "${TEST_DIR}/rm_log.txt" # Clear log
OUTPUT=$(echo "n" | bash "$SCRIPT_PATH" -c "${TEST_DIR}/dusty_dir")
assert_contains "Phew! Digital dust bunnies spared." "$OUTPUT"
assert_not_contains "MOCK_RM" "$(cat "${TEST_DIR}/rm_log.txt" 2>/dev/null || true)"
echo "Test 4 passed."

# Test 5: Force clean mode
echo "--- Test 5: Force clean mode ---"
> "${TEST_DIR}/rm_log.txt" # Clear log
OUTPUT=$(bash "$SCRIPT_PATH" -c -f "${TEST_DIR}/mixed_dir")
assert_not_contains "Do you wish to sweep" "$OUTPUT" # No prompt
assert_contains "[SWEPT] ${TEST_DIR}/mixed_dir/very_old.dat" "$OUTPUT"
assert_contains "MOCK_RM: Deleted ${TEST_DIR}/mixed_dir/very_old.dat" "$(cat "${TEST_DIR}/rm_log.txt")"
echo "Test 5 passed."

# Test 6: No directories specified
echo "--- Test 6: No directories specified ---"
OUTPUT=$(bash "$SCRIPT_PATH" 2>&1) # Capture stderr
assert_contains "Error: No directories specified." "$OUTPUT"
assert_contains "Usage: $0 [OPTIONS] <DIRECTORY1> [DIRECTORY2...>" "$OUTPUT"
echo "Test 6 passed."

# Test 7: Invalid age argument
echo "--- Test 7: Invalid age argument ---"
OUTPUT=$(bash "$SCRIPT_PATH" -a abc "${TEST_DIR}/dusty_dir" 2>&1)
assert_contains "Error: --age argument must be a positive integer." "$OUTPUT"
echo "Test 7 passed."

# Test 8: Non-existent directory
echo "--- Test 8: Non-existent directory ---"
OUTPUT=$(bash "$SCRIPT_PATH" "${TEST_DIR}/non_existent_dir")
assert_contains "Warning: Directory '${TEST_DIR}/non_existent_dir' does not exist or is not a directory. Skipping." "$OUTPUT"
assert_contains "Hooray! No digital dust bunnies found." "$OUTPUT" # Because the only dir was skipped
echo "Test 8 passed."

# Cleanup
rm -rf "$TEST_DIR"
unset -f find
unset -f rm
echo "All tests passed!"
