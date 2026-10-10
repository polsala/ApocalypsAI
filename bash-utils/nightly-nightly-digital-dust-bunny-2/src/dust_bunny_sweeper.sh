#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# Scans specified directories for large, old, or duplicate files.

# Configuration
LARGE_FILE_THRESHOLD_MB=50 # Files larger than this will be reported
OLD_FILE_THRESHOLD_DAYS=180 # Files older than this will be reported

# --- Helper Functions ---

# Function to display help message
show_help() {
    echo "Nightly Digital Dust Bunny Sweeper"
    echo "Usage: $0 [OPTIONS] [DIRECTORY]"
    echo ""
    echo "Scans specified directories for large, old, or duplicate files (digital dust bunnies)."
    echo "Presents a report of files that can be reviewed for potential cleanup."
    echo ""
    echo "Options:"
    echo "  -s <MB>    Set large file threshold in MB (default: ${LARGE_FILE_THRESHOLD_MB}MB)"
    echo "  -o <DAYS>  Set old file threshold in days (default: ${OLD_FILE_THRESHOLD_DAYS} days)"
    echo "  -h         Display this help message"
    echo ""
    echo "Arguments:"
    echo "  DIRECTORY  The directory to scan (default: current directory)"
    echo ""
    echo "Example:"
    echo "  $0 /var/log"
    echo "  $0 -s 100 -o 365 ~/Downloads"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# --- Main Script Logic ---

# Parse arguments
while getopts "s:o:h" opt; do
    case ${opt} in
        s ) LARGE_FILE_THRESHOLD_MB=$OPTARG ;;
        o ) OLD_FILE_THRESHOLD_DAYS=$OPTARG ;;
        h ) show_help; exit 0 ;;
        \? ) echo "Invalid option: -$OPTARG" >&2; show_help; exit 1 ;;
    esac
done
shift $((OPTIND -1))

TARGET_DIR="${1:-.}" # Default to current directory if no argument provided

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' not found." >&2
    exit 1
fi

# Check for required commands
if ! command_exists find || ! command_exists du || ! command_exists md5sum || ! command_exists sort || ! command_exists uniq || ! command_exists stat || ! command_exists awk || ! command_exists cut || ! command_exists bc || ! command_exists date; then
    echo "Error: Required commands (find, du, md5sum, sort, uniq, stat, awk, cut, bc, date) not found." >&2
    echo "Please ensure they are installed and in your PATH." >&2
    exit 1
fi

echo "--- Nightly Digital Dust Bunny Sweeper Report ---"
echo "Scanning directory: $(realpath "$TARGET_DIR")"
echo "Large file threshold: ${LARGE_FILE_THRESHOLD_MB}MB"
echo "Old file threshold: ${OLD_FILE_THRESHOLD_DAYS} days"
echo "-------------------------------------------------"
echo ""

# 1. Find Large Files
echo "### Large Files (>${LARGE_FILE_THRESHOLD_MB}MB) ###"
LARGE_FILES_OUTPUT=$(find "$TARGET_DIR" -type f -size +${LARGE_FILE_THRESHOLD_MB}M -print0 | while IFS= read -r -d $'\0' file; do
    size_kb=$(du -k "$file" 2>/dev/null | awk '{print $1}')
    if [ -n "$size_kb" ]; then
        size_mb=$(echo "scale=2; $size_kb / 1024" | bc 2>/dev/null)
        echo "  - ${size_mb}MB: $file"
    fi
done)
if [ -z "$LARGE_FILES_OUTPUT" ]; then
    echo "  (No large files found)"
else
    echo "$LARGE_FILES_OUTPUT"
fi
echo ""

# 2. Find Old Files
echo "### Old Files (> ${OLD_FILE_THRESHOLD_DAYS} days) ###"
OLD_FILES_OUTPUT=$(find "$TARGET_DIR" -type f -mtime +${OLD_FILE_THRESHOLD_DAYS} -print0 | while IFS= read -r -d $'\0' file; do
    mod_time=""
    if command_exists gstat; then # GNU stat for consistent output if available (e.g., via Homebrew on macOS)
        mod_time=$(gstat -c %y "$file" 2>/dev/null | cut -d' ' -f1)
    elif [[ "$OSTYPE" == "darwin"* ]]; then # macOS stat
        mod_time=$(stat -f %m "$file" 2>/dev/null | xargs -I {} date -r {} +%Y-%m-%d)
    else # Linux stat
        mod_time=$(stat -c %y "$file" 2>/dev/null | cut -d' ' -f1)
    fi

    if [ -n "$mod_time" ]; then
        echo "  - Last Modified: ${mod_time}: $file"
    fi
done)
if [ -z "$OLD_FILES_OUTPUT" ]; then
    echo "  (No old files found)"
else
    echo "$OLD_FILES_OUTPUT"
fi
echo ""

# 3. Find Duplicate Files
echo "### Duplicate Files ###"
# Use a temporary file for md5sums to handle large number of files
TEMP_MD5_FILE=$(mktemp)
find "$TARGET_DIR" -type f -print0 | xargs -0 md5sum > "$TEMP_MD5_FILE" 2>/dev/null

# Find duplicate hashes
DUPLICATE_HASHES=$(awk '{print $1}' "$TEMP_MD5_FILE" | sort | uniq -d)

if [ -z "$DUPLICATE_HASHES" ]; then
    echo "  (No duplicate files found)"
else
    echo "$DUPLICATE_HASHES" | while IFS= read -r hash; do
        echo "  - Hash: $hash"
        grep "^$hash" "$TEMP_MD5_FILE" | awk '{$1=""; print "    " $0}'
    done
fi
rm -f "$TEMP_MD5_FILE" # Clean up temporary file
echo ""

echo "-------------------------------------------------"
echo "Scan complete. Review the report for potential digital decluttering."
