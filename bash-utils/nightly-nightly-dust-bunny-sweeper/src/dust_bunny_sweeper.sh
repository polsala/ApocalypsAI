#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

DEFAULT_AGE_DAYS=30
DRY_RUN=false
AUTO_CONFIRM=false
TARGET_DIR="." # Default to current directory, can be changed by user

# --- Whimsical Messages ---
MSG_SCAN="Scanning for digital dust bunnies in '$TARGET_DIR'..."
MSG_FOUND="Found these fluffy bits of forgotten data:"
MSG_NO_BUNNIES="No digital dust bunnies found. Your system is sparkling clean (digitally speaking)!"
MSG_CONFIRM="Are you sure you want to sweep these away? (y/N): "
MSG_SWEEPING="Sweeping away the digital detritus..."
MSG_CLEAN="Your system is now sparkling clean (digitally speaking)!"
MSG_ABORT="Digital dust bunnies remain. Perhaps another sweep later?"

# --- Functions ---

usage() {
    echo "Usage: $0 [-d] [-a <days>] [-y] [<directory>]"
    echo "  -d : Dry run. Only list digital dust bunnies, do not delete."
    echo "  -a <days> : Specify the age in days for files to be considered dust bunnies (default: $DEFAULT_AGE_DAYS)."
    echo "  -y : Auto-confirm deletion without prompt (use with caution!)."
    echo "  <directory> : The directory to scan (default: current directory)."
    echo ""
    echo "This utility helps you find and sweep away old, unused files and empty directories."
}

find_old_files() {
    # Find files accessed more than $1 days ago
    find "$TARGET_DIR" -type f -atime +"$1" -print
}

find_empty_dirs() {
    # Find empty directories
    find "$TARGET_DIR" -type d -empty -print
}

# --- Main Logic ---

# Parse arguments
while getopts "da:y" opt; do
    case $opt in
        d) DRY_RUN=true ;;
        a) DEFAULT_AGE_DAYS="$OPTARG" ;;
        y) AUTO_CONFIRM=true ;;
        \?) usage; exit 1 ;;
    esac
done
shift $((OPTIND-1))

if [ -n "$1" ]; then
    TARGET_DIR="$1"
    if [ ! -d "$TARGET_DIR" ]; then
        echo "Error: Directory '$TARGET_DIR' not found." >&2
        exit 1
    fi
fi

echo "$MSG_SCAN"

OLD_FILES=$(find_old_files "$DEFAULT_AGE_DAYS")
EMPTY_DIRS=$(find_empty_dirs)

ALL_BUNNIES=""
if [ -n "$OLD_FILES" ]; then
    ALL_BUNNIES+="$OLD_FILES\n"
fi
if [ -n "$EMPTY_DIRS" ]; then
    ALL_BUNNIES+="$EMPTY_DIRS\n"
fi

if [ -z "$ALL_BUNNIES" ]; then
    echo "$MSG_NO_BUNNIES"
    exit 0
fi

echo "$MSG_FOUND"
echo -e "$ALL_BUNNIES" | sed '/^\s*$/d' # Remove potential empty lines

if "$DRY_RUN"; then
    echo "This was a dry run. No files were deleted."
    exit 0
fi

if ! "$AUTO_CONFIRM"; then
    read -p "$MSG_CONFIRM" CONFIRM
    if [[ ! "$CONFIRM" =~ ^[yY]$ ]]; then
        echo "$MSG_ABORT"
        exit 0
    fi
fi

echo "$MSG_SWEEPING"
# Delete old files
if [ -n "$OLD_FILES" ]; then
    echo -e "$OLD_FILES" | xargs -r rm -v
fi

# Delete empty directories (need to be careful with order, delete files first)
# Find empty directories again, as some might become empty after file deletion
EMPTY_DIRS_AFTER_FILE_CLEANUP=$(find "$TARGET_DIR" -type d -empty -print)
if [ -n "$EMPTY_DIRS_AFTER_FILE_CLEANUP" ]; then
    echo -e "$EMPTY_DIRS_AFTER_FILE_CLEANUP" | xargs -r rmdir -v
fi

echo "$MSG_CLEAN"
