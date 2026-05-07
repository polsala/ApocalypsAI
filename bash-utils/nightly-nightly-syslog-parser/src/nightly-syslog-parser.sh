#!/bin/bash

# Utility Name: nightly-syslog-parser
# Classifier: bash-utils
# Summary: A bash script to parse and filter system logs for specific keywords, with customizable output.

# --- Configuration ---
DEFAULT_LOG_FILES=("/var/log/syslog" "/var/log/auth.log")
DEFAULT_FORMAT="default"

# --- Functions ---

usage() {
    echo "Usage: $0 [-k <keyword>] [-l <logfile>] [-f <format>] [-h]"
    echo "  -k <keyword>    Specify a keyword to search for (can be used multiple times)."
    echo "  -l <logfile>    Specify a log file to parse (can be used multiple times)."
    echo "                  Defaults to ${DEFAULT_LOG_FILES[*]}."
    echo "  -f <format>     Specify output format: default, json, brief. Defaults to '$DEFAULT_FORMAT'."
    echo "  -h              Display this help message."
    exit 1
}

parse_log_entry() {
    local line="$1"
    local format="$2"

    case "$format" in
        "json")
            # Attempt to extract timestamp, hostname, process, and message
            # This is a simplified regex and might not cover all syslog formats perfectly.
            if [[ "$line" =~ ^([A-Za-z]{3}\s+[0-9]{1,2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2})\s+([^\s]+)\s+([^\s]+):
                timestamp="${BASH_REMATCH[1]}"
                hostname="${BASH_REMATCH[2]}"
                process="${BASH_REMATCH[3]}"
                message="${line#*${process}: }"
                echo "{\"timestamp\": \"$timestamp\", \"hostname\": \"$hostname\", \"process\": \"$process\", \"message\": \"$message\"}"
            else
                # Fallback for lines that don't match the expected pattern
                echo "{\"raw_line\": \"$line\"}"
            fi
            ;;
        "brief")
            # Extract timestamp and message, assuming a standard syslog format
            if [[ "$line" =~ ^([A-Za-z]{3}\s+[0-9]{1,2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2})\s+.*:\n                timestamp="${BASH_REMATCH[1]}"
                message="${line#*: }"
                echo "[$timestamp] $message"
            else
                echo "$line"
            fi
            ;;
        "default")
            echo "$line"
            ;;
        *)
            echo "Error: Unknown format '$format'. Using default."
            echo "$line"
            ;;
    esac
}

# --- Main Script ---

keywords=()
log_files=("${DEFAULT_LOG_FILES[@]}")
output_format="$DEFAULT_FORMAT"

# Parse command-line arguments
while getopts "k:l:f:h" opt;
do
    case "$opt" in
        k)
            keywords+=("$OPTARG")
            ;;
        l)
            log_files+=("$OPTARG")
            ;;
        f)
            output_format="$OPTARG"
            ;;
        h)
            usage
            ;;
        *)
            usage
            ;;
    esac
done

# Remove duplicate log files if any
readarray -t unique_log_files < <(printf "%s\n" "${log_files[@]}" | sort -u)
log_files=("${unique_log_files[@]}")

# Check if any keywords were provided
if [ ${#keywords[@]} -eq 0 ]; then
    echo "Error: No keywords provided. Use -k to specify keywords."
    usage
fi

# Construct the grep pattern
grep_pattern=""
for i in "${!keywords[@]}"; do
    if [ $i -gt 0 ]; then
        grep_pattern="$grep_pattern -e "
    fi
    grep_pattern="$grep_pattern -e ${keywords[$i]}"
done

# Process each log file
for log_file in "${log_files[@]}"; do
    if [ ! -f "$log_file" ]; then
        echo "Warning: Log file '$log_file' not found. Skipping." >&2
        continue
    fi

    # Use grep to find matching lines and then process them
    # The '-E' flag enables extended regular expressions for -e
    # The '-i' flag makes the search case-insensitive
    grep -E "${keywords[*]/#/-e }" "$log_file" | while IFS= read -r line;
    do
        parse_log_entry "$line" "$output_format"
    done
done

exit 0
