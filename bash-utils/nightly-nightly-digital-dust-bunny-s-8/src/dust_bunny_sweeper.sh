#!/bin/bash

# Whimsical header
echo "✨ Welcome to the Nightly Digital Dust Bunny Sweeper! ✨"
echo "Preparing to banish forgotten bytes and tidy up your digital realm."

# Usage
if [[ "$#" -lt 2 || "$#" -gt 3 ]]; then
    echo "Usage: $0 <directory> <age_in_days> [--dry-run]"
    echo "  <directory>    : The path to scan for old files and empty directories."
    echo "  <age_in_days>  : Files and empty directories older than this many days will be considered 'dust bunnies'."
    echo "  --dry-run      : (Optional) Show what would be deleted without actually deleting anything."
    exit 1
fi

TARGET_DIR="$1"
AGE_DAYS="$2"
DRY_RUN=false

if [[ "$3" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "🔍 Initiating a dry-run scan. No files will be harmed... yet."
elif [[ -n "$3" ]]; then
    echo "Error: Unknown argument '$3'."
    echo "Usage: $0 <directory> <age_in_days> [--dry-run]"
    exit 1
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Directory '$TARGET_DIR' not found or is not a directory."
    exit 1
fi

echo "Scanning '$TARGET_DIR' for files and empty directories older than $AGE_DAYS days..."
echo "----------------------------------------------------------------"

# Find files older than AGE_DAYS
# -type f: only files
# -mtime +AGE_DAYS: modification time older than AGE_DAYS
# -print0: print with null terminator for safety with filenames containing spaces/newlines
OLD_FILES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" -print0)

# Find empty directories older than AGE_DAYS
# -type d: only directories
# -empty: only empty directories
# -mtime +AGE_DAYS: modification time older than AGE_DAYS
OLD_DIRS=$(find "$TARGET_DIR" -type d -empty -mtime +"$AGE_DAYS" -print0)

if [[ -z "$OLD_FILES" && -z "$OLD_DIRS" ]]; then
    echo "🎉 No digital dust bunnies found! Your realm is sparkling clean."
    exit 0
fi

echo "Found these ancient artifacts and forgotten corners:
"

if [[ -n "$OLD_FILES" ]]; then
    echo -e "Files to be swept away:\n"
    echo "$OLD_FILES" | xargs -0 -I {} echo "  - {}"
fi

if [[ -n "$OLD_DIRS" ]]; then
    echo -e "\nEmpty Directories to be tidied:\n"
    echo "$OLD_DIRS" | xargs -0 -I {} echo "  - {}"
fi
echo "----------------------------------------------------------------"

if "$DRY_RUN"; then
    echo "✨ Dry run complete. These items *would* have been swept away."
    exit 0
fi

read -p "🧹 Ready to sweep these away? (y/N): " -n 1 -r
echo
if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
    echo "Aborting sweep. The dust bunnies live to see another day... for now."
    exit 0
fi

echo "Sweeping away forgotten bytes..."
if [[ -n "$OLD_FILES" ]]; then
    echo "$OLD_FILES" | xargs -0 rm -v
fi
if [[ -n "$OLD_DIRS" ]]; then
    echo "$OLD_DIRS" | xargs -0 rmdir -v # rmdir only removes empty directories
fi

echo "✅ Digital dust bunnies banished! Your system feels lighter."
