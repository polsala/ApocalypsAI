#!/bin/bash

# Source shunit2
# Assumes shunit2 is in the same directory or in PATH
. shunit2

# Define the script to be tested
SCRIPT="../src/syslog_filter.sh"

# Mock the script for testing purposes
# This allows us to control input and output without actually running the script
# Mock rationale: We are testing the logic of the filter script itself, not its interaction with the actual syslog daemon or file system. By mocking, we can provide controlled inputs and verify outputs deterministically.
_mock_script() {
    local input="$1"
    local script_content="$(cat "$SCRIPT")"
    # Inject mock patterns into the script content
    local mock_script_content="$(echo "$script_content" | sed 's/^INCLUDE_PATTERNS=("error" "warning")/INCLUDE_PATTERNS=("error" "warning" "critical")/' | sed 's/^EXCLUDE_PATTERNS=("systemd")/EXCLUDE_PATTERNS=("systemd" "debug" "verbose")/')"

    # Execute the modified script with the provided input
    echo "$input" | bash -c "$mock_script_content"
}

# Test case 1: Basic inclusion and exclusion
test_basic_filtering() {
    local input="
Line 1: This is an error message.
Line 2: A normal log entry.
Line 3: systemd process started.
Line 4: Another warning message.
Line 5: Critical system failure.
Line 6: Debugging info."
    local expected_output="
Line 1: This is an error message.
Line 4: Another warning message.
Line 5: Critical system failure."

    assertEquals "$(echo "$input" | _mock_script)" "$expected_output"
}

# Test case 2: No include patterns (should include everything not excluded)
test_no_include_patterns() {
    local input="
Line 1: This is an error message.
Line 2: A normal log entry.
Line 3: systemd process started.
Line 4: Another warning message.
Line 5: Critical system failure.
Line 6: Debugging info."
    # Mock script to have empty INCLUDE_PATTERNS
    local script_content="$(cat "$SCRIPT")"
    local mock_script_content="$(echo "$script_content" | sed 's/^INCLUDE_PATTERNS=("error" "warning" "critical")/INCLUDE_PATTERNS=()/')"

    local expected_output="
Line 1: This is an error message.
Line 2: A normal log entry.
Line 4: Another warning message.
Line 5: Critical system failure."

    assertEquals "$(echo "$input" | bash -c "$mock_script_content")" "$expected_output"
}

# Test case 3: Empty input
test_empty_input() {
    local input=""
    local expected_output=""
    assertEquals "$(echo "$input" | _mock_script)" "$expected_output"
}

# Test case 4: Only excluded lines
test_only_excluded_lines() {
    local input="
Line 1: systemd is running.
Line 2: debug message.
Line 3: verbose output."
    local expected_output=""
    assertEquals "$(echo "$input" | _mock_script)" "$expected_output"
}

# Test case 5: Lines with special characters in patterns
test_special_chars_in_patterns() {
    local input="
Line 1: Error: [CODE 123]
Line 2: Warning! (urgent)
Line 3: systemd: service restart."
    # Mock script to include lines with brackets and parentheses
    local script_content="$(cat "$SCRIPT")"
    local mock_script_content="$(echo "$script_content" | sed 's/^INCLUDE_PATTERNS=("error" "warning" "critical")/INCLUDE_PATTERNS=("error: \[CODE [0-9]+\]" "warning! \(urgent\)")/')"

    local expected_output="
Line 1: Error: [CODE 123]
Line 2: Warning! (urgent)"

    assertEquals "$(echo "$input" | bash -c "$mock_script_content")" "$expected_output"
}

# Test case 6: No matches at all
test_no_matches() {
    local input="
This line has no relevant keywords.
Another unrelated line."
    local expected_output=""
    assertEquals "$(echo "$input" | _mock_script)" "$expected_output"
}
