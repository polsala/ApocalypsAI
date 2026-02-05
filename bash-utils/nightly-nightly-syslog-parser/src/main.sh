#!/bin/bash

# Default log file
LOG_FILE="/var/log/syslog"
KEYWORDS=""
PATTERN=""
START_TIME=""
END_TIME=""
COUNT_MODE=0

# Function to display help message
show_help() {
    echo "Usage: $(basename "$0") [-f <logfile>] [-k <keyword1,keyword2,...>] [-p <pattern>] [-s <start_time>] [-e <end_time>] [-c] [-h]"
    echo "  -f <logfile>        Path to the syslog file to parse. Defaults to $LOG_FILE."
    echo "  -k <keywords>       Comma-separated list of keywords to search for (case-insensitive)."
    echo "  -p <pattern>        A regular expression pattern to search for. Overrides keyword search."
    echo "  -s <start_time>     Start time for filtering (e.g., 'YYYY-MM-DD HH:MM:SS')."
    echo "  -e <end_time>       End time for filtering (e.g., 'YYYY-MM-DD HH:MM:SS')."
    echo "  -c                  Count the number of matching log entries."
    echo "  -h                  Display this help message."
    exit 1
}

# Parse command-line options
while getopts "f:k:p:s:e:ch" opt;
do
    case "$opt" in
        f) LOG_FILE="$OPTARG";;
        k) KEYWORDS="$OPTARG";;
        p) PATTERN="$OPTARG";;
        s) START_TIME="$OPTARG";;
        e) END_TIME="$OPTARG";;
        c) COUNT_MODE=1;;
        h) show_help;;
        ?) show_help;;
    esac
done

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file '$LOG_FILE' not found." >&2
    exit 1
fi

# Build the grep command
GREP_CMD="grep -iE"

# Add pattern if provided
if [ -n "$PATTERN" ]; then
    GREP_CMD="$GREP_CMD \"$PATTERN\""
elif [ -n "$KEYWORDS" ]; then
    # Convert comma-separated keywords to an OR-ed regex pattern
    IFS=',' read -ra KEYWORD_ARRAY <<< "$KEYWORDS"
    OR_PATTERN=""
    for kw in "${KEYWORD_ARRAY[@]}"; do
        if [ -n "$OR_PATTERN" ]; then
            OR_PATTERN="$OR_PATTERN|"
        fi
        OR_PATTERN="$OR_PATTERN$kw"
    done
    GREP_CMD="$GREP_CMD \"$OR_PATTERN\""
else
    # If no keywords or pattern, just read the file (or do nothing if count mode)
    if [ "$COUNT_MODE" -eq 1 ]; then
        echo "0"
        exit 0
    fi
fi

# Add time filtering if start or end time is provided
if [ -n "$START_TIME" ] || [ -n "$END_TIME" ]; then
    # This part is a bit more complex and relies on the date format in syslog
    # For simplicity, we'll assume a standard syslog format like 'Oct 27 10:00:00'
    # A more robust solution might involve parsing dates more carefully.
    # For this example, we'll use a basic grep approach for date strings.
    
    # Construct a temporary file for filtered logs if time filtering is needed
    TEMP_FILTERED_LOG="/tmp/syslog_filter_$$_.log"
    
    # If only start time is given, filter from start time onwards
    if [ -n "$START_TIME" ] && [ -z "$END_TIME" ]; then
        # This is a simplified approach. Real syslog parsing for time ranges is complex.
        # We'll grep for lines that *look like* they are after the start time.
        # This is NOT a perfect solution for all syslog formats.
        echo "Warning: Time filtering is basic and may not be accurate for all syslog formats."
        # Attempt to extract date part from START_TIME for comparison
        START_DATE_PART=$(echo "$START_TIME" | cut -d' ' -f1-2)
        # This grep is a placeholder for more sophisticated date comparison
        grep "$START_DATE_PART" "$LOG_FILE" > "$TEMP_FILTERED_LOG"
        LOG_FILE="$TEMP_FILTERED_LOG"
    # If only end time is given, filter up to end time
    elif [ -z "$START_TIME" ] && [ -n "$END_TIME" ]; then
        END_DATE_PART=$(echo "$END_TIME" | cut -d' ' -f1-2)
        grep "$END_DATE_PART" "$LOG_FILE" > "$TEMP_FILTERED_LOG"
        LOG_FILE="$TEMP_FILTERED_LOG"
    # If both start and end times are given
    elif [ -n "$START_TIME" ] && [ -n "$END_TIME" ]; then
        START_DATE_PART=$(echo "$START_TIME" | cut -d' ' -f1-2)
        END_DATE_PART=$(echo "$END_TIME" | cut -d' ' -f1-2)
        # This is a very naive approach. A proper solution would involve date parsing.
        # For demonstration, we'll just filter lines that contain the date parts.
        grep "$START_DATE_PART" "$LOG_FILE" | grep "$END_DATE_PART" > "$TEMP_FILTERED_LOG"
        LOG_FILE="$TEMP_FILTERED_LOG"
    fi
fi

# Execute the grep command
if [ "$COUNT_MODE" -eq 1 ]; then
    eval "$GREP_CMD \"$LOG_FILE\" | wc -l"
else
    eval "$GREP_CMD \"$LOG_FILE\""
fi

# Clean up temporary file if created
if [ -n "$TEMP_FILTERED_LOG" ] && [ -f "$TEMP_FILTERED_LOG" ]; then
    rm -f "$TEMP_FILTERED_LOG"
fi

exit 0
