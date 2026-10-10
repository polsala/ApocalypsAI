#!/bin/bash

# wasteland_sweeper.sh

# Default values
DRY_RUN=false
AGE_DAYS=7
TARGET_PATH=""

# Function to display usage
usage() {
    echo "Usage: $0 <path> [age_in_days] [--dry-run]"
    echo "  <path>        : The directory to sweep for old files and empty folders."
    echo "  [age_in_days] : Optional. Files older than this many days will be targeted. Default is 7 days."
    echo "  --dry-run     : Optional. Simulate the cleanup without actually deleting anything."
    exit 1
}

# Parse arguments
if [[ "$#" -lt 1 ]]; then
    usage
fi

TARGET_PATH="$1"
shift

if [[ ! -d "$TARGET_PATH" ]]; then
    echo "Error: Path '$TARGET_PATH' does not exist or is not a directory." >&2
    exit 1
fi

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            if [[ "$1" =~ ^[0-9]+$ ]]; then
                AGE_DAYS="$1"
                shift
            else
                echo "Error: Unknown argument '$1'." >&2
                usage
            fi
            ;;
    esac
done

echo "--- Wasteland Sweeper Report ---"
echo "Target Path: $TARGET_PATH"
echo "Age Threshold: $AGE_DAYS days"
echo "Mode: $(if $DRY_RUN; then echo "Dry Run"; else echo "Live Cleanup"; fi)"
echo "--------------------------------"

# Find old files
echo ""
echo "Scanning for old files (older than $AGE_DAYS days):"
OLD_FILES=$(find "$TARGET_PATH" -type f -mtime +"$AGE_DAYS" 2>/dev/null)

if [[ -z "$OLD_FILES" ]]; then
    echo "  No old files found."
else
    echo "$OLD_FILES" | while IFS= read -r file; do
        echo "  [FILE] $file"
    done
    if $DRY_RUN; then
        echo "  (Dry run: Files listed above would be removed.)"
    else
        echo ""
        read -p "Proceed with deleting these files? (y/N): " CONFIRMATION
        if [[ "$CONFIRMATION" =~ ^[yY]$ ]]; then
            echo "$OLD_FILES" | xargs -r rm -v
            echo "  Old files removed."
        else
            echo "  File deletion skipped."
        fi
    fi
fi

# Find empty directories
echo ""
echo "Scanning for empty directories:"
EMPTY_DIRS=$(find "$TARGET_PATH" -type d -empty 2>/dev/null)

if [[ -z "$EMPTY_DIRS" ]]; then
    echo "  No empty directories found."
else
    # Filter out the target path itself if it's empty
    EMPTY_DIRS=$(echo "$EMPTY_DIRS" | grep -v "^$TARGET_PATH$")
    if [[ -z "$EMPTY_DIRS" ]]; then
        echo "  No empty directories found (excluding target path itself)."
    else
        echo "$EMPTY_DIRS" | while IFS= read -r dir; do
            echo "  [DIR] $dir"
        done
        if $DRY_RUN; then
            echo "  (Dry run: Directories listed above would be removed.)"
        else
            echo ""
            read -p "Proceed with deleting these empty directories? (y/N): " CONFIRMATION
            if [[ "$CONFIRMATION" =~ ^[yY]$ ]]; then
                # Use tac to delete from deepest to shallowest to avoid issues
                echo "$EMPTY_DIRS" | tac | xargs -r rm -rv
                echo "  Empty directories removed."
            else
                echo "  Empty directory deletion skipped."
            fi
        fi
    fi
fi

echo ""
echo "--- Sweeper complete. ---"
exit 0
