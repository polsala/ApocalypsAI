#!/bin/bash
set -euo pipefail

# Nightly Digital Dust Bunny Sweeper
# Identifies and optionally cleans up old, forgotten files and empty directories.

# Default values
TARGET_DIR="."
AGE_DAYS=30
ACTION="report" # or "delete"

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <age_days>] [-c <action>]"
    echo "  -d <directory> : The directory to scan (default: current directory)"
    echo "  -a <age_days>  : Files older than this many days will be considered 'dust bunnies' (default: 30)"
    echo "  -c <action>    : 'report' (default) to list findings, 'delete' to remove them"
    echo ""
    echo "Example: $0 -d /var/log -a 7 -c report"
    exit 1
}

# Parse command-line arguments
while getopts "d:a:c:h" opt; do
    case ${opt} in
        d ) TARGET_DIR=$OPTARG ;;
        a ) AGE_DAYS=$OPTARG ;;
        c ) ACTION=$OPTARG ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done
shift $((OPTIND -1))

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Directory '$TARGET_DIR' not found." >&2
    exit 1
fi

echo "Scanning '$TARGET_DIR' for digital dust bunnies (files older than $AGE_DAYS days and empty directories)..."

# Find old files
echo -e "\n--- Ancient Data Fragments (Files older than $AGE_DAYS days) ---"
OLD_FILES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" -print)
if [[ -z "$OLD_FILES" ]]; then
    echo "No ancient data fragments found. Your digital space is surprisingly tidy!"
else
    echo "$OLD_FILES"
    if [[ "$ACTION" == "delete" ]]; then
        echo -e "\nInitiating sweep protocol for ancient data fragments..."
        # Use a loop for safer deletion, handling filenames with spaces/special chars
        while IFS= read -r file; do
            echo "Deleting file: $file"
            rm -f "$file"
        done <<< "$OLD_FILES"
        echo "Ancient data fragments swept away!"
    fi
fi

# Find empty directories
echo -e "\n--- Echoing Voids (Empty Directories) ---"
EMPTY_DIRS=$(find "$TARGET_DIR" -type d -empty -print | grep -v "^$TARGET_DIR$") # Exclude the target dir itself if it becomes empty
if [[ -z "$EMPTY_DIRS" ]]; then
    echo "No echoing voids found. All directories contain purpose!"
else
    echo "$EMPTY_DIRS"
    if [[ "$ACTION" == "delete" ]]; then
        echo -e "\nInitiating sweep protocol for echoing voids..."
        # Use a loop for safer deletion, handling filenames with spaces/special chars
        # Sort in reverse order to delete deepest directories first
        while IFS= read -r dir; do
            echo "Deleting empty directory: $dir"
            rmdir "$dir" || true # `|| true` to prevent script from exiting if rmdir fails (e.g., dir not empty anymore)
        done <<< "$(echo "$EMPTY_DIRS" | sort -r)"
        echo "Echoing voids collapsed!"
    fi
fi

echo -e "\nDigital dust bunny sweep complete."
