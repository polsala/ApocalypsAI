#!/bin/bash

# Default values
TARGET_PATH="."
DAYS_OLD=90
REPORT_TYPE="summary" # Can be 'summary' or 'detailed'

# Function to display usage
usage() {
    echo "Usage: $0 [-p <path>] [-d <days>] [-t <type>] [-h]"
    echo "  -p <path>   : Target directory to scan (default: .)"
    echo "  -d <days>   : Files/directories not modified for this many days (default: 90)"
    echo "  -t <type>   : Report type: 'summary' or 'detailed' (default: summary)"
    echo "                'summary' shows counts per category."
    echo "                'detailed' lists all decayed items."
    echo "  -h          : Display this help message."
    exit 1
}

# Parse arguments
while getopts "p:d:t:h" opt; do
    case ${opt} in
        p ) TARGET_PATH=$OPTARG ;;
        d ) DAYS_OLD=$OPTARG ;;
        t ) REPORT_TYPE=$OPTARG ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done

# Validate DAYS_OLD
if ! [[ "$DAYS_OLD" =~ ^[0-9]+$ ]] || [ "$DAYS_OLD" -le 0 ]; then
    echo "Error: Days must be a positive integer." >&2
    usage
fi

# Validate REPORT_TYPE
if [[ "$REPORT_TYPE" != "summary" && "$REPORT_TYPE" != "detailed" ]]; then
    echo "Error: Report type must be 'summary' or 'detailed'." >&2
    usage
fi

# Check if target path exists and is a directory
if [ ! -d "$TARGET_PATH" ]; then
    echo "Error: Target path '$TARGET_PATH' does not exist or is not a directory." >&2
    exit 1
fi

echo "--- Digital Decay Detector Report ---"
echo "Scanning: $TARGET_PATH"
echo "Threshold: $DAYS_OLD days of inactivity"
echo "Report Type: $REPORT_TYPE"
echo "-------------------------------------"

# Find files and directories that haven't been modified in DAYS_OLD days
# Using -mtime for modification time. -mtime +N means modification time is N*24 hours ago or more.
# -print0 and xargs -0 for robust handling of filenames with spaces/special characters.

# Find files
DECAYED_FILES=$(find "$TARGET_PATH" -type f -mtime +"$DAYS_OLD" -print0)
FILE_COUNT=$(echo "$DECAYED_FILES" | grep -zc .)

# Find directories
DECAYED_DIRS=$(find "$TARGET_PATH" -type d -mtime +"$DAYS_OLD" -print0)
DIR_COUNT=$(echo "$DECAYED_DIRS" | grep -zc .)

if [ "$FILE_COUNT" -eq 0 ] && [ "$DIR_COUNT" -eq 0 ]; then
    echo "\nNo significant digital decay detected. Your system is spick and span!"
else
    echo "\n--- Decay Analysis ---"
    if [ "$FILE_COUNT" -gt 0 ]; then
        echo "Files showing signs of 'Forgotten Tomes' ($FILE_COUNT found):"
        if [ "$REPORT_TYPE" = "detailed" ]; then
            echo "$DECAYED_FILES" | xargs -0 -n 1 echo "  - "
        fi
    fi

    if [ "$DIR_COUNT" -gt 0 ]; then
        echo "Directories resembling 'Ancient Relics' ($DIR_COUNT found):"
        if [ "$REPORT_TYPE" = "detailed" ]; then
            echo "$DECAYED_DIRS" | xargs -0 -n 1 echo "  - "
        fi
    fi

    echo "\nTotal 'Digital Decay' items: $((FILE_COUNT + DIR_COUNT))"
    echo "Consider archiving or cleansing these forgotten fragments of the past."
fi

echo "-------------------------------------"
