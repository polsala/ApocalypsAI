#!/bin/bash

# Default values
TARGET_DIR="."
AGE_THRESHOLD_DAYS=90
COMPOST_DIR="./digital_compost_heap"
DRY_RUN=true

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "A whimsical script to find and suggest cleaning up digital 'dust bunnies' (old files and empty directories)."
    echo ""
    echo "Options:"
    echo "  -d, --directory <path>    Target directory to scan (default: current directory)"
    echo "  -a, --age <days>          Files older than this many days are considered dust bunnies (default: 90)"
    echo "  -c, --compost <path>      Directory to move dust bunnies to when sweeping (default: ./digital_compost_heap)"
    echo "  -s, --sweep               Actually move files to the compost heap (DANGER! Default: dry run)"
    echo "  -h, --help                Display this help message"
    echo ""
    echo "Example: $0 --directory /var/log --age 180 --sweep"
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d|--directory) TARGET_DIR="$2"; shift ;;
        -a|--age) AGE_THRESHOLD_DAYS="$2"; shift ;;
        -c|--compost) COMPOST_DIR="$2"; shift ;;
        -s|--sweep) DRY_RUN=false ;;
        -h|--help) usage ;;
        *) echo "Unknown parameter: $1"; usage ;;
    esac
    shift
done

# Validate target directory
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist."
    exit 1
fi

echo "--- Digital Dust Bunny Sweeper ---"
echo "Scanning: '$TARGET_DIR'"
echo "Looking for files older than: $AGE_THRESHOLD_DAYS days"

if $DRY_RUN; then
    echo "Mode: Dry Run (no changes will be made)"
else
    echo "Mode: SWEEPING! Dust bunnies will be moved to '$COMPOST_DIR'"
    mkdir -p "$COMPOST_DIR" || { echo "Error: Could not create compost directory '$COMPOST_DIR'"; exit 1; }
fi
echo "----------------------------------"
echo ""

# Find old files
echo "Searching for ancient scrolls (files older than $AGE_THRESHOLD_DAYS days):"
OLD_FILES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_THRESHOLD_DAYS" -print)
if [ -z "$OLD_FILES" ]; then
    echo "  No ancient scrolls found. Your digital library is pristine!"
else
    echo "$OLD_FILES" | while IFS= read -r file;
    do
        echo "  Found: $file"
        if ! $DRY_RUN; then
            # Ensure the target directory for mv exists in compost_dir
            RELATIVE_PATH="${file#$TARGET_DIR/}"
            COMPOST_TARGET_DIR="$(dirname "$COMPOST_DIR/$RELATIVE_PATH")"
            mkdir -p "$COMPOST_TARGET_DIR"
            mv "$file" "$COMPOST_TARGET_DIR/"
            echo "    Moved to: $COMPOST_TARGET_DIR/"
        fi
    done
fi
echo ""

# Find empty directories
echo "Searching for forgotten chambers (empty directories):"
EMPTY_DIRS=$(find "$TARGET_DIR" -mindepth 1 -type d -empty -print)
if [ -z "$EMPTY_DIRS" ]; then
    echo "  No forgotten chambers found. All spaces are bustling!"
else
    echo "$EMPTY_DIRS" | while IFS= read -r dir;
    do
        # Exclude the compost directory itself if it's within the target
        if [[ "$dir" == "$COMPOST_DIR"* ]]; then
            continue
        fi
        echo "  Found: $dir"
        if ! $DRY_RUN; then
            rmdir "$dir" 2>/dev/null # rmdir only removes empty directories
            if [ $? -eq 0 ]; then
                echo "    Sealed (removed) forgotten chamber: $dir"
            else
                echo "    Failed to seal (remove) $dir (might not be empty anymore or permissions issue)."
            fi
        fi
    done
fi
echo ""

echo "--- Sweeping complete! ---"
