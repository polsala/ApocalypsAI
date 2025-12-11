#!/bin/bash

# Apoc Log Scrubber
# Cleanses log files of sensitive information with a touch of post-apocalyptic flair.

# --- Configuration ---

# Define sensitive data patterns and their replacements.
# Each entry is a bash associative array: "(" "pattern" "REGEX" "replacement" "REPLACEMENT_STRING"
REDACTION_PATTERNS=(
    "(" "pattern" "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" "replacement" "XXX.XXX.XXX.XXX"
    "(" "pattern" "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" "replacement" "[REDACTED_EMAIL]"
    # Add more patterns here, e.g., for API keys, passwords, etc.
    # "(" "pattern" "^API_KEY=[a-zA-Z0-9]+" "replacement" "API_KEY=[REDACTED]"
)

# --- Functions ---

# Function to display messages with a whimsical prefix
log_message() {
    local message="$1"
    echo "[ApocScrubber] $message"
}

# Function to apply redaction rules to a line
apply_redactions() {
    local line="$1"
    local original_line="$line"

    # Iterate through each defined redaction pattern
    for ((i=0; i<${#REDACTION_PATTERNS[@]}; i+=4)); do
        local pattern="${REDACTION_PATTERNS[i+1]}"
        local replacement="${REDACTION_PATTERNS[i+3]}"
        line=$(echo "$line" | sed "s/${pattern}/${replacement}/g")
    done

    echo "$line"
}

# --- Main Execution ---

# Check for input file
if [ -z "$1" ]; then
    log_message "Usage: $0 <input_log_file> [--dry-run]"
    exit 1
fi

INPUT_FILE="$1"
DRY_RUN="false"

# Check for dry-run flag
if [ "$2" == "--dry-run" ]; then
    DRY_RUN="true"
    log_message "Dry run mode enabled. No files will be modified."
fi

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    log_message "Error: Input file '$INPUT_FILE' not found."
    exit 1
fi

log_message "Initiating log scrubbing for '$INPUT_FILE'..."

# Create a temporary file for scrubbed content
TEMP_FILE=$(mktemp)

# Process the log file line by line
while IFS= read -r line || [[ -n "$line" ]]; do
    scrubbed_line=$(apply_redactions "$line")
    echo "$scrubbed_line" >> "$TEMP_FILE"
done < "$INPUT_FILE"

# If not in dry-run mode, overwrite the original file
if [ "$DRY_RUN" == "false" ]; then
    mv "$TEMP_FILE" "$INPUT_FILE"
    log_message "Log file '$INPUT_FILE' has been scrubbed successfully!"
else
    # In dry-run mode, print the scrubbed content to stdout
    cat "$TEMP_FILE"
    log_message "Dry run complete. Scrubbed content shown above."
    rm "$TEMP_FILE" # Clean up temp file in dry-run
fi

exit 0
