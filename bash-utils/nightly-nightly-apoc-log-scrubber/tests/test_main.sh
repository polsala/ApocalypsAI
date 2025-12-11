#!/bin/bash

# Tests for Apoc Log Scrubber

# Mock rationale: We are mocking the behavior of the script by creating temporary files
# and asserting the output without relying on external services or complex system states.

# Source the script to be tested
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
SOURCE_SCRIPT="$SCRIPT_DIR/../src/main.sh"

# --- Helper Functions ---

# Function to create a temporary test file
create_test_file() {
    local content="$1"
    local filename="$(mktemp)"
    echo -e "$content" > "$filename"
    echo "$filename"
}

# Function to run the script and capture output
run_scrubber() {
    local input_file="$1"
    local dry_run_flag="$2"
    "$SOURCE_SCRIPT" "$input_file" "$dry_run_flag"
}

# Function to assert that a string contains another string
assert_contains() {
    local expected="$1"
    local actual="$2"
    local test_name="$3"

    if echo "$actual" | grep -qF "$expected"; then
        echo "✅ PASS: $test_name"
    else
        echo "❌ FAIL: $test_name"
        echo "  Expected to contain: '$expected'"
        echo "  Actual output: '$actual'"
        return 1
    fi
}

# Function to assert that a string does NOT contain another string
assert_not_contains() {
    local unexpected="$1"
    local actual="$2"
    local test_name="$3"

    if echo "$actual" | grep -qF "$unexpected"; then
        echo "❌ FAIL: $test_name"
        echo "  Expected NOT to contain: '$unexpected'"
        echo "  Actual output: '$actual'"
        return 1
    else
        echo "✅ PASS: $test_name"
    fi
}

# Function to assert that a file's content matches expected content
assert_file_content() {
    local expected_content="$1"
    local actual_file="$2"
    local test_name="$3"

    actual_content=$(cat "$actual_file")

    if [ "$actual_content" == "$expected_content" ]; then
        echo "✅ PASS: $test_name"
    else
        echo "❌ FAIL: $test_name"
        echo "  Expected content: '$expected_content'"
        echo "  Actual content: '$actual_content'"
        return 1
    fi
}

# --- Test Cases ---

run_all_tests() {
    local total_tests=0
    local passed_tests=0

    # Test 1: Basic IP address redaction (dry run)
    total_tests=$((total_tests + 1))
    test_file=$(create_test_file "INFO: User 192.168.1.1 logged in.")
    output=$(run_scrubber "$test_file" "--dry-run")
    if assert_contains "XXX.XXX.XXX.XXX" "$output" "Basic IP redaction (dry run)"; then
        passed_tests=$((passed_tests + 1))
    fi
    rm "$test_file"

    # Test 2: Basic email address redaction (dry run)
    total_tests=$((total_tests + 1))
    test_file=$(create_test_file "DEBUG: Sending email to test@example.com.")
    output=$(run_scrubber "$test_file" "--dry-run")
    if assert_contains "[REDACTED_EMAIL]" "$output" "Basic email redaction (dry run)"; then
        passed_tests=$((passed_tests + 1))
    fi
    rm "$test_file"

    # Test 3: Multiple redactions on a single line (dry run)
    total_tests=$((total_tests + 1))
    test_file=$(create_test_file "WARN: Connection from 10.0.0.5 to user@domain.org failed.")
    output=$(run_scrubber "$test_file" "--dry-run")
    if assert_contains "XXX.XXX.XXX.XXX" "$output" "Multiple redactions (IP) (dry run)"; then
        passed_tests=$((passed_tests + 1))
    fi
    if assert_contains "[REDACTED_EMAIL]" "$output" "Multiple redactions (email) (dry run)"; then
        passed_tests=$((passed_tests + 1))
    fi
    rm "$test_file"

    # Test 4: No sensitive data, should remain unchanged (dry run)
    total_tests=$((total_tests + 1))
    test_file=$(create_test_file "INFO: System is running smoothly.")
    output=$(run_scrubber "$test_file" "--dry-run")
    if assert_contains "System is running smoothly." "$output" "No sensitive data (dry run)"; then
        passed_tests=$((passed_tests + 1))
    fi
    rm "$test_file"

    # Test 5: Overwriting original file with IP redaction
    total_tests=$((total_tests + 1))
    original_content="INFO: User 192.168.1.1 logged in."
    expected_content="INFO: User XXX.XXX.XXX.XXX logged in."
    test_file=$(create_test_file "$original_content")
    run_scrubber "$test_file" ""
    if assert_file_content "$expected_content" "$test_file" "Overwrite IP redaction"; then
        passed_tests=$((passed_tests + 1))
    fi
    rm "$test_file"

    # Test 6: Overwriting original file with email redaction
    total_tests=$((total_tests + 1))
    original_content="DEBUG: Sending email to test@example.com."
    expected_content="DEBUG: Sending email to [REDACTED_EMAIL]."
    test_file=$(create_test_file "$original_content")
    run_scrubber "$test_file" ""
    if assert_file_content "$expected_content" "$test_file" "Overwrite email redaction"; then
        passed_tests=$((passed_tests + 1))
    fi
    rm "$test_file"

    # Test 7: Empty file handling (dry run)
    total_tests=$((total_tests + 1))
    test_file=$(create_test_file "")
    output=$(run_scrubber "$test_file" "--dry-run")
    if [ -z "$output" ]; then
        echo "✅ PASS: Empty file handling (dry run)"
        passed_tests=$((passed_tests + 1))
    else
        echo "❌ FAIL: Empty file handling (dry run)"
        echo "  Expected empty output, got: '$output'"
    fi
    rm "$test_file"

    # Test 8: File not found error
    total_tests=$((total_tests + 1))
    output=$(run_scrubber "/non/existent/file.log" "")
    if assert_contains "Error: Input file '/non/existent/file.log' not found." "$output" "File not found error"; then
        passed_tests=$((passed_tests + 1))
    fi

    echo "-----------------------------------"
    echo "Test Summary: $passed_tests / $total_tests passed."
    echo "-----------------------------------"

    if [ "$passed_tests" -eq "$total_tests" ]; then
        exit 0
    else
        exit 1
    fi
}

run_all_tests
