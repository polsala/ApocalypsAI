#!/bin/bash

# Mock log file for testing
MOCK_LOG_FILE="mock_syslog.log"

# Create a mock log file
cat << EOF > "$MOCK_LOG_FILE"
Oct 27 10:00:01 server1 kernel: [    0.000000] Linux version 5.15.0-87-generic (buildd@lcy02-amd64-030) (gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #97-Ubuntu SMP Mon Oct 2 20:10:43 UTC 2023
Oct 27 10:05:15 server1 systemd[1]: Started Network Manager.
Oct 27 10:10:30 server1 authpriv: sshd[1234]: Accepted password for user from 192.168.1.10 port 54321 ssh2
Oct 27 10:15:45 server1 kern.log: [    1.234567] Some kernel message with ERROR in it.
Oct 27 10:20:00 server1 user.info: User logged in successfully.
Oct 27 10:25:55 server1 daemon.warn: Some warning message about network configuration.
Oct 27 10:30:10 server1 kern.log: [    2.345678] Another kernel message.
Oct 27 10:35:20 server1 authpriv: sshd[5678]: Failed password for invalid user from 10.0.0.5 port 12345 ssh2
Oct 27 10:40:00 server1 systemd[1]: Stopping Network Manager...
Oct 27 10:45:00 server1 kern.log: [    3.456789] Critical system error detected!
Oct 27 10:50:00 server1 user.info: User logged out.
Oct 27 10:55:00 server1 daemon.info: Network service restarted.
Oct 27 11:00:00 server1 kernel: [    4.567890] System is now stable.
EOF

# Function to run a test case
run_test() {
    TEST_NAME="$1"
    EXPECTED_OUTPUT="$2"
    COMMAND="$3"

    echo "Running test: $TEST_NAME"
    ACTUAL_OUTPUT="$($COMMAND)"

    if [ "$ACTUAL_OUTPUT" == "$EXPECTED_OUTPUT" ]; then
        echo "  PASS"
    else
        echo "  FAIL"
        echo "    Expected: $EXPECTED_OUTPUT"
        echo "    Actual:   $ACTUAL_OUTPUT"
        return 1
    fi
    return 0
}

# --- Test Cases ---

TEST_COUNT=0
PASS_COUNT=0

# Test 1: Basic keyword search (case-insensitive)
TEST_NAME="Basic Keyword Search"
EXPECTED_OUTPUT="Oct 27 10:15:45 server1 authpriv: sshd[5678]: Failed password for invalid user from 10.0.0.5 port 12345 ssh2
Oct 27 10:45:00 server1 kern.log: [    3.456789] Critical system error detected!"
COMMAND="./src/nightly-syslog-parser.sh -k "failed" -f "$MOCK_LOG_FILE""
TEST_COUNT=$((TEST_COUNT + 1))
if run_test "$TEST_NAME" "$EXPECTED_OUTPUT" "$COMMAND"; then
    PASS_COUNT=$((PASS_COUNT + 1))
fi

# Test 2: Pattern search (regex)
TEST_NAME="Pattern Search (Regex)"
EXPECTED_OUTPUT="Oct 27 10:05:15 server1 systemd[1]: Started Network Manager.
Oct 27 10:25:55 server1 daemon.warn: Some warning message about network configuration.
Oct 27 10:55:00 server1 daemon.info: Network service restarted."
COMMAND="./src/nightly-syslog-parser.sh -p "Network" -f "$MOCK_LOG_FILE""
TEST_COUNT=$((TEST_COUNT + 1))
if run_test "$TEST_NAME" "$EXPECTED_OUTPUT" "$COMMAND"; then
    PASS_COUNT=$((PASS_COUNT + 1))
fi

# Test 3: Start time filter
TEST_NAME="Start Time Filter"
EXPECTED_OUTPUT="Oct 27 10:15:45 server1 authpriv: sshd[5678]: Failed password for invalid user from 10.0.0.5 port 12345 ssh2
Oct 27 10:20:00 server1 user.info: User logged in successfully.
Oct 27 10:25:55 server1 daemon.warn: Some warning message about network configuration.
Oct 27 10:30:10 server1 kern.log: [    2.345678] Another kernel message.
Oct 27 10:35:20 server1 authpriv: sshd[5678]: Failed password for invalid user from 10.0.0.5 port 12345 ssh2
Oct 27 10:40:00 server1 systemd[1]: Stopping Network Manager...
Oct 27 10:45:00 server1 kern.log: [    3.456789] Critical system error detected!
Oct 27 10:50:00 server1 user.info: User logged out.
Oct 27 10:55:00 server1 daemon.info: Network service restarted.
Oct 27 11:00:00 server1 kernel: [    4.567890] System is now stable."
COMMAND="./src/nightly-syslog-parser.sh -t "2023-10-27 10:15:45" -f "$MOCK_LOG_FILE""
TEST_COUNT=$((TEST_COUNT + 1))
if run_test "$TEST_NAME" "$EXPECTED_OUTPUT" "$COMMAND"; then
    PASS_COUNT=$((PASS_COUNT + 1))
fi

# Test 4: End time filter
TEST_NAME="End Time Filter"
EXPECTED_OUTPUT="Oct 27 10:00:01 server1 kernel: [    0.000000] Linux version 5.15.0-87-generic (buildd@lcy02-amd64-030) (gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #97-Ubuntu SMP Mon Oct 2 20:10:43 UTC 2023
Oct 27 10:05:15 server1 systemd[1]: Started Network Manager.
Oct 27 10:10:30 server1 authpriv: sshd[1234]: Accepted password for user from 192.168.1.10 port 54321 ssh2
Oct 27 10:15:45 server1 kern.log: [    1.234567] Some kernel message with ERROR in it.
Oct 27 10:20:00 server1 user.info: User logged in successfully.
Oct 27 10:25:55 server1 daemon.warn: Some warning message about network configuration.
Oct 27 10:30:10 server1 kern.log: [    2.345678] Another kernel message.
Oct 27 10:35:20 server1 authpriv: sshd[5678]: Failed password for invalid user from 10.0.0.5 port 12345 ssh2
Oct 27 10:40:00 server1 systemd[1]: Stopping Network Manager..."
COMMAND="./src/nightly-syslog-parser.sh -e "2023-10-27 10:40:00" -f "$MOCK_LOG_FILE""
TEST_COUNT=$((TEST_COUNT + 1))
if run_test "$TEST_NAME" "$EXPECTED_OUTPUT" "$COMMAND"; then
    PASS_COUNT=$((PASS_COUNT + 1))
fi

# Test 5: Start and End time filter
TEST_NAME="Start and End Time Filter"
EXPECTED_OUTPUT="Oct 27 10:15:45 server1 kern.log: [    1.234567] Some kernel message with ERROR in it.
Oct 27 10:20:00 server1 user.info: User logged in successfully.
Oct 27 10:25:55 server1 daemon.warn: Some warning message about network configuration.
Oct 27 10:30:10 server1 kern.log: [    2.345678] Another kernel message.
Oct 27 10:35:20 server1 authpriv: sshd[5678]: Failed password for invalid user from 10.0.0.5 port 12345 ssh2
Oct 27 10:40:00 server1 systemd[1]: Stopping Network Manager..."
COMMAND="./src/nightly-syslog-parser.sh -t "2023-10-27 10:15:45" -e "2023-10-27 10:40:00" -f "$MOCK_LOG_FILE""
TEST_COUNT=$((TEST_COUNT + 1))
if run_test "$TEST_NAME" "$EXPECTED_OUTPUT" "$COMMAND"; then
    PASS_COUNT=$((PASS_COUNT + 1))
fi

# Test 6: Keyword and Start time filter
TEST_NAME="Keyword and Start Time Filter"
EXPECTED_OUTPUT="Oct 27 10:15:45 server1 kern.log: [    1.234567] Some kernel message with ERROR in it.
Oct 27 10:45:00 server1 kern.log: [    3.456789] Critical system error detected!"
COMMAND="./src/nightly-syslog-parser.sh -k "kernel" -t "2023-10-27 10:15:00" -f "$MOCK_LOG_FILE""
TEST_COUNT=$((TEST_COUNT + 1))
if run_test "$TEST_NAME" "$EXPECTED_OUTPUT" "$COMMAND"; then
    PASS_COUNT=$((PASS_COUNT + 1))
fi

# Test 7: Output to file (check file content)
TEST_NAME="Output to File"
OUTPUT_FILE="test_output.log"
EXPECTED_OUTPUT="Oct 27 10:15:45 server1 authpriv: sshd[5678]: Failed password for invalid user from 10.0.0.5 port 12345 ssh2"
COMMAND="./src/nightly-syslog-parser.sh -k "failed" -f "$MOCK_LOG_FILE" -o "$OUTPUT_FILE" && cat "$OUTPUT_FILE""
TEST_COUNT=$((TEST_COUNT + 1))
if run_test "$TEST_NAME" "$EXPECTED_OUTPUT" "$COMMAND"; then
    PASS_COUNT=$((PASS_COUNT + 1))
fi
rm -f "$OUTPUT_FILE"

# Test 8: No matches
TEST_NAME="No Matches"
EXPECTED_OUTPUT=""
COMMAND="./src/nightly-syslog-parser.sh -k "NONEXISTENT" -f "$MOCK_LOG_FILE""
TEST_COUNT=$((TEST_COUNT + 1))
if run_test "$TEST_NAME" "$EXPECTED_OUTPUT" "$COMMAND"; then
    PASS_COUNT=$((PASS_COUNT + 1))
fi

# --- Summary ---

echo "--------------------"
echo "Test Summary: $PASS_COUNT / $TEST_COUNT passed."

# Clean up mock log file
rm "$MOCK_LOG_FILE"

if [ "$PASS_COUNT" -eq "$TEST_COUNT" ]; then
    exit 0
else
    exit 1
fi
