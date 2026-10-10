#!/bin/bash

# Mock rationale: We are mocking the behavior of grep and the log files themselves to ensure deterministic testing without relying on actual system logs or external commands.

# --- Mock Setup ---

# Mock log file content
LOG_CONTENT_SYSLOG="
Aug 10 10:00:01 hostname process1: This is an informational message.
Aug 10 10:01:05 hostname process2: An error occurred here.
Aug 10 10:02:15 hostname process3: Another informational message.
Aug 10 10:03:30 hostname process1: A warning about something.
Aug 10 10:04:00 hostname process4: Critical error detected!
"

LOG_CONTENT_AUTH_LOG="
Aug 10 10:05:00 auth_host sshd[123]: Successful login for user.
Aug 10 10:06:00 auth_host sudo[456]: User executed command.
Aug 10 10:07:00 auth_host sshd[789]: Failed password for invalid user.
"

# Mock grep function
mock_grep() {
    local pattern="$1"
    local file_content="$2"
    local temp_file="/tmp/mock_log_file_$$"
    echo "$file_content" > "$temp_file"
    # Simulate grep behavior: print lines matching the pattern
    grep -E "$pattern" "$temp_file"
    rm "$temp_file"
}

# Mock the script's behavior by replacing the actual grep call
# We'll pass the mock_grep function's output to the script's parsing logic
run_script_with_mocks() {
    local keywords_str="$1"
    local log_files_str="$2"
    local format="$3"

    # Convert keywords string to an array for the script
    IFS=' ' read -r -a keywords <<< "$keywords_str"

    # Construct command-line arguments for the script
    local script_args=""
    for kw in "${keywords[@]}"; do
        script_args+=" -k \"$kw\""
    done
    for lf in $log_files_str; do
        script_args+=" -l \"$lf\""
    done
    if [ -n "$format" ]; then
        script_args+=" -f \"$format\""
    fi

    # Execute the script with mocked grep and log files
    # We need to simulate the script's internal grep call and pipe its output to the script's parsing logic.
    # This is a bit tricky as we can't directly mock 'grep' inside the script easily.
    # Instead, we'll simulate the script's execution flow by directly calling its parsing function
    # with pre-filtered content.

    # For simplicity and to avoid complex mocking of internal script calls, we'll simulate the output
    # of the script's grep command and then pipe it to the script's parsing logic.
    # This requires modifying the script to accept mocked input or running it in a controlled environment.

    # A more robust approach is to test the script by providing mock files and then running it.
    # Let's create temporary mock files.
    local temp_dir="/tmp/syslog_parser_test_$$"
    mkdir -p "$temp_dir/var/log"
    echo "$LOG_CONTENT_SYSLOG" > "$temp_dir/var/log/syslog"
    echo "$LOG_CONTENT_AUTH_LOG" > "$temp_dir/var/log/auth.log"

    # Temporarily change directory to the script's location to run it
    local script_path="$(pwd)/src/nightly-syslog-parser.sh"
    local original_dir=$(pwd)
    cd "$temp_dir"

    # Construct the command to run the script with mocked paths
    # We need to override the default log files if they are specified
    local cmd="$script_path"
    for kw in "${keywords[@]}"; do
        cmd+=" -k \"$kw\""
    done
    if [ -n "$log_files_str" ]; then
        for lf in $log_files_str; do
            # Adjust path for mock files
            mock_lf="$temp_dir/var/log/$(basename $lf)"
            cmd+=" -l \"$mock_lf\""
        done
    else
        # Use mock default files if no specific files are given
        cmd+=" -l \"$temp_dir/var/log/syslog\""
        cmd+=" -l \"$temp_dir/var/log/auth.log\""
    fi
    if [ -n "$format" ]; then
        cmd+=" -f \"$format\""
    fi

    # Execute the command and capture output
    local output=$(eval $cmd)

    # Clean up temporary files
    cd "$original_dir"
    rm -rf "$temp_dir"

    echo "$output"
}

# --- Test Cases ---

run_test() {
    local test_name="$1"
    local expected="$2"
    local actual="$3"

    echo "Running test: $test_name"
    if [ "$actual" == "$expected" ]; then
        echo "  PASS"
    else
        echo "  FAIL"
        echo "    Expected:"
        echo "$expected"
        echo "    Actual:"
        echo "$actual"
        return 1
    fi
    return 0
}

# Test 1: Basic keyword search (default format)
keywords1="error warning"
logs1="/var/log/syslog /var/log/auth.log"
expected1="Aug 10 10:01:05 hostname process2: An error occurred here.
Aug 10 10:03:30 hostname process1: A warning about something.
Aug 10 10:04:00 hostname process4: Critical error detected!"
actual1=$(run_script_with_mocks "$keywords1" "$logs1")
run_test "Basic keyword search (default format)" "$expected1" "$actual1"

# Test 2: JSON output format
keywords2="login failed"
logs2="/var/log/auth.log"
expected2="{\"timestamp\": \"Aug 10 10:05:00\", \"hostname\": \"auth_host\", \"process\": \"sshd[123]\", \"message\": \"Successful login for user.\"}
{\"timestamp\": \"Aug 10 10:07:00\", \"hostname\": \"auth_host\", \"process\": \"sshd[789]\", \"message\": \"Failed password for invalid user.\"}"
actual2=$(run_script_with_mocks "$keywords2" "$logs2" "json")
run_test "JSON output format" "$expected2" "$actual2"

# Test 3: Brief output format
keywords3="error"
logs3="/var/log/syslog"
expected3="[Aug 10 10:01:05] An error occurred here.
[Aug 10 10:04:00] Critical error detected!"
actual3=$(run_script_with_mocks "$keywords3" "$logs3" "brief")
run_test "Brief output format" "$expected3" "$actual3"

# Test 4: Multiple keywords and multiple log files
keywords4="user sudo"
logs4="/var/log/syslog /var/log/auth.log"
expected4="Aug 10 10:05:00 auth_host sshd[123]: Successful login for user.
Aug 10 10:07:00 auth_host sshd[789]: Failed password for invalid user.
Aug 10 10:06:00 auth_host sudo[456]: User executed command."
actual4=$(run_script_with_mocks "$keywords4" "$logs4")
run_test "Multiple keywords and multiple log files" "$expected4" "$actual4"

# Test 5: Keyword not found
keywords5="nonexistent"
logs5="/var/log/syslog"
expected5=""
actual5=$(run_script_with_mocks "$keywords5" "$logs5")
run_test "Keyword not found" "$expected5" "$actual5"

# Test 6: Non-existent log file (should warn and continue)
keywords6="error"
logs6="/var/log/syslog /var/log/nonexistent.log"
expected6="Aug 10 10:01:05 hostname process2: An error occurred here.
Aug 10 10:03:30 hostname process1: A warning about something.
Aug 10 10:04:00 hostname process4: Critical error detected!"
actual6=$(run_script_with_mocks "$keywords6" "$logs6")
# The warning message goes to stderr, so we only check stdout for the parsed logs.
# This test assumes the warning is printed to stderr and the actual logs to stdout.
# The current run_script_with_mocks captures all output, so we'll check the stdout part.
# A more precise test would capture stderr separately.
# For now, we assume the script correctly handles non-existent files and proceeds.
# The expected output here is only the parsed lines from the existing file.
run_test "Non-existent log file handling" "$expected6" "$actual6"

# Test 7: Default log files if none specified
keywords7="error"
# We don't specify logs, so it should use defaults.
# The run_script_with_mocks will simulate the default paths.
expected7="Aug 10 10:01:05 hostname process2: An error occurred here.
Aug 10 10:03:30 hostname process1: A warning about something.
Aug 10 10:04:00 hostname process4: Critical error detected!"
actual7=$(run_script_with_mocks "$keywords7" "")
run_test "Default log files" "$expected7" "$actual7"

exit 0
