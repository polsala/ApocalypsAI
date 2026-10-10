#!/bin/bash

# Utility: nightly-syslog-filter-cli
# Description: Filters and processes syslog messages with customizable patterns.

SYSLOG_FILE="/var/log/syslog"

# Default values
PATTERNS=()
SEVERITIES=()
START_TIME=""
END_TIME=""
OUTPUT_FORMAT="raw"

# --- Helper Functions ---

# Function to display help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo "Filters and processes syslog messages with customizable patterns."
    echo ""
    echo "Options:"
    echo "  -p, --pattern <regex>      Filter logs matching the given regular expression."
    echo "  -s, --severity <level>     Filter logs by severity level (e.g., emerg, alert, crit, err, warning, notice, info, debug)."
    echo "  -t, --time-range <start> <end> Filter logs within a specified time range. Times should be in YYYY-MM-DD HH:MM:SS format."
    echo "  -o, --output-format <format> Specify the output format. Supported: raw, json. (default: raw)"
    echo "  -h, --help                 Display this help message."
    echo ""
    echo "Example: $(basename "$0") -s err -t '2023-10-27 10:00:00' '2023-10-27 11:00:00'"
}

# Function to check if a log line matches severity
check_severity() {
    local line="$1"
    local severity="$2"
    local log_severity=$(echo "$line" | awk '{print $3}' | sed 's/[()]//g')

    if [[ -z "$log_severity" ]]; then
        # Handle lines without explicit severity (e.g., kernel messages)
        # For simplicity, we'll consider them as not matching unless explicitly handled
        return 1
    fi

    # Convert to lowercase for case-insensitive comparison
    log_severity=$(echo "$log_severity" | tr '[:upper:]' '[:lower:]')
    severity=$(echo "$severity" | tr '[:upper:]' '[:lower:]')

    if [[ "$log_severity" == "$severity" ]]; then
        return 0 # Match
    else
        return 1 # No match
    fi
}

# Function to check if a log line is within the time range
check_time_range() {
    local line="$1"
    local start="$2"
    local end="$3"

    # Extract timestamp from log line (assuming format like 'Oct 27 10:00:00')
    # This is a simplification; real syslog parsing can be complex.
    # We'll try to parse the first few fields that look like a date/time.
    local log_timestamp_str=$(echo "$line" | awk '{print $1, $2, $3}')

    # Attempt to convert to a comparable format (e.g., Unix timestamp)
    # This is a heuristic and might fail for some syslog formats.
    # For robust parsing, a dedicated tool or more complex logic would be needed.
    local log_timestamp_unix=$(date -d "$log_timestamp_str" +%s 2>/dev/null)
    local start_unix=$(date -d "$start" +%s 2>/dev/null)
    local end_unix=$(date -d "$end" +%s 2>/dev/null)

    if [[ -z "$log_timestamp_unix" || -z "$start_unix" || -z "$end_unix" ]]; then
        # If parsing fails, assume it doesn't match the time range
        return 1
    fi

    if (( log_timestamp_unix >= start_unix && log_timestamp_unix <= end_unix )); then
        return 0 # Match
    else
        return 1 # No match
    fi
}

# Function to format output as JSON
format_json() {
    local line="$1"
    local timestamp_str=$(echo "$line" | awk '{print $1, $2, $3}')
    local hostname=$(echo "$line" | awk '{print $4}')
    local process=$(echo "$line" | awk '{print $5}' | sed 's/://')
    local message=$(echo "$line" | cut -d ':' -f 2- | sed 's/^ *//')
    local severity=$(echo "$line" | awk '{print $3}' | sed 's/[()]//g')

    # Basic JSON escaping for the message content
    local escaped_message=$(echo "$message" | sed -e 's/"/\"/g' -e 's/\n/\\n/g' -e 's/\r/\\r/g' -e 's/\t/\\t/g')

    echo "{\"timestamp\": \"$timestamp_str\", \"hostname\": \"$hostname\", \"process\": \"$process\", \"severity\": \"$severity\", \"message\": \"$escaped_message\"}"
}

# --- Argument Parsing ---

while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        -p|--pattern)
            PATTERNS+=("$2")
            shift # past argument
            shift # past value
            ;;
        -s|--severity)
            SEVERITIES+=("$2")
            shift # past argument
            shift # past value
            ;;
        -t|--time-range)
            START_TIME="$2"
            END_TIME="$3"
            shift # past argument
            shift # past value
            shift # past value
            ;;
        -o|--output-format)
            OUTPUT_FORMAT="$2"
            shift # past argument
            shift # past value
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# --- Validation ---

if [[ ! -f "$SYSLOG_FILE" ]]; then
    echo "Error: Syslog file not found at '$SYSLOG_FILE'. Please check the path or ensure logs are being written." >&2
    exit 1
fi

if [[ -n "$START_TIME" && -z "$END_TIME" ]] || [[ -z "$START_TIME" && -n "$END_TIME" ]]; then
    echo "Error: Both start and end times must be provided for --time-range." >&2
    exit 1
fi

# Validate output format
if [[ "$OUTPUT_FORMAT" != "raw" && "$OUTPUT_FORMAT" != "json" ]]; then
    echo "Error: Invalid output format '$OUTPUT_FORMAT'. Supported formats are 'raw' and 'json'." >&2
    exit 1
fi

# --- Processing ---

# Read syslog file line by line
while IFS= read -r line;
do
    # Apply filters
    skip_line=0

    # Pattern filter
    if [ ${#PATTERNS[@]} -gt 0 ]; then
        match_pattern=0
        for pattern in "${PATTERNS[@]}"; do
            if echo "$line" | grep -qE "$pattern"; then
                match_pattern=1
                break
            fi
        done
        if [ "$match_pattern" -eq 0 ]; then
            skip_line=1
        fi
    fi

    # Severity filter
    if [ "$skip_line" -eq 0 ] && [ ${#SEVERITIES[@]} -gt 0 ]; then
        match_severity=0
        for severity in "${SEVERITIES[@]}"; do
            if check_severity "$line" "$severity"; then
                match_severity=1
                break
            fi
        done
        if [ "$match_severity" -eq 0 ]; then
            skip_line=1
        fi
    fi

    # Time range filter
    if [ "$skip_line" -eq 0 ] && [[ -n "$START_TIME" && -n "$END_TIME" ]]; then
        if ! check_time_range "$line" "$START_TIME" "$END_TIME"; then
            skip_line=1
        fi
    fi

    # If line passed all filters, process and output
    if [ "$skip_line" -eq 0 ]; then
        if [ "$OUTPUT_FORMAT" == "json" ]; then
            format_json "$line"
        else
            echo "$line"
        fi
    fi

done < "$SYSLOG_FILE"

exit 0
