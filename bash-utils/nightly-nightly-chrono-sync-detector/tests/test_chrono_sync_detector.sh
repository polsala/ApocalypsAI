#!/bin/bash

# Test suite for Nightly Chrono-Sync Anomaly Detector

SCRIPT_PATH="../src/chrono_sync_detector.sh"

# Helper function to run a test
run_test() {
    local test_name="$1"
    local mock_output="$2"
    local expected_exit_code="$3"
    local expected_output_regex="$4"

    echo "--- Running test: $test_name ---"

    # Mock rationale: We are mocking the `timedatectl` command to control its output
    # and simulate different system states without actually changing the system's NTP status.
    # This ensures deterministic and offline testing.
    MOCKED_TIMEDATECTL() {
        echo -e "$mock_output"
    }
    export -f MOCKED_TIMEDATECTL # Export the function so it's available in subshells

    # Override timedatectl with our mock
    PATH_ORIGINAL="$PATH"
    MOCK_BIN_DIR="$(pwd)/mock_bin"
    export PATH="$MOCK_BIN_DIR:$PATH"
    mkdir -p "$MOCK_BIN_DIR"
    echo '#!/bin/bash' > "$MOCK_BIN_DIR/timedatectl"
    echo 'MOCKED_TIMEDATECTL "$@"' >> "$MOCK_BIN_DIR/timedatectl"
    chmod +x "$MOCK_BIN_DIR/timedatectl"

    # Run the script with the mocked command
    OUTPUT=$(bash "$SCRIPT_PATH" 2>&1)
    EXIT_CODE=$?

    # Clean up mock
    rm -f "$MOCK_BIN_DIR/timedatectl"
    rmdir "$MOCK_BIN_DIR"
    export PATH="$PATH_ORIGINAL"
    unset -f MOCKED_TIMEDATECTL

    echo "Script Output:"
    echo "$OUTPUT"
    echo "Exit Code: $EXIT_CODE"

    if [[ $EXIT_CODE -eq $expected_exit_code ]] && [[ "$OUTPUT" =~ $expected_output_regex ]]; then
        echo "Test PASSED: $test_name"
        return 0
    else
        echo "Test FAILED: $test_name"
        echo "Expected Exit Code: $expected_exit_code, Got: $EXIT_CODE"
        echo "Expected Output Regex: '$expected_output_regex'"
        echo "Actual Output: '$OUTPUT'"
        return 1
    fi
}

# Test Case 1: System clock synchronized
MOCK_SYNC_OUTPUT="
               Local time: Mon 2023-10-26 10:00:00 UTC
           Universal time: Mon 2023-10-26 10:00:00 UTC
                 RTC time: Mon 2023-10-26 10:00:00
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
"
run_test "Synchronized Clock" "$MOCK_SYNC_OUTPUT" 0 "STATUS: Temporal alignment achieved! System clock is synchronized with NTP." || exit 1

# Test Case 2: NTP service active but clock not synchronized
MOCK_UNSYNC_OUTPUT="
               Local time: Mon 2023-10-26 10:00:05 UTC
           Universal time: Mon 2023-10-26 10:00:05 UTC
                 RTC time: Mon 2023-10-26 10:00:00
                Time zone: UTC (UTC, +0000)
System clock synchronized: no
              NTP service: active
          RTC in local TZ: no
"
run_test "Unsynchronized Clock (NTP active)" "$MOCK_UNSYNC_OUTPUT" 1 "WARNING: Temporal flux detected! NTP service is active, but system clock is NOT synchronized." || exit 1

# Test Case 3: NTP service inactive
MOCK_INACTIVE_OUTPUT="
               Local time: Mon 2023-10-26 10:00:00 UTC
           Universal time: Mon 2023-10-26 10:00:00 UTC
                 RTC time: Mon 2023-10-26 10:00:00
                Time zone: UTC (UTC, +0000)
System clock synchronized: no
              NTP service: inactive
          RTC in local TZ: no
"
run_test "NTP Service Inactive" "$MOCK_INACTIVE_OUTPUT" 1 "WARNING: Chrono-Sync slumbering. NTP service is inactive. System clock may drift." || exit 1

# Test Case 4: timedatectl command not found
# Mock rationale: Simulate `timedatectl` not being present on the system.
# For this test, we don't provide any mock_output to MOCKED_TIMEDATECTL, 
# as the check happens before the mock function is even called.
run_test "timedatectl Not Found" "" 1 "ERROR: timedatectl command not found. Cannot check NTP status." || exit 1

echo "All tests completed."
