#!/bin/bash

# Default log file
LOG_FILE="/var/log/syslog"
KEYWORD=""
PATTERN=""
START_TIME=""
END_TIME=""
OUTPUT_FILE=""

# Function to display help message
help() {
    echo "Usage: $0 [-k keyword] [-p pattern] [-f logfile] [-s start_time] [-e end_time] [-o output_file] [-h]"
    echo "  -k <keyword>      : Search for a specific keyword (case-insensitive)."
    echo "  -p <pattern>      : Search using a regular expression pattern."
    echo "  -f <logfile>      : The path to the syslog file to parse. Defaults to $LOG_FILE."
    echo "  -s <start_time>   : Filter logs from this start time (e.g., \"YYYY-MM-DD HH:MM:SS\")."
    echo "  -e <end_time>     : Filter logs up to this end time (e.g., \"YYYY-MM-DD HH:MM:SS\")."
    echo "  -o <output_file>  : Redirect the output to a specified file."
    echo "  -h                : Display this help message."
    exit 1
}

# Parse command-line options
while getopts "k:p:f:s:e:o:h" opt;
do
    case $opt in
        k) KEYWORD="$OPTARG";;
        p) PATTERN="$OPTARG";;
        f) LOG_FILE="$OPTARG";;
        s) START_TIME="$OPTARG";;
        e) END_TIME="$OPTARG";;
        o) OUTPUT_FILE="$OPTARG";;
        h) help;; 
        *)
            echo "Invalid option: -$OPTARG" >&2
            help
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

# Add keyword if provided
if [ -n "$KEYWORD" ]; then
    GREP_CMD="$GREP_CMD \"$KEYWORD\""
fi

# Add pattern if provided
if [ -n "$PATTERN" ]; then
    # If keyword is also provided, we need to combine them with OR logic in grep
    if [ -n "$KEYWORD" ]; then
        GREP_CMD="$GREP_CMD -E \"($KEYWORD|$PATTERN)\""
    else
        GREP_CMD="$GREP_CMD -E \"$PATTERN\""
    fi
elif [ -n "$KEYWORD" ]; then
    # If only keyword is provided, use it directly
    GREP_CMD="$GREP_CMD \"$KEYWORD\""
else
    # If neither keyword nor pattern is provided, we'll just show all lines (or apply time filters)
    GREP_CMD="cat"
fi

# Prepare for time filtering
FILTERED_LOG=""

if [ -n "$START_TIME" ] || [ -n "$END_TIME" ]; then
    # Convert human-readable dates to epoch seconds for comparison
    # Mock rationale: Using standard date command for time conversion. In a real scenario, error handling for invalid date formats would be crucial.
    START_EPOCH=$(date -d "$START_TIME" +%s 2>/dev/null)
    END_EPOCH=$(date -d "$END_TIME" +%s 2>/dev/null)

    # If date conversion failed, exit with an error
    if [ -n "$START_TIME" ] && [ -z "$START_EPOCH" ]; then
        echo "Error: Invalid start time format. Please use YYYY-MM-DD HH:MM:SS."
        exit 1
    fi
    if [ -n "$END_TIME" ] && [ -z "$END_EPOCH" ]; then
        echo "Error: Invalid end time format. Please use YYYY-MM-DD HH:MM:SS."
        exit 1
    fi

    # Process log file line by line for time filtering
    while IFS= read -r line;
    do
        # Extract timestamp from the log line. This is a common format, but might need adjustment for different syslog formats.
        # Mock rationale: Assuming a common syslog timestamp format like 'Oct 27 10:00:00'. More robust parsing might be needed for varied formats.
        log_timestamp_str=$(echo "$line" | awk '{print $1, $2, $3}')
        log_epoch=$(date -d "$log_timestamp_str" +%s 2>/dev/null)

        if [ -n "$log_epoch" ]; then
            # Check if the log entry falls within the specified time range
            time_match=true
            if [ -n "$START_EPOCH" ] && [ "$log_epoch" -lt "$START_EPOCH" ]; then
                time_match=false
            fi
            if [ -n "$END_EPOCH" ] && [ "$log_epoch" -gt "$END_EPOCH" ]; then
                time_match=false
            fi

            if $time_match;
            then
                FILTERED_LOG="$FILTERED_LOG$line\n"
            fi
        fi
    done < <(eval "$GREP_CMD < \"$LOG_FILE\"") # Execute the grep command and pipe its output
else
    # No time filtering, just execute the grep command directly
    FILTERED_LOG=$(eval "$GREP_CMD < \"$LOG_FILE\"")
fi

# Output the results
if [ -n "$OUTPUT_FILE" ]; then
    echo -e "$FILTERED_LOG" > "$OUTPUT_FILE"
    echo "Filtered logs saved to '$OUTPUT_FILE'."
else
    echo -e "$FILTERED_LOG"
fi

exit 0
