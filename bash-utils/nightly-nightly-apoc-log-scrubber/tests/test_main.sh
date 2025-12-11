#!/bin/bash

# Mock rationale: These tests mock the input log files and configuration files to ensure the script's logic for pattern matching and output generation is correct without relying on external system states or actual log files.

# Define test directories and files
TEST_DIR="$(dirname "$0")"
SRC_DIR="$TEST_DIR/../src"
CONFIG_DIR="$TEST_DIR/../config"

# Create mock input log file
TEST_INPUT_LOG="$TEST_DIR/mock_input.log"
cat << EOF > "$TEST_INPUT_LOG"
2023-10-27T10:00:00 INFO User 192.168.1.100 logged in
2023-10-27T10:01:05 DEBUG Session ID: a1b2c3d4-e5f6-7890-1234-567890abcdef
2023-10-27T10:02:15 INFO System reboot initiated.
2023-10-27T10:03:30 WARN Disk space low on /dev/sda1.
2023-10-27T10:04:45 DEBUG Another session: 09876543-21fe-dcba-0987-654321fedcba
EOF

# Create mock default configuration file
TEST_DEFAULT_CONFIG="$CONFIG_DIR/default.conf"
mkdir -p "$CONFIG_DIR"
cat << EOF > "$TEST_DEFAULT_CONFIG"
# Default patterns to scrub
^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*\s+INFO\s+User\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+logged in
^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*\s+DEBUG\s+Session ID: [a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}
EOF

# Create mock custom configuration file
TEST_CUSTOM_CONFIG="$TEST_DIR/custom.conf"
cat << EOF > "$TEST_CUSTOM_CONFIG"
# Custom patterns
^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*\s+WARN\s+Disk space low on /dev/sda1.
EOF

# Create mock output log file path
TEST_OUTPUT_LOG="$TEST_DIR/mock_output.log"

# --- Test Cases ---

# Test Case 1: Scrubbing with default configuration
echo "Running Test Case 1: Default Configuration..."
"$SRC_DIR/main.sh" "$TEST_INPUT_LOG" "$TEST_OUTPUT_LOG"

# Expected output for Test Case 1
EXPECTED_OUTPUT_DEFAULT="$TEST_DIR/expected_output_default.log"
cat << EOF > "$EXPECTED_OUTPUT_DEFAULT"
2023-10-27T10:00:00 INFO User REDACTED logged in
2023-10-27T10:01:05 DEBUG Session ID: REDACTED
2023-10-27T10:02:15 INFO System reboot initiated.
2023-10-27T10:03:30 WARN Disk space low on /dev/sda1.
2023-10-27T10:04:45 DEBUG Another session: REDACTED
EOF

if diff -q "$TEST_OUTPUT_LOG" "$EXPECTED_OUTPUT_DEFAULT" > /dev/null;
then
    echo "Test Case 1 PASSED."
else
    echo "Test Case 1 FAILED."
    echo "--- Expected Output (Default) ---"
    cat "$EXPECTED_OUTPUT_DEFAULT"
    echo "--- Actual Output ---"
    cat "$TEST_OUTPUT_LOG"
    exit 1
fi

# Test Case 2: Scrubbing with custom configuration
echo "Running Test Case 2: Custom Configuration..."
"$SRC_DIR/main.sh" "$TEST_INPUT_LOG" "$TEST_OUTPUT_LOG" "$TEST_CUSTOM_CONFIG"

# Expected output for Test Case 2
EXPECTED_OUTPUT_CUSTOM="$TEST_DIR/expected_output_custom.log"
cat << EOF > "$EXPECTED_OUTPUT_CUSTOM"
2023-10-27T10:00:00 INFO User 192.168.1.100 logged in
2023-10-27T10:01:05 DEBUG Session ID: a1b2c3d4-e5f6-7890-1234-567890abcdef
2023-10-27T10:02:15 INFO System reboot initiated.
2023-10-27T10:03:30 WARN REDACTED
2023-10-27T10:04:45 DEBUG Another session: 09876543-21fe-dcba-0987-654321fedcba
EOF

if diff -q "$TEST_OUTPUT_LOG" "$EXPECTED_OUTPUT_CUSTOM" > /dev/null;
then
    echo "Test Case 2 PASSED."
else
    echo "Test Case 2 FAILED."
    echo "--- Expected Output (Custom) ---"
    cat "$EXPECTED_OUTPUT_CUSTOM"
    echo "--- Actual Output ---"
    cat "$TEST_OUTPUT_LOG"
    exit 1
fi

# Test Case 3: Input file not found
echo "Running Test Case 3: Input File Not Found..."
"$SRC_DIR/main.sh" "/non/existent/file.log" "$TEST_OUTPUT_LOG" > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "Test Case 3 PASSED."
else
    echo "Test Case 3 FAILED."
    exit 1
fi

# Test Case 4: Non-existent custom config file (should fall back to default)
echo "Running Test Case 4: Non-existent Custom Config..."
"$SRC_DIR/main.sh" "$TEST_INPUT_LOG" "$TEST_OUTPUT_LOG" "/non/existent/custom.conf"

if diff -q "$TEST_OUTPUT_LOG" "$EXPECTED_OUTPUT_DEFAULT" > /dev/null;
then
    echo "Test Case 4 PASSED."
else
    echo "Test Case 4 FAILED."
    exit 1
fi

# Clean up mock files
rm "$TEST_INPUT_LOG"
rm "$TEST_OUTPUT_LOG"
rm "$EXPECTED_OUTPUT_DEFAULT"
rm "$EXPECTED_OUTPUT_CUSTOM"
rm "$TEST_CUSTOM_CONFIG"
rm "$TEST_DEFAULT_CONFIG"
rmdir "$CONFIG_DIR"

echo "All tests completed."
exit 0
