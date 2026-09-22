#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# A whimsical utility to tidy up your digital space.

# Default values
DEFAULT_DAYS_OLD=90
TARGET_DIR="."
DRY_RUN=true
CLEAN_MODE=false

# --- Whimsical ASCII Art ---
echo "
  _   _           _ _       _   _ _ _
 | | | |         | | |     | | | (_) |
 | | | |_   _  __| | | __ _| | | |_| |_ ___ _ __
 | | | | | | |/ _\` | |/ _\` | | | | | __/ _ \\ '__|
 | |_| | |_| | (_| | | (_| | |_| | | ||  __/ |
  \\___/ \\__,_|\\__,_|_|\\__,_|\\___/|_|\\__\\___|_|

  Nightly Digital Dust Bunny Sweeper Activated!
  Searching for forgotten digital fluff...
"

# --- Helper Functions ---

show_help() {
    echo "Usage: $0 [OPTIONS] [DIRECTORY]"
    echo ""
    echo "A whimsical Bash script to find and report digital 'dust bunnies' (old, unused files and empty directories) on your system."
    echo ""
    echo "Options:"
    echo "  -d <days>   Files older than <days> will be considered dust bunnies (default: $DEFAULT_DAYS_OLD)."
    echo "  -c          Clean mode: actually delete found dust bunnies. USE WITH CAUTION!"
    echo "  -h          Show this help message."
    echo ""
    echo "Arguments:"
    echo "  DIRECTORY   The directory to scan (default: current directory '.')."
    echo ""
    echo "Example:"
    echo "  $0 -d 180 /var/log"
    echo "  $0 -c ~/Downloads"
    echo ""
    echo "Remember: Always backup important data before cleaning!"
}

# --- Main Logic ---

# Parse arguments
while getopts "d:ch" opt; do
    case ${opt} in
        d )
            if [[ "$OPTARG" =~ ^[0-9]+$ ]]; then
                DEFAULT_DAYS_OLD=$OPTARG
            else
                echo "Error: -d requires a positive integer for days." >&2
                exit 1
            fi
            ;;
        c )
            CLEAN_MODE=true
            DRY_RUN=false
            ;;
        h )
            show_help
            exit 0
            ;;
        \? )
            echo "Invalid option: -$OPTARG" >&2
            show_help
            exit 1
            ;;
    esac
done
shift $((OPTIND -1))

if [ -n "$1" ]; then
    TARGET_DIR="$1"
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist or is not a directory." >&2
    exit 1
fi

echo "Scanning '$TARGET_DIR' for digital dust bunnies older than $DEFAULT_DAYS_OLD days..."
echo "Mode: $(if $DRY_RUN; then echo "Dry Run (no changes)"; else echo "Cleaning (deleting files)"; fi)"
echo ""

# Find old files
echo "--- Old File Dust Bunnies ---"
OLD_FILES=$(find "$TARGET_DIR" -type f -mtime +$DEFAULT_DAYS_OLD \( -name "*.tmp" -o -name "*.log" -o -name "*.bak" -o -name "*.old" -o -name "*-old" -o -name "*.swp" -o -name "*.swo" -o -name "*.cache" \) 2>/dev/null)

if [ -z "$OLD_FILES" ]; then
    echo "  No ancient file dust bunnies found. Your files are spry!"
else
    echo "  Found these ancient file dust bunnies:"
    echo "$OLD_FILES" | while IFS= read -r file; do
        echo "    - $file"
        if ! $DRY_RUN; then
            rm -f "$file"
            if [ $? -eq 0 ]; then
                echo "      (Swept away: $file)"
            else
                echo "      (Failed to sweep: $file)" >&2
            fi
        fi
    done
fi
echo ""

# Find empty directories
echo "--- Empty Directory Dust Bunnies ---"
EMPTY_DIRS=$(find "$TARGET_DIR" -type d -empty -not -path "$TARGET_DIR" 2>/dev/null)

if [ -z "$EMPTY_DIRS" ]; then
    echo "  No lonely, empty directory dust bunnies found. All directories are bustling!"
else
    echo "  Found these empty directory dust bunnies:"
    echo "$EMPTY_DIRS" | while IFS= read -r dir; do
        echo "    - $dir"
        if ! $DRY_RUN; then
            rmdir "$dir" 2>/dev/null
            if [ $? -eq 0 ]; then
                echo "      (Swept away: $dir)"
            else
                echo "      (Failed to sweep: $dir - perhaps it's not truly empty or permissions issue)" >&2
            fi
        fi
    done
fi
echo ""

echo "Digital Dust Bunny Sweeper finished its rounds."
if $DRY_RUN; then
    echo "Run with '-c' to actually sweep them away!"
else
    echo "Your digital space is now a bit cleaner!"
fi
