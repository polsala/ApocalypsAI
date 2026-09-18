#!/bin/bash

# Nightly Scavenger's Stash Sorter
# A whimsical yet practical bash utility for organizing your digital "finds" (files)
# into categorized subdirectories, much like a diligent scavenger sorting their precious loot.

set -euo pipefail

# --- Configuration ---
declare -A CATEGORIES=(
    ["documents"]="pdf doc docx txt rtf odt md csv xls xlsx ppt pptx"
    ["images"]="jpg jpeg png gif bmp tiff webp svg"
    ["archives"]="zip tar gz bz2 xz rar 7z"
    ["executables"]="sh run bin"
    ["audio"]="mp3 wav aac flac ogg"
    ["video"]="mp4 mkv avi mov webm"
    ["code"]="py js ts html css json xml yml yaml go rs java c cpp h hpp"
)
OTHER_FINDS_DIR="other_finds"

# --- Global Variables ---
DRY_RUN=false
SOURCE_DIR=""

# --- Functions ---

# Function to display help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS] <source_directory>"
    echo ""
    echo "A bash utility to organize files in a specified directory into categorized subdirectories."
    echo ""
    echo "Arguments:"
    echo "  <source_directory>  The path to the directory whose contents you want to sort."
    echo ""
    echo "Options:"
    echo "  -d, --dry-run       Perform a dry run. The script will print what it *would* do without making any changes."
    echo "  -h, --help          Display this help message."
    echo ""
    echo "Example:"
    echo "  $(basename "$0") --dry-run ."
    echo "  $(basename "$0") /home/user/Downloads"
}

# Function to get file extension
get_extension() {
    local filename=$(basename -- "$1")
    local extension="${filename##*.}"
    if [[ "$filename" == "$extension" ]]; then # No extension found
        echo ""
    else
        echo "$extension"
    fi
}

# Function to determine category based on extension
get_category() {
    local ext="$1"
    local category=""

    for cat in "${!CATEGORIES[@]}"; do
        local extensions="${CATEGORIES[$cat]}"
        for known_ext in $extensions; do
            if [[ "$ext" == "$known_ext" ]]; then
                category="$cat"
                break 2 # Break from inner and outer loop
            fi
        done
    done

    if [[ -z "$category" ]]; then
        echo "$OTHER_FINDS_DIR"
    else
        echo "$category"
    fi
}

# --- Main Logic ---

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d|--dry-run)
            DRY_RUN=true
            shift
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
            if [[ -z "$SOURCE_DIR" ]]; then
                SOURCE_DIR="$1"
            else
                echo "Error: Too many arguments. Source directory already specified as '$SOURCE_DIR'." >&2
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate source directory
if [[ -z "$SOURCE_DIR" ]]; then
    echo "Error: Source directory not specified." >&2
    show_help
    exit 1
fi

if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist or is not a directory." >&2
    exit 1
fi

# Resolve source directory to absolute path
SOURCE_DIR=$(realpath "$SOURCE_DIR")

echo "--- Nightly Scavenger's Stash Sorter ---"
echo "Source Directory: $SOURCE_DIR"
if "$DRY_RUN"; then
    echo "Mode: DRY RUN (no changes will be made)"
else
    echo "Mode: LIVE RUN (files will be moved)"
fi
echo "----------------------------------------"
echo ""

# Create target directories if they don't exist
for cat in "${!CATEGORIES[@]}"; do
    TARGET_PATH="$SOURCE_DIR/$cat"
    if "$DRY_RUN"; then
        echo "DRY RUN: Would create directory: $TARGET_PATH"
    else
        mkdir -p "$TARGET_PATH"
        echo "Created directory: $TARGET_PATH"
    fi
done
TARGET_PATH="$SOURCE_DIR/$OTHER_FINDS_DIR"
if "$DRY_RUN"; then
    echo "DRY RUN: Would create directory: $TARGET_PATH"
else
    mkdir -p "$TARGET_PATH"
    echo "Created directory: $TARGET_PATH"
fi
echo ""

# Iterate through files in the source directory
# Using find with -maxdepth 1 to only process immediate children, not subdirectories recursively
# Using -print0 and read -d $'\0' to handle filenames with spaces or special characters
find "$SOURCE_DIR" -maxdepth 1 -type f -print0 | while IFS= read -r -d $'\0' file; do
    filename=$(basename -- "$file")
    ext=$(get_extension "$filename")
    target_category=$(get_category "$ext")
    target_dir="$SOURCE_DIR/$target_category"
    destination_path="$target_dir/$filename"

    if [[ "$file" == "$destination_path" ]]; then
        echo "Skipping '$filename': Already in its correct category '$target_category'."
        continue
    fi

    if "$DRY_RUN"; then
        echo "DRY RUN: Would move '$filename' to '$target_dir/'"
    else
        if mv -n "$file" "$target_dir/"; then # -n prevents overwriting existing files
            echo "Moved '$filename' to '$target_dir/'"
        else
            echo "Error moving '$filename' to '$target_dir/'" >&2
        fi
    fi
done

echo ""
echo "--- Sorting Complete ---"
if "$DRY_RUN"; then
    echo "No files were actually moved (dry run)."
else
    echo "Files have been sorted."
fi
echo "------------------------"
