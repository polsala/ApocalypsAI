#!/bin/bash

# Test script for Nightly-Nightly-Wasteland-Log-Scrambler

# Define the path to the main script
SCRIPT_PATH="$(dirname "$0")"/../src/scrambler.sh

# Define a temporary directory for test files
TEST_DIR="$(mktemp -d)"

# Mock rationale:
# The `get_random_word` function in `scrambler.sh` uses the `RANDOM` shell variable,
# which is non-deterministic. To ensure deterministic tests, we set `RANDOM=0`
# before executing the main script. This forces `RANDOM % num_words` to always
# evaluate to `0`, causing `get_random_word` to consistently return the first
# element of the `REPLACEMENT_WORDS` array ("Glimmer").

# Setup function
setup() {
    # Ensure the test directory is clean
    rm -rf "$TEST_DIR"
    mkdir -p "$TEST_DIR"
}

# Teardown function
teardown() {
    rm -rf "$TEST_DIR"
}

# Test case 1: Scramble a file with default patterns
test_default_patterns() {
    local input_file="${TEST_DIR}/input.log"
    local output_file="${TEST_DIR}/output.log"

    echo "192.168.1.1 failed login for user@example.com on 2023-10-27 at 14:30:00. UUID: a1b2c3d4-e5f6-7890-1234-567890abcdef" > "$input_file"

    # Execute the main script with RANDOM=0 for deterministic replacement
    RANDOM=0 "$SCRIPT_PATH" "$input_file" "$output_file"

    if [[ $? -ne 0 ]]; then
        echo "Test failed: Script exited with error for default patterns." >&2
        return 1
    fi

    local scrambled_content=$(cat "$output_file")

    # Check if original patterns are gone
    if echo "$scrambled_content" | grep -qE "192\.168\.1\.1|user@example\.com|2023-10-27|14:30:00|a1b2c3d4-e5f6-7890-1234-567890abcdef"; then
        echo "Test failed: Original sensitive patterns found in scrambled content." >&2
        return 1
    fi

    # Check if the deterministic replacement word is present
    if ! echo "$scrambled_content" | grep -q "Glimmer"; then
        echo "Test failed: Replacement word 'Glimmer' not found." >&2
        return 1
    fi

    echo "Test passed: Default patterns scrambled correctly."
    return 0
}

# Test case 2: Scramble with custom patterns via SCRAMBLE_PATTERNS env var
test_custom_patterns() {
    local input_file="${TEST_DIR}/input_custom.log"
    local output_file="${TEST_DIR}/output_custom.log"

    echo "SecretKey: ABCDEF123456, UserID: 7890" > "$input_file"

    # Custom pattern for "SecretKey: [alphanumeric]" and "UserID: [digits]"
    export SCRAMBLE_PATTERNS='SecretKey: [A-Za-z0-9]+,UserID: [0-9]+'
    RANDOM=0 "$SCRIPT_PATH" "$input_file" "$output_file"
    unset SCRAMBLE_PATTERNS # Clean up env var

    if [[ $? -ne 0 ]]; then
        echo "Test failed: Script exited with error for custom patterns." >&2
        return 1
    fi

    local scrambled_content=$(cat "$output_file")

    # Check if original custom patterns are gone
    if echo "$scrambled_content" | grep -qE "SecretKey: ABCDEF123456|UserID: 7890"; then
        echo "Test failed: Custom patterns not scrambled." >&2
        return 1
    fi

    # Check if the deterministic replacement word is present
    if ! echo "$scrambled_content" | grep -q "Glimmer"; then
        echo "Test failed: Replacement word 'Glimmer' not found for custom patterns." >&2
        return 1
    fi

    echo "Test passed: Custom patterns scrambled correctly."
    return 0
}

# Test case 3: Input file not found
test_input_file_not_found() {
    local non_existent_file="${TEST_DIR}/non_existent.log"
    local output_file="${TEST_DIR}/output_error.log"

    # Run the script and capture stderr
    local error_output
    error_output=$("$SCRIPT_PATH" "$non_existent_file" "$output_file" 2>&1 >/dev/null)
    local exit_code=$?

    if [[ $exit_code -eq 0 ]]; then
        echo "Test failed: Script did not exit with error for non-existent file." >&2
        return 1
    fi
    if ! echo "$error_output" | grep -q "Error: Input file '$non_existent_file' not found."; then
        echo "Test failed: Incorrect error message for non-existent file." >&2
        return 1
    fi

    echo "Test passed: Handles non-existent input file correctly."
    return 0
}

# Test case 4: Output to stdout when no output file is specified
test_output_to_stdout() {
    local input_file="${TEST_DIR}/input_stdout.log"
    echo "Sensitive data: 1.2.3.4" > "$input_file"

    local stdout_output
    RANDOM=0 stdout_output=$("$SCRIPT_PATH" "$input_file")
    local exit_code=$?

    if [[ $exit_code -ne 0 ]]; then
        echo "Test failed: Script exited with error when outputting to stdout." >&2
        return 1
    fi

    if echo "$stdout_output" | grep -q "1\.2\.3\.4"; then
        echo "Test failed: IP address not scrambled when outputting to stdout." >&2
        return 1
    fi
    if ! echo "$stdout_output" | grep -q "Glimmer"; then
        echo "Test failed: Replacement word 'Glimmer' not found in stdout output." >&2
        return 1
    fi

    echo "Test passed: Outputs to stdout correctly."
    return 0
}

# Run all tests
run_tests() {
    setup

    local overall_status=0

    test_default_patterns || overall_status=1
    test_custom_patterns || overall_status=1
    test_input_file_not_found || overall_status=1
    test_output_to_stdout || overall_status=1

    teardown

    if [[ $overall_status -eq 0 ]]; then
        echo "All tests passed!"
        return 0
    else
        echo "Some tests failed." >&2
        return 1
    fi
}

run_tests
