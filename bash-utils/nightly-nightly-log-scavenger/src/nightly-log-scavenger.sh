#!/bin/bash

# Nightly Log Scavenger: A whimsical utility to scan system logs for critical events.

LOG_FILE="${1:-/var/log/syslog}" # Default to syslog if no argument provided

# Define keywords for different categories of "finds"
VALUABLE_SCRAPS_KEYWORDS="error|critical|fail|denied|fatal|panic"
QUESTIONABLE_FINDS_KEYWORDS="warning|warn|notice|timeout|unreachable"

# --- Functions ---

# Function to check if a file exists and is readable
check_log_file() {
    if [[ ! -f "$LOG_FILE" ]]; then
        echo "ERROR: Log file '$LOG_FILE' not found. Please specify a valid path." >&2
        exit 1
    fi
    if [[ ! -r "$LOG_FILE" ]]; then
        echo "ERROR: Log file '$LOG_FILE' is not readable. Check permissions." >&2
        exit 1
    fi
}

# Function to perform the scavenging
scavenge_logs() {
    local valuable_count=0
    local questionable_count=0

    echo "--- Nightly Log Scavenger Report ---"
    echo "Scanning: $LOG_FILE"
    echo "------------------------------------"

    # Valuable Scraps (Critical/Error events)
    echo ""
    echo "### Valuable Scraps (Critical Events) ###"
    echo "Keywords: $VALUABLE_SCRAPS_KEYWORDS"
    grep -E -i "$VALUABLE_SCRAPS_KEYWORDS" "$LOG_FILE" | while IFS= read -r line; do
        echo "  [SCRAP] $line"
        ((valuable_count++))
    done
    echo "Total Valuable Scraps Found: $valuable_count"

    # Questionable Finds (Warning/Notice events)
    echo ""
    echo "### Questionable Finds (Warning/Notice Events) ###"
    echo "Keywords: $QUESTIONABLE_FINDS_KEYWORDS"
    grep -E -i "$QUESTIONABLE_FINDS_KEYWORDS" "$LOG_FILE" | while IFS= read -r line; do
        echo "  [FIND] $line"
        ((questionable_count++))
    done
    echo "Total Questionable Finds: $questionable_count"

    echo ""
    echo "--- Scavenging Summary ---"
    echo "Valuable Scraps (Errors/Critical): $valuable_count"
    echo "Questionable Finds (Warnings/Notices): $questionable_count"

    if [[ "$valuable_count" -gt 0 ]]; then
        echo "STATUS: ALERT! High-value scraps detected. Immediate attention recommended!"
        exit 2 # Indicate critical issues
    elif [[ "$questionable_count" -gt 0 ]]; then
        echo "STATUS: CAUTION! Some questionable finds. Worth a closer look."
        exit 1 # Indicate warnings
    else
        echo "STATUS: All clear! The wasteland is quiet tonight."
        exit 0 # Indicate no issues
    fi
}

# --- Main execution ---
check_log_file
scavenge_logs
