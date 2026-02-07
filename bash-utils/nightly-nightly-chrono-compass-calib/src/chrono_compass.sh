#!/bin/bash

# Nightly Chrono-Compass Calibrator
# Checks system time synchronization status and reports any significant drift.

# Configuration
MAX_ACCEPTABLE_DRIFT_MS=50    # Max drift for "Stable" status
WARN_DRIFT_MS=200             # Drift threshold for "Minor Drift" warning

# Function to get drift using timedatectl (systemd)
get_timedatectl_drift() {
    if command -v timedatectl &> /dev/null; then
        # Mock rationale: timedatectl output is parsed. We need to simulate synced and unsynced states.
        # For this utility, we'll use the 'NTP synchronized' status as a primary indicator.
        # If 'NTP synchronized: yes', we'll report minimal drift.
        # If 'NTP synchronized: no', we'll report potential significant drift.
        STATUS=$(timedatectl status 2>/dev/null)
        if echo "$STATUS" | grep -q "NTP synchronized: yes"; then
            echo "0" # Assume 0ms drift if synchronized
        else
            echo "1000" # Assume 1000ms drift if not synchronized (significant)
        fi
        return 0
    fi
    return 1
}

# Function to get drift using chronyc (chrony daemon)
get_chronyc_drift() {
    if command -v chronyc &> /dev/null; then
        # Mock rationale: chronyc tracking output is parsed. We need to simulate different offsets.
        TRACKING_INFO=$(chronyc tracking 2>/dev/null)
        if echo "$TRACKING_INFO" | grep -q "Reference ID"; then
            OFFSET_LINE=$(echo "$TRACKING_INFO" | grep "Last offset")
            OFFSET_SECONDS=$(echo "$OFFSET_LINE" | awk '{print $3}')
            # Calculate absolute milliseconds
            ABS_OFFSET_SECONDS=$(echo "scale=6; if ($OFFSET_SECONDS < 0) -$OFFSET_SECONDS else $OFFSET_SECONDS" | bc)
            DRIFT_MS=$(echo "$ABS_OFFSET_SECONDS * 1000" | bc | awk '{print int($1)}')
            echo "$DRIFT_MS"
            return 0
        fi
    fi
    return 1
}

# Function to get drift using ntpdate (legacy NTP client)
get_ntpdate_drift() {
    if command -v ntpdate &> /dev/null; then
        # Mock rationale: ntpdate output is parsed. We need to simulate different offsets.
        NTP_SERVER="pool.ntp.org" # Use a common NTP server, mocked in tests
        OUTPUT=$(ntpdate -q "$NTP_SERVER" 2>&1)
        if echo "$OUTPUT" | grep -q "offset"; then
            OFFSET_LINE=$(echo "$OUTPUT" | grep "offset")
            OFFSET_SECONDS=$(echo "$OFFSET_LINE" | awk '{print $NF}' | sed 's/sec//')
            # Calculate absolute milliseconds
            ABS_OFFSET_SECONDS=$(echo "scale=6; if ($OFFSET_SECONDS < 0) -$OFFSET_SECONDS else $OFFSET_SECONDS" | bc)
            DRIFT_MS=$(echo "$ABS_OFFSET_SECONDS * 1000" | bc | awk '{print int($1)}')
            echo "$DRIFT_MS"
            return 0
        fi
    fi
    return 1
}

# Main logic
echo "Nightly Chrono-Compass Calibrator Initiating Temporal Scan..."
echo "---------------------------------------------------"

DRIFT_MS=""

# Try timedatectl first
DRIFT_MS=$(get_timedatectl_drift)
if [ -n "$DRIFT_MS" ]; then
    echo "Using timedatectl for temporal readings."
elif [ -z "$DRIFT_MS" ]; then # If timedatectl didn't provide a drift, try chronyc
    DRIFT_MS=$(get_chronyc_drift)
    if [ -n "$DRIFT_MS" ]; then
        echo "Using chronyc for temporal readings."
    elif [ -z "$DRIFT_MS" ]; then # If chronyc didn't provide a drift, try ntpdate
        DRIFT_MS=$(get_ntpdate_drift)
        if [ -n "$DRIFT_MS" ]; then
            echo "Using ntpdate for temporal readings."
        fi
    fi
fi

if [ -z "$DRIFT_MS" ]; then
    echo "ERROR: No suitable NTP client (timedatectl, chronyc, ntpdate) found or able to report drift."
    echo "Temporal stability cannot be assessed. Please ensure an NTP client is installed and configured."
    exit 1
fi

echo "Detected temporal offset: ${DRIFT_MS} ms"

STATUS="UNKNOWN"
if (( DRIFT_MS <= MAX_ACCEPTABLE_DRIFT_MS )); then
    STATUS="STABLE"
elif (( DRIFT_MS <= WARN_DRIFT_MS )); then
    STATUS="MINOR_DRIFT"
else
    STATUS="MAJOR_DRIFT"
fi

# Calculate Temporal Stability Score (0-100)
# Score is inversely proportional to drift. Max drift for 0 score is 1000ms.
# If drift is 0, score is 100. If drift is 1000ms or more, score is 0.
# Linear interpolation: Score = 100 - (drift_ms / 1000) * 100
# Clamp score between 0 and 100.
SCORE=$(echo "scale=2; 100 - ($DRIFT_MS / 1000) * 100" | bc)
if (( $(echo "$SCORE < 0" | bc -l) )); then
    SCORE=0
elif (( $(echo "$SCORE > 100" | bc -l) )); then
    SCORE=100
fi
SCORE_INT=$(printf "%.0f" "$SCORE") # Round to nearest integer

echo "Temporal Status: $STATUS"
echo "Temporal Stability Score: $SCORE_INT/100"

case "$STATUS" in
    "STABLE")
        echo "The Chrono-Compass hums contentedly. Temporal alignment is pristine!"
        exit 0
        ;;
    "MINOR_DRIFT")
        echo "A slight shimmer in the temporal fabric. Minor adjustments may be needed."
        exit 0 # Minor drift is a warning, but not a critical failure for the script itself
        ;;
    "MAJOR_DRIFT")
        echo "WARNING: The Chrono-Compass is wildly spinning! Significant temporal distortion detected!"
        echo "Immediate recalibration recommended to prevent timeline anomalies."
        exit 1
        ;;
    *)
        echo "Temporal status is indeterminate. Proceed with caution."
        exit 1
        ;;
esac
