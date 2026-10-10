#!/bin/bash

# Default values
SEARCH_PATH="."
AGE_DAYS=30
SEARCH_TYPE="f" # Default to files

# Function to display usage
usage() {
    echo "Usage: $0 [-p <path>] [-a <age_days>] [-t <type>] [-h]"
    echo "  -p <path>      : Directory to search (default: current directory)"
    echo "  -a <age_days>  : Minimum age in days (default: 30 days)"
    echo "  -t <type>      : Type of digital dust bunny to hunt ('f' for files, 'd' for directories, 'a' for all - default: f)"
    echo "  -h             : Display this help message"
    echo ""
    echo "Hunts down and reports files or directories that haven't been modified in a specified number of days, like digital dust bunnies."
    exit 1
}

# Parse arguments
while getopts "p:a:t:h" opt; do
    case ${opt} in
        p ) SEARCH_PATH=$OPTARG ;;
        a ) AGE_DAYS=$OPTARG ;;
        t ) SEARCH_TYPE=$OPTARG ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done

# Validate age
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]]; then
    echo "Error: Age must be a positive integer." >&2
    usage
fi

# Validate search type
case "$SEARCH_TYPE" in
    f|d|a) ;;
    *) echo "Error: Invalid search type. Use 'f' for files, 'd' for directories, or 'a' for all." >&2
       usage ;;
esac

echo "--- Digital Dust Bunny Hunt Initiated! ---"
echo "Searching for forgotten digital relics older than $AGE_DAYS days in: $SEARCH_PATH"
echo "Targeting: $(case "$SEARCH_TYPE" in f) echo "Files" ;; d) echo "Directories" ;; a) echo "Files and Directories" ;; esac)"
echo "-----------------------------------------"

FIND_ARGS=()

# find -mtime +N means N+1 days or older. So +$AGE_DAYS means older than AGE_DAYS days.
FIND_ARGS+=("-mtime" "+$AGE_DAYS")

case "$SEARCH_TYPE" in
    f) FIND_ARGS+=("-type" "f") ;;
    d) FIND_ARGS+=("-type" "d") ;;
    a) ;;
esac

# Execute find command
# Mock rationale: The 'find' command is not mocked directly. Instead, the test script
# creates a controlled temporary filesystem with files/directories having specific,
# deterministic modification times. This allows the actual 'find' command to run
# against a known state, ensuring deterministic test results without complex mocking.
find "$SEARCH_PATH" "${FIND_ARGS[@]}" -print0 | while IFS= read -r -d $'\0' file; do
    # Check if file still exists (might be removed by another process in a real-world scenario)
    if [ -e "$file" ]; then
        echo "  * Found a dusty relic: $file"
    fi
done

echo "-----------------------------------------"
echo "Digital Dust Bunny Hunt Complete! May your storage be ever clean."
