#!/bin/bash

# Default values
TARGET_DIR="."
AGE_DAYS=30
ACTION="list" # or "delete"

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <age_in_days>] [-c <action>]"
    echo "  -d <directory> : Target directory to scan (default: current directory)"
    echo "  -a <age_in_days> : Files older than this many days will be considered 'dust bunnies' (default: 30)"
    echo "  -c <action>    : Action to perform: 'list' (default) or 'delete'"
    echo "                   'list': Show what would be cleaned."
    echo "                   'delete': Actually remove the identified items."
    echo ""
    echo "Example: $0 -d /var/log -a 90 -c list"
    exit 1
}

# Parse command-line arguments
while getopts "d:a:c:h" opt; do
    case ${opt} in
        d ) TARGET_DIR=$OPTARG ;;
        a ) AGE_DAYS=$OPTARG ;;
        c ) ACTION=$OPTARG ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist."
    exit 1
fi

echo "ApocalypsAI Digital Dust Bunny Sweeper Initiated!"
echo "Scanning '$TARGET_DIR' for temporal detritus older than $AGE_DAYS days..."
echo "Action: $ACTION"
echo "---"

# Find old files
echo "Searching for stale temporal fragments (files older than $AGE_DAYS days):"
OLD_FILES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" 2>/dev/null)
if [[ -z "$OLD_FILES" ]]; then
    echo "  No ancient digital lint found."
else
    echo "$OLD_FILES" | while IFS= read -r file;
    do
        echo "  - File: $file"
        if [[ "$ACTION" == "delete" ]]; then
            rm -f "$file"
            if [[ $? -eq 0 ]]; then
                echo "    [SWEEPED] $file"
            else
                echo "    [FAILED TO SWEEP] $file"
            fi
        fi
    done
fi

echo "---"

# Find empty directories
echo "Searching for abandoned temporal chambers (empty directories):"
EMPTY_DIRS=$(find "$TARGET_DIR" -type d -empty 2>/dev/null)
# Filter out the target directory itself if it's empty and was passed as "."
# This prevents the script from trying to remove the root of its operation if it becomes empty.
if [[ "$TARGET_DIR" == "." ]]; then
    EMPTY_DIRS=$(echo "$EMPTY_DIRS" | grep -v "^.$|^./$")
fi

if [[ -z "$EMPTY_DIRS" ]]; then
    echo "  No vacant digital spaces detected."
else
    echo "$EMPTY_DIRS" | while IFS= read -r dir;
    do
        echo "  - Directory: $dir"
        if [[ "$ACTION" == "delete" ]]; then
            rmdir "$dir" 2>/dev/null # rmdir only removes empty directories
            if [[ $? -eq 0 ]]; then
                echo "    [SWEEPED] $dir"
            else
                echo "    [FAILED TO SWEEP] $dir (might not be empty anymore or permissions issue)"
            fi
        fi
    done
fi

echo "---"
echo "Digital Dust Bunny Sweeper complete. Your temporal landscape is a bit tidier!"
exit 0
