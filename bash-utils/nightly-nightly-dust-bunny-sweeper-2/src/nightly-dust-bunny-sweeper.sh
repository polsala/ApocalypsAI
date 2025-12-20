#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

# Default values
TARGET_DIR=""
CLEAN_MODE=0
AGE_DAYS=30 # Files older than 30 days

# Function to display usage
usage() {
    echo "Usage: $0 -d <directory> [--clean] [--age <days>]"
    echo "  -d <directory> : The directory to sweep for digital dust bunnies."
    echo "  --clean        : Enable cleaning mode (deletes old files and empty directories)."
    echo "  --age <days>   : Files older than this many days will be considered 'dust bunnies'. Default is 30."
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d)
            TARGET_DIR="$2"
            shift
            ;;
        --clean)
            CLEN_MODE=1
            ;;
        --age)
            AGE_DAYS="$2"
            shift
            ;;
        *)
            usage
            ;;
    esac
    shift
done

if [ -z "$TARGET_DIR" ]; then
    echo "Error: Target directory must be specified."
    usage
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist."
    exit 1
fi

echo "📑 Initiating Nightly Digital Dust Bunny Sweep in '$TARGET_DIR' (files older than $AGE_DAYS days)..."
echo "--------------------------------------------------------------------------------"

# Find old files
echo "🔍 Searching for ancient scrolls (files older than $AGE_DAYS days):"
OLD_FILES=$(find "$TARGET_DIR" -type f -mtime +$AGE_DAYS -print)
if [ -z "$OLD_FILES" ]; then
    echo "  No ancient scrolls found. Your digital library is pristine!"
else
    echo "$OLD_FILES" | while IFS= read -r file; do
        echo "  - File: $file"
    done
    if [ "$CLEAN_MODE" -eq 1 ]; then
        echo "🗑️ Sweeping away ancient scrolls..."
        echo "$OLD_FILES" | xargs -r rm -v
        echo "  Ancient scrolls swept!"
    else
        echo "  (Run with --clean to sweep these ancient scrolls away.)"
    fi
fi

echo ""

# Find empty directories
echo "🔍 Searching for forgotten chambers (empty directories):"
EMPTY_DIRS=$(find "$TARGET_DIR" -type d -empty -print)
# Filter out the target directory itself if it becomes empty
EMPTY_DIRS=$(echo "$EMPTY_DIRS" | grep -v "^$TARGET_DIR$")

if [ -z "$EMPTY_DIRS" ]; then
    echo "  No forgotten chambers found. All spaces are bustling!"
else
    echo "$EMPTY_DIRS" | while IFS= read -r dir; do
        echo "  - Directory: $dir"
    done
    if [ "$CLEAN_MODE" -eq 1 ]; then
        echo "🗑️ Sealing forgotten chambers..."
        # Use tac to delete from deepest to shallowest
        echo "$EMPTY_DIRS" | tac | xargs -r rmdir -v
        echo "  Forgotten chambers sealed!"
    else
        echo "  (Run with --clean to seal these forgotten chambers.)"
    fi
fi

echo "--------------------------------------------------------------------------------"
echo "✨ Nightly Digital Dust Bunny Sweep complete!"
