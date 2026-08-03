#!/bin/bash

# Nightly Chrono-Sync Anomaly Detector

# Function to check NTP synchronization status using timedatectl
check_ntp_status() {
    # Mock rationale: In a real scenario, this would execute `timedatectl status`.
    # For testing, we'll rely on a mocked version of this command.
    if ! command -v timedatectl &> /dev/null; then
        echo "ERROR: timedatectl command not found. Cannot check NTP status." >&2
        return 1
    fi

    STATUS_OUTPUT=$(timedatectl status 2>&1)
    
    if echo "$STATUS_OUTPUT" | grep -q "NTP service: active"; then
        if echo "$STATUS_OUTPUT" | grep -q "System clock synchronized: yes"; then
            echo "STATUS: Temporal alignment achieved! System clock is synchronized with NTP."
            return 0
        else
            echo "WARNING: Temporal flux detected! NTP service is active, but system clock is NOT synchronized."
            return 1
        fi
    elif echo "$STATUS_OUTPUT" | grep -q "NTP service: inactive"; then
        echo "WARNING: Chrono-Sync slumbering. NTP service is inactive. System clock may drift."
        return 1
    else
        echo "ERROR: Unable to determine Chrono-Sync status. Is timedatectl working as expected?" >&2
        echo "Raw output: $STATUS_OUTPUT" >&2
        return 1
    fi
}

# Main execution
check_ntp_status
exit $?
