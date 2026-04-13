#!/bin/bash

# nightly-syslog-parser.sh tests

# Exit immediately if a command exits with a non-zero status.
set -e

# Mock log file content
# Mock rationale: Create a temporary file with predictable content for deterministic testing.
TEST_LOG_CONTENT="2023-10-27T10:00:00Z INFO: System started successfully.
2023-10-27T10:01:05Z WARNING: Disk space low on /var.
2023-10-27T10:02:15Z ERROR: Failed to connect to database.
2023-10-27T10:03:30Z INFO: User 'admin' logged in.
2023-10-27T10:04:45Z ERROR: Network timeout occurred.
2023-10-27T10:05:00Z DEBUG: Processing request."

TEST_LOG_FILE=$(mktemp)
echo -e "$TEST_LOG_CONTENT" > "$TEST_LOG_FILE"

# --- Test Cases ---

# Test 1: Basic keyword search (case-insensitive)
echo "Running Test 1: Basic keyword search (case-insensitive)..."
EXPECTED_OUTPUT="2023-10-27T10:01:05Z WARNING: Disk space low on /var.
2023-10-27T10:02:15Z ERROR: Failed to connect to database.
2023-10-27T10:04:45Z ERROR: Network timeout occurred."
ACTUAL_OUTPUT=$(./src/main.sh "$TEST_LOG_FILE" ERROR)

if [ "$ACTUAL_OUTPUT" = "$EXPECTED_OUTPUT" ]; then
    echo "Test 1 Passed."
else
    echo "Test 1 Failed."
    echo "Expected:"
    echo "$EXPECTED_OUTPUT"
    echo "Actual:"
    echo "$ACTUAL_OUTPUT"
    exit 1
fi

# Test 2: Multiple keywords (OR logic)
echo "Running Test 2: Multiple keywords (OR logic)..."
EXPECTED_OUTPUT="2023-10-27T10:01:05Z WARNING: Disk space low on /var.
2023-10-27T10:02:15Z ERROR: Failed to connect to database.
2023-10-27T10:04:45Z ERROR: Network timeout occurred."
ACTUAL_OUTPUT=$(./src/main.sh "$TEST_LOG_FILE" WARNING ERROR)

if [ "$ACTUAL_OUTPUT" = "$EXPECTED_OUTPUT" ]; then
    echo "Test 2 Passed."
else
    echo "Test 2 Failed."
    echo "Expected:"
    echo "$EXPECTED_OUTPUT"
    echo "Actual:"
    echo "$ACTUAL_OUTPUT"
    exit 1
fi

# Test 3: Keyword not found
echo "Running Test 3: Keyword not found..."
EXPECTED_OUTPUT=""
ACTUAL_OUTPUT=$(./src/main.sh "$TEST_LOG_FILE" CRITICAL)

if [ "$ACTUAL_OUTPUT" = "$EXPECTED_OUTPUT" ]; then
    echo "Test 3 Passed."
else
    echo "Test 3 Failed."
    echo "Expected:"
    echo "$EXPECTED_OUTPUT"
    echo "Actual:"
    echo "$ACTUAL_OUTPUT"
    exit 1
fi

# Test 4: Invalid log file path
echo "Running Test 4: Invalid log file path..."
EXPECTED_OUTPUT="Error: Log file 'non_existent_file.log' not found or not readable."
ACTUAL_OUTPUT=$(./src/main.sh non_existent_file.log ERROR 2>&1 || true)

if [ "$ACTUAL_OUTPUT" = "$EXPECTED_OUTPUT" ]; then
    echo "Test 4 Passed."
else
    echo "Test 4 Failed."
    echo "Expected:"
    echo "$EXPECTED_OUTPUT"
    echo "Actual:"
    echo "$ACTUAL_OUTPUT"
    exit 1
fi

# Test 5: No keywords provided
echo "Running Test 5: No keywords provided..."
EXPECTED_OUTPUT="Usage: ./src/main.sh <log_file> <keyword1> [keyword2 ...]"
ACTUAL_OUTPUT=$(./src/main.sh "$TEST_LOG_FILE" 2>&1 || true)

if [ "$ACTUAL_OUTPUT" = "$EXPECTED_OUTPUT" ]; then
    echo "Test 5 Passed."
else
    echo "Test 5 Failed."
    echo "Expected:"
    echo "$EXPECTED_OUTPUT"
    echo "Actual:"
    echo "$ACTUAL_OUTPUT"
    exit 1
fi

# Clean up the mock log file
rm "$TEST_LOG_FILE"

echo "All tests completed successfully!"
exit 0
