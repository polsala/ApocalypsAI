#!/bin/bash

# Test suite for Nightly Chrono-Compass Calibrator

SCRIPT_PATH="../src/chrono_compass.sh"

# Mock commands
# Mock rationale: We need to control the output of system commands like timedatectl,
# chronyc, and ntpdate to simulate different system time synchronization states
# (synced, minor drift, major drift, no client available) without actually
# modifying the system's time or requiring network access. This ensures
# deterministic and offline testing.

mock_timedatectl() {
    case "$1" in
        "synced")
            echo "  System clock synchronized: yes"
            echo "  NTP synchronized: yes"
            ;;
        "unsynced")
            echo "  System clock synchronized: no"
            echo "  NTP synchronized: no"
            ;;
        *)
            echo "" # No output, simulate command not found or error
            ;;
    esac
}

mock_chronyc() {
    case "$1" in
        "synced")
            echo "Reference ID    : 0A0B0C0D (ntp.example.com)"
            echo "Stratum         : 3"
            echo "Ref time (UTC)  : Thu Jan 01 00:00:00 1970"
            echo "System time     : 0.000000000 seconds slow of NTP time"
            echo "Last offset     : +0.000000000 seconds"
            ;;
        "minor_drift")
            echo "Reference ID    : 0A0B0C0D (ntp.example.com)"
            echo "Stratum         : 3"
            echo "Ref time (UTC)  : Thu Jan 01 00:00:00 1970"
            echo "System time     : 0.000000000 seconds slow of NTP time"
            echo "Last offset     : -0.100000000 seconds" # 100ms drift
            ;;
        "major_drift")
            echo "Reference ID    : 0A0B0C0D (ntp.example.com)"
            echo "Stratum         : 3"
            echo "Ref time (UTC)  : Thu Jan 01 00:00:00 1970"
            echo "System time     : 0.000000000 seconds slow of NTP time"
            echo "Last offset     : +0.500000000 seconds" # 500ms drift
            ;;
        *)
            echo "" # No output, simulate command not found or error
            ;;
    esac
}

mock_ntpdate() {
    case "$1" in
        "synced")
            echo "19 Feb 10:00:00 ntpdate[1234]: adjust time server 1.2.3.4 offset -0.000000 sec"
            ;;
        "minor_drift")
            echo "19 Feb 10:00:00 ntpdate[1234]: adjust time server 1.2.3.4 offset +0.075000 sec" # 75ms drift
            ;;
        "major_drift")
            echo "19 Feb 10:00:00 ntpdate[1234]: adjust time server 1.2.3.4 offset -0.300000 sec" # 300ms drift
            ;;
        *)
            echo "" # No output, simulate command not found or error
            ;;
    esac
}

# Override commands for testing
# This creates temporary functions that mimic the real commands but output our mock data.
# This is a common pattern for mocking in bash tests.
timedatectl() { mock_timedatectl "$MOCK_STATE_TIMEDATECTL"; }
chronyc() { mock_chronyc "$MOCK_STATE_CHRONYC"; }
ntpdate() { mock_ntpdate "$MOCK_STATE_NTPDATE"; }

# Save original 'command' to allow fallback for non-mocked commands
declare -f -p command > /dev/null && command_orig=$(declare -f command) || unset command_orig

command() {
    # Mock rationale: The 'command -v' check needs to be mocked to control which
    # NTP client the script "finds" first. We simulate its presence based on MOCK_STATE.
    if [ "$1" = "-v" ]; then
        case "$2" in
            "timedatectl") [ "$MOCK_STATE_TIMEDATECTL" != "not_found" ];; # Returns true if not 'not_found'
            "chronyc") [ "$MOCK_STATE_CHRONYC" != "not_found" ];;       # Returns true if not 'not_found'
            "ntpdate") [ "$MOCK_STATE_NTPDATE" != "not_found" ];;       # Returns true if not 'not_found'
            *) command_orig "$@";; # Fallback for other commands
        esac
    else
        command_orig "$@"
    fi
}

run_test() {
    local test_name="$1"
    local expected_exit_code="$2"
    local expected_status_regex="$3"
    local expected_score_regex="$4"
    local expected_message_regex="$5"

    echo "--- Running Test: $test_name ---"

    # Clear previous mock states
    MOCK_STATE_TIMEDATECTL="not_found"
    MOCK_STATE_CHRONYC="not_found"
    MOCK_STATE_NTPDATE="not_found"

    # Set specific mock states for this test
    if [ -n "$6" ]; then MOCK_STATE_TIMEDATECTL="$6"; fi
    if [ -n "$7" ]; then MOCK_STATE_CHRONYC="$7"; fi
    if [ -n "$8" ]; then MOCK_STATE_NTPDATE="$8"; fi

    OUTPUT=$("$SCRIPT_PATH" 2>&1)
    ACTUAL_EXIT_CODE=$?

    echo "Script Output:"
    echo "$OUTPUT"
    echo "Actual Exit Code: $ACTUAL_EXIT_CODE"

    if [ "$ACTUAL_EXIT_CODE" -ne "$expected_exit_code" ]; then
        echo "FAIL: $test_name - Expected exit code $expected_exit_code, got $ACTUAL_EXIT_CODE"
        return 1
    fi

    if ! echo "$OUTPUT" | grep -qE "$expected_status_regex"; then
        echo "FAIL: $test_name - Output did not contain expected status regex: $expected_status_regex"
        return 1
    fi

    if ! echo "$OUTPUT" | grep -qE "$expected_score_regex"; then
        echo "FAIL: $test_name - Output did not contain expected score regex: $expected_score_regex"
        return 1
    fi

    if ! echo "$OUTPUT" | grep -qE "$expected_message_regex"; then
        echo "FAIL: $test_name - Output did not contain expected message regex: $expected_message_regex"
        return 1
    fi

    echo "PASS: $test_name"
    return 0
}

# Test Cases

# Test 1: timedatectl reports synced
run_test "timedatectl - Synced" 0 "Temporal Status: STABLE" "Temporal Stability Score: 100/100" "Chrono-Compass hums contentedly" "synced" "not_found" "not_found" || exit 1

# Test 2: timedatectl reports unsynced (major drift)
run_test "timedatectl - Unsynced" 1 "Temporal Status: MAJOR_DRIFT" "Temporal Stability Score: 0/100" "WARNING: The Chrono-Compass is wildly spinning!" "unsynced" "not_found" "not_found" || exit 1

# Test 3: chronyc reports synced (timedatectl not found)
run_test "chronyc - Synced" 0 "Temporal Status: STABLE" "Temporal Stability Score: 100/100" "Chrono-Compass hums contentedly" "not_found" "synced" "not_found" || exit 1

# Test 4: chronyc reports minor drift (timedatectl not found)
run_test "chronyc - Minor Drift" 0 "Temporal Status: MINOR_DRIFT" "Temporal Stability Score: 90/100" "slight shimmer in the temporal fabric" "not_found" "minor_drift" "not_found" || exit 1

# Test 5: chronyc reports major drift (timedatectl not found)
run_test "chronyc - Major Drift" 1 "Temporal Status: MAJOR_DRIFT" "Temporal Stability Score: 50/100" "WARNING: The Chrono-Compass is wildly spinning!" "not_found" "major_drift" "not_found" || exit 1

# Test 6: ntpdate reports synced (timedatectl, chronyc not found)
run_test "ntpdate - Synced" 0 "Temporal Status: STABLE" "Temporal Stability Score: 100/100" "Chrono-Compass hums contentedly" "not_found" "not_found" "synced" || exit 1

# Test 7: ntpdate reports minor drift (timedatectl, chronyc not found)
run_test "ntpdate - Minor Drift" 0 "Temporal Status: MINOR_DRIFT" "Temporal Stability Score: 93/100" "slight shimmer in the temporal fabric" "not_found" "not_found" "minor_drift" || exit 1

# Test 8: ntpdate reports major drift (timedatectl, chronyc not found)
run_test "ntpdate - Major Drift" 1 "Temporal Status: MAJOR_DRIFT" "Temporal Stability Score: 70/100" "WARNING: The Chrono-Compass is wildly spinning!" "not_found" "not_found" "major_drift" || exit 1

# Test 9: No NTP client found
run_test "No NTP Client" 1 "ERROR: No suitable NTP client" "Temporal Stability Score: [0-9]{1,3}/100" "Temporal stability cannot be assessed" "not_found" "not_found" "not_found" || exit 1

echo "All tests passed!"
exit 0
