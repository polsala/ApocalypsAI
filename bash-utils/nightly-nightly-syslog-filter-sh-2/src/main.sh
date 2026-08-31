#!/bin/bash

# nightly-syslog-filter-sh
# A bash script to filter system logs based on customizable patterns.

# --- Configuration ---
# Set to 'true' to enable color highlighting for matched lines.
ENABLE_COLOR="true"
# Color codes for highlighting (if ENABLE_COLOR is true)
COLOR_RED="\033[0;31m"
COLOR_YELLOW="\033[0;33m"
COLOR_GREEN="\033[0;32m"
COLOR_BLUE="\033[0;34m"
COLOR_NC="\033[0m" # No Color

# --- Helper Functions ---

# Function to print colored output
print_colored() {
    local message="$1"
    local color="$2"
    if [ "$ENABLE_COLOR" = "true" ]; then
        echo -e "${color}${message}${COLOR_NC}"
    else
        echo "$message"
    fi
}

# --- Main Logic ---

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <log_file> <pattern_file>"
    exit 1
fi

LOG_FILE="$1"
PATTERN_FILE="$2"

# Check if log file exists and is readable
if [ ! -f "$LOG_FILE" ] || [ ! -r "$LOG_FILE" ]; then
    echo "Error: Log file '$LOG_FILE' not found or not readable."
    exit 1
fi

# Check if pattern file exists and is readable
if [ ! -f "$PATTERN_FILE" ] || [ ! -r "$PATTERN_FILE" ]; then
    echo "Error: Pattern file '$PATTERN_FILE' not found or not readable."
    exit 1
fi

# Construct the grep command with patterns from the file
# Using egrep for extended regular expressions and -i for case-insensitivity
# The patterns are read from the file and passed as arguments to grep

# Build a single grep pattern string from the file
GREP_PATTERN=$(paste -sd "|" "$PATTERN_FILE")

if [ -z "$GREP_PATTERN" ]; then
    echo "Warning: Pattern file '$PATTERN_FILE' is empty. No filtering will occur."
    cat "$LOG_FILE"
    exit 0
fi

# Apply filtering
# We use grep -E to allow extended regex and -i for case-insensitivity.
# The output is piped to a loop for optional coloring.


# Temporary file to store filtered lines before coloring
FILTERED_OUTPUT=$(mktemp)

grep -E -i "$GREP_PATTERN" "$LOG_FILE" > "$FILTERED_OUTPUT"

# Process the filtered output for coloring
while IFS= read -r line;
do
    # Simple coloring logic: if any pattern matches, color the whole line.
    # More complex coloring could be implemented here based on specific keywords.
    if echo "$line" | grep -qi "ERROR"; then
        print_colored "$line" "$COLOR_RED"
    elif echo "$line" | grep -qi "WARNING"; then
        print_colored "$line" "$COLOR_YELLOW"
    elif echo "$line" | grep -qi "Accepted password"; then
        print_colored "$line" "$COLOR_GREEN"
    elif echo "$line" | grep -qi "CRON"; then
        print_colored "$line" "$COLOR_BLUE"
    else
        echo "$line"
    fi
done < "$FILTERED_OUTPUT"

# Clean up the temporary file
rm "$FILTERED_OUTPUT"

exit 0
