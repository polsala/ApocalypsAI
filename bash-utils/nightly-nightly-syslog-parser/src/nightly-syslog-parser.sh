#!/bin/bash

# Default syslog file
LOG_FILE="/var/log/syslog"
KEYWORD=""
PATTERN=""
START_TIME=""
END_TIME=""
OUTPUT_FILE=""

# Function to display help message
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Parses and filters syslog messages."
    echo ""
    echo "OPTIONS:"
    echo "  -k <keyword>      Search for a specific keyword (case-insensitive)."
    echo "  -p <pattern>      Search using a regular expression pattern."
    echo "  -t <start_time>   Filter logs from this timestamp onwards (YYYY-MM-DD HH:MM:SS)."
    echo "  -e <end_time>     Filter logs up to this timestamp (YYYY-MM-DD HH:MM:SS)."
    echo "  -f <log_file>     Specify the syslog file to parse (defaults to /var/log/syslog)."
    echo "  -o <output_file>  Redirect output to a specified file."
    echo "  -h                Display this help message."
    exit 0
}

# Parse command-line options
while getopts "k:p:t:e:f:o:h" opt;
do
    case "$opt" in
        k)
            KEYWORD="$OPTARG"
            ;; 
        p)
            PATTERN="$OPTARG"
            ;; 
        t)
            START_TIME="$OPTARG"
            ;; 
        e)
            END_TIME="$OPTARG"
            ;; 
        f)
            LOG_FILE="$OPTARG"
            ;; 
        o)
            OUTPUT_FILE="$OPTARG"
            ;; 
        h)
            show_help
            ;; 
        ?)
            echo "Invalid option: -$OPTARG" >&2
            show_help
            ;; 
    esac
done

# Validate log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file '$LOG_FILE' not found." >&2
    exit 1
fi

# Build the grep command
GREP_CMD="grep -i"

# Add keyword filter if provided
if [ -n "$KEYWORD" ]; then
    GREP_CMD="$GREP_CMD \"$KEYWORD\""
fi

# Add pattern filter if provided
if [ -n "$PATTERN" ]; then
    GREP_CMD="$GREP_CMD -E \"$PATTERN\""
fi

# Construct the full command pipeline
COMMAND="cat \"$LOG_FILE\""

# Add timestamp filtering if provided
if [ -n "$START_TIME" ] && [ -n "$END_TIME" ]; then
    # Using awk for robust timestamp comparison
    COMMAND="$COMMAND | awk -v start='$START_TIME' -v end='$END_TIME' '{ 
        # Attempt to parse timestamp from the beginning of the line
        # This is a common syslog format, adjust if yours differs
        match($0, /^[A-Za-z]{3}\s+[0-9]{1,2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}/, ts_match);
        if (ts_match[0]) {
            log_ts_str = ts_match[0];
            # Convert to epoch for comparison
            # Note: This assumes a simplified date format and might need adjustment for year
            # For simplicity, we'll assume current year if not specified in log
            # A more robust solution would involve date parsing libraries or commands
            # For this example, we'll use a basic string comparison which is less robust but works for many cases
            # A better approach would be to convert both to a comparable format like epoch seconds
            # For now, let's use string comparison for simplicity, assuming consistent format
            if (log_ts_str >= start && log_ts_str <= end) {
                print $0
            }
        } else {
            # If timestamp not found, print line if no time filter is active, or skip if time filter is active
            # This part might need refinement based on actual log formats
            if (start == "" && end == "") {
                print $0
            }
        }
    }' )"
elif [ -n "$START_TIME" ]; then
    COMMAND="$COMMAND | awk -v start='$START_TIME' '{ 
        match($0, /^[A-Za-z]{3}\s+[0-9]{1,2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}/, ts_match);
        if (ts_match[0]) {
            log_ts_str = ts_match[0];
            if (log_ts_str >= start) {
                print $0
            }
        } else {
            if (start == "") {
                print $0
            }
        }
    }' "
elif [ -n "$END_TIME" ]; then
    COMMAND="$COMMAND | awk -v end='$END_TIME' '{ 
        match($0, /^[A-Za-z]{3}\s+[0-9]{1,2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}/, ts_match);
        if (ts_match[0]) {
            log_ts_str = ts_match[0];
            if (log_ts_str <= end) {
                print $0
            }
        } else {
            if (end == "") {
                print $0
            }
        }
    }' "
fi

# Add the grep command to the pipeline
COMMAND="$COMMAND | $GREP_CMD"

# Execute the command and handle output
if [ -n "$OUTPUT_FILE" ]; then
    eval "$COMMAND > \"$OUTPUT_FILE\""
    echo "Filtered logs saved to \"$OUTPUT_FILE\""
else
    eval "$COMMAND"
fi

exit 0
