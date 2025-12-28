#!/bin/bash

# Default values
TARGET_DIR="."
AGE_DAYS=30
ACTION="report" # report, re-energize, archive
ARCHIVE_DIR=""

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <age_days>] [-x <action>] [-o <archive_output_dir>] [-h]"
    echo "  -d <directory>        : Target directory to scan (default: current directory)"
    echo "  -a <age_days>         : Files older than this many days (default: 30)"
    echo "  -x <action>           : Action to perform: 'report', 're-energize', 'archive' (default: report)"
    echo "  -o <archive_output_dir> : Directory to move archived files to (required for 'archive' action)"
    echo "  -h                    : Display this help message"
    echo ""
    echo "Whimsical-yet-useful: Hunt down digital dust bunnies!"
    exit 1
}

# Parse arguments
while getopts "d:a:x:o:h" opt; do
    case ${opt} in
        d ) TARGET_DIR=$OPTARG ;;
        a ) AGE_DAYS=$OPTARG ;;
        x ) ACTION=$OPTARG ;;
        o ) ARCHIVE_DIR=$OPTARG ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done
shift $((OPTIND -1))

# Validate arguments
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist." >&2
    exit 1
fi

if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || (( AGE_DAYS < 0 )); then
    echo "Error: Age days must be a non-negative integer." >&2
    exit 1
fi

case "$ACTION" in
    "report" | "re-energize" )
        # No special checks for these actions
        ;;
    "archive" )
        if [[ -z "$ARCHIVE_DIR" ]]; then
            echo "Error: Archive directory (-o) is required for 'archive' action." >&2
            exit 1
        fi
        if [[ ! -d "$ARCHIVE_DIR" ]]; then
            echo "Creating archive directory: $ARCHIVE_DIR"
            # Mock rationale: In tests, `mkdir` will be a mocked function.
            mkdir -p "$ARCHIVE_DIR" || { echo "Error: Could not create archive directory '$ARCHIVE_DIR'." >&2; exit 1; }
        fi
        ;;
    * )
        echo "Error: Invalid action '$ACTION'. Must be 'report', 're-energize', or 'archive'." >&2
        usage
        ;;
esac

echo "Scanning '$TARGET_DIR' for digital dust bunnies older than $AGE_DAYS days..."

# Find files
# Mock rationale: In tests, `find` will be a mocked function.
# We use -maxdepth 1 to only consider files directly in the target directory, not subdirectories.
FOUND_FILES=$(find "$TARGET_DIR" -maxdepth 1 -type f -mtime +"$AGE_DAYS" 2>/dev/null)

if [[ -z "$FOUND_FILES" ]]; then
    echo "No digital dust bunnies found. Your digital space is sparkling clean!"
    exit 0
fi

echo "Found the following digital dust bunnies:"
echo "$FOUND_FILES" | while IFS= read -r file; do
    case "$ACTION" in
        "report" )
            echo "  - $file (ready for inspection)"
            ;;
        "re-energize" )
            # Mock rationale: In tests, `touch` will be a mocked function.
            touch "$file"
            echo "  - $file (re-energized, timestamp updated!)"
            ;;
        "archive" )
            # Mock rationale: In tests, `mv` will be a mocked function.
            mv "$file" "$ARCHIVE_DIR/"
            echo "  - $file (archived to the void: $ARCHIVE_DIR)"
            ;;
    esac
done

echo "Digital dust bunny hunt complete!"
