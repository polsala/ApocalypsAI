#!/bin/bash

# Nightly Scavenger's Stash Sorter
# Brings order to your chaotic post-apocalyptic digital hauls.

STASH_DIR="$1"

# --- Configuration ---
declare -A CATEGORIES
CATEGORIES=(
    ["Documents"]="txt md pdf doc docx odt"
    ["Images"]="jpg jpeg png gif bmp tiff"
    ["Archives"]="zip tar gz rar 7z"
    ["Executables"]="sh run bin exe"
)
OTHER_CATEGORY="Other"

# --- Functions ---

# Function to print usage information
print_usage() {
    echo "Usage: $0 <directory_path>"
    echo "  <directory_path>: The path to the directory containing your stash."
    echo ""
    echo "Example: $0 ~/my_apocalyptic_loot"
}

# Function to create category directories if they don't exist
create_category_dirs() {
    local base_dir="$1"
    echo "Preparing your stash area in '$base_dir'..."
    for category in "${!CATEGORIES[@]}"; do
        if [ ! -d "$base_dir/$category" ]; then
            mkdir -p "$base_dir/$category"
            echo "  - Forging a new compartment: '$category'."
        fi
    done
    if [ ! -d "$base_dir/$OTHER_CATEGORY" ]; then
        mkdir -p "$base_dir/$OTHER_CATEGORY"
        echo "  - Setting aside a corner for '$OTHER_CATEGORY' findings."
    fi
}

# Function to sort files
sort_files() {
    local base_dir="$1"
    echo "Scanning your haul for valuable provisions in '$base_dir'..."

    local files_found=0
    local files_sorted=0

    # Iterate over all files (not directories) in the base_dir
    for item in "$base_dir"/*; do
        if [ -f "$item" ]; then
            files_found=$((files_found + 1))
            local filename=$(basename "$item")
            local extension="${filename##*.}"
            local moved=false

            # Check if the file is already in a category subdirectory
            for category in "${!CATEGORIES[@]}"; do
                if [[ "$item" == "$base_dir/$category/$filename" ]]; then
                    echo "  - '$filename' already secured in '$category'. Skipping."
                    moved=true
                    break
                fi
            done
            if [[ "$item" == "$base_dir/$OTHER_CATEGORY/$filename" ]]; then
                echo "  - '$filename' already filed under '$OTHER_CATEGORY'. Skipping."
                moved=true
            fi

            if ! $moved; then
                local target_category=""
                for category in "${!CATEGORIES[@]}"; do
                    local extensions="${CATEGORIES[$category]}"
                    if [[ " ${extensions[@]} " =~ " ${extension} " ]]; then
                        target_category="$category"
                        break
                    fi
                done

                if [ -n "$target_category" ]; then
                    echo "  - Found a '$extension' artifact: '$filename'! Stashing it with other '$target_category' intel."
                    mv "$item" "$base_dir/$target_category/"
                    files_sorted=$((files_sorted + 1))
                else
                    echo "  - Discovered an unknown artifact: '$filename'. Placing in '$OTHER_CATEGORY' for later identification."
                    mv "$item" "$base_dir/$OTHER_CATEGORY/"
                    files_sorted=$((files_sorted + 1))
                fi
            fi
        fi
    done

    if [ "$files_found" -eq 0 ]; then
        echo "No new provisions found in '$base_dir'. The stash remains untouched."
    elif [ "$files_sorted" -eq 0 ]; then
        echo "All provisions in '$base_dir' were already sorted. Good work, survivor!"
    else
        echo "Stash sorted! Your inventory is now more manageable, survivor. ($files_sorted items moved)"
    fi
}

# --- Main Logic ---

# Check for correct number of arguments
if [ "$#" -ne 1 ]; then
    print_usage
    exit 1
fi

# Validate directory
if [ ! -d "$STASH_DIR" ]; then
    echo "Error: Stash directory '$STASH_DIR' not found or is not a directory."
    exit 1
fi

# Resolve absolute path for consistency
STASH_DIR=$(realpath "$STASH_DIR")

create_category_dirs "$STASH_DIR"
sort_files "$STASH_DIR"

exit 0
