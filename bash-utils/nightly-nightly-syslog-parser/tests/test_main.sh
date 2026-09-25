#!/bin/bash

# Mock log files

# Mock rationale: These files simulate different log scenarios for deterministic testing.

# Mock log file 1: Basic log entries
cat << EOF > mock_syslog.log
2023-10-27 10:00:01 INFO: System started successfully.
2023-10-27 10:01:15 WARN: Disk space low on /var/log.
2023-10-27 10:02:30 ERROR: Failed to connect to database.
2023-10-27 10:03:45 INFO: User 'admin' logged in.
2023-10-27 10:04:50 DEBUG: Processing request.
2023-10-27 10:05:01 ERROR: Another critical error occurred.
EOF

# Mock log file 2: Different timestamp format and more noise
cat << EOF > mock_auth.log
Oct 27 10:10:05 server sshd[1234]: Accepted password for user from 192.168.1.100 port 54321 ssh2
Oct 27 10:11:10 server sshd[1235]: Failed password for invalid user test from 192.168.1.101 port 12345 ssh2
Oct 27 10:12:00 server sudo: user : TTY=pts/0 ; PWD=/home/user ; USER=root ; COMMAND=/bin/bash
Oct 27 10:13:05 server sshd[1236]: Accepted password for user from 192.168.1.100 port 54322 ssh2
Oct 27 10:14:10 server sshd[1237]: Failed password for invalid user admin from 192.168.1.102 port 67890 ssh2
EOF

# Mock log file 3: No relevant entries for some tests
cat << EOF > mock_empty.log
EOF

# --- Test Functions ---

run_test() {
    local test_name="$1"
    local expected_output="$2"
    local actual_output="$3"

    if [ "$expected_output" == "$actual_output" ]; then
        echo "✅ PASS: $test_name"
    else
        echo "❌ FAIL: $test_name"
        echo "  Expected: $expected_output"
        echo "  Actual:   $actual_output"
        return 1
    fi
    return 0
}

# Test 1: Basic keyword search

TEST_NAME="Basic keyword search (INFO)"
EXPECTED="2023-10-27 10:00:01 INFO: System started successfully.
2023-10-27 10:03:45 INFO: User 'admin' logged in."
ACTUAL=$(./src/main.sh -k INFO mock_syslog.log)
run_test "$TEST_NAME" "$EXPECTED" "$ACTUAL"

TEST_NAME="Basic keyword search (ERROR)"
EXPECTED="2023-10-27 10:02:30 ERROR: Failed to connect to database.
2023-10-27 10:05:01 ERROR: Another critical error occurred."
ACTUAL=$(./src/main.sh -k ERROR mock_syslog.log)
run_test "$TEST_NAME" "$EXPECTED" "$ACTUAL"

# Test 2: Pattern search

TEST_NAME="Pattern search (Failed password)"
EXPECTED="Oct 27 10:11:10 server sshd[1235]: Failed password for invalid user test from 192.168.1.101 port 12345 ssh2
Oct 27 10:14:10 server sshd[1237]: Failed password for invalid user admin from 192.168.1.102 port 67890 ssh2"
ACTUAL=$(./src/main.sh -p "Failed password" mock_auth.log)
run_test "$TEST_NAME" "$EXPECTED" "$ACTUAL"

# Test 3: Timestamp filtering (start time)

TEST_NAME="Timestamp filtering (start time)"
EXPECTED="2023-10-27 10:01:15 WARN: Disk space low on /var/log.
2023-10-27 10:02:30 ERROR: Failed to connect to database.
2023-10-27 10:03:45 INFO: User 'admin' logged in.
2023-10-27 10:04:50 DEBUG: Processing request.
2023-10-27 10:05:01 ERROR: Another critical error occurred."
ACTUAL=$(./src/main.sh -s "2023-10-27 10:01:00" mock_syslog.log)
run_test "$TEST_NAME" "$EXPECTED" "$ACTUAL"

# Test 4: Timestamp filtering (end time)

TEST_NAME="Timestamp filtering (end time)"
EXPECTED="2023-10-27 10:00:01 INFO: System started successfully.
2023-10-27 10:01:15 WARN: Disk space low on /var/log.
2023-10-27 10:02:30 ERROR: Failed to connect to database."
ACTUAL=$(./src/main.sh -e "2023-10-27 10:03:00" mock_syslog.log)
run_test "$TEST_NAME" "$EXPECTED" "$ACTUAL"

# Test 5: Timestamp filtering (start and end time)

TEST_NAME="Timestamp filtering (start and end time)"
EXPECTED="2023-10-27 10:02:30 ERROR: Failed to connect to database.
2023-10-27 10:03:45 INFO: User 'admin' logged in."
ACTUAL=$(./src/main.sh -s "2023-10-27 10:02:00" -e "2023-10-27 10:04:00" mock_syslog.log)
run_test "$TEST_NAME" "$EXPECTED" "$ACTUAL"

# Test 6: Log level highlighting

TEST_NAME="Log level highlighting (WARN)"
# Mock rationale: ANSI escape codes are used for coloring. The expected output includes these codes.
EXPECTED="2023-10-27 10:00:01 INFO: System started successfully.
2023-10-27 10:01:15 \033[0;33mWARN\033[0m: Disk space low on /var/log.
2023-10-27 10:02:30 ERROR: Failed to connect to database.
2023-10-27 10:03:45 INFO: User 'admin' logged in.
2023-10-27 10:04:50 DEBUG: Processing request.
2023-10-27 10:05:01 ERROR: Another critical error occurred."
ACTUAL=$(./src/main.sh -l WARN mock_syslog.log)
run_test "$TEST_NAME" "$EXPECTED" "$ACTUAL"

# Test 7: Log level highlighting (ERROR)

TEST_NAME="Log level highlighting (ERROR)"
EXPECTED="2023-10-27 10:00:01 INFO: System started successfully.
2023-10-27 10:01:15 WARN: Disk space low on /var/log.
2023-10-27 10:02:30 \033[0;31mERROR\033[0m: Failed to connect to database.
2023-10-27 10:03:45 INFO: User 'admin' logged in.
2023-10-27 10:04:50 DEBUG: Processing request.
2023-10-27 10:05:01 \033[0;31mERROR\033[0m: Another critical error occurred."
ACTUAL=$(./src/main.sh -l ERROR mock_syslog.log)
run_test "$TEST_NAME" "$EXPECTED" "$ACTUAL"

# Test 8: No filters applied

TEST_NAME="No filters applied"
EXPECTED=$(cat mock_syslog.log)
ACTUAL=$(./src/main.sh mock_syslog.log)
run_test "$TEST_NAME" "$EXPECTED" "$ACTUAL"

# Test 9: Empty log file

TEST_NAME="Empty log file"
EXPECTED=""
ACTUAL=$(./src/main.sh mock_empty.log)
run_test "$TEST_NAME" "$EXPECTED" "$ACTUAL"

# Test 10: Invalid log file

TEST_NAME="Invalid log file"
EXPECTED="Error: Log file 'non_existent_log.log' not found."
ACTUAL=$(./src/main.sh non_existent_log.log 2>&1)
run_test "$TEST_NAME" "$EXPECTED" "$ACTUAL"

# Test 11: Invalid timestamp format

TEST_NAME="Invalid start timestamp format"
EXPECTED="Error: Invalid start time format. Please use 'YYYY-MM-DD HH:MM:SS'."
ACTUAL=$(./src/main.sh -s "invalid-date" mock_syslog.log 2>&1)
run_test "$TEST_NAME" "$EXPECTED" "$ACTUAL"

# Clean up mock files
rm mock_syslog.log mock_auth.log mock_empty.log

exit 0
