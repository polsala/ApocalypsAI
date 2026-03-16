#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

# Default values
DEFAULT_AGE_DAYS=7
DEFAULT_TARGET_DIR="/tmp" # Can be overridden by user or script logic

# Function to display help message
show_help() {
    echo "Usage: $0 [OPTIONS] [DIRECTORY]"
    echo ""
    echo "A whimsical Bash script to find and sweep away old, unused 'digital dust bunnies' (files)"
    echo "from specified directories."
    echo ""
    echo "Options:"
    echo "  -a, --age DAYS      Files older than DAYS will be considered dust bunnies (default: $DEFAULT_AGE_DAYS days)."
    echo "  -d, --delete        Delete the identified dust bunnies. USE WITH CAUTION!"
    echo "  -h, --help          Display this help message and exit."
    echo "  -v, --verbose       Show detailed output during operation."
    echo ""
    echo "Arguments:"
    echo "  DIRECTORY           The directory to scan for dust bunnies. If not specified,"
    echo "                      it defaults to common temporary directories like /tmp."
    echo "                      Multiple directories can be specified."
    echo ""
    echo "Example:"
    echo "  $0 -a 30 /var/log"
    echo "  $0 -d /tmp /var/cache"
}

# Parse arguments
AGE_DAYS=$DEFAULT_AGE_DAYS
DELETE_MODE=0
VERBOSE_MODE=0
TARGET_DIRS=()

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -a|--age)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo "Error: --age requires a numeric argument." >&2
                exit 1
            fi
            AGE_DAYS="$2"
            shift
            ;;
        -d|--delete)
            DELETE_MODE=1
            ;;
        -v|--verbose)
            VERBOSE_MODE=1
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "Error: Unknown option '$1'" >&2
            show_help
            exit 1
            ;;
        *)
            TARGET_DIRS+=("$1")
            ;;
    esac
    shift
done

# If no target directories specified, use default
if [ ${#TARGET_DIRS[@]} -eq 0 ]; then
    TARGET_DIRS=("$DEFAULT_TARGET_DIR")
fi

echo "--- Nightly Digital Dust Bunny Sweeper ---"
echo "Scanning for files older than $AGE_DAYS days."
if [ $DELETE_MODE -eq 1 ]; then
    echo "WARNING: Delete mode is ENABLED. Files will be permanently removed!"
else
    echo "Dry run mode: Files will be listed but NOT deleted. Use -d to delete."
fi
echo "------------------------------------------"

FOUND_BUNNIES=0
DELETED_BUNNIES=0

for DIR in "${TARGET_DIRS[@]}"; do
    if [ ! -d "$DIR" ]; then
        echo "Error: Directory '$DIR' does not exist or is not a directory. Skipping." >&2
        continue
    fi

    if [ $VERBOSE_MODE -eq 1 ]; then
        echo "Searching in: $DIR"
    fi

    # Find files older than AGE_DAYS
    # -type f: only regular files
    # -mtime +AGE_DAYS: modification time older than AGE_DAYS
    # -print0: null-terminated output for safety with filenames containing spaces/newlines
    
    # Use a subshell to capture output for listing
    if [ $DELETE_MODE -eq 0 ]; then
        echo "Dust bunnies found in '$DIR':"
        find "$DIR" -type f -mtime +"$AGE_DAYS" -print0 | while IFS= read -r -d $'\0' FILE; do
            echo "  - $FILE"
            FOUND_BUNNIES=$((FOUND_BUNNIES + 1))
        done
    else
        # In delete mode, find and delete
        find "$DIR" -type f -mtime +"$AGE_DAYS" -print0 | while IFS= read -r -d $'\0' FILE; do
            if [ $VERBOSE_MODE -eq 1 ]; then
                echo "Sweeping away: $FILE"
            fi
            rm -f "$FILE"
            if [ $? -eq 0 ]; then
                DELETED_BUNNIES=$((DELETED_BUNNIES + 1))
            else
                echo "Warning: Failed to sweep '$FILE'." >&2
            fi
            FOUND_BUNNIES=$((FOUND_BUNNIES + 1)) # Count even if deletion fails
        done
    fi
done

echo "------------------------------------------"
if [ $DELETE_MODE -eq 0 ]; then
    echo "Found $FOUND_BUNNIES digital dust bunnies."
    echo "To sweep them away, run with the -d or --delete option."
else
    echo "Swept away $DELETED_BUNNIES out of $FOUND_BUNNIES identified digital dust bunnies."
fi
echo "--- Sweeping complete! ---"

exit 0
