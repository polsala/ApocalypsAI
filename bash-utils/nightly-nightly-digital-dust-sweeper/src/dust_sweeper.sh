#!/bin/bash

# Nightly Digital Dust Sweeper
# A whimsical bash script to unearth and report on old, forgotten files and directories.

# Default age for "digital dust bunnies" (in days)
DEFAULT_AGE_DAYS=90

# Function to display usage information
usage() {
    echo "Usage: $0 <path> [age_in_days]"
    echo "  <path>: The directory to start sweeping for digital dust."
    echo "  [age_in_days]: (Optional) Minimum age in days for files/directories to be considered 'dust bunnies'."
    echo "                 Defaults to $DEFAULT_AGE_DAYS days if not specified."
    echo ""
    echo "This script reports old files/directories; it does NOT delete anything."
    exit 1
}

# Check if at least one argument (path) is provided
if [ -z "$1" ]; then
    usage
fi

TARGET_PATH="$1"
AGE_DAYS="${2:-$DEFAULT_AGE_DAYS}" # Use default if second argument is not provided

# Validate TARGET_PATH
if [ ! -d "$TARGET_PATH" ]; then
    echo "Error: Target path '$TARGET_PATH' is not a valid directory."
    exit 1
fi

# Validate AGE_DAYS is a positive integer
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [ "$AGE_DAYS" -le 0 ]; then
    echo "Error: Age in days must be a positive integer."
    exit 1
fi

echo "Sweeping for digital dust bunnies in '$TARGET_PATH' older than $AGE_DAYS days..."
echo "--------------------------------------------------------------------------------"

# Use find to locate files and directories older than AGE_DAYS
# -mtime +N: File's data was last modified N*24 hours ago. (+N means > N days)
# -print0: Print the full file name on the standard output, followed by a null character.
# xargs -0: Read items from standard input, separated by null characters.
# stat -c: Display information based on the format string.
# %y: Last data modification time, human-readable.
# %n: File name.
# %F: File type.

# Find files and directories, then get their modification time and path
find "$TARGET_PATH" -depth -mindepth 1 \( -type f -o -type d \) -mtime +"$AGE_DAYS" -print0 | while IFS= read -r -d $'\0' item; do
    # Get modification timestamp (seconds since epoch)
    MOD_TIMESTAMP=$(stat -c %Y "$item")
    CURRENT_TIMESTAMP=$(date +%s)
    
    # Calculate age in days
    AGE_SECONDS=$((CURRENT_TIMESTAMP - MOD_TIMESTAMP))
    ITEM_AGE_DAYS=$((AGE_SECONDS / 86400)) # 86400 seconds in a day

    # Only report if it's actually older than the specified age (find's +N is > N days)
    if [ "$ITEM_AGE_DAYS" -gt "$AGE_DAYS" ]; then
        MOD_DATE=$(stat -c %y "$item" | cut -d' ' -f1) # Extract YYYY-MM-DD
        FILE_TYPE=$(stat -c %F "$item")
        echo "  [${ITEM_AGE_DAYS} days old] [${MOD_DATE}] [${FILE_TYPE}] ${item}"
    fi
done

echo "--------------------------------------------------------------------------------"
echo "Sweep complete. No digital dust bunnies were harmed (or deleted) in this process."
