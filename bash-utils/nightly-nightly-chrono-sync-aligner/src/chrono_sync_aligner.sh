#!/bin/bash

# Nightly Chrono-Sync File Aligner
# Compares file modification times between two directories.

set -euo pipefail

# Function to get file modification time in epoch seconds
# Assumes GNU stat (Linux). For BSD/macOS, 'stat -f %m' would be needed.
get_mtime() {
    stat -c %Y "$1" 2>/dev/null || echo ""
}

# Check for correct number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_directory> <target_directory>"
    exit 1
fi

SOURCE_DIR="$(realpath "$1")"
TARGET_DIR="$(realpath "$2")"

# Check if directories exist
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' not found."
    exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory '$TARGET_DIR' not found."
    exit 1
fi

# Use associative arrays to store file paths and their modification times (requires Bash 4+)
declare -A source_files
declare -A target_files

# Populate source_files array
while IFS= read -r -d '' file_path; do
    relative_path="${file_path#$SOURCE_DIR/}"
    source_files["$relative_path"]="$(get_mtime "$file_path")"
done < <(find "$SOURCE_DIR" -type f -print0)

# Populate target_files array
while IFS= read -r -d '' file_path; do
    relative_path="${file_path#$TARGET_DIR/}"
    target_files["$relative_path"]="$(get_mtime "$file_path")"
done < <(find "$TARGET_DIR" -type f -print0)

# Compare files from source to target
for relative_path in "${!source_files[@]}"; do
    source_mtime="${source_files["$relative_path"]}"

    if [[ -v target_files["$relative_path"] ]]; then
        target_mtime="${target_files["$relative_path"]}"
        if [ "$source_mtime" -eq "$target_mtime" ]; then
            echo "[ALIGNED] $relative_path (Source: $source_mtime, Target: $target_mtime)"
        else
            echo "[MISALIGNED] $relative_path (Source: $source_mtime, Target: $target_mtime)"
        fi
    else
        echo "[MISSING_TARGET] $relative_path (Source: $source_mtime)"
    fi
done

# Find files that are only in the target directory (missing in source)
for relative_path in "${!target_files[@]}"; do
    if [[ ! -v source_files["$relative_path"] ]]; then
        target_mtime="${target_files["$relative_path"]}"
        echo "[MISSING_SOURCE] $relative_path (Target: $target_mtime)"
    fi
done
