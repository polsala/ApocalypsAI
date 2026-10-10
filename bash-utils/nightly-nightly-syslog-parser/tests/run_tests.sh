#!/bin/bash

# Mock log file content

# Test case 1: Basic keyword search
TEST_LOG_1="Oct 27 10:00:00 hostname kernel: [    0.000000] Linux version 5.15.0-87-generic (buildd@lcy02-amd64-038) (gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #97-Ubuntu SMP Mon Oct 2 21:09:21 UTC 2023"
TEST_LOG_2="Oct 27 10:01:05 hostname CRON[1234]: (root) CMD (command -v debian-sa1 > /dev/null && debian-sa1 1 1)"
TEST_LOG_3="Oct 27 10:02:10 hostname systemd[1]: Started Session 1 of user root."
TEST_LOG_4="Oct 27 10:03:15 hostname kernel: [    0.123456] ACPI: Added _OSI(Linux)"
TEST_LOG_5="Oct 27 10:04:20 hostname CRON[5678]: (www-data) CMD (php /var/www/html/cron.php)"
TEST_LOG_6="Oct 27 10:05:25 hostname systemd[1]: Stopping Session 1 of user root."
TEST_LOG_7="Oct 27 10:06:30 hostname kernel: [    0.789012] EXT4-fs (sda1): mounted filesystem with ordered data mode. Opts: (null)"
TEST_LOG_8="Oct 27 10:07:35 hostname CRON[9012]: (root) CMD (apt update)"
TEST_LOG_9="Oct 27 10:08:40 hostname systemd[1]: Started User Manager for UID 1000."
TEST_LOG_10="Oct 27 10:09:45 hostname kernel: [    1.234567] random: crng init done"

# Test case 2: Pattern search
TEST_LOG_PATTERN_1="Oct 27 11:00:00 hostname sshd[1111]: Accepted password for user from 192.168.1.100 port 54321 ssh2"
TEST_LOG_PATTERN_2="Oct 27 11:01:00 hostname systemd[1]: Starting NetworkManager..."
TEST_LOG_PATTERN_3="Oct 27 11:02:00 hostname CRON[2222]: (root) CMD (echo 'hello')"
TEST_LOG_PATTERN_4="Oct 27 11:03:00 hostname sshd[3333]: Failed password for invalid user from 10.0.0.5 port 12345 ssh2"

# Test case 3: Time filtering
TEST_LOG_TIME_1="Oct 27 09:00:00 hostname systemd[1]: Started Session 0 of user root."
TEST_LOG_TIME_2="Oct 27 09:30:00 hostname kernel: [    0.000000] Booting system."
TEST_LOG_TIME_3="Oct 27 10:00:00 hostname CRON[1234]: (root) CMD (echo 'midday')"
TEST_LOG_TIME_4="Oct 27 10:30:00 hostname systemd[1]: Stopping Session 0 of user root."
TEST_LOG_TIME_5="Oct 27 11:00:00 hostname kernel: [    0.123456] System is shutting down."

# Mock log file creation
create_mock_log() {
    local filename="$1"
    shift
    echo -e "$@" > "$filename"
}

# Cleanup mock files
cleanup_mock_files() {
    rm -f mock_syslog.log mock_output.log
}

# Test function
test_case() {
    local test_name="$1"
    local expected_output="$2"
    local script_args="$3"
    local mock_log_content="$4"
    local mock_log_file="mock_syslog.log"

    echo "Running test: $test_name"

    create_mock_log "$mock_log_file" $mock_log_content

    # Mock rationale: Executing the script with provided arguments and capturing its output.
    actual_output=$(./src/nightly-syslog-parser.sh $script_args -f "$mock_log_file")

    # Remove trailing newlines for comparison
    actual_output=$(echo -e "$actual_output" | sed '/^$/d')
    expected_output=$(echo -e "$expected_output" | sed '/^$/d')

    if [ "$actual_output" == "$expected_output" ]; then
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

# --- Test Execution ---

cleanup_mock_files

# Test 1: Keyword search for 'kernel'
test_case "Keyword Search (kernel)" "$TEST_LOG_1\n$TEST_LOG_4\n$TEST_LOG_7\n$TEST_LOG_10" "-k kernel" "$TEST_LOG_1\n$TEST_LOG_2\n$TEST_LOG_3\n$TEST_LOG_4\n$TEST_LOG_5\n$TEST_LOG_6\n$TEST_LOG_7\n$TEST_LOG_8\n$TEST_LOG_9\n$TEST_LOG_10"
if [ $? -ne 0 ]; then exit 1; fi

# Test 2: Keyword search for 'CRON'
test_case "Keyword Search (CRON)" "$TEST_LOG_2\n$TEST_LOG_5\n$TEST_LOG_8" "-k CRON" "$TEST_LOG_1\n$TEST_LOG_2\n$TEST_LOG_3\n$TEST_LOG_4\n$TEST_LOG_5\n$TEST_LOG_6\n$TEST_LOG_7\n$TEST_LOG_8\n$TEST_LOG_9\n$TEST_LOG_10"
if [ $? -ne 0 ]; then exit 1; fi

# Test 3: Pattern search for IP addresses starting with 192.168.1.
test_case "Pattern Search (IP Address)" "$TEST_LOG_PATTERN_1" "-p \"^.*192\.168\.1\.\d+\"" "$TEST_LOG_PATTERN_1\n$TEST_LOG_PATTERN_2\n$TEST_LOG_PATTERN_3\n$TEST_LOG_PATTERN_4"
if [ $? -ne 0 ]; then exit 1; fi

# Test 4: Pattern search for 'sshd' and keyword 'Failed'
test_case "Combined Pattern and Keyword Search" "$TEST_LOG_PATTERN_4" "-p sshd -k Failed" "$TEST_LOG_PATTERN_1\n$TEST_LOG_PATTERN_2\n$TEST_LOG_PATTERN_3\n$TEST_LOG_PATTERN_4"
if [ $? -ne 0 ]; then exit 1; fi

# Test 5: Time filtering - start time only
test_case "Time Filtering (Start Time Only)" "$TEST_LOG_TIME_3\n$TEST_LOG_TIME_4\n$TEST_LOG_TIME_5" "-s \"2023-10-27 10:00:00\"" "$TEST_LOG_TIME_1\n$TEST_LOG_TIME_2\n$TEST_LOG_TIME_3\n$TEST_LOG_TIME_4\n$TEST_LOG_TIME_5"
if [ $? -ne 0 ]; then exit 1; fi

# Test 6: Time filtering - end time only
test_case "Time Filtering (End Time Only)" "$TEST_LOG_TIME_1\n$TEST_LOG_TIME_2\n$TEST_LOG_TIME_3" "-e \"2023-10-27 10:00:00\"" "$TEST_LOG_TIME_1\n$TEST_LOG_TIME_2\n$TEST_LOG_TIME_3\n$TEST_LOG_TIME_4\n$TEST_LOG_TIME_5"
if [ $? -ne 0 ]; then exit 1; fi

# Test 7: Time filtering - start and end time
test_case "Time Filtering (Start and End Time)" "$TEST_LOG_TIME_3" "-s \"2023-10-27 10:00:00\" -e \"2023-10-27 10:30:00\"" "$TEST_LOG_TIME_1\n$TEST_LOG_TIME_2\n$TEST_LOG_TIME_3\n$TEST_LOG_TIME_4\n$TEST_LOG_TIME_5"
if [ $? -ne 0 ]; then exit 1; fi

# Test 8: Output to file
OUTPUT_FILENAME="mock_output.log"
EXPECTED_OUTPUT_FILE_CONTENT="$TEST_LOG_1\n$TEST_LOG_4"

# Mock rationale: Executing the script to write to a file and then reading the file content for verification.
./src/nightly-syslog-parser.sh -k kernel -o "$OUTPUT_FILENAME" -f "$mock_log_file"
if [ $? -ne 0 ]; then echo "  FAIL (Output to file)"; exit 1; fi

actual_output_file_content=$(cat "$OUTPUT_FILENAME")

actual_output_file_content=$(echo -e "$actual_output_file_content" | sed '/^$/d')
EXPECTED_OUTPUT_FILE_CONTENT=$(echo -e "$EXPECTED_OUTPUT_FILE_CONTENT" | sed '/^$/d')

if [ "$actual_output_file_content" == "$EXPECTED_OUTPUT_FILE_CONTENT" ]; then
    echo "  PASS (Output to file)"
else
    echo "  FAIL (Output to file)"
    echo "    Expected:"
    echo "$EXPECTED_OUTPUT_FILE_CONTENT"
    echo "    Actual:"
    echo "$actual_output_file_content"
    exit 1
fi

# Test 9: No matches
test_case "No Matches" "" "-k non_existent_keyword" "$TEST_LOG_1\n$TEST_LOG_2"
if [ $? -ne 0 ]; then exit 1; fi

# Test 10: Invalid log file
echo "Running test: Invalid Log File"
# Mock rationale: Expecting an error message when the specified log file does not exist.
actual_output=$(./src/nightly-syslog-parser.sh -f /non/existent/log/file)
if [[ "$actual_output" == *"Error: Log file '/non/existent/log/file' not found."* ]]; then
    echo "  PASS"
else
    echo "  FAIL"
    echo "    Expected: Error message for non-existent file."
    echo "    Actual:"
    echo "$actual_output"
    exit 1
fi

cleanup_mock_files

echo "All tests passed!"
exit 0
