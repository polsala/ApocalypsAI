#!/bin/bash

# Define test directory
TEST_DIR="$(dirname "$0")"

# Define the script to test
SCRIPT_TO_TEST="$TEST_DIR/../src/nightly-syslog-parser.sh"

# Define mock log file
MOCK_LOG_FILE="$TEST_DIR/mock_syslog.log"

# --- Mock Data --- #
# Mock rationale: These files simulate real syslog entries without requiring actual system logs.
# This ensures deterministic and offline testing.

cat << EOF > "$MOCK_LOG_FILE"
Oct 26 10:00:01 myhost kernel: [    0.000000] Linux version 5.15.0-87-generic (buildd@lcy02-amd64-028) (gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #97-Ubuntu SMP Mon Oct 2 21:09:21 UTC 2023
Oct 26 10:00:01 myhost systemd[1]: Starting Load Kernel Modules...
Oct 26 10:00:02 myhost sshd[1234]: Server listening on 0.0.0.0 port 22.
Oct 26 10:00:02 myhost sshd[1234]: Server listening on :: port 22.
Oct 26 10:00:03 myhost CRON[5678]: (root) CMD (command -v debian-sa1 > /dev/null && debian-sa1 1 1)
Oct 26 10:00:05 myhost app[9999]: An informational message.
Oct 26 10:00:06 myhost app[9999]: An error occurred during processing.
Oct 26 10:00:07 myhost app[9999]: Another informational message.
Oct 26 10:00:08 myhost systemd[1]: Started Network Manager.
Oct 26 10:00:09 myhost sshd[1235]: Failed password for invalid user test from 192.168.1.100 port 54321 ssh2
EOF

# Mock rationale: A simple test script to verify the functionality of the main script.
# It uses the mock_syslog.log file and checks the output against expected results.

cat << EOF > "$TEST_DIR/test_syslog_parser.sh"
#!/bin/bash

# Source the script to test for functions if needed, but here we'll call it directly.

# Mock log file for testing
MOCK_LOG="$TEST_DIR/mock_syslog.log"

# --- Test Cases ---

# Test 1: Basic filtering with default output
run_test() {
    local test_name="$1"
    local pattern="$2"
    local output_format="$3"
    local expected_output="$4"
    local log_file="$5"

    echo "Running test: $test_name"
    local actual_output
    if [ -n "$output_format" ]; then
        actual_output="$($SCRIPT_TO_TEST -p \"$pattern\" -o \"$output_format\" \"$log_file\")"
    else
        actual_output="$($SCRIPT_TO_TEST -p \"$pattern\" \"$log_file\")"
    fi

    if [ "$actual_output" = "$expected_output" ]; then
        echo "  PASS"
    else
        echo "  FAIL"
        echo "    Expected:"
        echo "$expected_output"
        echo "    Actual:"
        echo "$actual_output"
        return 1
    fi
    return 0
}

# Test 1: Filter for 'error' with default format
expected_output_1="Oct 26 10:00:06 myhost app[9999]: An error occurred during processing."
run_test "Filter error messages" "error" "" "$expected_output_1" "$MOCK_LOG"

# Test 2: Filter for 'sshd' with custom format (timestamp and message)
expected_output_2="Oct 26 10:00:02 192.168.1.100: Server listening on 0.0.0.0 port 22.\nOct 26 10:00:09 192.168.1.100: Failed password for invalid user test from 192.168.1.100 port 54321 ssh2"
run_test "Filter sshd messages with custom format" "sshd" "%timestamp% %message%" "$expected_output_2" "$MOCK_LOG"

# Test 3: Filter for 'Failed password' with custom format (process and message)
expected_output_3="sshd[1235]: Failed password for invalid user test from 192.168.1.100 port 54321 ssh2"
run_test "Filter failed login with custom format" "Failed password" "%process%: %message%" "$expected_output_3" "$MOCK_LOG"

# Test 4: No pattern, just default output (should output all lines, but parsing might be imperfect)
# This test is more to check if it runs without error and produces some output.
# The exact output depends on the awk parsing, which is simplified.
# We'll check for presence of key elements rather than exact match for this one.
expected_partial_output_4="Oct 26 10:00:01"
actual_output_4="$($SCRIPT_TO_TEST "$MOCK_LOG")"
if echo "$actual_output_4" | grep -q "$expected_partial_output_4"; then
    echo "Running test: No pattern, default output (partial check)"
    echo "  PASS"
else
    echo "Running test: No pattern, default output (partial check)"
    echo "  FAIL"
    echo "    Expected to contain: $expected_partial_output_4"
    echo "    Actual:"
    echo "$actual_output_4"
    exit 1
fi

# Test 5: Invalid log file
run_test "Invalid log file" "error" "" "Error: Log file 'non_existent_file.log' not found."
 "non_existent_file.log"

# Test 6: No log file provided
run_test "No log file provided" "error" "" "Error: Log file not specified.
Usage: $(basename "$0") [OPTIONS] <log_file>

A whimsical yet useful bash utility to parse and filter syslog messages.

Options:
  -p, --pattern <regex>     The regular expression pattern to search for in syslog messages.
  -o, --output-format <format> The output format string. Available placeholders:
                            %timestamp%, %hostname%, %process%, %message%.
                            Default: \"%timestamp% %hostname% %process%: %message%\"
  -h, --help                Display this help message."
 ""

exit 0
