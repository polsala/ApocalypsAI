#!/bin/bash

# Utility Name: nightly-syslog-parser
# Description: Parses and filters system logs for keywords, patterns, or IP addresses.
# Classifier: bash-utils

# --- Configuration ---
DEFAULT_LOG_FILE="/var/log/syslog"

# --- Functions ---
usage() {
    echo "Usage: $(basename "$0") [-k "keyword"] [-p "pattern"] [-i <ip_address>] [-s <start_time>] [-e <end_time>] [-o <output_file>] [--help]"
    echo ""
    echo "Options:"
    echo "  -k "keyword"      Search for log entries containing the specified keyword."
    echo "  -p "pattern"      Search for log entries matching the given regular expression pattern."
    echo "  -i <ip_address>   Filter logs by a specific IP address (IPv4 or IPv6)."
    echo "  -s <start_time>   Filter logs starting from this timestamp (e.g., \"YYYY-MM-DD HH:MM:SS\")."
    echo "  -e <end_time>     Filter logs up to this timestamp (e.g., \"YYYY-MM-DD HH:MM:SS\")."
    echo "  -o <output_file>  Write the filtered output to the specified file instead of stdout."
    echo "  --help            Display this help message."
    exit 1
}

# --- Argument Parsing ---
KEYWORD=""
PATTERN=""
IP_ADDRESS=""
START_TIME=""
END_TIME=""
OUTPUT_FILE=""

while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        -k|--keyword)
        KEYWORD="$2"
        shift # past argument
        shift # past value
        ;; 
        -p|--pattern)
        PATTERN="$2"
        shift # past argument
        shift # past value
        ;; 
        -i|--ip)
        IP_ADDRESS="$2"
        shift # past argument
        shift # past value
        ;; 
        -s|--start)
        START_TIME="$2"
        shift # past argument
        shift # past value
        ;; 
        -e|--end)
        END_TIME="$2"
        shift # past argument
        shift # past value
        ;; 
        -o|--output)
        OUTPUT_FILE="$2"
        shift # past argument
        shift # past value
        ;; 
        --help)
        usage
        ;; 
        *)
        echo "Unknown option: $1"
        usage
        ;; 
    esac
done

# --- Main Logic ---

# Construct the grep command
GREP_CMD="grep -E "

# Add keyword filter if provided
if [ -n "$KEYWORD" ]; then
    GREP_CMD+="-e \"$KEYWORD\" "
fi

# Add pattern filter if provided
if [ -n "$PATTERN" ]; then
    GREP_CMD+="-e \"$PATTERN\" "
fi

# Add IP address filter if provided
if [ -n "$IP_ADDRESS" ]; then
    GREP_CMD+="-e \"$IP_ADDRESS\" "
fi

# Construct the date filtering logic
DATE_FILTER_CMD=""
if [ -n "$START_TIME" ] || [ -n "$END_TIME" ]; then
    # Convert human-readable dates to epoch for comparison
    if [ -n "$START_TIME" ]; then
        START_EPOCH=$(date -d "$START_TIME" +%s)
        DATE_FILTER_CMD+="awk -v start_epoch=$START_EPOCH '{ if (strftime(\"%s\", \"$1 \"$2 \"$3\") >= start_epoch) print }' " # Assuming date is first 3 fields
    fi
    if [ -n "$END_TIME" ]; then
        END_EPOCH=$(date -d "$END_TIME" +%s)
        # If start time was also provided, we need to chain awk commands or use a more complex one
        if [ -n "$START_TIME" ]; then
            DATE_FILTER_CMD="$DATE_FILTER_CMD | awk -v end_epoch=$END_EPOCH '{ if (strftime(\"%s\", \"$1 \"$2 \"$3\") <= end_epoch) print }' "
        else
            DATE_FILTER_CMD+="awk -v end_epoch=$END_EPOCH '{ if (strftime(\"%s\", \"$1 \"$2 \"$3\") <= end_epoch) print }' "
        fi
    fi
fi

# Determine the log file to use
LOG_FILE="$DEFAULT_LOG_FILE"
# In a real-world scenario, you might want to allow specifying a log file path
# For this example, we'll stick to the default or use a mock for testing.

# Build the final command pipeline
CMD_PIPELINE="cat "

# Add date filtering if specified
if [ -n "$DATE_FILTER_CMD" ]; then
    CMD_PIPELINE+="| $DATE_FILTER_CMD "
fi

# Add grep filtering if specified
if [ "$GREP_CMD" != "grep -E " ]; then
    CMD_PIPELINE+="| $GREP_CMD "
fi

# Add output redirection if specified
if [ -n "$OUTPUT_FILE" ]; then
    CMD_PIPELINE+=" > \"$OUTPUT_FILE\" "
fi

# Execute the command pipeline
# For testing purposes, we'll use a mock log file if it exists
if [ -f "./mock_syslog.log" ]; then
    echo "Using mock log file: ./mock_syslog.log"
    MOCK_LOG_CMD="cat ./mock_syslog.log"
    eval "$MOCK_LOG_CMD $CMD_PIPELINE"
else
    echo "Using default log file: $LOG_FILE"
    eval "cat \"$LOG_FILE\" $CMD_PIPELINE"
fi

exit 0
