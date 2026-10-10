#!/bin/bash

# Nightly Digital Garden Weeder

# Default values
TARGET_PATH="."
MAX_AGE_DAYS=30
DRY_RUN=false
AUTO_CONFIRM=false

# Whimsical messages
MSG_START="🌿 Initiating Digital Garden Weeding Protocol..."
MSG_DRY_RUN="🔍 Performing a dry run. No actual changes will be made."
MSG_NO_WEEDS="✨ Your digital garden is already pristine! No withered leaves or empty plots found."
MSG_FOUND_FILES="🍂 Found these ancient digital weeds (files older than ${MAX_AGE_DAYS} days):"
MSG_FOUND_DIRS="🗑️ Found these desolate empty plots (directories):"
MSG_CONFIRM="❓ Proceed with recycling these withered data leaves and reclaiming empty plots? (y/N): "
MSG_DELETING="🧹 Recycling withered data leaves and reclaiming empty plots..."
MSG_COMPLETE="✅ Digital Garden Weeding complete! Your digital garden is now flourishing."
MSG_CANCELLED="❌ Weeding cancelled. Your digital garden remains as is."
MSG_ERROR="🚨 A thorny issue encountered during weeding."

# Function to display help message
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "A whimsical Bash script to prune old, unused files and empty directories,"
    echo "keeping your digital garden tidy."
    echo ""
    echo "Options:"
    echo "  -p, --path <path>    Specify the root path of your digital garden (default: .)"
    echo "  -a, --age <days>     Files older than this many days will be considered weeds (default: 30)"
    echo "  -d, --dry-run        Perform a dry run without making any changes."
    echo "  -y, --confirm        Automatically confirm deletion without prompt."
    echo "  -h, --help           Display this help message."
    echo ""
    echo "Example:"
    echo "  $0 --path /var/log --age 7 --dry-run"
    echo "  $0 -p ~/Downloads -a 90 -y"
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -p|--path)
            TARGET_PATH="$2"
            shift
            ;;
        -a|--age)
            MAX_AGE_DAYS="$2"
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            ;;
        -y|--confirm)
            AUTO_CONFIRM=true
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
    shift
done

echo "$MSG_START"
if "$DRY_RUN"; then
    echo "$MSG_DRY_RUN"
fi

# Find old files
echo "$MSG_FOUND_FILES"
OLD_FILES=$(find "$TARGET_PATH" -type f -mtime +"$MAX_AGE_DAYS" -print 2>/dev/null)
if [ -z "$OLD_FILES" ]; then
    echo "  (None found)"
fi
echo -e "$OLD_FILES"

# Find empty directories
echo "$MSG_FOUND_DIRS"
EMPTY_DIRS=$(find "$TARGET_PATH" -type d -empty -not -path "$TARGET_PATH" -print 2>/dev/null)
if [ -z "$EMPTY_DIRS" ]; then
    echo "  (None found)"
fi
echo -e "$EMPTY_DIRS"

# Combine candidates
CANDIDATES=""
if [ -n "$OLD_FILES" ]; then
    CANDIDATES+="$OLD_FILES\n"
fi
if [ -n "$EMPTY_DIRS" ]; then
    CANDIDATES+="$EMPTY_DIRS\n"
fi

# Remove blank lines from CANDIDATES for a more accurate check
CLEAN_CANDIDATES=$(echo -e "$CANDIDATES" | sed '/^\s*$/d')

if [ -z "$CLEAN_CANDIDATES" ]; then
    echo "$MSG_NO_WEEDS"
    exit 0
fi

if "$DRY_RUN"; then
    echo "$MSG_COMPLETE (Dry Run)"
    exit 0
fi

if ! "$AUTO_CONFIRM"; then
    read -p "$MSG_CONFIRM" -n 1 -r
    echo "" # Newline after read -n 1
    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
        echo "$MSG_CANCELLED"
        exit 1
    fi
fi

echo "$MSG_DELETING"

# Delete old files
DELETE_FILES_SUCCESS=0
if [ -n "$OLD_FILES" ]; then
    echo -e "$OLD_FILES" | grep -v '^\s*$' | xargs -r rm -v 2>/dev/null || \
        echo -e "$OLD_FILES" | grep -v '^\s*$' | while IFS= read -r file; do
            [ -n "$file" ] && rm -v "$file" 2>/dev/null
        done
    if [ $? -ne 0 ]; then
        DELETE_FILES_SUCCESS=1
    fi
fi

# Delete empty directories (re-run find as deleting files might make some dirs empty)
DELETE_DIRS_SUCCESS=0
NEWLY_EMPTY_DIRS=$(find "$TARGET_PATH" -type d -empty -not -path "$TARGET_PATH" -print 2>/dev/null)
if [ -n "$NEWLY_EMPTY_DIRS" ]; then
    echo -e "$NEWLY_EMPTY_DIRS" | sort -r | xargs -r rm -rv 2>/dev/null || \
        echo -e "$NEWLY_EMPTY_DIRS" | sort -r | while IFS= read -r dir; do
            [ -n "$dir" ] && rm -rv "$dir" 2>/dev/null
        done
    if [ $? -ne 0 ]; then
        DELETE_DIRS_SUCCESS=1
    fi
fi

if [ "$DELETE_FILES_SUCCESS" -eq 0 ] && [ "$DELETE_DIRS_SUCCESS" -eq 0 ]; then
    echo "$MSG_COMPLETE"
    exit 0
else
    echo "$MSG_ERROR"
    exit 1
fi
