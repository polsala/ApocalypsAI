#!/bin/bash

# Mock rationale:
# We are testing the shell script's logic and its interaction with files,
# not the internal workings of `grep`, `sed`, `find`, `cp`, `mv`, or `rm`.
# By creating temporary files and directories, and asserting their content
# after the script runs, we achieve deterministic and offline testing.
# The core utilities (`grep`, `sed`, etc.) are assumed to work correctly
# as they are standard system tools.

# Setup a temporary directory for tests
TEST_DIR=$(mktemp -d)
SCRIPT_PATH="$(dirname "$0")"/../src/main.sh

# Ensure the script is executable
chmod +x "$SCRIPT_PATH"

# Cleanup function
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

echo "Running tests in $TEST_DIR"

# Test 1: Dry run on a single file with sensitive data
echo "Test 1: Dry run on a single file with sensitive data"
TEST_FILE="$TEST_DIR/test1.log"
echo "This is a log entry with an email: user@example.com" > "$TEST_FILE"
echo "Another entry with an IP address: 192.168.1.100" >> "$TEST_FILE"
echo "And a secret API_KEY=abcdef1234567890abcdef1234567890" >> "$TEST_FILE"
echo "A password entry: password=mysecretpwd123" >> "$TEST_FILE"
echo "No sensitive data here." >> "$TEST_FILE"

OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_FILE" --dry-run)

if echo "$OUTPUT" | grep -q "user@example.com" && \
   echo "$OUTPUT" | grep -q "192.168.1.100" && \
   echo "$OUTPUT" | grep -q "API_KEY=abcdef1234567890abcdef1234567890" && \
   echo "$OUTPUT" | grep -q "password=mysecretpwd123" && \
   ! grep -q "REDACTED" "$TEST_FILE"; then
    echo "Test 1 PASSED: Dry run correctly identified sensitive data without modifying file."
else
    echo "Test 1 FAILED: Dry run did not work as expected."
    echo "Output:"
    echo "$OUTPUT"
    exit 1
fi

# Test 2: Actual redaction on a single file with sensitive data
echo "Test 2: Actual redaction on a single file with sensitive data"
TEST_FILE="$TEST_DIR/test2.log"
echo "This is a log entry with an email: user@example.com" > "$TEST_FILE"
echo "Another entry with an IP address: 192.168.1.100" >> "$TEST_FILE"
echo "And a secret API_KEY=abcdef1234567890abcdef1234567890" >> "$TEST_FILE"
echo "A password entry: password=mysecretpwd123" >> "$TEST_FILE"
echo "No sensitive data here." >> "$TEST_FILE"

bash "$SCRIPT_PATH" "$TEST_FILE" > /dev/null # Suppress stdout for cleaner test output

if grep -q "REDACTED" "$TEST_FILE" && \
   ! grep -q "user@example.com" "$TEST_FILE" && \
   ! grep -q "192.168.1.100" "$TEST_FILE" && \
   ! grep -q "API_KEY=abcdef1234567890abcdef1234567890" "$TEST_FILE" && \
   ! grep -q "password=mysecretpwd123" "$TEST_FILE"; then
    echo "Test 2 PASSED: Redaction correctly modified file."
else
    echo "Test 2 FAILED: Redaction did not work as expected."
    echo "File content after redaction:"
    cat "$TEST_FILE"
    exit 1
fi

# Test 3: No sensitive data in file
echo "Test 3: No sensitive data in file"
TEST_FILE="$TEST_DIR/test3.log"
echo "This log has no secrets." > "$TEST_FILE"
echo "Just plain text." >> "$TEST_FILE"
ORIGINAL_CONTENT=$(cat "$TEST_FILE")

bash "$SCRIPT_PATH" "$TEST_FILE" > /dev/null

if [ "$(cat "$TEST_FILE")" == "$ORIGINAL_CONTENT" ]; then
    echo "Test 3 PASSED: File with no sensitive data was not modified."
else
    echo "Test 3 FAILED: File with no sensitive data was modified."
    cat "$TEST_FILE"
    exit 1
fi

# Test 4: Directory scan with mixed files
echo "Test 4: Directory scan with mixed files"
TEST_DIR_SCAN="$TEST_DIR/scan_dir"
mkdir -p "$TEST_DIR_SCAN"

FILE_WITH_SECRETS="$TEST_DIR_SCAN/secrets.log"
echo "Email: test@domain.com, IP: 10.0.0.1, API_KEY=xyz123, password=foo" > "$FILE_WITH_SECRETS"

FILE_WITHOUT_SECRETS="$TEST_DIR_SCAN/clean.txt"
echo "This file is clean." > "$FILE_WITHOUT_SECRETS"
ORIGINAL_CLEAN_CONTENT=$(cat "$FILE_WITHOUT_SECRETS")

FILE_SKIPPED="$TEST_DIR_SCAN/binary.bin"
echo -e "\x89PNG\r\n\x1a\n" > "$FILE_SKIPPED" # Simulate a binary file

bash "$SCRIPT_PATH" "$TEST_DIR_SCAN" > /dev/null

if grep -q "REDACTED" "$FILE_WITH_SECRETS" && \
   ! grep -q "test@domain.com" "$FILE_WITH_SECRETS" && \
   ! grep -q "10.0.0.1" "$FILE_WITH_SECRETS" && \
   ! grep -q "API_KEY=xyz123" "$FILE_WITH_SECRETS" && \
   ! grep -q "password=foo" "$FILE_WITH_SECRETS" && \
   [ "$(cat "$FILE_WITHOUT_SECRETS")" == "$ORIGINAL_CLEAN_CONTENT" ]; then
    echo "Test 4 PASSED: Directory scan correctly processed files."
else
    echo "Test 4 FAILED: Directory scan did not work as expected."
    echo "Secrets file content after redaction:"
    cat "$FILE_WITH_SECRETS"
    echo "Clean file content after scan:"
    cat "$FILE_WITHOUT_SECRETS"
    exit 1
fi

# Test 5: Invalid path
echo "Test 5: Invalid path"
OUTPUT=$(bash "$SCRIPT_PATH" "$TEST_DIR/non_existent_path" 2>&1)
if echo "$OUTPUT" | grep -q "Error: '.*' is not a valid file or directory." && \
   echo "$OUTPUT" | grep -q "Usage:"; then
    echo "Test 5 PASSED: Invalid path handled gracefully."
else
    echo "Test 5 FAILED: Invalid path handling failed."
    echo "Output:"
    echo "$OUTPUT"
    exit 1
fi

echo "All tests passed!"
