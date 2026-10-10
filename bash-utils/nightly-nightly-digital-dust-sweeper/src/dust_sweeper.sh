#!/bin/bash

# Default values
TARGET_DIR="."
AGE_DAYS=7
DRY_RUN=false
CONFIRM=true

# Function to display help message
show_help() {
    echo "Nightly Digital Dust Bunny Sweeper"
    echo "Usage: $0 [OPTIONS] [PATH]"
    echo ""
    echo "Identifies and optionally cleans up old, forgotten files and empty directories (digital dust bunnies)."
    echo ""
    echo "Options:"
    echo "  -a, --age <days>    Files older than <days> will be considered dust bunnies (default: 7 days)."
    echo "  -n, --dry-run       Show what would be swept, but don't actually sweep anything."
    echo "  -y, --yes           Skip confirmation prompt and sweep automatically."
    echo "  -h, --help          Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 /var/log"
    echo "  $0 -a 30 /tmp"
    echo "  $0 -n -a 14 ."
    echo "  $0 -y /home/user/downloads"
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -a|--age)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo "Error: --age requires a number of days." >&2
                exit 1
            fi
            AGE_DAYS="$2"
            shift
            ;;
        -n|--dry-run)
            DRY_RUN=true
            ;;
        -y|--yes)
            CONFIRM=false
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
            TARGET_DIR="$1"
            ;;
    esac
    shift
done

# Validate AGE_DAYS
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]]; then
    echo "Error: Age must be a positive integer." >&2
    exit 1
fi

echo "--- Nightly Digital Dust Bunny Sweeper ---"
echo "Scanning for digital dust bunnies in: '$TARGET_DIR'"
echo "Looking for files/directories older than: $AGE_DAYS days"
echo ""

# Find old files and empty directories
# Using -atime for access time, -mtime for modification time. -atime is generally better for "unused".
# For empty directories, find -type d -empty is used.
# Exclude the target directory itself from deletion if it's empty.
DUST_BUNNIES=$(find "$TARGET_DIR" -depth \( \
    -type f -atime +"$AGE_DAYS" -o \
    -type d -empty -atime +"$AGE_DAYS" \
\) -print 2>/dev/null | grep -v "^$TARGET_DIR$") # Exclude the target directory itself

if [ -z "$DUST_BUNNIES" ]; then
    echo "No digital dust bunnies found! Your digital space is sparkling clean."
    exit 0
fi

echo "Found the following digital dust bunnies:"
echo "$DUST_BUNNIES"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "This was a dry run. No files were swept away."
    exit 0
fi

if [ "$CONFIRM" = true ]; then
    read -p "Ready to sweep these dust bunnies into the digital void? (y/N): " -n 1 -r
    echo ""
    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
        echo "Phew! Digital dust bunnies spared for another cycle. They'll be back."
        exit 0
    fi
fi

echo "Sweeping away digital dust bunnies..."
# Use xargs to handle spaces in filenames correctly
echo "$DUST_BUNNIES" | xargs -r rm -rf

if [ $? -eq 0 ]; then
    echo "Digital dust bunnies successfully swept! Your system breathes a little easier."
else
    echo "Uh oh! Some dust bunnies resisted the sweep. Manual intervention might be needed."
    exit 1
fi
