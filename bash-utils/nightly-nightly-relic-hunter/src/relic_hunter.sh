#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 <path> [days_old]"
    echo "Hunts down old, forgotten files and directories, presenting them as digital relics."
    echo "  <path>     : The directory to start hunting from."
    echo "  [days_old] : Optional. Files/directories older than this many days will be considered relics. Default is 90 days."
    echo ""
    echo "Example: $0 /var/log 180"
    echo "         $0 ~/Downloads"
    exit 1
}

# Check for required arguments
if [ -z "$1" ]; then
    usage
fi

TARGET_PATH="$1"
DAYS_OLD="${2:-90}" # Default to 90 days if not provided

# Validate TARGET_PATH
if [ ! -d "$TARGET_PATH" ]; then
    echo "Error: Path '$TARGET_PATH' is not a valid directory."
    exit 1
fi

# Validate DAYS_OLD is a positive integer
if ! [[ "$DAYS_OLD" =~ ^[0-9]+$ ]] || [ "$DAYS_OLD" -le 0 ]; then
    echo "Error: Days old must be a positive integer."
    exit 1
fi

echo "---\\ Nightly Relic Hunter Report /---"
echo "Hunting for digital relics older than $DAYS_OLD days in: $TARGET_PATH"
echo "-----------------------------------"

# Use find to locate files and directories older than DAYS_OLD
# -mtime +N: files modified N*24 hours ago. +N means more than N days.
# -print0: prints full file name on stdout, followed by a null character. Safer for filenames with spaces.
# while IFS= read -r -d $'\0': reads null-separated items safely.
# stat -c %Y: prints last modification time in seconds since epoch (GNU stat).
# date +%s: prints current date in seconds since epoch (GNU date).
# date -d @<seconds>: converts seconds since epoch to human readable (GNU date).

# Find files and directories up to maxdepth 5
find "$TARGET_PATH" -maxdepth 5 \( -type f -o -type d \) -mtime +"$DAYS_OLD" -print0 | while IFS= read -r -d $'\0' relic; do
    # Get last modification timestamp in seconds
    MOD_TIMESTAMP=$(stat -c %Y "$relic")
    CURRENT_TIMESTAMP=$(date +%s)

    # Calculate age in days
    AGE_SECONDS=$((CURRENT_TIMESTAMP - MOD_TIMESTAMP))
    AGE_DAYS=$((AGE_SECONDS / 86400)) # 86400 seconds in a day

    # Format output
    printf "  [Relic Found] Age: %-4s days | Last Modified: %-20s | Path: %s\\n" "$AGE_DAYS" "$(date -d "@$MOD_TIMESTAMP" +"%Y-%m-%d %H:%M:%S")" "$relic"
done

echo "-----------------------------------"
echo "Relic hunt complete. No action taken, just reporting."
echo "Consider archiving or deleting these digital relics if they are no longer needed."
