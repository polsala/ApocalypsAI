#!/bin/bash

# Ensure we have at least one keyword
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <keyword1> [keyword2] ..." >&2
    exit 1
fi

# Construct the grep pattern
GREP_PATTERN=""
for keyword in "$@"; do
    if [ -n "$GREP_PATTERN" ]; then
        GREP_PATTERN="$GREP_PATTERN|"
    fi
    GREP_PATTERN="$GREP_PATTERN$keyword"
done

# Define the syslog file path (common locations, adjust if needed)
SYSLOG_FILE="/var/log/syslog"
if [ ! -f "$SYSLOG_FILE" ]; then
    SYSLOG_FILE="/var/log/messages"
fi
if [ ! -f "$SYSLOG_FILE" ]; then
    echo "Error: Could not find syslog file at /var/log/syslog or /var/log/messages." >&2
    exit 1
fi

# Whimsical prefixes for different severity levels (can be expanded)
WHIMSICAL_PREFIXES=(
    "A faint tremor in the data stream..."
    "The digital ether whispers a warning..."
    "A cosmic anomaly detected in the logs!"
    "The system sighs a cryptic message..."
    "A fleeting shadow crosses the console..."
    "The void echoes with a peculiar note..."
)

# Function to get a random whimsical prefix
get_random_prefix() {
    local num_prefixes=${#WHIMSICAL_PREFIXES[@]}
    local random_index=$((RANDOM % num_prefixes))
    echo "${WHIMSICAL_PREFIXES[$random_index]}"
}

echo "Syslog Whisperer activated. Listening for: $GREP_PATTERN"
echo "--------------------------------------------------"

tail -f "$SYSLOG_FILE" | while IFS= read -r line;
do
    if echo "$line" | grep -qE "$GREP_PATTERN"; then
        prefix=$(get_random_prefix)
        echo "$prefix [$(date '+%Y-%m-%d %H:%M:%S')] $line"
    fi
done
