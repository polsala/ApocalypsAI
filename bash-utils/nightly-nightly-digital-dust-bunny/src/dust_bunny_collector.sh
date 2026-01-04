#!/bin/bash

# Nightly Digital Dust Bunny Collector
# Summary: A whimsical Bash utility to find and archive old, unused files, metaphorically sweeping digital dust bunnies into a void archive.

set -euo pipefail

# --- Configuration ---
TARGET_DIR=""
ARCHIVE_DIR=""
AGE_DAYS=""

# --- Functions ---

# Function to display usage information
usage() {
    echo "Usage: $(basename "$0") <target_directory> <archive_directory> <age_in_days>"
    echo ""
    echo "  <target_directory>: The directory to scan for old files."
    echo "  <archive_directory>: The directory where old files will be moved (the 'void archive')."
    echo "  <age_in_days>: Files older than this many days will be archived."
    echo ""
    echo "Example: $(basename "$0") /var/log /mnt/archive 90"
    exit 1
}

# Function to validate input
validate_input() {
    if [[ -z "$TARGET_DIR" || -z "$ARCHIVE_DIR" || -z "$AGE_DAYS" ]]; then
        echo "Error: All arguments are required." >&2
        usage
    fi

    if [[ ! -d "$TARGET_DIR" ]]; then
        echo "Error: Target directory '$TARGET_DIR' does not exist or is not a directory." >&2
        exit 1
    fi

    if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [[ "$AGE_DAYS" -lt 0 ]]; then
        echo "Error: Age in days must be a non-negative integer." >&2
        exit 1
    fi
}

# --- Main Script Logic ---

# Parse arguments
if [[ "$#" -ne 3 ]]; then
    usage
fi

# Use realpath for robust absolute path resolution
# Check if realpath is available, otherwise provide a warning or fallback
if ! command -v realpath &> /dev/null; then
    echo "Warning: 'realpath' command not found. Path resolution might be less robust." >&2
    # Fallback to a simpler absolute path resolution if realpath is not available
    TARGET_DIR="$(cd "$1" && pwd)"
    ARCHIVE_DIR="$(cd "$2" && pwd)"
else
    TARGET_DIR="$(realpath "$1")"
    ARCHIVE_DIR="$(realpath "$2")"
fi

AGE_DAYS="$3"

validate_input

# Ensure archive directory exists
mkdir -p "$ARCHIVE_DIR"

echo "Sweeping for digital dust bunnies in '$TARGET_DIR' (older than $AGE_DAYS days)..."
echo "Archiving to '$ARCHIVE_DIR'"
echo "--------------------------------------------------"

DUST_BUNNIES_FOUND=0

# Find files and process them
# Using -print0 and read -d '' for robust handling of filenames with spaces or special characters
while IFS= read -r -d '' FILE_PATH; do
    # Calculate relative path
    RELATIVE_PATH="${FILE_PATH#"$TARGET_DIR/"}"
    
    # Determine destination path in archive
    DEST_PATH="$ARCHIVE_DIR/$RELATIVE_PATH"
    DEST_DIR="$(dirname "$DEST_PATH")"

    # Create destination directory if it doesn't exist
    mkdir -p "$DEST_DIR"

    # Move the file
    if mv "$FILE_PATH" "$DEST_PATH"; then
        echo "  Moved: '$RELATIVE_PATH' -> '$DEST_PATH'"
        DUST_BUNNIES_FOUND=$((DUST_BUNNIES_FOUND + 1))
    else
        echo "  Error moving: '$RELATIVE_PATH'" >&2
    fi
done < <(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" -print0)

echo "--------------------------------------------------"
if [[ "$DUST_BUNNIES_FOUND" -eq 0 ]]; then
    echo "Your digital space is sparkling clean! No dust bunnies found."
else
    echo "Successfully swept $DUST_BUNNIES_FOUND digital dust bunnies into the void archive."
fi
