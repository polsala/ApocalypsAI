#!/bin/bash

# Default values
TARGET_DIR="."
AGE_DAYS=90
ACTION="list" # or "move"
ARCHIVE_DIR=""

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <days>] [-m <archive_directory>] [-h]"
    echo "       -d <directory>   : Directory to forage (default: current directory)"
    echo "       -a <days>        : Files older than this many days (default: 90)"
    echo "       -m <archive_dir> : Move forgotten files to this directory instead of just listing them"
    echo "       -h               : Display this help message"
    exit 1
}

# Parse arguments
while getopts "d:a:m:h" opt; do
    case ${opt} in
        d ) TARGET_DIR=$OPTARG ;;
        a ) AGE_DAYS=$OPTARG ;;
        m ) ACTION="move"; ARCHIVE_DIR=$OPTARG ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done

# Validate archive directory if move action is chosen
if [[ "$ACTION" == "move" ]]; then
    if [[ -z "$ARCHIVE_DIR" ]]; then
        echo "Error: Archive directory must be specified with -m option."
        usage
    fi
    if [[ ! -d "$ARCHIVE_DIR" ]]; then
        echo "Creating archive directory: $ARCHIVE_DIR"
        mkdir -p "$ARCHIVE_DIR" || { echo "Error: Could not create archive directory."; exit 1; }
    fi
fi

echo "--- Nightly Forgotten File Forager ---"
echo "Scanning '$TARGET_DIR' for files older than $AGE_DAYS days..."

# Find forgotten files
# Mock rationale: The 'find' command is a standard system utility. For tests, we will
# create a controlled temporary filesystem with files of known modification times
# to ensure deterministic output without relying on the actual system's file state.
FORGOTTEN_FILES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" 2>/dev/null)

if [[ -z "$FORGOTTEN_FILES" ]]; then
    echo "No forgotten digital relics found. Your digital garden is pristine!"
else
    echo "Found these forgotten digital relics:"
    echo "$FORGOTTEN_FILES"

    if [[ "$ACTION" == "move" ]]; then
        echo "Moving them to the digital archive: '$ARCHIVE_DIR'..."
        while IFS= read -r file; do
            # Mock rationale: The 'mv' command is a standard system utility. For tests,
            # we will verify the presence of files in the archive directory and their
            # absence from the original location, ensuring deterministic behavior.
            mv "$file" "$ARCHIVE_DIR/" || echo "Warning: Could not move '$file'."
        done <<< "$FORGOTTEN_FILES"
        echo "Relics archived. May they rest in peace (or be rediscovered later)."
    else
        echo "To move these relics to an archive, run with '-m <archive_directory>'."
    fi
fi
