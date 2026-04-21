#!/bin/bash

# Mocking functions and external commands for testing

# Mock rationale: We need to mock the reading of the syslog file and external commands like 'date', 'grep', 'awk', 'sed', 'echo', 'read' to ensure deterministic and offline tests.

# Mocking the syslog file content
# This variable will hold the content that the script will 'read' from.
# We'll use a heredoc to simulate reading from a file.
SYSLOG_MOCK_CONTENT=""

# Mocking the 'read' command to read from SYSLOG_MOCK_CONTENT
_mock_read() {
    local -n _read_var="$1"
    local line_num="$2"
    if [[ -z "$line_num" ]]; then
        # If no line number is specified, read the next line from the mock content
        if [[ -n "$SYSLOG_MOCK_CONTENT" ]]; then
            _read_var=$(echo "$SYSLOG_MOCK_CONTENT" | head -n 1)
            SYSLOG_MOCK_CONTENT=$(echo "$SYSLOG_MOCK_CONTENT" | tail -n +2)
            return 0 # Success
        else
            return 1 # EOF
        fi
    else
        # If a line number is specified, read that specific line
        _read_var=$(echo "$SYSLOG_MOCK_CONTENT" | sed -n "${line_num}p")
        return 0 # Success
    fi
}

# Mocking the 'date' command
_mock_date() {
    local format="$1"
    local input_str="$2"

    # Simulate date conversion for specific test cases
    case "$input_str" in
        "2023-10-27 10:00:00") echo "1698397200" ;; # Example Unix timestamp
        "2023-10-27 10:05:00") echo "1698397500" ;; 
        "2023-10-27 10:10:00") echo "1698397800" ;; 
        "2023-10-27 11:00:00") echo "1698400800" ;; 
        "2023-10-27 11:05:00") echo "1698401100" ;; 
        "2023-10-27 11:10:00") echo "1698401400" ;; 
        "2023-10-27 12:00:00") echo "1698404400" ;; 
        "2023-10-27 13:00:00") echo "1698408000" ;; 
        "2023-10-27 14:00:00") echo "1698411600" ;; 
        "2023-10-27 15:00:00") echo "1698415200" ;; 
        *) 
            # Fallback for actual date conversion if needed, but ideally all test cases are covered
            # For offline tests, this should ideally not be reached or should be a controlled fallback
            echo "$(date -d "$input_str" +%s 2>/dev/null)"
            ;;
    esac
}

# Mocking 'grep' to return specific results based on patterns
_mock_grep() {
    local pattern="$1"
    local input_line="$2"

    # Simple mock: if pattern is in line, return 0 (match), else 1 (no match)
    if echo "$input_line" | grep -qE "$pattern"; then
        return 0
    else
        return 1
    fi
}

# Mocking 'awk' for specific field extraction
_mock_awk() {
    local script="$1"
    local input_line="$2"

    # Mock specific awk commands used in the script
    case "$script" in
        '{print $3}' | '{print $3}' | sed 's/[()]//g') # Severity extraction
            echo "$(echo "$input_line" | awk '{print $3}' | sed 's/[()]//g')"
            ;;
        '{print $1, $2, $3}') # Timestamp part extraction
            echo "$(echo "$input_line" | awk '{print $1, $2, $3}')"
            ;;
        '{print $4}') # Hostname extraction
            echo "$(echo "$input_line" | awk '{print $4}')"
            ;;
        '{print $5}' | sed 's/://') # Process extraction
            echo "$(echo "$input_line" | awk '{print $5}' | sed 's/://')"
            ;;
        *) # Default awk behavior for other cases
            echo "$input_line" | awk "$script"
            ;;
    esac
}

# Mocking 'sed' for specific substitutions
_mock_sed() {
    local script="$1"
    local input_line="$2"

    case "$script" in
        "s/[()]//g") # Remove parentheses
            echo "$input_line" | sed "s/[()]//g"
            ;;
        "s/^ *//") # Trim leading spaces
            echo "$input_line" | sed "s/^ *//"
            ;;
        "s/\"/\\\"/g" | "s/\n/\\n/g" | "s/\r/\\r/g" | "s/\t/\\t/g") # JSON escaping
            echo "$input_line" | sed -e "s/\"/\\\"/g" -e "s/\n/\\n/g" -e "s/\r/\\r/g" -e "s/\t/\\t/g"
            ;;
        *) # Default sed behavior
            echo "$input_line" | sed "$script"
            ;;
    esac
}

# Mocking 'echo' to capture output
_mock_echo() {
    local output="$@"
    # In a real test runner, we'd capture this. For bashunit, we can just let it print.
    # Or, we can store it in a global variable for assertion.
    ECHO_OUTPUT+="$output\n"
}

# Mocking 'cut' for specific field extraction
_mock_cut() {
    local delimiter="$1"
    local fields="$2"
    local input_line="$3"

    # Mocking the specific cut command used for message extraction
    if [[ "$delimiter" == ":" && "$fields" == "f 2-" ]]; then
        echo "$input_line" | cut -d ':' -f 2- | sed 's/^ *//'
    else
        echo "$input_line" | cut "$delimiter" "$fields"
    fi
}

# Mocking 'basename' for help message
_mock_basename() {
    echo "nightly-syslog-filter-cli.sh"
}

# Mocking 'command -v' to report commands as found
_mock_command_v() {
    local cmd="$1"
    case "$cmd" in
        "grep") return 0 ;; 
        "awk") return 0 ;; 
        "sed") return 0 ;; 
        "date") return 0 ;; 
        "read") return 0 ;; 
        "echo") return 0 ;; 
        "cut") return 0 ;; 
        "basename") return 0 ;; 
        "tail") return 0 ;; 
        "head") return 0 ;; 
        "dirname") return 0 ;; 
        "cd") return 0 ;; 
        "source") return 0 ;; 
        "exit") return 0 ;; 
        *) return 1 ;; # Assume not found for others
    esac
}

# Mocking 'exit' to prevent script termination during tests
_mock_exit() {
    echo "Mock exit called with status $1"
    return $1
}

# --- Test Cases ---

# Test case 1: Basic filtering by severity
test_filter_by_severity() {
    SYSLOG_MOCK_CONTENT="
Oct 27 10:00:00 server1 kernel: [    0.000000] Linux version 5.15.0-87-generic (buildd@lcy02-amd64-026) (gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #97-Ubuntu SMP Mon Oct 2 21:09:21 UTC 2023
Oct 27 10:05:00 server1 rsyslogd: imuxsock: Activated with system event queue.
Oct 27 10:10:00 server1 CRON[1234]: (root) CMD (command -v apt-get >/dev/null && apt-get update)
Oct 27 11:00:00 server1 sshd[5678]: Accepted password for user from 192.168.1.10 port 54321 ssh2
Oct 27 11:05:00 server1 kernel: [  123.456789] ACPI: Added _OSI(Linux)
Oct 27 11:10:00 server1 systemd[1]: Started Session 12 of user root.
Oct 27 12:00:00 server1 ERROR: Something went wrong.
Oct 27 13:00:00 server1 WARNING: Potential issue detected.
Oct 27 14:00:00 server1 INFO: Service started successfully.
Oct 27 15:00:00 server1 DEBUG: Variable x = 10
"

    # Mocking the actual file read to use our mock content
    # We need to replace the `while IFS= read -r line; do ... done < "$SYSLOG_FILE"` loop
    # This is tricky in bash. A simpler approach is to mock 'read' directly.
    # Let's redefine the loop to use our mock read.
    
    # Temporarily override the read command for this test
    ORIG_READ="read"
    read() { _mock_read "@"; }

    # Capture the output of the script
    OUTPUT=$(
        ./nightly-syslog-filter-cli.sh -s err
    )

    # Restore the original read command
    read="$ORIG_READ"

    # Assertions
    assert_equal "Oct 27 12:00:00 server1 ERROR: Something went wrong." "$OUTPUT"
}

# Test case 2: Filtering by pattern
test_filter_by_pattern() {
    SYSLOG_MOCK_CONTENT="
Oct 27 10:00:00 server1 kernel: [    0.000000] Linux version 5.15.0-87-generic
Oct 27 10:05:00 server1 rsyslogd: imuxsock: Activated.
Oct 27 10:10:00 server1 CRON[1234]: (root) CMD (command -v apt-get >/dev/null && apt-get update)
Oct 27 11:00:00 server1 sshd[5678]: Accepted password for user from 192.168.1.10 port 54321 ssh2
Oct 27 11:05:00 server1 kernel: [  123.456789] ACPI: Added _OSI(Linux)
Oct 27 11:10:00 server1 systemd[1]: Started Session 12 of user root.
Oct 27 12:00:00 server1 ERROR: Something went wrong.
Oct 27 13:00:00 server1 WARNING: Potential issue detected.
Oct 27 14:00:00 server1 INFO: Service started successfully.
Oct 27 15:00:00 server1 DEBUG: Variable x = 10
"

    ORIG_READ="read"
    read() { _mock_read "@"; }

    OUTPUT=$(
        ./nightly-syslog-filter-cli.sh -p 'Accepted password'
    )

    read="$ORIG_READ"

    assert_equal "Oct 27 11:00:00 server1 sshd[5678]: Accepted password for user from 192.168.1.10 port 54321 ssh2" "$OUTPUT"
}

# Test case 3: Filtering by time range
test_filter_by_time_range() {
    SYSLOG_MOCK_CONTENT="
Oct 27 10:00:00 server1 INFO: Start of test period.
Oct 27 10:05:00 server1 DEBUG: Processing item A.
Oct 27 10:10:00 server1 WARNING: Item B might be slow.
Oct 27 11:00:00 server1 INFO: Mid-period event.
Oct 27 11:05:00 server1 ERROR: Failed to process item C.
Oct 27 11:10:00 server1 INFO: End of test period.
Oct 27 12:00:00 server1 INFO: Outside of range.
"

    ORIG_READ="read"
    read() { _mock_read "@"; }

    OUTPUT=$(
        ./nightly-syslog-filter-cli.sh -t "2023-10-27 10:00:00" "2023-10-27 11:10:00"
    )

    read="$ORIG_READ"

    EXPECTED_OUTPUT="Oct 27 10:00:00 server1 INFO: Start of test period.
Oct 27 10:05:00 server1 DEBUG: Processing item A.
Oct 27 10:10:00 server1 WARNING: Item B might be slow.
Oct 27 11:00:00 server1 INFO: Mid-period event.
Oct 27 11:05:00 server1 ERROR: Failed to process item C.
Oct 27 11:10:00 server1 INFO: End of test period."

    assert_equal "$EXPECTED_OUTPUT" "$OUTPUT"
}

# Test case 4: Filtering by multiple severities (OR logic)
test_filter_by_multiple_severities() {
    SYSLOG_MOCK_CONTENT="
Oct 27 10:00:00 server1 INFO: Normal operation.
Oct 27 10:05:00 server1 WARNING: A warning occurred.
Oct 27 10:10:00 server1 ERROR: An error occurred.
Oct 27 11:00:00 server1 NOTICE: A notice was issued.
Oct 27 11:05:00 server1 DEBUG: Debugging info.
"

    ORIG_READ="read"
    read() { _mock_read "@"; }

    OUTPUT=$(
        ./nightly-syslog-filter-cli.sh -s warning -s error
    )

    read="$ORIG_READ"

    EXPECTED_OUTPUT="Oct 27 10:05:00 server1 WARNING: A warning occurred.
Oct 27 10:10:00 server1 ERROR: An error occurred."

    assert_equal "$EXPECTED_OUTPUT" "$OUTPUT"
}

# Test case 5: Filtering by pattern and severity
test_filter_by_pattern_and_severity() {
    SYSLOG_MOCK_CONTENT="
Oct 27 10:00:00 server1 INFO: Normal operation.
Oct 27 10:05:00 server1 WARNING: Potential issue with service X.
Oct 27 10:10:00 server1 ERROR: Service X failed to start.
Oct 27 11:00:00 server1 NOTICE: Service Y is running.
Oct 27 11:05:00 server1 ERROR: Another error, unrelated.
"

    ORIG_READ="read"
    read() { _mock_read "@"; }

    OUTPUT=$(
        ./nightly-syslog-filter-cli.sh -p 'Service X' -s error
    )

    read="$ORIG_READ"

    assert_equal "Oct 27 10:10:00 server1 ERROR: Service X failed to start." "$OUTPUT"
}

# Test case 6: Output format as JSON
test_output_as_json() {
    SYSLOG_MOCK_CONTENT="
Oct 27 10:00:00 server1 INFO: This is a test message.
Oct 27 10:05:00 server1 ERROR: Another message with "quotes" and \backslashes\.
"

    ORIG_READ="read"
    read() { _mock_read "@"; }

    OUTPUT=$(
        ./nightly-syslog-filter-cli.sh -o json
    )

    read="$ORIG_READ"

    EXPECTED_OUTPUT="{\"timestamp\": \"Oct 27 10:00:00\", \"hostname\": \"server1\", \"process\": \"INFO\", \"severity\": \"info\", \"message\": \"This is a test message.\"}
{\"timestamp\": \"Oct 27 10:05:00\", \"hostname\": \"server1\", \"process\": \"ERROR\", \"severity\": \"error\", \"message\": \"Another message with \"quotes\" and \\backslashes\\.\"}"

    assert_equal "$EXPECTED_OUTPUT" "$OUTPUT"
}

# Test case 7: JSON output with specific filtering
test_json_output_with_filter() {
    SYSLOG_MOCK_CONTENT="
Oct 27 10:00:00 server1 INFO: Normal operation.
Oct 27 10:05:00 server1 WARNING: Potential issue with service X.
Oct 27 10:10:00 server1 ERROR: Service X failed to start.
Oct 27 11:00:00 server1 NOTICE: Service Y is running.
Oct 27 11:05:00 server1 ERROR: Another error, unrelated.
"

    ORIG_READ="read"
    read() { _mock_read "@"; }

    OUTPUT=$(
        ./nightly-syslog-filter-cli.sh -p 'Service X' -s error -o json
    )

    read="$ORIG_READ"

    EXPECTED_OUTPUT="{\"timestamp\": \"Oct 27 10:10:00\", \"hostname\": \"server1\", \"process\": \"ERROR\", \"severity\": \"error\", \"message\": \"Service X failed to start.\"}"

    assert_equal "$EXPECTED_OUTPUT" "$OUTPUT"
}

# Test case 8: No matching logs
test_no_matching_logs() {
    SYSLOG_MOCK_CONTENT="
Oct 27 10:00:00 server1 INFO: All good here.
Oct 27 10:05:00 server1 DEBUG: Nothing to see.
"

    ORIG_READ="read"
    read() { _mock_read "@"; }

    OUTPUT=$(
        ./nightly-syslog-filter-cli.sh -s err
    )

    read="$ORIG_READ"

    assert_equal "" "$OUTPUT"
}

# Test case 9: Invalid time range (missing end time)
test_invalid_time_range_missing_end() {
    SYSLOG_MOCK_CONTENT="Oct 27 10:00:00 server1 INFO: Test"

    ORIG_READ="read"
    read() { _mock_read "@"; }

    # Expecting an error message and exit code 1
    OUTPUT=$(
        ./nightly-syslog-filter-cli.sh -t "2023-10-27 10:00:00"
    )
    EXIT_CODE=$?

    read="$ORIG_READ"

    assert_equal 1 "$EXIT_CODE"
    assert_match "Error: Both start and end times must be provided for --time-range." "$OUTPUT"
}

# Test case 10: Invalid output format
test_invalid_output_format() {
    SYSLOG_MOCK_CONTENT="Oct 27 10:00:00 server1 INFO: Test"

    ORIG_READ="read"
    read() { _mock_read "@"; }

    OUTPUT=$(
        ./nightly-syslog-filter-cli.sh -o xml
    )
    EXIT_CODE=$?

    read="$ORIG_READ"

    assert_equal 1 "$EXIT_CODE"
    assert_match "Error: Invalid output format 'xml'. Supported formats are 'raw' and 'json'." "$OUTPUT"
}

# Test case 11: Syslog file not found
test_syslog_file_not_found() {
    # Temporarily remove the syslog file to simulate it not existing
    mv /var/log/syslog /tmp/syslog_backup_for_test_$$ || true
    
    OUTPUT=$(
        ./nightly-syslog-filter-cli.sh
    )
    EXIT_CODE=$?

    # Restore the syslog file
    mv /tmp/syslog_backup_for_test_$$ /var/log/syslog || true

    assert_equal 1 "$EXIT_CODE"
    assert_match "Error: Syslog file not found at '/var/log/syslog'." "$OUTPUT"
}

# --- Setup and Teardown for Mocks ---

# Override actual commands with mocks before each test
before_each() {
    ECHO_OUTPUT=""
    ORIG_READ="read"
    ORIG_DATE="date"
    ORIG_GREP="grep"
    ORIG_AWK="awk"
    ORIG_SED="sed"
    ORIG_CUT="cut"
    ORIG_BASENAME="basename"
    ORIG_COMMAND_V="command -v"
    ORIG_EXIT="exit"

    read() { _mock_read "@"; }
    date() { _mock_date "@"; }
    grep() { _mock_grep "@"; }
    awk() { _mock_awk "@"; }
    sed() { _mock_sed "@"; }
    cut() { _mock_cut "@"; }
    basename() { _mock_basename "@"; }
    command() { _mock_command_v "@"; }
    exit() { _mock_exit "@"; }
}

# Restore original commands after each test
after_each() {
    read="$ORIG_READ"
    date="$ORIG_DATE"
    grep="$ORIG_GREP"
    awk="$ORIG_AWK"
    sed="$ORIG_SED"
    cut="$ORIG_CUT"
    basename="$ORIG_BASENAME"
    command="$ORIG_COMMAND_V"
    exit="$ORIG_EXIT"
}
