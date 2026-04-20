#!/bin/bash

# Test suite for Nightly Digital Dust Bunny Sweeper

SCRIPT_PATH="../src/dust_bunny_sweeper.sh"
TEST_DIR="/tmp/dust_bunny_test_$(date +%s%N)"

# --- Mock Functions ---

# Mock rationale: We don't want to actually create/delete files or traverse the real filesystem during tests.
# These mocks simulate the behavior of 'find', 'du', and 'rm'.

# Mock 'find' command
# It will output predefined paths based on a global array `MOCK_FIND_FILES`.
find() {
    for file in "${MOCK_FIND_FILES[@]}"; do
        printf "%s\0" "$file"
    done
}

# Mock 'du' command
# It will output a predefined size based on a global variable `MOCK_DU_OUTPUT`.
du() {
    echo "$MOCK_DU_OUTPUT"
}

# Mock 'rm' command
# Instead of deleting, it logs the file it would have deleted to a temporary file.
# This allows us to verify which files 'rm' was called with.
rm() {
    for arg in "$@"; do
        if [[ "$arg" != "-f" ]]; then
            echo "$arg" >> "$TEST_DIR/mock_rm_log.txt"
        fi
    done
    return 0 # Always succeed for mock
}

# Mock 'read' command for user input
# It will return a predefined response based on a global variable `MOCK_READ_REPLY`.
read() {
    # Simulate user input for confirmation
    if [[ "$1" == "-p" && "$2" == "Ready to sweep these digital dust bunnies away? (y/N):" ]]; then
        REPLY="$MOCK_READ_REPLY"
    fi
    # Suppress actual prompt output
    return 0
}

# --- Test Helpers ---

setup_test_env() {
    mkdir -p "$TEST_DIR"
    MOCK_RM_LOG="$TEST_DIR/mock_rm_log.txt"
    > "$MOCK_RM_LOG" # Clear log file
    MOCK_FIND_FILES=() # Clear array
    MOCK_DU_OUTPUT=""
    MOCK_READ_REPLY="n" # Default to no confirmation
}

cleanup_test_env() {
    rm -rf "$TEST_DIR"
}

assert_contains() {
    local expected="$1"
    local actual="$2"
    if ! echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: Expected output to contain '$expected', but got: '$actual'"
        return 1
    fi
    return 0
}

assert_not_contains() {
    local expected="$1"
    local actual="$2"
    if echo "$actual" | grep -qF "$expected"; then
        echo "FAIL: Expected output NOT to contain '$expected', but got: '$actual'"
        return 1
    fi
    return 0
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    if [[ "$expected" != "$actual" ]]; then
        echo "FAIL: Expected '$expected', but got '$actual'"
        return 1
    fi
    return 0
}

run_test() {
    local test_name="$1"
    local command="$2"
    local expected_output_contains="$3"
    local expected_output_not_contains="$4"
    local expected_rm_log_contains="$5"
    local expected_rm_log_not_contains="$6"
    local expected_exit_code="$7"

    setup_test_env

    echo "Running test: $test_name"
    # Execute the script, redirecting stderr to stdout for capture
    OUTPUT=$(eval "$command" 2>&1)
    EXIT_CODE=$?

    local test_failed=0

    if [[ -n "$expected_output_contains" ]]; then
        assert_contains "$expected_output_contains" "$OUTPUT" || test_failed=1
    fi
    if [[ -n "$expected_output_not_contains" ]]; then
        assert_not_contains "$expected_output_not_contains" "$OUTPUT" || test_failed=1
    fi

    local RM_LOG_CONTENT=""
    if [[ -f "$MOCK_RM_LOG" ]]; then
        RM_LOG_CONTENT=$(cat "$MOCK_RM_LOG")
    fi

    if [[ -n "$expected_rm_log_contains" ]]; then
        assert_contains "$expected_rm_log_contains" "$RM_LOG_CONTENT" || test_failed=1
    fi
    if [[ -n "$expected_rm_log_not_contains" ]]; then
        assert_not_contains "$expected_rm_log_not_contains" "$RM_LOG_CONTENT" || test_failed=1
    fi

    if [[ -n "$expected_exit_code" ]]; then
        assert_equals "$expected_exit_code" "$EXIT_CODE" || test_failed=1
    fi

    if [[ "$test_failed" -eq 0 ]]; then
        echo "PASS: $test_name"
    else
        echo "--- Test Output ---"
        echo "$OUTPUT"
        echo "--- Mock RM Log ---"
        echo "$RM_LOG_CONTENT"
        echo "-------------------"
        exit 1 # Exit on first failure
    fi

    cleanup_test_env
}

# --- Test Cases ---

# Test 1: No dust bunnies found
MOCK_FIND_FILES=()
MOCK_DU_OUTPUT="0B\ttotal"
run_test "No dust bunnies" "$SCRIPT_PATH" "No digital dust bunnies found" "" "" "" 0

# Test 2: Dust bunnies found, dry run
MOCK_FIND_FILES=("/path/to/old_log.txt" "/path/to/old_download.zip")
MOCK_DU_OUTPUT="1.5M\ttotal"
run_test "Dry run with dust bunnies" "$SCRIPT_PATH --dry-run" "Dry Run Mode" "Sweeping away" "/path/to/old_log.txt" "" 0

# Test 3: Dust bunnies found, user declines sweep
MOCK_FIND_FILES=("/path/to/old_log.txt" "/path/to/old_download.zip")
MOCK_DU_OUTPUT="1.5M\ttotal"
MOCK_READ_REPLY="n"
run_test "User declines sweep" "$SCRIPT_PATH" "Operation cancelled" "Sweeping away" "" "/path/to/old_log.txt" 0

# Test 4: Dust bunnies found, user confirms sweep
MOCK_FIND_FILES=("/path/to/old_log.txt" "/path/to/old_download.zip")
MOCK_DU_OUTPUT="1.5M\ttotal"
MOCK_READ_REPLY="y"
run_test "User confirms sweep" "$SCRIPT_PATH" "Sweep complete!" "Operation cancelled" "/path/to/old_log.txt\n/path/to/old_download.zip" "" 0

# Test 5: Assume yes flag
MOCK_FIND_FILES=("/path/to/old_log.txt")
MOCK_DU_OUTPUT="500K\ttotal"
run_test "Assume yes flag" "$SCRIPT_PATH -y" "Sweep complete!" "Operation cancelled" "/path/to/old_log.txt" "" 0

# Test 6: Custom path and age
MOCK_FIND_FILES=("/custom/path/old_file.txt")
MOCK_DU_OUTPUT="2.1G\ttotal"
run_test "Custom path and age" "$SCRIPT_PATH -p /custom/path -a 90 -y" "Scanning for files older than 90 days in:" "Scanning for files older than 30 days in:" "/custom/path/old_file.txt" "" 0

# Test 7: Invalid path provided
MOCK_FIND_FILES=() # No files found because the path is invalid
MOCK_DU_OUTPUT="0B\ttotal"
run_test "Invalid path" "$SCRIPT_PATH -p /nonexistent/path" "Warning: Directory '/nonexistent/path' does not exist or is not readable. Skipping." "No digital dust bunnies found" "" "" 0

# Test 8: Help message
run_test "Help message" "$SCRIPT_PATH -h" "Usage: $0 [OPTIONS]" "" "" "" 0

# Test 9: Unknown option
run_test "Unknown option" "$SCRIPT_PATH --unknown" "Error: Unknown option '--unknown'" "" "" "" 1

echo ""
echo "All tests passed!"
