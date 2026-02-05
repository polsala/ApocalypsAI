#!/bin/bash

# Mock log file content

MOCK_LOG_CONTENT_1="Oct 26 10:00:01 server kernel: Some kernel message.
Oct 26 10:05:15 server systemd[1]: Started Session 1 of user root.
Oct 26 10:10:30 server sshd[1234]: Accepted password for user admin from 192.168.1.100 port 54321 ssh2
Oct 26 10:15:00 server kernel: Error: Disk read failed on /dev/sda1.
Oct 26 10:20:05 server systemd[1]: Stopping Session 1 of user root.
Oct 26 10:25:00 server kernel: Another kernel message with error.
Oct 27 09:00:00 server CRON[5678]: (root) CMD (command)
Oct 27 09:05:00 server kernel: Warning: Low memory detected."

MOCK_LOG_CONTENT_2="Oct 27 10:00:00 server systemd[1]: Started Session 2 of user test.
Oct 27 10:01:00 server sshd[9876]: Invalid user test from 10.0.0.5
Oct 27 10:02:00 server kernel: segfault at 0 ip 00007f...
Oct 27 10:03:00 server systemd[1]: Stopping Session 2 of user test.
Oct 27 10:04:00 server kernel: Out of memory: Kill process 12345 (my_app) score 1000 or sacrifice child
Oct 27 10:05:00 server CRON[1111]: (user) CMD (another command)"

# --- Test Functions ---

# Mock function to simulate reading a log file
# This function will be called by the script when it tries to read a file.
# It returns predefined content based on the filename.
mock_read_log() {
    local file="$1"
    if [[ "$file" == "/mock/syslog.log" ]]; then
        echo -e "$MOCK_LOG_CONTENT_1"
    elif [[ "$file" == "/mock/messages.log" ]]; then
        echo -e "$MOCK_LOG_CONTENT_2"
    elif [[ "$file" == "/mock/empty.log" ]]; then
        echo ""
    else
        echo "Error: Mock log file '$file' not found." >&2
        return 1
    fi
}

# Mock function to simulate the date command for time filtering
# This allows us to control the output of 'date' for deterministic tests.
mock_date() {
    local format="$1"
    case "$format" in
        "+%Y-%m-%d %H:%M:%S")
            # Mocking specific dates for testing
            if [[ "$2" == "1 hour ago" ]]; then
                echo "2023-10-27 09:05:00"
            else
                echo "2023-10-27 10:05:00"
            fi
            ;;
        *) echo "Mocked date: $format";;
    esac
}

# Function to run a single test case
run_test() {
    local test_name="$1"
    local expected_output="$2"
    local script_args="$3"
    local script_path="../src/main.sh"
    
    echo "Running test: $test_name..."
    
    # Mocking the environment
    # We'll use a subshell to isolate the mocked functions
    ( 
        # Override the actual commands with our mocks
        alias grep='echo "Mocked grep:" && grep'
        alias wc='echo "Mocked wc:" && wc'
        alias date='mock_date'
        
        # Redirect stdout and stderr to capture output
        actual_output=$(bash "$script_path" $script_args 2>&1)
        
        # Check if the actual output matches the expected output
        if [[ "$actual_output" == "$expected_output" ]]; then
            echo "  PASS"
        else
            echo "  FAIL"
            echo "    Expected:"
            echo "$expected_output"
            echo "    Actual:"
            echo "$actual_output"
            return 1
        fi
    )
    return $?
}

# --- Test Cases ---

# Test 1: Basic keyword search
# Mock rationale: Simulates reading /mock/syslog.log and searching for 'error'.
# The script's internal grep will be mocked to show it's being called.
run_test "Basic keyword search" "Mocked grep: Oct 26 10:15:00 server kernel: Error: Disk read failed on /dev/sda1.
Mocked grep: Oct 26 10:25:00 server kernel: Another kernel message with error." "-f /mock/syslog.log -k error"

# Test 2: Multiple keywords search
# Mock rationale: Simulates searching for 'error' OR 'warning' in /mock/syslog.log.
run_test "Multiple keywords search" "Mocked grep: Oct 26 10:15:00 server kernel: Error: Disk read failed on /dev/sda1.
Mocked grep: Oct 26 10:25:00 server kernel: Another kernel message with error.
Mocked grep: Oct 27 09:05:00 server kernel: Warning: Low memory detected." "-f /mock/syslog.log -k error,warning"

# Test 3: Pattern matching
# Mock rationale: Simulates searching for a specific regex pattern in /mock/messages.log.
run_test "Pattern matching" "Mocked grep: Oct 27 10:02:00 server kernel: segfault at 0 ip 00007f..." "-f /mock/messages.log -p 'segfault'"

# Test 4: Count mode
# Mock rationale: Simulates counting 'error' messages in /mock/syslog.log.
run_test "Count mode" "Mocked wc -l
2" "-f /mock/syslog.log -k error -c"

# Test 5: No matching keywords
# Mock rationale: Searches for a keyword that doesn't exist in the mock log.
run_test "No matching keywords" "" "-f /mock/syslog.log -k "nonexistent_keyword""

# Test 6: Empty log file
# Mock rationale: Searches in an empty mock log file.
run_test "Empty log file" "" "-f /mock/empty.log -k "any""

# Test 7: Time filtering (start time only - basic mock)
# Mock rationale: This test is a simplified representation. The actual date filtering in the script is basic.
# We mock 'date' to return a specific value and expect the script to filter based on that.
# The script's internal grep will be mocked to show it's being called.
# Note: The script's time filtering is a simplification and might not work for all syslog formats.
run_test "Time filtering (start time only)" "Mocked grep: Oct 27 09:05:00 server kernel: Warning: Low memory detected." "-f /mock/syslog.log -s '2023-10-27 09:00:00'"

# Test 8: Time filtering (start and end time - basic mock)
# Mock rationale: Similar to Test 7, but with both start and end times.
run_test "Time filtering (start and end time)" "Mocked grep: Oct 27 10:02:00 server kernel: segfault at 0 ip 00007f..." "-f /mock/messages.log -s '2023-10-27 10:00:00' -e '2023-10-27 10:03:00'"

# Test 9: No arguments (should default to /var/log/syslog and show help if it doesn't exist)
# Mock rationale: This test assumes /var/log/syslog does not exist in the test environment.
# The script should output an error message.
run_test "No arguments (default log file not found)" "Error: Log file '/var/log/syslog' not found." ""

# Test 10: Help message
# Mock rationale: Ensure the help message is displayed when -h is used.
run_test "Help message" "Usage: main.sh -f <logfile> -k <keyword1,keyword2,...> -p <pattern> -s <start_time> -e <end_time> -c -h
  -f <logfile>        Path to the syslog file to parse. Defaults to /var/log/syslog.
  -k <keywords>       Comma-separated list of keywords to search for (case-insensitive).
  -p <pattern>        A regular expression pattern to search for. Overrides keyword search.
  -s <start_time>     Start time for filtering (e.g. 'YYYY-MM-DD HH:MM:SS').
  -e <end_time>       End time for filtering (e.g. 'YYYY-MM-DD HH:MM:SS').
  -c                  Count the number of matching log entries.
  -h                  Display this help message." "-h"


# --- Mocking Setup for the actual script execution within tests ---
# We need to ensure that when the script is called, it uses our mock functions.
# This is achieved by aliasing or redefining functions within the subshell of run_test.
# The `alias` command is used here for simplicity, but `declare -f` could also be used.

# To make the script runnable directly for testing, we need to create mock log files.
# This is done by creating temporary files and writing mock content to them.

# Create mock log files for testing

# Mock syslog.log
cat << EOF > /tmp/mock_syslog.log
$MOCK_LOG_CONTENT_1
EOF

# Mock messages.log
cat << EOF > /tmp/mock_messages.log
$MOCK_LOG_CONTENT_2
EOF

# Mock empty.log
touch /tmp/mock_empty.log

# Replace the default log file path in the script arguments with our mock paths
# This is a bit hacky, but necessary for this bash-only testing setup.
# A better approach would be to modify the script to accept a mock file path directly.

# Re-run tests with actual mock file paths

# Test 1: Basic keyword search
run_test "Basic keyword search (real mock files)" "Mocked grep: Oct 26 10:15:00 server kernel: Error: Disk read failed on /dev/sda1.
Mocked grep: Oct 26 10:25:00 server kernel: Another kernel message with error." "-f /tmp/mock_syslog.log -k error"

# Test 2: Multiple keywords search
run_test "Multiple keywords search (real mock files)" "Mocked grep: Oct 26 10:15:00 server kernel: Error: Disk read failed on /dev/sda1.
Mocked grep: Oct 26 10:25:00 server kernel: Another kernel message with error.
Mocked grep: Oct 27 09:05:00 server kernel: Warning: Low memory detected." "-f /tmp/mock_syslog.log -k error,warning"

# Test 3: Pattern matching
run_test "Pattern matching (real mock files)" "Mocked grep: Oct 27 10:02:00 server kernel: segfault at 0 ip 00007f..." "-f /tmp/mock_messages.log -p 'segfault'"

# Test 4: Count mode
run_test "Count mode (real mock files)" "Mocked wc -l
2" "-f /tmp/mock_syslog.log -k error -c"

# Test 7: Time filtering (start time only - basic mock)
# Mock rationale: This test is a simplified representation. The actual date filtering in the script is basic.
# We mock 'date' to return a specific value and expect the script to filter based on that.
# The script's internal grep will be mocked to show it's being called.
# Note: The script's time filtering is a simplification and might not work for all syslog formats.
run_test "Time filtering (start time only - real mock files)" "Mocked grep: Oct 27 09:05:00 server kernel: Warning: Low memory detected." "-f /tmp/mock_syslog.log -s '2023-10-27 09:00:00'"

# Test 8: Time filtering (start and end time - basic mock)
run_test "Time filtering (start and end time - real mock files)" "Mocked grep: Oct 27 10:02:00 server kernel: segfault at 0 ip 00007f..." "-f /tmp/mock_messages.log -s '2023-10-27 10:00:00' -e '2023-10-27 10:03:00'"

# Test 6: Empty log file
run_test "Empty log file (real mock files)" "" "-f /tmp/mock_empty.log -k "any""

# Clean up mock log files
rm -f /tmp/mock_syslog.log /tmp/mock_messages.log /tmp/mock_empty.log

exit 0
