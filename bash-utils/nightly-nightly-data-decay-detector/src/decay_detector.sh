#!/bin/bash

# Default values
TARGET_DIR="."
AGE_DAYS=90
QUARANTINE_MODE=0
QUARANTINE_DIR=""

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS] <target_directory>"
    echo "Detects and reports on files and directories older than a specified age."
    echo ""
    echo "Options:"
    echo "  -a, --age <days>       Minimum age in days for files/dirs to be considered 'decaying' (default: 90)"
    echo "  -q, --quarantine       Enable quarantine mode: move decaying items to a quarantine directory"
    echo "  -d, --quarantine-dir <path>  Directory to move quarantined items to (required with -q)"
    echo "  -h, --help             Display this help message"
    echo ""
    echo "Example: $0 -a 180 /var/log"
    echo "Example: $0 -q -d /tmp/quarantine /home/user/old_data"
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -a|--age)
            AGE_DAYS="$2"
            shift
            ;;
        -q|--quarantine)
            QUARANTINE_MODE=1
            ;;
        -d|--quarantine-dir)
            QUARANTINE_DIR="$2"
            shift
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "Error: Unknown option $1"
            usage
            ;;
        *)
            TARGET_DIR="$1"
            ;;
    esac
    shift
done

# Validate inputs
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist or is not a directory."
    exit 1
fi

if [[ "$QUARANTINE_MODE" -eq 1 && -z "$QUARANTINE_DIR" ]]; then
    echo "Error: Quarantine mode requires a quarantine directory (--quarantine-dir)."
    usage
fi

if [[ "$QUARANTINE_MODE" -eq 1 && ! -d "$QUARANTINE_DIR" ]]; then
    echo "Creating quarantine directory: $QUARANTINE_DIR"
    mkdir -p "$QUARANTINE_DIR" || { echo "Error: Could not create quarantine directory."; exit 1; }
fi

echo "Scanning '$TARGET_DIR' for items older than $AGE_DAYS days..."
echo "---"

# Find decaying items
# Using -print0 and xargs -0 for safe handling of filenames with spaces/special chars
# -maxdepth 1 -mindepth 1 ensures only direct children of TARGET_DIR are considered
DECAYING_ITEMS=$(find "$TARGET_DIR" -maxdepth 1 -mindepth 1 \( -type f -o -type d \) -mtime +"$AGE_DAYS" -print0)

if [[ -z "$DECAYING_ITEMS" ]]; then
    echo "No decaying items found in '$TARGET_DIR'."
else
    echo "Decaying items found:"
    echo "$DECAYING_ITEMS" | xargs -0 -I {} echo "  - {}"

    if [[ "$QUARANTINE_MODE" -eq 1 ]]; then
        echo "---"
        echo "Quarantining items to '$QUARANTINE_DIR'..."
        # Use -t for target directory to handle multiple arguments safely
        echo "$DECAYING_ITEMS" | xargs -0 mv -t "$QUARANTINE_DIR"
        echo "Quarantine complete."
    fi
fi

echo "---"
echo "Scan complete."
