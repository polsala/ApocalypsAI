#!/bin/bash

# nightly-syslog-parser-cli.sh
# A bash script to parse and filter system logs with customizable patterns.

# --- Mock Rationale ---
# The test function mocks the behavior of reading from a log file and applying grep.
# This allows deterministic testing without relying on actual system logs or external commands.

# Function to display usage information
usage() {
    echo "Usage: $0 <log_file> <pattern>"
    echo "       $0 --test"
    echo "Parses and filters system logs."
    echo "  <log_file>: Path to the syslog file."
    echo "  <pattern>: Grep-compatible pattern to filter log entries."
    echo "  --test: Run built-in tests."
    exit 1
}

# Function to run tests
test_syslog_parser() {
    echo "Running tests for nightly-syslog-parser-cli..."

    # Mock log file content
    MOCK_LOG_CONTENT=""
    MOCK_LOG_CONTENT+="Jan 1 00:00:01 hostname kernel: Some kernel message\n"
    MOCK_LOG_CONTENT+="Jan 1 00:01:02 hostname sshd[1234]: Authentication failed for user root\n"
    MOCK_LOG_CONTENT+="Jan 1 00:02:03 hostname systemd[1]: Started Session 1 of user root.\n"
    MOCK_LOG_CONTENT+="Jan 1 00:03:04 hostname sshd[5678]: Accepted password for user testuser\n"
    MOCK_LOG_CONTENT+="Jan 1 00:04:05 hostname kernel: Another kernel message\n"
    MOCK_LOG_CONTENT+="Jan 1 00:05:06 hostname CRON[9012]: (root) CMD (command)"

    # Mock grep function
    mock_grep() {
        local pattern="$1"
        local input="$2"
        echo "$input" | grep -E "$pattern"
    }

    # Test case 1: Filter by 'sshd'
    echo "Test Case 1: Filtering by 'sshd'"
    EXPECTED_OUTPUT="Jan 1 00:01:02 hostname sshd[1234]: Authentication failed for user root\nJan 1 00:03:04 hostname sshd[5678]: Accepted password for user testuser"
    ACTUAL_OUTPUT=$(mock_grep "sshd" "$MOCK_LOG_CONTENT")

    if [ "$ACTUAL_OUTPUT" == "$EXPECTED_OUTPUT" ]; then
        echo "  PASSED: Correctly filtered 'sshd' entries."
    else
        echo "  FAILED: 'sshd' filtering mismatch."
        echo "    Expected: $EXPECTED_OUTPUT"
        echo "    Got: $ACTUAL_OUTPUT"
        exit 1
    fi

    # Test case 2: Filter by 'kernel' (case-sensitive)
    echo "Test Case 2: Filtering by 'kernel'"
    EXPECTED_OUTPUT="Jan 1 00:00:01 hostname kernel: Some kernel message\nJan 1 00:04:05 hostname kernel: Another kernel message"
    ACTUAL_OUTPUT=$(mock_grep "kernel" "$MOCK_LOG_CONTENT")

    if [ "$ACTUAL_OUTPUT" == "$EXPECTED_OUTPUT" ]; then
        echo "  PASSED: Correctly filtered 'kernel' entries."
    else
        echo "  FAILED: 'kernel' filtering mismatch."
        echo "    Expected: $EXPECTED_OUTPUT"
        echo "    Got: $ACTUAL_OUTPUT"
        exit 1
    fi

    # Test case 3: Filter by 'CRON' (case-sensitive)
    echo "Test Case 3: Filtering by 'CRON'"
    EXPECTED_OUTPUT="Jan 1 00:05:06 hostname CRON[9012]: (root) CMD (command)"
    ACTUAL_OUTPUT=$(mock_grep "CRON" "$MOCK_LOG_CONTENT")

    if [ "$ACTUAL_OUTPUT" == "$EXPECTED_OUTPUT" ]; then
        echo "  PASSED: Correctly filtered 'CRON' entries."
    else
        echo "  FAILED: 'CRON' filtering mismatch."
        echo "    Expected: $EXPECTED_OUTPUT"
        echo "    Got: $ACTUAL_OUTPUT"
        exit 1
    fi

    # Test case 4: Filter with a pattern that matches nothing
    echo "Test Case 4: Filtering with no matches"
    EXPECTED_OUTPUT=""
    ACTUAL_OUTPUT=$(mock_grep "nonexistent_pattern" "$MOCK_LOG_CONTENT")

    if [ "$ACTUAL_OUTPUT" == "$EXPECTED_OUTPUT" ]; then
        echo "  PASSED: Correctly returned no matches."
    else
        echo "  FAILED: No match filtering mismatch."
        echo "    Expected: $EXPECTED_OUTPUT"
        echo "    Got: $ACTUAL_OUTPUT"
        exit 1
    fi

    echo "All tests passed!"
    exit 0
}

# --- Main script logic ---

# Check for test flag
if [ "$1" == "--test" ]; then
    test_syslog_parser
fi

# Check for correct number of arguments
if [ $# -ne 2 ]; then
    usage
fi

LOG_FILE="$1"
PATTERN="$2"

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file '$LOG_FILE' not found."
    exit 1
fi

# Parse and filter logs
cat "$LOG_FILE" | grep -E "$PATTERN"

exit 0
