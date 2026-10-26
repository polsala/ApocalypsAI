#!/bin/bash

# Tests for nightly-syslog-filter-sh

# Mock rationale: Using temporary files to simulate log and pattern files.
# This ensures deterministic and offline testing.

# --- Setup ---

# Create mock log file
cat << EOF > mock_sys.log
Oct 26 10:00:00 server kernel: System started successfully.
Oct 26 10:01:05 server sshd[1234]: Accepted password for user root from 192.168.1.100 port 54321 ssh2
Oct 26 10:02:10 server CRON[5678]: (root) CMD (command to run)
Oct 26 10:03:00 server kernel: WARNING: Disk usage is high.
Oct 26 10:04:00 server systemd[1]: Started Session 12 of user. 
Oct 26 10:05:00 server kernel: ERROR: Network interface down.
Oct 26 10:06:00 server auth: User 'admin' logged in.
EOF

# Create mock pattern file
cat << EOF > mock_patterns.txt
ERROR
WARNING
CRON
Accepted password
EOF

# Create an empty pattern file for testing empty pattern scenario
cat << EOF > empty_patterns.txt
EOF

# Create a pattern file with only case variations
cat << EOF > case_patterns.txt
error
warning
accepted password
EOF

# --- Test Cases ---

run_test() {
    local test_name="$1"
    local script_args="$2"
    local expected_output="$3"
    local actual_output=$(./src/main.sh $script_args 2>/dev/null)
    local exit_code=$?

    echo "Running test: $test_name"
    if [ "$exit_code" -eq 0 ] && [ "$actual_output" = "$expected_output" ]; then
        echo "  PASSED"
    else
        echo "  FAILED"
        echo "    Expected Exit Code: 0, Got: $exit_code"
        echo "    Expected Output:"
        echo "$expected_output"
        echo "    Actual Output:"
        echo "$actual_output"
    fi
}

# Test 1: Basic filtering with color enabled
expected_output_1="Oct 26 10:01:05 server sshd[1234]: Accepted password for user root from 192.168.1.100 port 54321 ssh2\nOct 26 10:02:10 server CRON[5678]: (root) CMD (command to run)\nOct 26 10:03:00 server kernel: WARNING: Disk usage is high.\nOct 26 10:05:00 server kernel: ERROR: Network interface down."
run_test "Basic Filtering (Color Enabled)" "mock_sys.log mock_patterns.txt" "$expected_output_1"

# Test 2: Filtering with case variations (should still match)
expected_output_2="Oct 26 10:01:05 server sshd[1234]: Accepted password for user root from 192.168.1.100 port 54321 ssh2\nOct 26 10:03:00 server kernel: WARNING: Disk usage is high.\nOct 26 10:05:00 server kernel: ERROR: Network interface down."
run_test "Case Insensitive Filtering" "mock_sys.log case_patterns.txt"

# Test 3: No matching patterns (should output nothing)
cat << EOF > no_match_patterns.txt
NONEXISTENT_PATTERN
ANOTHER_FAKE_ONE
EOF
run_test "No Matching Patterns" "mock_sys.log no_match_patterns.txt" ""

# Test 4: Empty pattern file (should output original log)
# Note: The script currently handles empty pattern file by printing a warning and then the original log.
# The expected output here reflects that behavior.
expected_output_4="Oct 26 10:00:00 server kernel: System started successfully.\nOct 26 10:01:05 server sshd[1234]: Accepted password for user root from 192.168.1.100 port 54321 ssh2\nOct 26 10:02:10 server CRON[5678]: (root) CMD (command to run)\nOct 26 10:03:00 server kernel: WARNING: Disk usage is high.\nOct 26 10:04:00 server systemd[1]: Started Session 12 of user. \nOct 26 10:05:00 server kernel: ERROR: Network interface down.\nOct 26 10:06:00 server auth: User 'admin' logged in."
run_test "Empty Pattern File" "mock_sys.log empty_patterns.txt" "$expected_output_4"

# Test 5: Invalid log file path
run_test "Invalid Log File" "non_existent_log.log mock_patterns.txt" ""

# Test 6: Invalid pattern file path
run_test "Invalid Pattern File" "mock_sys.log non_existent_patterns.txt" ""

# Test 7: Incorrect number of arguments
run_test "Incorrect Arguments (Too Few)" "mock_sys.log" ""
run_test "Incorrect Arguments (Too Many)" "mock_sys.log mock_patterns.txt extra_arg" ""

# --- Cleanup ---
rm mock_sys.log mock_patterns.txt empty_patterns.txt case_patterns.txt no_match_patterns.txt

exit 0
