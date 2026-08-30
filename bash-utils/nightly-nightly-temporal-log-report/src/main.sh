#!/bin/bash

# Function to check for NTP/time sync issues in journalctl
# This function is designed to be easily mockable for testing.
check_journalctl_impl() {
    if command -v journalctl &> /dev/null; then
        journalctl --since "1 week ago" -u systemd-timesyncd.service -u ntp.service -u chrony.service -g "NTP|time sync|clock drift|offset" --no-pager
    else
        echo "journalctl not found. Skipping journalctl check."
        return 1
    fi
}

# Function to check for time-related issues in dmesg
# This function is designed to be easily mockable for testing.
check_dmesg_impl() {
    if command -v dmesg &> /dev/null; then
        dmesg | grep -iE "time|clock|drift|ntp" | tail -n 20
    else
        echo "dmesg not found. Skipping dmesg check."
        return 1
    fi
}

# Public interface for checking journalctl (can be overridden by tests)
check_journalctl() {
    check_journalctl_impl
}

# Public interface for checking dmesg (can be overridden by tests)
check_dmesg() {
    check_dmesg_impl
}

# Main report generation logic
generate_report() {
    echo "🌌 Nightly Temporal Anomaly Report 🌌"
    echo "-------------------------------------"
    echo "Scanning for ripples in the spacetime continuum (aka system time issues)..."
    echo ""

    local journal_output=$(check_journalctl)
    local dmesg_output=$(check_dmesg)

    local anomalies_found=0

    # Check if journalctl found anything meaningful
    if [ -n "$journal_output" ] && ! echo "$journal_output" | grep -q "journalctl not found"; then
        echo "🌠 Journalctl Whispers (systemd-timesyncd, NTP, Chrony):"
        echo "-------------------------------------------------"
        echo "$journal_output"
        anomalies_found=1
    fi

    # Check if dmesg found anything meaningful
    if [ -n "$dmesg_output" ] && ! echo "$dmesg_output" | grep -q "dmesg not found"; then
        echo ""
        echo "🕰️ Dmesg Echoes (kernel time events):"
        echo "------------------------------------"
        echo "$dmesg_output"
        anomalies_found=1
    fi

    if [ "$anomalies_found" -eq 0 ]; then
        echo "✨ All clear! The temporal fabric appears stable. No significant anomalies detected."
        echo "   (Or perhaps the anomalies are too subtle for our current instruments...)"
    else
        echo ""
        echo "⚠️ Warning: Potential temporal distortions detected! Further investigation recommended."
        echo "   These ripples might indicate a slight desynchronization with the cosmic clock."
    fi

    echo ""
    echo "-------------------------------------"
    echo "Report generated on: $(date)"
}

# Execute the report generation if the script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    generate_report
fi
