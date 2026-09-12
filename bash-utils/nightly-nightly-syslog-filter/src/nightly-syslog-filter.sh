#!/bin/bash

# Configuration Variables
# Patterns to include in the output. If empty, all lines are considered for exclusion.
INCLUDE_PATTERNS=()
# Patterns to exclude from the output.
EXCLUDE_PATTERNS=()
# Set to 'true' to add a timestamp to each output line.
ADD_TIMESTAMP="false"

# --- Script Logic ---

# Function to display help message
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Filters syslog messages based on include/exclude patterns."
    echo "Reads from stdin if no --log-file is specified."
    echo ""
    echo "Options:"
    echo "  --include PATTERN   Add a pattern to include log lines."
    echo "  --exclude PATTERN   Add a pattern to exclude log lines."
    echo "  --log-file FILE     Process messages from a specific file."
    echo "  --timestamp         Prepend a timestamp to each output line."
    echo "  -h, --help          Display this help message."
    echo ""
    echo "Configuration can also be set via environment variables or by editing the script."
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        --include)
        INCLUDE_PATTERNS+=("$2")
        shift # past argument
        shift # past value
        ;; 
        --exclude)
        EXCLUDE_PATTERNS+=("$2")
        shift # past argument
        shift # past value
        ;; 
        --log-file)
        LOG_FILE="$2"
        shift # past argument
        shift # past value
        ;; 
        --timestamp)
        ADD_TIMESTAMP="true"
        shift # past argument
        ;; 
        -h|--help)
        show_help
        exit 0
        ;; 
        *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;; 
    esac
done

# Determine input source
if [[ -n "$LOG_FILE" ]]; then
    if [[ ! -f "$LOG_FILE" ]]; then
        echo "Error: Log file '$LOG_FILE' not found." >&2
        exit 1
    fi
    INPUT_SOURCE="<("cat "$LOG_FILE")"
else
    INPUT_SOURCE="/dev/stdin"
fi

# Build the grep command for inclusion
INCLUDE_GREP_CMD=""
if [ ${#INCLUDE_PATTERNS[@]} -gt 0 ]; then
    INCLUDE_GREP_CMD="grep -E "
    first=true
    for pattern in "${INCLUDE_PATTERNS[@]}"; do
        if [ "$first" = true ]; then
            INCLUDE_GREP_CMD+="$pattern"
            first=false
        else
            INCLUDE_GREP_CMD+="|$pattern"
        fi
    done
fi

# Build the grep command for exclusion
EXCLUDE_GREP_CMD=""
if [ ${#EXCLUDE_PATTERNS[@]} -gt 0 ]; then
    EXCLUDE_GREP_CMD="grep -vE "
    first=true
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        if [ "$first" = true ]; then
            EXCLUDE_GREP_CMD+="$pattern"
            first=false
        else
            EXCLUDE_GREP_CMD+="|$pattern"
        fi
    done
fi

# Process the input

# If ADD_TIMESTAMP is true, we need to process line by line to add timestamps
if [[ "$ADD_TIMESTAMP" == "true" ]]; then
    while IFS= read -r line;
    do
        # Apply include filters first
        if [[ -n "$INCLUDE_GREP_CMD" ]]; then
            if ! echo "$line" | eval "$INCLUDE_GREP_CMD" > /dev/null 2>&1; then
                continue # Skip if it doesn't match include patterns
            fi
        fi

        # Apply exclude filters
        if [[ -n "$EXCLUDE_GREP_CMD" ]]; then
            if echo "$line" | eval "$EXCLUDE_GREP_CMD" > /dev/null 2>&1; then
                continue # Skip if it matches exclude patterns
            fi
        fi

        # If we reached here, the line passes filters. Add timestamp.
        echo "$(date '+%Y-%m-%d %H:%M:%S') - $line"
    done < $INPUT_SOURCE
else
    # No timestamping, use a pipeline for efficiency
    PIPELINE="cat $INPUT_SOURCE"

    if [[ -n "$INCLUDE_GREP_CMD" ]]; then
        PIPELINE+=" | eval "$INCLUDE_GREP_CMD""
    fi

    if [[ -n "$EXCLUDE_GREP_CMD" ]]; then
        PIPELINE+=" | eval "$EXCLUDE_GREP_CMD""
    fi

    eval "$PIPELINE"
fi
