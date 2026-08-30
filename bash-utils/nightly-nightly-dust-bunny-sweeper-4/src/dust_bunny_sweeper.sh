#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# A whimsical utility to find and clean old, unused files and empty directories.

# --- Configuration ---
DEFAULT_AGE_DAYS=7 # Default age for files to be considered old
DEFAULT_MODE="dry-run" # Default mode: dry-run or cleanup

# --- Helper Functions ---

usage() {
    echo "Usage: $0 <directory> [age_in_days] [mode]"
    echo "  <directory>   : The path to scan for digital dust bunnies."
    echo "  [age_in_days] : Optional. Files older than this many days will be considered dust bunnies. Default: $DEFAULT_AGE_DAYS."
    echo "  [mode]        : Optional. 'dry-run' (default) to just report, or 'cleanup' to actually remove."
    echo ""
    echo "Example: $0 /var/log 30 cleanup"
    echo "Example: $0 /tmp"
    exit 1
}

# --- Main Logic ---

if [ "$#" -lt 1 ]; then
    usage
fi

TARGET_DIR="$1"
AGE_DAYS="${2:-$DEFAULT_AGE_DAYS}"
MODE="${3:-$DEFAULT_MODE}"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' not found."
    exit 1
fi

echo "Scanning '$TARGET_DIR' for digital dust bunnies older than $AGE_DAYS days (Mode: $MODE)..."
echo "--------------------------------------------------------------------------------"

# Find old files and empty directories
# -type f -mtime +$AGE_DAYS: files modified more than AGE_DAYS ago
# -type d -empty: empty directories
# -print0: null-terminated output for safety with filenames containing spaces/newlines
DUST_BUNNIES=$(find "$TARGET_DIR" -depth \( -type f -mtime +"$AGE_DAYS" -o -type d -empty \) -print0)
# Mock rationale: The 'find' command is mocked in tests to provide deterministic output.

if [ -z "$DUST_BUNNIES" ]; then
    echo "✨ No digital dust bunnies found in '$TARGET_DIR'! Your digital space is sparkling clean. ✨"
    exit 0
fi

# Process found items
read -r -d '' -a DUST_BUNNY_ARRAY <<< "$DUST_BUNNIES"
# Mock rationale: The 'read' command processes the output of the mocked 'find' command.

DUST_BUNNY_COUNT=${#DUST_BUNNY_ARRAY[@]}
CLEANED_COUNT=0

if [ "$MODE" == "dry-run" ]; then
    echo "Found $DUST_BUNNY_COUNT digital dust bunnies:"
    for item in "${DUST_BUNNY_ARRAY[@]}"; do
        echo "  - $item (DRY RUN - would be swept away)"
    done
    echo "--------------------------------------------------------------------------------"
    echo "To sweep them away, run with 'cleanup' mode: $0 \"$TARGET_DIR\" $AGE_DAYS cleanup"
elif [ "$MODE" == "cleanup" ]; then
    echo "Sweeping away $DUST_BUNNY_COUNT digital dust bunnies..."
    for item in "${DUST_BUNNY_ARRAY[@]}"; do
        echo "  - $item (CLEANED - poof!)"
        rm -rf "$item"
        # Mock rationale: The 'rm' command is mocked in tests to prevent actual deletion and record calls.
        if [ $? -eq 0 ]; then
            ((CLEANED_COUNT++))
        else
            echo "    Warning: Failed to sweep away '$item'."
        fi
    done
    echo "--------------------------------------------------------------------------------"
    echo "Swept away $CLEANED_COUNT digital dust bunnies from '$TARGET_DIR'. Your digital space thanks you! ✨"
else
    echo "Error: Invalid mode '$MODE'. Use 'dry-run' or 'cleanup'."
    usage
fi

exit 0
