#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# Identifies old, potentially unused files in specified directories.

DEFAULT_DAYS=90
RECURSIVE=0
LIST_ONLY=0
TARGET_DIR=""

# Function to display help message
show_help() {
    echo "Usage: $0 [OPTIONS] <directory>"
    echo ""
    echo "Identifies old, potentially unused files (digital dust bunnies) in specified directories."
    echo ""
    echo "Options:"
    echo "  -d <days>   Specify the age threshold in days. Files older than this will be considered."
    echo "              Default: ${DEFAULT_DAYS} days."
    echo "  -r          Enable recursive scanning of subdirectories."
    echo "  -l          List only the file paths, without additional details (age, size)."
    echo "  -h          Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 -d 180 -r ~/my_bunker_logs"
    echo "  $0 -l ."
}

# Parse command-line arguments
while getopts "d:rlh" opt; do
    case ${opt} in
        d )
            if [[ ${OPTARG} =~ ^[0-9]+$ ]]; then
                DEFAULT_DAYS=${OPTARG}
            else
                echo "Error: -d requires a positive integer for days." >&2
                exit 1
            fi
            ;;
        r )
            RECURSIVE=1
            ;;
        l )
            LIST_ONLY=1
            ;;
        h )
            show_help
            exit 0
            ;;
        \? )
            echo "Invalid option: -${OPTOPT}" >&2
            show_help
            exit 1
            ;;
    esac
done
shift $((OPTIND -1))

TARGET_DIR="$1"

if [ -z "$TARGET_DIR" ]; then
    echo "Error: No directory specified." >&2
    show_help
    exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist or is not a directory." >&2
    exit 1
fi

echo "Scanning '$TARGET_DIR' for digital dust bunnies older than ${DEFAULT_DAYS} days..."
echo "-----------------------------------------------------------------"

FIND_CMD="find \"$TARGET_DIR\" -type f -mtime +${DEFAULT_DAYS}"

if [ "$RECURSIVE" -eq 0 ]; then
    FIND_CMD="find \"$TARGET_DIR\" -maxdepth 1 -type f -mtime +${DEFAULT_DAYS}"
fi

# Execute find and process results
eval "$FIND_CMD" | while IFS= read -r file; do
    if [ -f "$file" ]; then # Double check if it's a file
        if [ "$LIST_ONLY" -eq 1 ]; then
            echo "$file"
        else
            # Get modification time in seconds since epoch
            MOD_TIME_EPOCH=$(stat -c %Y "$file")
            CURRENT_TIME_EPOCH=$(date +%s)
            
            # Calculate age in days
            AGE_SECONDS=$((CURRENT_TIME_EPOCH - MOD_TIME_EPOCH))
            AGE_DAYS=$((AGE_SECONDS / 86400)) # 86400 seconds in a day

            # Get file size
            FILE_SIZE=$(du -h "$file" | awk '{print $1}')

            echo "  - $(basename "$file") (Path: $file, Age: ${AGE_DAYS} days, Size: ${FILE_SIZE})"
        fi
    fi
done

echo "-----------------------------------------------------------------"
echo "Scan complete. Time to sweep!"
