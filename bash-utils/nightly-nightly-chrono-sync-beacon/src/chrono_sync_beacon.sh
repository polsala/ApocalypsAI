#!/bin/bash

# Default configuration values
NTP_SERVER="${NTP_SERVER:-pool.ntp.org}"
DRIFT_THRESHOLD_SECONDS="${DRIFT_THRESHOLD_SECONDS:-5}" # seconds
SYNC_ENABLED="${SYNC_ENABLED:-false}" # Set to 'true' to enable actual time synchronization
LOG_FILE="${LOG_FILE:-/var/log/chrono_sync_beacon.log}"

# Function to log messages
log_message() {
    local type="$1"
    local message="$2"
    echo "$(date '+%Y-%m-%d %H:%M:%S') [CHRONO-SYNC-BEACON][$type] $message" | tee -a "$LOG_FILE"
}

# --- Pre-flight Checks ---

# Check if sntp is available
if ! command -v sntp &> /dev/null; then
    log_message "ERROR" "sntp command not found. Please install ntpdate or ntp client utilities (e.g., 'sudo apt install ntpdate' or 'sudo apt install ntpsec-ntpclient')."
    exit 1
fi

# Check if bc is available for floating-point comparisons
if ! command -v bc &> /dev/null; then
    log_message "ERROR" "bc command not found. Please install it (e.g., 'sudo apt install bc')."
    exit 1
fi

log_message "INFO" "Initiating temporal scan with NTP server: $NTP_SERVER"

# --- Get Offset from NTP Server ---

# sntp -d outputs offset in seconds. Example: "sntp: offset -0.000000 sec"
NTP_OUTPUT=$(sntp -d "$NTP_SERVER" 2>&1)
NTP_EXIT_CODE=$?

if [ $NTP_EXIT_CODE -ne 0 ]; then
    log_message "ERROR" "Failed to query NTP server $NTP_SERVER. Check network connectivity or NTP server availability. Output: $NTP_OUTPUT"
    exit 1
fi

# Parse offset from sntp output
OFFSET_STR=$(echo "$NTP_OUTPUT" | grep -oP 'offset \K[+-]?[0-9]+\.[0-9]+')

if [ -z "$OFFSET_STR" ]; then
    log_message "ERROR" "Could not parse offset from sntp output: $NTP_OUTPUT"
    exit 1
fi

# Calculate absolute offset for comparison
OFFSET_ABS=$(echo "$OFFSET_STR" | awk '{print ($1 < 0 ? -$1 : $1)}')

log_message "INFO" "Detected temporal offset: ${OFFSET_STR} seconds."

# --- Compare with Threshold and Synchronize if Needed ---

# Use 'bc -l' for floating-point comparison
if (( $(echo "$OFFSET_ABS > $DRIFT_THRESHOLD_SECONDS" | bc -l) )); then
    log_message "WARNING" "Significant temporal anomaly detected! Offset: ${OFFSET_STR}s (Threshold: ${DRIFT_THRESHOLD_SECONDS}s)"
    if [ "$SYNC_ENABLED" = "true" ]; then
        log_message "INFO" "Attempting to synchronize system time..."
        # sntp -s synchronizes the time. Requires root privileges.
        SYNC_OUTPUT=$(sudo sntp -s "$NTP_SERVER" 2>&1)
        SYNC_EXIT_CODE=$?
        if [ $SYNC_EXIT_CODE -eq 0 ]; then
            log_message "SUCCESS" "System time synchronized. Output: $SYNC_OUTPUT"
        else
            log_message "ERROR" "Failed to synchronize system time. Check sudo permissions for sntp or sntp issues. Output: $SYNC_OUTPUT"
            exit 1
        fi
    else
        log_message "INFO" "Synchronization is disabled (SYNC_ENABLED=false). Manual intervention may be required to correct the temporal anomaly."
    fi
else
    log_message "INFO" "Temporal stability confirmed. Offset within acceptable limits."
fi

exit 0
