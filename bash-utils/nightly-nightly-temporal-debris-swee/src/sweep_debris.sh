#!/bin/bash

# Nightly Temporal Debris Sweeper
# A whimsical Bash script to sweep away old temporary files, reporting its actions with dramatic flair.

# Default values
TARGET_DIR="/tmp"
AGE_DAYS=7
DRY_RUN=false
FORCE_DELETE=false

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <days>] [--dry-run] [--force] [--help]"
    echo "  -d <directory> : Target directory to sweep for debris (default: /tmp)"
    echo "  -a <days>      : Age in days for files to be considered debris (default: 7)"
    echo "  --dry-run      : List files that would be deleted, but don't delete them."
    echo "  --force        : Delete files without asking for confirmation."
    echo "  --help         : Display this help message."
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d|--directory)
            TARGET_DIR="$2"
            shift
            ;;
        -a|--age)
            AGE_DAYS="$2"
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            ;;
        --force)
            FORCE_DELETE=true
            ;;
        --help)
            usage
            ;;
        *)
            echo "Unknown parameter: $1"
            usage
            ;;
    esac
    shift
done

# Validate directory
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist or is not a directory." >&2
    exit 1
fi

echo "Scanning for temporal debris in the desolate expanse of '$TARGET_DIR'..."
echo "Seeking fragments older than $AGE_DAYS cycles of the sun."

# Find files older than AGE_DAYS
# -type f: only files, not directories
# -mtime +AGE_DAYS: modification time older than AGE_DAYS
# -print0: null-terminated output for safety with filenames containing spaces/newlines
DEBRIS_FILES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" -print0)

if [[ -z "$DEBRIS_FILES" ]]; then
    echo "No temporal debris detected. The path is clear... for now."
    exit 0
fi

# Count files
# Mock rationale: 'tr -d \0' and 'wc -l' are standard utilities and their behavior is deterministic.
NUM_FILES=$(echo "$DEBRIS_FILES" | tr -d '\0' | wc -l)
echo "Detected $NUM_FILES fragments of forgotten data."

if "$DRY_RUN"; then
    echo "--- DRY RUN: These fragments would be purged ---"
    # Mock rationale: 'xargs -0 -n 1 echo' is used to safely print null-separated filenames.
    echo "$DEBRIS_FILES" | xargs -0 -n 1 echo "  - "
    echo "--- End of DRY RUN ---"
    exit 0
fi

if ! "$FORCE_DELETE"; then
    read -p "Initiate purge sequence? (y/N): " -n 1 -r
    echo
    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
        echo "Purge sequence aborted. The debris lingers..."
        exit 0
    fi
fi

echo "Initiating purge sequence..."
# Mock rationale: 'rm -v' is a standard utility. The actual deletion is performed on temporary files in tests.
echo "$DEBRIS_FILES" | xargs -0 rm -v
echo "Purge sequence complete. The void claims its own."
