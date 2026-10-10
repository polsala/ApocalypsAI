#!/bin/bash

# Configuration for syslog filtering
# Lines matching any pattern in INCLUDE_PATTERNS will be considered for inclusion.
# Lines matching any pattern in EXCLUDE_PATTERNS will be discarded, regardless of inclusion.

# Default patterns: include 'error' and 'warning', exclude 'systemd'
INCLUDE_PATTERNS=("error" "warning")
EXCLUDE_PATTERNS=("systemd")

# Function to check if a line matches any pattern in an array
# Args: $1 - line to check, $2 - array name
matches_any_pattern() {
    local line="$1"
    local -n patterns="$2"
    for pattern in "${patterns[@]}"; do
        if [[ "$line" =~ $pattern ]]; then
            return 0 # Match found
        fi
    done
    return 1 # No match found
}

# Determine the input source
if [ -t 0 ]; then
    # Stdin is not a terminal, assume piped input or file argument
    if [ $# -gt 0 ]; then
        # Process file argument
        exec < "$1"
    else
        echo "Usage: $0 [log_file]" >&2
        echo "Piping syslog to stdin is also supported." >&2
        exit 1
    fi
fi

# Process each line from stdin
while IFS= read -r line;
do
    # First, check for exclusion patterns
    if matches_any_pattern "$line" EXCLUDE_PATTERNS;
    then
        continue # Skip this line if it matches an exclusion pattern
    fi

    # If no exclusion patterns matched, check for inclusion patterns
    # If INCLUDE_PATTERNS is empty, all lines (not excluded) are included.
    if [ ${#INCLUDE_PATTERNS[@]} -eq 0 ]; then
        echo "$line"
    elif matches_any_pattern "$line" INCLUDE_PATTERNS;
    then
        echo "$line"
    fi
done
