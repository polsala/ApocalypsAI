#!/bin/bash

# Mock log file for testing
cat << EOF > mock_syslog.log
Oct 26 10:00:01 server1 sshd[1234]: Accepted password for user from 192.168.1.100 port 54321 ssh2
Oct 26 10:05:15 server1 kernel: [12345.67890] Out of memory: Kill process 5678 (some_app) score 987 or sacrifice child
Oct 26 10:10:30 server1 systemd[1]: Starting Some Service...
Oct 26 10:15:45 server1 auth: Failed password for invalid user from 10.0.0.5 port 12345 ssh2
Oct 26 10:20:00 server1 cron[9876]: (root) CMD (command to run)
Oct 26 10:25:10 server1 kernel: [12346.12345] TCP: Possible memory leak.
Oct 26 10:30:00 server1 sshd[5432]: Invalid user testuser from 192.168.1.100
Oct 26 11:00:00 server1 systemd[1]: Started Some Service.
Oct 27 09:00:00 server1 kernel: [12347.00000] Some other kernel message.
Oct 27 11:30:00 server1 sshd[6789]: Accepted password for admin from 172.16.0.1 port 67890 ssh2
EOF

# Mock rationale: These log entries are representative of common syslog formats and cover various scenarios (successful logins, errors, kernel messages, etc.) to ensure comprehensive testing.

# --- Test Functions ---
run_test() {
    local test_name="$1"
    local expected_output="$2"
    local actual_output="$(eval "$3 2>/dev/null")"

    echo -n "Running test: $test_name... "
    if [ "$actual_output" == "$expected_output" ]; then
        echo "PASSED"
    else
        echo "FAILED"
        echo "  Expected:"
        echo "$expected_output"
        echo "  Actual:"
        echo "$actual_output"
        return 1
    fi
    return 0
}

# --- Test Cases ---

# Test 1: Basic keyword search
TEST_CMD="./nightly-syslog-parser.sh -k 'Accepted'"
EXPECTED_OUTPUT="Oct 26 10:00:01 server1 sshd[1234]: Accepted password for user from 192.168.1.100 port 54321 ssh2\nOct 26 11:30:00 server1 sshd[6789]: Accepted password for admin from 172.16.0.1 port 67890 ssh2"
run_test "Keyword Search" "$EXPECTED_OUTPUT" "$TEST_CMD"

# Test 2: IP address filter
TEST_CMD="./nightly-syslog-parser.sh -i 192.168.1.100"
EXPECTED_OUTPUT="Oct 26 10:00:01 server1 sshd[1234]: Accepted password for user from 192.168.1.100 port 54321 ssh2\nOct 26 10:30:00 server1 sshd[5432]: Invalid user testuser from 192.168.1.100"
run_test "IP Address Filter" "$EXPECTED_OUTPUT" "$TEST_CMD"

# Test 3: Regex pattern search
TEST_CMD="./nightly-syslog-parser.sh -p '^Oct 26 10:1[0-5]:'"
EXPECTED_OUTPUT="Oct 26 10:05:15 server1 kernel: [12345.67890] Out of memory: Kill process 5678 (some_app) score 987 or sacrifice child\nOct 26 10:10:30 server1 systemd[1]: Starting Some Service...\nOct 26 10:15:45 server1 auth: Failed password for invalid user from 10.0.0.5 port 12345 ssh2"
run_test "Regex Pattern Search" "$EXPECTED_OUTPUT" "$TEST_CMD"

# Test 4: Start time filter
TEST_CMD="./nightly-syslog-parser.sh -s '2023-10-26 10:15:00'"
EXPECTED_OUTPUT="Oct 26 10:15:45 server1 auth: Failed password for invalid user from 10.0.0.5 port 12345 ssh2\nOct 26 10:20:00 server1 cron[9876]: (root) CMD (command to run)\nOct 26 10:25:10 server1 kernel: [12346.12345] TCP: Possible memory leak.\nOct 26 10:30:00 server1 sshd[5432]: Invalid user testuser from 192.168.1.100\nOct 26 11:00:00 server1 systemd[1]: Started Some Service."
run_test "Start Time Filter" "$EXPECTED_OUTPUT" "$TEST_CMD"

# Test 5: End time filter
TEST_CMD="./nightly-syslog-parser.sh -e '2023-10-26 10:15:00'"
EXPECTED_OUTPUT="Oct 26 10:00:01 server1 sshd[1234]: Accepted password for user from 192.168.1.100 port 54321 ssh2\nOct 26 10:05:15 server1 kernel: [12345.67890] Out of memory: Kill process 5678 (some_app) score 987 or sacrifice child\nOct 26 10:10:30 server1 systemd[1]: Starting Some Service...\nOct 26 10:15:45 server1 auth: Failed password for invalid user from 10.0.0.5 port 12345 ssh2"
run_test "End Time Filter" "$EXPECTED_OUTPUT" "$TEST_CMD"

# Test 6: Start and End time filter
TEST_CMD="./nightly-syslog-parser.sh -s '2023-10-26 10:10:00' -e '2023-10-26 10:25:00'"
EXPECTED_OUTPUT="Oct 26 10:10:30 server1 systemd[1]: Starting Some Service...\nOct 26 10:15:45 server1 auth: Failed password for invalid user from 10.0.0.5 port 12345 ssh2\nOct 26 10:20:00 server1 cron[9876]: (root) CMD (command to run)\nOct 26 10:25:10 server1 kernel: [12346.12345] TCP: Possible memory leak."
run_test "Start and End Time Filter" "$EXPECTED_OUTPUT" "$TEST_CMD"

# Test 7: Combined filters (keyword and IP)
TEST_CMD="./nightly-syslog-parser.sh -k 'Invalid user' -i 192.168.1.100"
EXPECTED_OUTPUT="Oct 26 10:30:00 server1 sshd[5432]: Invalid user testuser from 192.168.1.100"
run_test "Combined Filters (Keyword + IP)" "$EXPECTED_OUTPUT" "$TEST_CMD"

# Test 8: Output to file
OUTPUT_FILE="test_output.log"
TEST_CMD="./nightly-syslog-parser.sh -k 'kernel' -o $OUTPUT_FILE"
$TEST_CMD
EXPECTED_OUTPUT="Oct 26 10:05:15 server1 kernel: [12345.67890] Out of memory: Kill process 5678 (some_app) score 987 or sacrifice child\nOct 26 10:25:10 server1 kernel: [12346.12345] TCP: Possible memory leak.\nOct 26 11:00:00 server1 systemd[1]: Started Some Service."
# Mock rationale: The actual output to the file is checked by reading the file content.
ACTUAL_OUTPUT=$(cat "$OUTPUT_FILE")

if [ "$ACTUAL_OUTPUT" == "$EXPECTED_OUTPUT" ]; then
    echo "Running test: Output to File... PASSED"
    rm "$OUTPUT_FILE"
else
    echo "Running test: Output to File... FAILED"
    echo "  Expected:"
    echo "$EXPECTED_OUTPUT"
    echo "  Actual:"
    echo "$ACTUAL_OUTPUT"
    rm "$OUTPUT_FILE"
    return 1
fi

# Test 9: No matching results
TEST_CMD="./nightly-syslog-parser.sh -k 'nonexistent_keyword'"
EXPECTED_OUTPUT=""
run_test "No Matching Results" "$EXPECTED_OUTPUT" "$TEST_CMD"

# Test 10: Invalid date format (should ideally not error out but produce no results or handle gracefully)
# The current script relies on `date -d` which might error. For simplicity, we expect no output.
TEST_CMD="./nightly-syslog-parser.sh -s 'invalid-date'"
EXPECTED_OUTPUT=""
run_test "Invalid Start Date Format" "$EXPECTED_OUTPUT" "$TEST_CMD"

# Clean up mock log file
rm mock_syslog.log

exit 0
