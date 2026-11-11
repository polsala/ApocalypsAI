#!/bin/bash

# Configuration
SOURCE_DIR="$1"
DEST_ROOT="${2:-./sorted_stash}" # Default to ./sorted_stash if not provided

# Categories and their extensions
declare -A CATEGORIES
CATEGORIES=(
    ["documents"]="txt docx pdf md rtf"
    ["images"]="jpg jpeg png gif bmp tiff webp"
    ["archives"]="zip tar gz bz2 xz rar 7z"
    ["scripts"]="sh py js rb pl"
    ["data"]="csv json xml yml yaml"
    ["audio"]="mp3 wav ogg flac"
    ["video"]="mp4 avi mkv mov"
)

# --- Functions ---

# Function to display usage
usage() {
    echo "Usage: $0 <source_directory> [destination_root_directory]"
    echo "  <source_directory>: The directory containing files to sort."
    echo "  [destination_root_directory]: Optional. The root directory where sorted categories will be created. Defaults to './sorted_stash'."
    echo ""
    echo "Example: $0 ./my_scavenged_loot ./my_organized_vault"
    exit 1
}

# Function to create directories
create_dirs() {
    echo "Creating destination directories under: $DEST_ROOT"
    mkdir -p "$DEST_ROOT/unknown" || { echo "Error: Could not create $DEST_ROOT/unknown"; exit 1; }
    for category in "${!CATEGORIES[@]}"; do
        mkdir -p "$DEST_ROOT/$category" || { echo "Error: Could not create $DEST_ROOT/$category"; exit 1; }
    done
}

# Function to classify and move files
sort_files() {
    local file
    local filename
    local extension
    local category_found
    local dest_path
    local manifest_entry

    MANIFEST_FILE="$DEST_ROOT/stash_manifest.txt"
    echo "# Scavenged Stash Manifest - $(date)" > "$MANIFEST_FILE"
    echo "# Source: $SOURCE_DIR" >> "$MANIFEST_FILE"
    echo "# Destination Root: $DEST_ROOT" >> "$MANIFEST_FILE"
    echo "--------------------------------------------------" >> "$MANIFEST_FILE"

    echo "Starting file sorting from '$SOURCE_DIR'..."

    # Use find to iterate files, excluding directories
    find "$SOURCE_DIR" -maxdepth 1 -type f -print0 | while IFS= read -r -d $'\0' file; do
        filename=$(basename "$file")
        extension=""
        if [[ "$filename" == *.* ]]; then
            extension="${filename##*.}"
            extension="${extension,,}" # Convert to lowercase for consistent matching
        fi
        category_found=false

        for category in "${!CATEGORIES[@]}"; do
            if [[ " ${CATEGORIES[$category]} " =~ " ${extension} " ]]; then
                dest_path="$DEST_ROOT/$category/$filename"
                echo "  Sorting '$filename' into '$category'..."
                mv "$file" "$dest_path" || { echo "Warning: Could not move '$file'. Skipping."; continue; }
                manifest_entry="$category/$filename"
                echo "$manifest_entry" >> "$MANIFEST_FILE"
                category_found=true
                break
            fi
        done

        if ! $category_found; then
            dest_path="$DEST_ROOT/unknown/$filename"
            echo "  Sorting '$filename' into 'unknown' (extension: .$extension)..."
            mv "$file" "$dest_path" || { echo "Warning: Could not move '$file'. Skipping."; continue; }
            manifest_entry="unknown/$filename"
            echo "$manifest_entry" >> "$MANIFEST_FILE"
        fi
    done

    echo "--------------------------------------------------" >> "$MANIFEST_FILE"
    echo "Sorting complete. Manifest generated at '$MANIFEST_FILE'."
}

# --- Main execution ---

# Check for required arguments
if [ -z "$SOURCE_DIR" ]; then
    usage
fi

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' not found."
    exit 1
fi

# Create destination directories
create_dirs

# Sort files
sort_files

echo "Operation finished."
