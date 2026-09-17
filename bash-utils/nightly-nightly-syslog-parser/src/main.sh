#!/bin/bash

# Default values
KEYWORD=""
PATTERN=""
START_TIME=""
END_TIME=""
LOG_LEVEL=""

# Function to display help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS] <log_file>"
    echo "Parses and filters system logs for specific keywords or patterns."
    echo ""
    echo "Options:"
    echo "  -k, --keyword <keyword>     Search for a specific keyword (case-insensitive)."
    echo "  -p, --pattern <regex>       Search using a regular expression."
    echo "  -s, --start-time <timestamp> Filter logs from this timestamp onwards (e.g., 'YYYY-MM-DD HH:MM:SS')."
    echo "  -e, --end-time <timestamp>   Filter logs up to this timestamp (e.g., 'YYYY-MM-DD HH:MM:SS')."
    echo "  -l, --log-level <level>     Highlight a specific log level (e.g., 'ERROR', 'WARN', 'INFO')."
    echo "  -h, --help                  Display this help message."
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") -k error /var/log/syslog"
    echo "  $(basename "$0") -p \"failed login\" /var/log/auth.log"
    echo "  $(basename "$0") -s \"2023-10-27 10:00:00\" -e \"2023-10-27 11:00:00\" /var/log/syslog"
    echo "  $(basename "$0") -l WARN /var/log/messages"
    exit 1
}

# Parse command-line options
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
        -s|--start-time)
        START_TIME="$2"
        shift # past argument
        shift # past value
        ;;
        -e|--end-time)
        END_TIME="$2"
        shift # past argument
        shift # past value
        ;;
        -l|--log-level)
        LOG_LEVEL="$2"
        shift # past argument
        shift # past value
        ;;
        -h|--help)
        show_help
        ;;
        -*) # unknown option
        echo "Unknown option: $1"
        show_help
        ;;
        *)
        LOG_FILE="$1"
        shift # past argument
        ;;
    esac
done

# Check if log file is provided
if [ -z "$LOG_FILE" ]; then
    echo "Error: Log file is required."
    show_help
fi

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file '$LOG_FILE' not found."
    exit 1
fi

# Build the grep command
GREP_CMD="grep -i"

# Add keyword filter
if [ -n "$KEYWORD" ]; then
    GREP_CMD="$GREP_CMD \"$KEYWORD\""
fi

# Add pattern filter
if [ -n "$PATTERN" ]; then
    GREP_CMD="$GREP_CMD -E \"$PATTERN\""
fi

# Process the log file

# Initial filtering based on keyword/pattern
if [ -n "$KEYWORD" ] || [ -n "$PATTERN" ]; then
    FILTERED_LOG=$(eval "$GREP_CMD ""$LOG_FILE""")
else
    # If no keyword or pattern, use the whole file
    FILTERED_LOG=$(cat "$LOG_FILE")
fi

# Apply timestamp filtering if specified
if [ -n "$START_TIME" ] || [ -n "$END_TIME" ]; then
    # Convert timestamps to epoch for easier comparison
    START_EPOCH=$(date -d "$START_TIME" +%s 2>/dev/null)
    END_EPOCH=$(date -d "$END_TIME" +%s 2>/dev/null)

    # Check for valid date conversions
    if [ -n "$START_TIME" ] && [ -z "$START_EPOCH" ]; then
        echo "Error: Invalid start time format. Please use 'YYYY-MM-DD HH:MM:SS'."
        exit 1
    fi
    if [ -n "$END_TIME" ] && [ -z "$END_EPOCH" ]; then
        echo "Error: Invalid end time format. Please use 'YYYY-MM-DD HH:MM:SS'."
        exit 1
    fi

    # Filter by timestamp using awk
    FILTERED_LOG=$(echo "$FILTERED_LOG" | awk -v start="$START_EPOCH" -v end="$END_EPOCH" 'BEGIN { 
        if (start == "") start = 0; 
        if (end == "") end = systime(); 
    } {
        # Attempt to parse timestamp from the beginning of the line
        # This is a common syslog format, adjust if needed
        match($0, /[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}/, ts_arr);
        if (ts_arr[0] != "") {
            log_epoch = mktime(gensub(/-/, " ", "g", ts_arr[0]));
            if (log_epoch >= start && log_epoch <= end) {
                print $0
            }
        } else {
            # If no timestamp found, assume it's part of a previous entry or irrelevant
            # For simplicity, we might skip lines without a clear timestamp or include them if start/end are not strict
            # Here, we'll skip lines without a parsable timestamp for strict filtering
        }
    }')
fi

# Apply log level highlighting if specified
if [ -n "$LOG_LEVEL" ]; then
    # Use ANSI escape codes for coloring
    # Basic coloring: Red for ERROR, Yellow for WARN, Cyan for INFO
    case "${LOG_LEVEL^^}" in # Convert to uppercase for case-insensitive matching
        ERROR)
            COLOR="\033[0;31m"
            ;; # Red
        WARN|WARNING)
            COLOR="\033[0;33m"
            ;; # Yellow
        INFO|INFORMATION)
            COLOR="\033[0;36m"
            ;; # Cyan
        *)
            COLOR=""
            ;; # No color for unknown levels
    esac

    if [ -n "$COLOR" ]; then
        # Highlight the specific log level, then print the whole line
        # This assumes the log level is a distinct word in the log line
        FILTERED_LOG=$(echo "$FILTERED_LOG" | sed "s/\(${LOG_LEVEL^^}\)/${COLOR}\1\033[0m/g")
    fi
fi

# Output the final result
echo "$FILTERED_LOG"
