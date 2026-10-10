#!/bin/bash

# nightly-syslog-parser.sh
# Parses system logs for specified keywords.

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if log file and at least one keyword are provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <log_file> <keyword1> [keyword2 ...]"
    exit 1
fi

LOG_FILE="$1"
shift # Remove the log file from the arguments, leaving only keywords
KEYWORDS="$@"

# Check if the log file exists and is readable
if [ ! -f "$LOG_FILE" ] || [ ! -r "$LOG_FILE" ]; then
    echo "Error: Log file '$LOG_FILE' not found or not readable."
    exit 1
fi

# Construct the grep command dynamically
# -i for case-insensitive search
# -E for extended regular expressions (though not strictly needed for simple keywords, good practice)
# -e for specifying multiple patterns (OR logic)
GREP_CMD="grep -iE"

for keyword in $KEYWORDS;
do
    GREP_CMD="$GREP_CMD -e \"$keyword\""
done

# Execute the grep command on the log file
# Use eval to correctly interpret the dynamically built command string
eval $GREP_CMD "$LOG_FILE"

exit 0
