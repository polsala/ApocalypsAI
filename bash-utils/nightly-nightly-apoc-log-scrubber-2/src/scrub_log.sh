#!/bin/bash

# Apoc Log Scrubber
# A whimsical yet practical bash utility designed to help you clean up your log files by intelligently scrubbing sensitive information.

# Default patterns for common sensitive data
DEFAULT_PATTERNS=(
    "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"  # IP Addresses
    "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" # Email Addresses
    "[A-Za-z0-9+/]{40,}" # Generic API Keys (base64-like, 40+ chars)
    "\b(password|secret|token|apikey|auth_key)\b[:=]\s*['"]?[^'"]*['"]?" # Common sensitive keywords followed by values
)

# Function to display help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS] <log_file>"
    echo ""
    echo "A whimsical yet practical bash utility designed to help you clean up your log files by intelligently scrubbing sensitive information."
    echo ""
    echo "Options:"
    echo "  -d, --dry-run       Perform a dry run, showing what would be scrubbed without modifying the file."
    echo "  -i, --in-place      Modify the log file in place. Use with caution!"
    echo "  -p <pattern_file>, --pattern-file <pattern_file> Specify a custom file containing additional regex patterns to scrub."
    echo "  -h, --help          Display this help message."
    echo ""
    echo "Example:"
    echo "  $(basename "$0") -i /var/log/apoc_system.log"
    echo "  $(basename "$0") --dry-run -p custom_patterns.txt /var/log/apoc_system.log"
}

# Initialize variables
DRY_RUN=false
IN_PLACE=false
CUSTOM_PATTERNS_FILE=""

# Parse command-line options
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        -d|--dry-run)
            DRY_RUN=true
            shift # past argument
            ;;
        -i|--in-place)
            IN_PLACE=true
            shift # past argument
            ;;
        -p|--pattern-file)
            CUSTOM_PATTERNS_FILE="$2"
            shift # past argument
            shift # past value
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            # Assume the last argument is the log file
            LOG_FILE="$1"
            shift # past argument
            ;;
    esac
done

# Validate log file
if [ -z "$LOG_FILE" ]; then
    echo "Error: Log file not specified."
    show_help
    exit 1
fi

if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file '$LOG_FILE' not found."
    exit 1
fi

# Combine default and custom patterns
ALL_PATTERNS=("${DEFAULT_PATTERNS[@]}")
if [ -n "$CUSTOM_PATTERNS_FILE" ]; then
    if [ ! -f "$CUSTOM_PATTERNS_FILE" ]; then
        echo "Error: Custom patterns file '$CUSTOM_PATTERNS_FILE' not found."
        exit 1
    fi
    # Read custom patterns, ignoring comments and empty lines
    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ -n "$line" && ! "$line" =~ ^# ]]; then
            ALL_PATTERNS+=("$line")
        fi
d    done < "$CUSTOM_PATTERNS_FILE"
fi

# Construct the sed command
SED_COMMAND="s/"

# Escape special characters for sed's s command (basic escaping)
# This is a simplified approach; a more robust solution might involve a loop or more complex regex handling.
# For now, we'll focus on common characters that might break sed.
escape_sed_pattern() {
    local pattern="$1"
    pattern=$(echo "$pattern" | sed 's/[&/\\\]/\\&/g') # Escape &, /, \, \
    echo "$pattern"
}

# Build the sed expression for each pattern
first_pattern=true
for pattern in "${ALL_PATTERNS[@]}"; do
    escaped_pattern=$(escape_sed_pattern "$pattern")
    if [ "$first_pattern" = true ]; then
        SED_COMMAND+="${escaped_pattern}"
        first_pattern=false
    else
        SED_COMMAND+="|${escaped_pattern}"
    fi
done

SED_COMMAND+="/REDACTED/g"

# Execute the scrubbing
if [ "$IN_PLACE" = true ]; then
    if [ "$DRY_RUN" = true ]; then
        echo "Warning: Dry run with in-place modification is redundant. Proceeding with in-place modification."
    fi
    # Use a temporary file for in-place editing to avoid data loss if sed fails mid-way
    TMP_FILE=$(mktemp)
    if sed "$SED_COMMAND" "$LOG_FILE" > "$TMP_FILE"; then
        mv "$TMP_FILE" "$LOG_FILE"
        echo "Successfully scrubbed '$LOG_FILE' in place."
    else
        echo "Error: Failed to scrub '$LOG_FILE'. Temporary file '$TMP_FILE' may contain partial results."
        rm -f "$TMP_FILE"
        exit 1
    fi
elif [ "$DRY_RUN" = true ]; then
    echo "--- Dry Run: Scrubbing Preview ---"
    sed "$SED_COMMAND" "$LOG_FILE"
    echo "-----------------------------------"
    echo "No changes were made to '$LOG_FILE'."
else
    # Default behavior: print to stdout
    sed "$SED_COMMAND" "$LOG_FILE"
fi

exit 0
