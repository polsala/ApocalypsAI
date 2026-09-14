#!/bin/bash

# nightly-log-whisperer.sh
# Analyzes log files for 'whispers' of potential issues.

# --- Configuration ---
DEFAULT_KEYWORDS="ERROR WARN FAIL EXCEPTION CRITICAL"

# --- Helper Functions ---

# Prints a formatted message to stderr
log_message() {
    echo "[LOG WHISPERER] $1" >&2
}

# Prints a formatted warning to stderr
log_warning() {
    echo "[LOG WHISPERER - WARNING] $1" >&2
}

# Prints a formatted error to stderr and exits
log_error() {
    echo "[LOG WHISPERER - ERROR] $1" >&2
    exit 1
}

# --- Main Logic ---

# Check if a log file is provided
if [ -z "$1" ]; then
    log_error "No log file specified. Usage: $0 <log_file_path> [keyword1 keyword2 ...]"
fi

LOG_FILE="$1"
shift # Remove the log file from arguments

# Combine default and user-provided keywords
KEYWORDS="$DEFAULT_KEYWORDS $@"

# Check if the log file exists and is readable
if [ ! -f "$LOG_FILE" ] || [ ! -r "$LOG_FILE" ]; then
    log_error "Log file '$LOG_FILE' not found or not readable."
fi

log_message "Starting analysis of '$LOG_FILE' for whispers..."

# --- Analysis Steps ---

# 1. Find lines matching keywords
log_message "Searching for keywords: $KEYWORDS"
MATCHING_LINES=$(grep -E "$KEYWORDS" "$LOG_FILE")

if [ -z "$MATCHING_LINES" ]; then
    log_message "No lines found matching the specified keywords."
else
    echo "\n--- Potential Whispers (Keyword Matches) ---"
    echo "$MATCHING_LINES"
fi

# 2. Frequency analysis of matching lines
if [ -n "$MATCHING_LINES" ]; then
    log_message "Performing frequency analysis on matching lines..."
    # Use awk to count occurrences of each unique line
    # Then sort by count and filter for lines appearing more than once
    FREQUENCY_ANALYSIS=$(echo "$MATCHING_LINES" | awk '{count[$0]++} END {for (line in count) if (count[line] > 1) print count[line] " : " line}' | sort -nr)

    if [ -z "$FREQUENCY_ANALYSIS" ]; then
        log_message "No lines appeared more than once."
    else
        echo "\n--- Frequent Whispers (Repeated Occurrences) ---"
        echo "$FREQUENCY_ANALYSIS"
    fi
fi

log_message "Analysis complete."
exit 0
