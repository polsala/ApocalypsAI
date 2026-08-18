#!/bin/bash

# Nightly Temporal Cache Sweeper

# Default age for "ancient" files (in days)
DEFAULT_AGE_DAYS=7

# Function to display usage
usage() {
    echo "Usage: $0 <directory> [age_in_days] [--sweep]"
    echo "  <directory>    : The directory to scan for ancient files."
    echo "  [age_in_days]  : Optional. Files older than this will be considered ancient. Default: ${DEFAULT_AGE_DAYS} days."
    echo "  --sweep        : Optional. If present, ancient files will be deleted. Otherwise, they are just listed."
    echo ""
    echo "Example: $0 /tmp 30"
    echo "Example: $0 ~/.cache --sweep"
    exit 1
}

# Parse arguments
TARGET_DIR=""
AGE_DAYS=${DEFAULT_AGE_DAYS}
SWEEP_MODE=0

if [[ "$#" -lt 1 ]]; then
    usage
fi

TARGET_DIR="$1"
shift

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --sweep)
            SWEEP_MODE=1
            ;;
        *)
            if [[ "$1" =~ ^[0-9]+$ ]]; then
                AGE_DAYS="$1"
            else
                echo "Error: Invalid argument '$1'"
                usage
            fi
            ;;
    esac
    shift
done

# Validate target directory
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Directory '$TARGET_DIR' not found or is not a directory."
    exit 1
fi

echo "🌌 Scanning for temporal anomalies in '$TARGET_DIR'..."
echo "⏳ Identifying files older than ${AGE_DAYS} days..."

# Find ancient files
# Using -mtime +N: files modified N*24 hours ago. +N means N+1 days or more.
# So, for "older than 7 days", we use +7.

if [[ "$SWEEP_MODE" -eq 1 ]]; then
    echo "🧹 Initiating temporal sweep protocol..."
    # Use find -delete for safety and efficiency
    find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" -delete
    if [[ "$TARGET_DIR" == "/" && "$AGE_DAYS" -lt 1 ]]; then
        echo "WARNING: Attempted to sweep root directory with very low age. This is dangerous and likely unintended."
    fi
    if [[ "$?" -eq 0 ]]; then
        echo "✅ Temporal detritus successfully purged!"
    else
        echo "❌ Failed to purge some temporal detritus. Check permissions or if files were locked."
        exit 1
    fi
else
    ANCIENT_FILES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" -print)

    if [[ -z "$ANCIENT_FILES" ]]; then
        echo "✨ All files in '$TARGET_DIR' are temporally aligned. No ancient detritus found!"
        exit 0
    fi

    echo ""
    echo "📜 Behold! These files have lingered beyond their temporal prime:"
    echo "-----------------------------------------------------------------"
    echo "$ANCIENT_FILES"
    echo "-----------------------------------------------------------------"
    echo ""
    echo "💡 To purge this temporal detritus, run with the '--sweep' flag."
fi

exit 0
