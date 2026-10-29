#!/bin/bash

# nightly-digital-dust-bunny-sweeper

# Default values
DEFAULT_AGE_DAYS=90
TARGET_DIR="."

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <age_in_days>]"
    echo "  -d <directory> : The directory to sweep for digital dust bunnies (default: current directory)."
    echo "  -a <age_in_days> : Files/directories older than this many days are considered dust bunnies (default: 90 days)."
    echo "  -h             : Display this help message."
    exit 1
}

# Parse command-line arguments
while getopts "d:a:h" opt; do
    case ${opt} in
        d ) TARGET_DIR=$OPTARG ;;
        a ) DEFAULT_AGE_DAYS=$OPTARG ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done

# Validate age
if ! [[ "$DEFAULT_AGE_DAYS" =~ ^[0-9]+$ ]]; then
    echo "Error: Age must be a positive integer."
    usage
fi

echo "Sweeping for digital dust bunnies in '$TARGET_DIR' older than $DEFAULT_AGE_DAYS days..."
echo "------------------------------------------------------------------"

# Find files and directories older than DEFAULT_AGE_DAYS
# -maxdepth 1 to only check immediate children, not recursively
# -mindepth 1 to exclude the TARGET_DIR itself
# -mtime +N means N+1 days old or more (e.g., +90 means 91 days or older)
# -print0 for null-separated output, safer for filenames with spaces/special chars
find "$TARGET_DIR" -maxdepth 1 -mindepth 1 -mtime +"$DEFAULT_AGE_DAYS" -print0 | while IFS= read -r -d $'\0' item; do
    if [ -f "$item" ]; then
        echo "  FILE: \"$item\" - A forgotten scroll, perhaps? Consider 'composting' (rm) or 'rehoming' (mv)."
    elif [ -d "$item" ]; then
        echo "  DIR:  \"$item\" - A dusty old lair! Consider 'composting' (rm -r) or 'reorganizing' (mv)."
    fi
done

echo "------------------------------------------------------------------"
echo "Sweep complete! Remember to handle your digital dust bunnies responsibly."
