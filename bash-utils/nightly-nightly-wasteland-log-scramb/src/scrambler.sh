#!/bin/bash

# Nightly-Nightly-Wasteland-Log-Scrambler

# Configuration for replacement words
REPLACEMENT_WORDS=(
    "Glimmer" "Echo" "Dust" "Whisper" "Rubble" "Scrap" "Anomaly" "Void"
    "Temporal Rift" "Quantum Quip" "Data Shard" "Memory Fragment" "Ghost Signal"
)

# Function to get a random replacement word
get_random_word() {
    local num_words=${#REPLACEMENT_WORDS[@]}
    local random_index=$(( RANDOM % num_words ))
    echo "${REPLACEMENT_WORDS[$random_index]}"
}

# Usage function
usage() {
    echo "Usage: $0 <input_file> [output_file]" >&2
    echo "Scrambles sensitive patterns in log files with whimsical wasteland jargon." >&2
    echo "" >&2
    echo "Arguments:" >&2
    echo "  <input_file>   Path to the log file to scramble." >&2
    echo "  [output_file]  Optional. Path to save the scrambled output. If not provided, prints to stdout." >&2
    echo "" >&2
    echo "Environment Variables (for patterns):" >&2
    echo "  SCRAMBLE_PATTERNS: Comma-separated list of regex patterns to scramble." >&2
    echo "                     Example: 'IP_ADDRESS_REGEX,EMAIL_REGEX'" >&2
    echo "                     Default patterns are used if not set." >&2
    echo "" >&2
    echo "Default Patterns (if SCRAMBLE_PATTERNS is not set):" >&2
    echo "  - IP Addresses (IPv4 & IPv6)" >&2
    echo "  - Email Addresses" >&2
    echo "  - Common UUID/GUID formats" >&2
    echo "  - Dates (YYYY-MM-DD, MM/DD/YYYY)" >&2
    echo "  - Timestamps (HH:MM:SS)" >&2
}

# Default patterns if SCRAMBLE_PATTERNS is not set
DEFAULT_PATTERNS=(
    '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' # IPv4
    '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b' # Email
    '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}' # UUID
    '\b\d{4}-\d{2}-\d{2}\b' # YYYY-MM-DD
    '\b\d{2}/\d{2}/\d{4}\b' # MM/DD/YYYY
    '\b\d{2}:\d{2}:\d{2}\b' # HH:MM:SS
)

# Main scrambling logic
scramble_file() {
    local input_file="$1"
    local output_target="$2" # Can be a file path or empty for stdout

    if [[ ! -f "$input_file" ]]; then
        echo "Error: Input file '$input_file' not found." >&2
        exit 1
    fi

    local patterns_to_use
    if [[ -n "$SCRAMBLE_PATTERNS" ]]; then
        IFS=',' read -r -a patterns_to_use <<< "$SCRAMBLE_PATTERNS"
    else
        patterns_to_use=("${DEFAULT_PATTERNS[@]}")
    fi

    local scrambled_content
    scrambled_content=$(cat "$input_file")

    for pattern in "${patterns_to_use[@]}"; do
        local replacement_word
        replacement_word=$(get_random_word)
        scrambled_content=$(echo "$scrambled_content" | sed -E "s/$pattern/$replacement_word/g")
    done

    if [[ -n "$output_target" ]]; then
        echo "$scrambled_content" > "$output_target"
    else
        echo "$scrambled_content"
    fi
}

# --- Script execution ---
if [[ "$#" -lt 1 || "$#" -gt 2 ]]; then
    usage
    exit 1
fi

scramble_file "$1" "$2"
