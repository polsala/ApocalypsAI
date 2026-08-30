#!/bin/bash

# tests/run_tests.sh
# Runs all tests for the nightly-log-whisperer utility.

TEST_DIR="$(dirname "$0")"
UTIL_DIR="$(dirname "$TEST_DIR")"
SCRIPT_PATH="$UTIL_DIR/src/nightly-log-whisperer.sh"

# --- Mock Data ---

# Mock log file for basic keyword matching
cat << EOF > "$TEST_DIR/mock_log_basic.txt"
INFO: System started successfully.
WARN: Disk space is getting low.
ERROR: Failed to connect to database.
INFO: User logged in.
ERROR: Failed to connect to database.
DEBUG: Processing request.
EOF

# Mock log file for frequency analysis
cat << EOF > "$TEST_DIR/mock_log_frequency.txt"
INFO: Processing item A.
WARN: Configuration mismatch.
ERROR: Network timeout.
INFO: Processing item B.
ERROR: Network timeout.
INFO: Processing item A.
ERROR: Network timeout.
DEBUG: Task completed.
WARN: Configuration mismatch.
INFO: Processing item C.
EOF

# Mock log file with no matches
cat << EOF > "$TEST_DIR/mock_log_no_matches.txt"
INFO: Everything is fine.
DEBUG: Some debug info.
EOF

# --- Test Functions ---

run_test() {
    local test_name="$1"
    local command="$2"
    local expected_output="$3"
    local expected_error="$4"

    echo "Running test: $test_name"

    # Capture stdout and stderr
    actual_output=$(eval "$command" 2>&1)
    local exit_code=$?

    # Check exit code
    if [ $exit_code -ne 0 ]; then
        echo "  FAIL: Command exited with non-zero status $exit_code."
        echo "  Command: $command"
        echo "  Stderr/Stdout: $actual_output"
        return 1
    fi

    # Check stderr for expected error messages (if any)
    if [ -n "$expected_error" ]; then
        if ! echo "$actual_output" | grep -qF "$expected_error"; then
            echo "  FAIL: Expected error message not found."
            echo "  Expected: $expected_error"
            echo "  Actual: $actual_output"
            return 1
        fi
    fi

    # Check stdout for expected output (if any)
    if [ -n "$expected_output" ]; then
        # Normalize whitespace for comparison
        normalized_actual=$(echo "$actual_output" | sed 's/[[:space:]]\+/ /g' | xargs)
        normalized_expected=$(echo "$expected_output" | sed 's/[[:space:]]\+/ /g' | xargs)

        if [ "$normalized_actual" != "$normalized_expected" ]; then
            echo "  FAIL: Output mismatch."
            echo "  Expected: $normalized_expected"
            echo "  Actual:   $normalized_actual"
            return 1
        fi
    fi

    echo "  PASS"
    return 0
}

# --- Test Cases ---

# Test 1: Basic keyword matching
run_test "Basic Keyword Matching" \
    "$SCRIPT_PATH $TEST_DIR/mock_log_basic.txt" \
    "--- Potential Whispers (Keyword Matches) ---
WARN: Disk space is getting low.
ERROR: Failed to connect to database.
ERROR: Failed to connect to database."

# Test 2: Frequency analysis
run_test "Frequency Analysis" \
    "$SCRIPT_PATH $TEST_DIR/mock_log_frequency.txt" \
    "--- Potential Whispers (Keyword Matches) ---
WARN: Configuration mismatch.
ERROR: Network timeout.
ERROR: Network timeout.
ERROR: Network timeout.
WARN: Configuration mismatch.
--- Frequent Whispers (Repeated Occurrences) ---
2 : WARN: Configuration mismatch.
3 : ERROR: Network timeout."

# Test 3: No matching keywords
run_test "No Matching Keywords" \
    "$SCRIPT_PATH $TEST_DIR/mock_log_no_matches.txt" \
    "No lines found matching the specified keywords."

# Test 4: Custom keywords
run_test "Custom Keywords" \
    "$SCRIPT_PATH $TEST_DIR/mock_log_frequency.txt CRITICAL" \
    "No lines found matching the specified keywords."

# Test 5: Log file not found
run_test "Log File Not Found" \
    "$SCRIPT_PATH non_existent_log.txt" \
    "[LOG WHISPERER - ERROR] Log file 'non_existent_log.txt' not found or not readable."

# Test 6: No log file provided
run_test "No Log File Provided" \
    "$SCRIPT_PATH" \
    "[LOG WHISPERER - ERROR] No log file specified. Usage: $SCRIPT_PATH <log_file_path> [keyword1 keyword2 ...]"

# --- Cleanup ---
rm -f "$TEST_DIR/mock_log_basic.txt"
rm -f "$TEST_DIR/mock_log_frequency.txt"
rm -f "$TEST_DIR/mock_log_no_matches.txt"

exit 0
