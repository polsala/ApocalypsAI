#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# Whimsically sweeps away digital dust bunnies (old files) from a directory.

# Default values
AGE_THRESHOLD_DAYS=30
TARGET_DIR=""
DELETE_MODE=0
FORCE_DELETE=0

# Command for deletion. Mocked in tests.
RM_CMD="rm -v"

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS] <directory>"
    echo "Whimsically sweeps away digital dust bunnies (old files) from a directory."
    echo ""
    echo "Options:"
    echo "  -a, --age <days>    Files older than this many days will be considered dust bunnies. Default: ${AGE_THRESHOLD_DAYS}"
    echo "  -d, --delete        Delete the identified dust bunnies. USE WITH CAUTION!"
    echo "  -f, --force         Force deletion without confirmation (only with --delete)."
    echo "  -h, --help          Display this help message."
    echo ""
    echo "Example: $0 -a 60 /var/log"
    echo "Example: $0 --delete -f /tmp/old_cache"
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -a|--age)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo "Error: --age requires a numeric argument." >&2
                usage
            fi
            if ! [[ "$2" =~ ^[0-9]+$ ]]; then
                echo "Error: --age must be a positive integer." >&2
                usage
            fi
            AGE_THRESHOLD_DAYS="$2"
            shift
            ;;
        -d|--delete)
            DELETE_MODE=1
            ;;
        -f|--force)
            FORCE_DELETE=1
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "Error: Unknown option '$1'" >&2
            usage
            ;;
        *)
            if [[ -z "$TARGET_DIR" ]]; then
                TARGET_DIR="$1"
            else
                echo "Error: Multiple directories specified. Only one allowed." >&2
                usage
            fi
            ;;
    esac
    shift
done

# Validate target directory
if [[ -z "$TARGET_DIR" ]]; then
    echo "Error: No directory specified." >&2
    usage
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Directory '$TARGET_DIR' not found or is not a directory." >&2
    exit 1
fi

echo "Scanning for digital dust bunnies older than ${AGE_THRESHOLD_DAYS} days in: ${TARGET_DIR}"
echo "---------------------------------------------------------------------"

# Find files
# Using -type f to only target regular files, not directories
# Using -print0 and xargs -0 for safe handling of filenames with spaces/special chars
# -mtime +N means files whose data was last modified N*24 hours ago.
OLD_FILES_RAW=$(find "$TARGET_DIR" -type f -mtime +"$AGE_THRESHOLD_DAYS" -print0)

# Convert null-separated list to newline-separated for easier processing and display
# This also filters out empty results from find, preventing xargs from running on empty input
OLD_FILES=$(echo "$OLD_FILES_RAW" | xargs -0 -I {} echo "{}")

if [[ -z "$OLD_FILES" ]]; then
    echo "No digital dust bunnies found. Your digital space is sparkling clean!"
    exit 0
fi

echo "Found the following digital dust bunnies:"
echo "$OLD_FILES" | while IFS= read -r file; do
    echo "  - $file"
done

if [[ "$DELETE_MODE" -eq 1 ]]; then
    if [[ "$FORCE_DELETE" -eq 0 ]]; then
        read -p "Are you sure you want to sweep these dust bunnies into the void? (y/N): " CONFIRMATION
        if [[ ! "$CONFIRMATION" =~ ^[Yy]$ ]]; then
            echo "Sweep aborted. Digital dust bunnies live to see another day."
            exit 0
        fi
    fi

    echo "Sweeping away the digital dust bunnies..."
    # Use the RM_CMD variable, which can be mocked for testing
    echo "$OLD_FILES_RAW" | xargs -0 "$RM_CMD"
    echo "Digital dust bunnies swept away!"
else
    echo "To sweep these dust bunnies away, run with the --delete flag."
fi
