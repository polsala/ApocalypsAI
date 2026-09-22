#!/bin/bash

# test_nightly-syslog-parser.sh
# Unit tests for the nightly-syslog-parser.sh script.

# --- Mock Setup ---

# Create a temporary directory for test files
TEST_DIR=$(mktemp -d)

# Mock log files
TEST_LOG_FILE_1="$TEST_DIR/syslog_test_1.log"
TEST_LOG_FILE_2="$TEST_DIR/syslog_test_2.log"

# Mock rationale: These files simulate different syslog contents for testing.
cat << EOF > "$TEST_LOG_FILE_1"
Oct 10 10:00:01 server1 kernel: [ 123.456] Some informational message.
Oct 10 10:01:02 server1 auth: Failed login for user 'admin' from 192.168.1.100
Oct 10 10:02:03 server1 daemon: Service started successfully.
Oct 10 10:03:04 server1 kernel: [ 789.012] Another info message.
Oct 10 10:04:05 server1 auth: Successful login for user 'guest' from 10.0.0.5
Oct 10 10:05:06 server1 daemon: Warning: Disk space low.
Oct 10 10:06:07 server1 kernel: [ 111.222] Critical error encountered.
EOF

cat << EOF > "$TEST_LOG_FILE_2"
Oct 10 11:00:01 server2 kernel: [ 321.654] System reboot initiated.
Oct 10 11:01:02 server2 auth: Failed login for user 'root' from 192.168.1.100
Oct 10 11:02:03 server2 daemon: Service stopped.
Oct 10 11:03:04 server2 kernel: [ 987.012] Another critical event.
Oct 10 11:04:05 server2 auth: Successful login for user 'admin' from 10.0.0.5
EOF

# Path to the script being tested
SCRIPT="./src/nightly-syslog-parser.sh"

# --- Test Functions ---

run_test() {
  local test_name="$1"
  local expected_output="$2"
  local actual_output="$3"
  local exit_code="$4"
  local actual_exit_code="$5"

  if [ "$actual_exit_code" -ne "$exit_code" ]; then
    echo "FAIL: $test_name (Exit Code Mismatch)"
    echo "  Expected Exit Code: $exit_code"
    echo "  Actual Exit Code:   $actual_exit_code"
    return 1
  fi

  if [ "$actual_output" == "$expected_output" ]; then
    echo "PASS: $test_name"
    return 0
  else
    echo "FAIL: $test_name"
    echo "  Expected: '$expected_output'"
    echo "  Actual:   '$actual_output'"
    return 1
  fi
}

# --- Test Cases ---

# Test 1: Basic keyword search in one file
test_keyword_single_file() {
  local expected="Oct 10 10:01:02 server1 auth: Failed login for user 'admin' from 192.168.1.100"
  local actual=$($SCRIPT -f "$TEST_LOG_FILE_1" -k "Failed login" 2>/dev/null)
  local exit_code=$?
  run_test "Keyword Search Single File" "$expected" "$actual" 0 "$exit_code"
}

# Test 2: IP address search in multiple files
test_ip_multiple_files() {
  local expected="Oct 10 10:01:02 server1 auth: Failed login for user 'admin' from 192.168.1.100
Oct 10 11:01:02 server2 auth: Failed login for user 'root' from 192.168.1.100"
  local actual=$($SCRIPT -f "$TEST_LOG_FILE_1" -f "$TEST_LOG_FILE_2" -i "192.168.1.100" 2>/dev/null)
  local exit_code=$?
  run_test "IP Address Search Multiple Files" "$expected" "$actual" 0 "$exit_code"
}

# Test 3: Regex pattern search
test_regex_pattern() {
  local expected="Oct 10 10:05:06 server1 daemon: Warning: Disk space low.
Oct 10 10:06:07 server1 kernel: [ 111.222] Critical error encountered.
Oct 10 11:03:04 server2 kernel: [ 987.012] Another critical event."
  local actual=$($SCRIPT -f "$TEST_LOG_FILE_1" -f "$TEST_LOG_FILE_2" -p "(warning|critical)" 2>/dev/null)
  local exit_code=$?
  run_test "Regex Pattern Search" "$expected" "$actual" 0 "$exit_code"
}

# Test 4: Counting matching lines
test_count_only() {
  local expected="3"
  local actual=$($SCRIPT -f "$TEST_LOG_FILE_1" -f "$TEST_LOG_FILE_2" -k "login" -c 2>/dev/null)
  local exit_code=$?
  run_test "Count Only" "$expected" "$actual" 0 "$exit_code"
}

# Test 5: No log files provided (error case)
test_no_log_files() {
  local expected="Error: No log files specified. Use -f <file>."
  local actual=$($SCRIPT -k "error" 2>&1)
  local exit_code=$?
  run_test "No Log Files Provided" "$expected" "$actual" 1 "$exit_code"
}

# Test 6: No search criteria provided (error case)
test_no_search_criteria() {
  local expected="Error: No search criteria provided. Use -k, -i, or -p."
  local actual=$($SCRIPT -f "$TEST_LOG_FILE_1" 2>&1)
  local exit_code=$?
  run_test "No Search Criteria Provided" "$expected" "$actual" 1 "$exit_code"
}

# Test 7: Non-existent log file
test_nonexistent_log_file() {
  local expected="Warning: Log file not found: /non/existent/log.log"
  local actual=$($SCRIPT -f "$TEST_LOG_FILE_1" -f "/non/existent/log.log" -k "info" 2>&1)
  local exit_code=$?
  # The actual output will contain the warning and the matching line from the existing file.
  # We need to check for the warning specifically.
  if [[ "$actual" == *"$expected"* ]]; then
    echo "PASS: Non-existent Log File (Warning Found)"
    return 0
  else
    echo "FAIL: Non-existent Log File (Warning Not Found)"
    echo "  Expected Warning: '$expected'"
    echo "  Actual Output: '$actual'"
    return 1
  fi
}

# Test 8: Multiple keywords and IP addresses
test_multiple_keywords_ips() {
  local expected="Oct 10 10:01:02 server1 auth: Failed login for user 'admin' from 192.168.1.100
Oct 10 11:01:02 server2 auth: Failed login for user 'root' from 192.168.1.100"
  local actual=$($SCRIPT -f "$TEST_LOG_FILE_1" -f "$TEST_LOG_FILE_2" -k "Failed login" -i "192.168.1.100" 2>/dev/null)
  local exit_code=$?
  run_test "Multiple Keywords and IPs" "$expected" "$actual" 0 "$exit_code"
}

# Test 9: Case-insensitive keyword search
test_case_insensitive_keyword() {
  local expected="Oct 10 10:05:06 server1 daemon: Warning: Disk space low."
  local actual=$($SCRIPT -f "$TEST_LOG_FILE_1" -k "warning" 2>/dev/null)
  local exit_code=$?
  run_test "Case-Insensitive Keyword Search" "$expected" "$actual" 0 "$exit_code"
}

# --- Test Execution ---

TOTAL_TESTS=0
PASSED_TESTS=0

run_all_tests() {
  local -n tests_to_run="$1"
  for test_func in "${tests_to_run[@]}"; do
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if "$test_func"; then
      PASSED_TESTS=$((PASSED_TESTS + 1))
    fi
  done
}

# Array of test functions to run
TEST_FUNCTIONS=(
  test_keyword_single_file
  test_ip_multiple_files
  test_regex_pattern
  test_count_only
  test_no_log_files
  test_no_search_criteria
  test_nonexistent_log_file
  test_multiple_keywords_ips
  test_case_insensitive_keyword
)

run_all_tests TEST_FUNCTIONS

# --- Cleanup ---
rm -rf "$TEST_DIR"

# --- Summary ---

echo "---------------------"
echo "Test Summary:"
echo "---------------------"
echo "Total Tests: $TOTAL_TESTS"
echo "Passed Tests: $PASSED_TESTS"
echo "Failed Tests: $((TOTAL_TESTS - PASSED_TESTS))"

if [ "$TOTAL_TESTS" -eq "$PASSED_TESTS" ]; then
  exit 0 # Success
else
  exit 1 # Failure
fi
