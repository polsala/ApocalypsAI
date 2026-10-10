#!/bin/bash

# Nightly Syslog Filter
# Filters syslog messages based on a configuration file.

# --- Configuration --- 
# Default configuration file if none is provided
DEFAULT_CONFIG="config.txt"

# --- Helper Functions ---

# Function to log messages with a specific prefix
log_message() {
    local prefix="$1"
    local message="$2"
    echo "$prefix: $message"
}

# Function to send an alert
alert_message() {
    local level="$1"
    local message="$2"
    log_message "ALERT ($level)" "$message"
    # In a real-world scenario, this could send an email, trigger a webhook, etc.
    # For this utility, we'll just echo to stderr.
    echo "ALERT: Critical event detected - $message" >&2
}

# --- Main Logic ---

# Determine the configuration file
CONFIG_FILE=${1:-$DEFAULT_CONFIG}

# Check if configuration file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file '$CONFIG_FILE' not found." >&2
    exit 1
fi

# Read and process the configuration file line by line
while IFS= read -r line || [[ -n "$line" ]]; do
    # Skip comments and empty lines
    if [[ "$line" =~ ^#.* ]] || [ -z "$line" ]; then
        continue
    fi

    # Parse the rule: LEVEL:PATTERN:ACTION
    IFS=':' read -r LEVEL PATTERN ACTION <<< "$line"

    # Default action is LOG if not specified
    ACTION=${ACTION:-LOG}

    # Construct the grep pattern, handling optional level
    GREP_PATTERN=""
    if [ -n "$LEVEL" ]; then
        # Basic syslog level matching (can be extended for more complex formats)
        GREP_PATTERN="^$LEVEL:"
    fi

    if [ -n "$PATTERN" ]; then
        if [ -n "$GREP_PATTERN" ]; then
            GREP_PATTERN="$GREP_PATTERN.*$PATTERN"
        else
            GREP_PATTERN="^.*$PATTERN"
        fi
    fi

    # If no pattern is specified, it means match all lines for the given level (or all if no level)
    if [ -z "$GREP_PATTERN" ] && [ -n "$LEVEL" ]; then
        GREP_PATTERN="^$LEVEL:"
    fi

    # Apply the filter to standard input
    # We use a subshell to process each rule independently
    ( 
        if [ -n "$GREP_PATTERN" ]; then
            grep -E "$GREP_PATTERN"
        else
            # If no GREP_PATTERN, it means we should process all lines for the specified level, or all lines if no level specified.
            # This case is tricky and might need refinement based on exact syslog format. For now, if no pattern, we assume it's a broad rule.
            # If only LEVEL is specified, we match lines starting with that level.
            if [ -n "$LEVEL" ]; then
                grep "^$LEVEL:"
            else
                # If neither LEVEL nor PATTERN, this rule is likely malformed or intended to match everything.
                # For safety, we'll assume it's an error or a no-op if no specific pattern.
                # A more robust solution would validate this.
                cat # Pass through all lines if no specific pattern and no level
            fi
        fi
    ) <&0 | while IFS= read -r msg || [[ -n "$msg" ]]; do
        case "$ACTION" in
            "DROP")
                # Do nothing, effectively dropping the message
                ;; 
            "ALERT")
                # Log the original message and send an alert
                alert_message "$LEVEL" "$msg"
                ;; 
            "LOG" | *)
                # Log the message with its original format
                echo "$msg"
                ;; 
        esac
    done

done < "$CONFIG_FILE"

exit 0
