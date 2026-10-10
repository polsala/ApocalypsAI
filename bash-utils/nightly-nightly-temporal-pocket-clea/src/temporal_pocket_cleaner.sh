#!/bin/bash

set -euo pipefail

# Define the temporal pocket directory name
POCKET_DIR_NAME=".temporal_pocket"

# Function to display usage
usage() {
    echo "Usage: $0 <command> <directory> [options]"
    echo ""
    echo "Commands:"
    echo "  clean <directory> <age_in_days> - Moves files older than age_in_days into the temporal pocket."
    echo "  list <directory>                - Lists files currently in the temporal pocket."
    echo "  retrieve <directory> [filename_pattern] - Retrieves files from the temporal pocket."
    echo ""
    echo "Examples:"
    echo "  $0 clean /path/to/data 30"
    echo "  $0 list /path/to/data"
    echo "  $0 retrieve /path/to/data \"report_*.log\""
    echo "  $0 retrieve /path/to/data"
    exit 1
}

# Function to clean (move old files to pocket)
clean_pocket() {
    local target_dir="$1"
    local age_days="$2"

    if [[ ! -d "$target_dir" ]]; then
        echo "Error: Directory '$target_dir' not found." >&2
        exit 1
    fi

    local pocket_path="${target_dir}/${POCKET_DIR_NAME}"
    mkdir -p "$pocket_path"

    echo "Scanning '$target_dir' for files older than $age_days days..."
    
    # Find files (not directories) older than age_days
    # -maxdepth 1 to only consider files directly in target_dir, not subdirectories
    # -type f to only select files
    # -mtime +$age_days to find files modified more than age_days ago
    # -print0 for null-separated output, safe for filenames with spaces/special chars
    find "$target_dir" -maxdepth 1 -type f -mtime +"$age_days" -print0 | while IFS= read -r -d $'\0' file; do
        local filename=$(basename "$file")
        echo "  Moving '$filename' to temporal pocket."
        mv "$file" "$pocket_path/"
    done

    echo "Cleaning complete. Check '$pocket_path' for moved files."
}

# Function to list files in the pocket
list_pocket() {
    local target_dir="$1"
    local pocket_path="${target_dir}/${POCKET_DIR_NAME}"

    if [[ ! -d "$pocket_path" ]]; then
        echo "Temporal pocket '$pocket_path' does not exist or is empty."
        return 0
    }

    echo "Files in temporal pocket '$pocket_path':"
    # Use find to list files, excluding directories
    find "$pocket_path" -maxdepth 1 -type f -printf "  %f\n" | sort
    if [[ $(find "$pocket_path" -maxdepth 1 -type f | wc -l) -eq 0 ]]; then
        echo "  (Pocket is empty)"
    fi
}

# Function to retrieve files from the pocket
retrieve_pocket() {
    local target_dir="$1"
    local filename_pattern="${2:-*}" # Default to '*' if no pattern is provided
    local pocket_path="${target_dir}/${POCKET_DIR_NAME}"

    if [[ ! -d "$pocket_path" ]]; then
        echo "Error: Temporal pocket '$pocket_path' does not exist." >&2
        exit 1
    }

    echo "Retrieving files matching '$filename_pattern' from temporal pocket '$pocket_path'..."

    local files_found=0
    # Use find to locate files matching the pattern within the pocket
    # -maxdepth 1 to only consider files directly in the pocket
    # -type f to only select files
    # -name "$filename_pattern" to match the pattern
    # -print0 for null-separated output
    find "$pocket_path" -maxdepth 1 -type f -name "$filename_pattern" -print0 | while IFS= read -r -d $'\0' file; do
        local filename=$(basename "$file")
        echo "  Retrieving '$filename'."
        mv "$file" "$target_dir/"
        files_found=$((files_found + 1))
    done

    if [[ "$files_found" -eq 0 ]]; then
        echo "No files matching '$filename_pattern' found in the temporal pocket."
    else
        echo "Retrieval complete."
    fi
}

# Main script logic
if [[ $# -lt 2 ]]; then
    usage
fi

COMMAND="$1"
TARGET_DIRECTORY="$2"

case "$COMMAND" in
    clean)
        if [[ $# -ne 3 ]]; then
            usage
        fi
        AGE_DAYS="$3"
        if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]]; then
            echo "Error: Age in days must be a positive integer." >&2
            exit 1
        fi
        clean_pocket "$TARGET_DIRECTORY" "$AGE_DAYS"
        ;;
    list)
        if [[ $# -ne 2 ]]; then
            usage
        fi
        list_pocket "$TARGET_DIRECTORY"
        ;;
    retrieve)
        if [[ $# -lt 2 || $# -gt 3 ]]; then
            usage
        fi
        RETRIEVE_PATTERN="${3:-}" # Optional third argument for pattern
        retrieve_pocket "$TARGET_DIRECTORY" "$RETRIEVE_PATTERN"
        ;;
    *)
        echo "Error: Unknown command '$COMMAND'." >&2
        usage
        ;;
esac
