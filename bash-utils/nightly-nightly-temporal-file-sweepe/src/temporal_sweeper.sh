#!/bin/bash

# Nightly Temporal File Sweeper - A whimsical guide to managing digital echoes.

# --- Configuration ---
ARCHIVE_DIR_NAME="chrono_vault" # Subdirectory name for archiving
# --- End Configuration ---

# Function to display usage information
usage() {
    echo "Usage: $0 <directory_to_scan> <age_in_days>"
    echo "  <directory_to_scan>: The path to the directory to scan for temporal echoes."
    echo "  <age_in_days>: The minimum age (in days) for a file to be considered a 'temporal echo'."
    exit 1
}

# Validate arguments
if [ "$#" -ne 2 ]; then
    usage
fi

SCAN_DIR="$1"
AGE_DAYS="$2"

# Check if directory exists
if [ ! -d "$SCAN_DIR" ]; then
    echo "Error: Directory '$SCAN_DIR' not found."
    exit 1
fi

# Check if age is a positive integer
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [ "$AGE_DAYS" -le 0 ]; then
    echo "Error: Age in days must be a positive integer."
    exit 1
fi

echo "🌌 Initiating Temporal Echo Scan in '$SCAN_DIR' for files older than $AGE_DAYS days..."
echo ""

# Find files older than AGE_DAYS
# Using -mtime +N means files modified N+1 days ago or more.
# For example, -mtime +30 finds files older than 30 days.
# -type f ensures only regular files are considered.
# -print0 is used for null-terminated output, safe for filenames with spaces/special chars.
find "$SCAN_DIR" -type f -mtime +"$AGE_DAYS" -print0 | while IFS= read -r -d $'\0' file; do
    # Get last modification date in YYYY-MM-DD format
    # Mock rationale: In a real scenario, 'stat' or 'date' would be used. For testing, we control file mtimes
    # and primarily verify file paths and suggested commands, not the exact date string.
    # This uses GNU stat, common on Linux. For BSD/macOS, 'stat -f %m' would be needed.
    LAST_MOD_DATE=$(stat -c %y "$file" 2>/dev/null | cut -d ' ' -f 1 || echo "Unknown Date")

    echo "⏳ Temporal Echo Detected: \"$file\" (Last modified: $LAST_MOD_DATE)"
    echo "   Suggested Fates:"
    echo "     1. Archive to the Chrono-Vault: mkdir -p \"$SCAN_DIR/$ARCHIVE_DIR_NAME\" && mv \"$file\" \"$SCAN_DIR/$ARCHIVE_DIR_NAME/\""
    echo "     2. Vanish into the Aether: rm \"$file\""
    echo "     3. Re-energize for the Present: touch \"$file\""
    echo ""
done

echo "✨ Temporal Echo Scan Complete! May your digital space be ever harmonious."
