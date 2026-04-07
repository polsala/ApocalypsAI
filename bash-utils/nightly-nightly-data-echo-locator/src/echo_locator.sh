#!/bin/bash
set -euo pipefail # Exit on error, unset variables, and pipefail

# Function to display usage
usage() {
    echo "Usage: $0 <directory>"
    echo "Detects 'temporal data echoes' (duplicate files) in the specified directory."
    echo "Reports groups of files with identical content."
    exit 1
}

# Check for directory argument
if [ -z "${1:-}" ]; then # Check if $1 is unset or empty
    usage
fi

TARGET_DIR="$1"

# Check if directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' not found." >&2 # Send error to stderr
    exit 1
fi

echo "Initiating Temporal Data Echo Scan in: $TARGET_DIR"
echo "--------------------------------------------------"

# Find all regular files, calculate their MD5 checksums, and sort them
# Then use 'uniq -w32 --all-repeated=separate' to show only duplicate lines
# Mock rationale: md5sum is a standard utility and its output for a given file is deterministic and offline.
# File system operations are deterministic within the isolated test environment.
find "$TARGET_DIR" -type f -print0 | xargs -0 md5sum | sort | uniq -w32 --all-repeated=separate
