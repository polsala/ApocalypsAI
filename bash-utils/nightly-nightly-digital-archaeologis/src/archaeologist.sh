#!/bin/bash

# Default values
TARGET_DIR="."
MIN_AGE_DAYS=365 # 1 year
MIN_SIZE_MB=100  # 100 MB

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <min_age_days>] [-s <min_size_mb>]"
    echo "  -d <directory>   : Directory to scan (default: current directory)"
    echo "  -a <min_age_days>: Minimum age in days for files (default: 365)"
    echo "  -s <min_size_mb> : Minimum size in MB for files (default: 100)"
    echo "  -h               : Display this help message"
    exit 1
}

# Parse command-line arguments
while getopts "d:a:s:h" opt; do
    case ${opt} in
        d ) TARGET_DIR=$OPTARG ;;
        a ) MIN_AGE_DAYS=$OPTARG ;;
        s ) MIN_SIZE_MB=$OPTARG ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done

# Validate inputs
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Directory '$TARGET_DIR' not found." >&2
    exit 1
fi

if ! [[ "$MIN_AGE_DAYS" =~ ^[0-9]+$ ]] || [[ "$MIN_AGE_DAYS" -lt 0 ]]; then
    echo "Error: Minimum age must be a non-negative integer." >&2
    exit 1
fi

if ! [[ "$MIN_SIZE_MB" =~ ^[0-9]+$ ]] || [[ "$MIN_SIZE_MB" -lt 0 ]]; then
    echo "Error: Minimum size must be a non-negative integer." >&2
    exit 1
fi

echo "--- Nightly Digital Archaeologist Report ---"
echo "Unearthing digital artifacts from: '$TARGET_DIR'"
echo "Searching for relics older than: $MIN_AGE_DAYS days"
echo "Searching for relics larger than: $MIN_SIZE_MB MB"
echo "------------------------------------------"
echo ""

# Convert MB to bytes for find -size
MIN_SIZE_BYTES=$((MIN_SIZE_MB * 1024 * 1024))

# Find files
# -type f: only files
# -mtime +N: files modified N*24 hours ago (N days)
# -size +Nc: files larger than N bytes
# -print0: null-separated output for safer parsing
find "$TARGET_DIR" -type f -mtime +"$MIN_AGE_DAYS" -size +"$MIN_SIZE_BYTES" -print0 | while IFS= read -r -d $'\0' file; do
    FILE_SIZE=$(du -h "$file" | awk '{print $1}')
    FILE_MTIME=$(stat -c %y "$file" | cut -d' ' -f1)
    echo "  [ARTIFACT FOUND] Path: $file"
    echo "    Size: $FILE_SIZE"
    echo "    Last Modified: $FILE_MTIME"
    echo "    (A relic from a bygone digital era...)"
    echo ""
done

echo "--- End of Archaeological Survey ---"
echo "Consider cataloging these finds or repatriating them to the void."
