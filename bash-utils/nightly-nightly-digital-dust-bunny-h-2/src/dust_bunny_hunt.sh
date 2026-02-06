#!/bin/bash

# Default values
DEFAULT_DIRS=("/tmp" "$HOME/.cache" "$HOME/.local/share/Trash/files")
DEFAULT_AGE_DAYS=90 # Files older than 90 days

# Function to get file type based on extension or common patterns
get_file_type() {
    local filename=$(basename "$1")
    case "$filename" in
        *.log|*.txt) echo "Log/Text File";;
        *.tmp|*.temp) echo "Temporary File";;
        *.bak|*.old) echo "Backup/Old Version";;
        *.tar.gz|*.zip|*.rar|*.7z) echo "Archive";;
        *.deb|*.rpm|*.pkg) echo "Package";;
        *.iso|*.img) echo "Disk Image";;
        *.cache) echo "Cache File";;
        *) echo "Miscellaneous Digital Dust";;
    esac
}

# Main function to hunt for dust bunnies
hunt_dust_bunnies() {
    local target_dirs=("${@}")
    local age_threshold="$DEFAULT_AGE_DAYS"

    if [[ -z "${target_dirs[*]}" ]]; then
        target_dirs=("${DEFAULT_DIRS[@]}")
    fi

    echo "🧹 ApocalypsAI Digital Dust Bunny Hunter 🧹"
    echo "Scanning for digital dust bunnies older than ${age_threshold} days..."
    echo "Target directories: ${target_dirs[*]}"
    echo "---------------------------------------------------"

    local total_dust_bunnies=0
    declare -A bunny_types # Associative array for counts by type (requires Bash 4+)

    for dir in "${target_dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            echo "Warning: Directory '$dir' not found or not a directory. Skipping."
            continue
        fi

        echo "\nSearching in: $dir"
        # Find files older than the age threshold, suppress errors for unreadable directories
        local found_files=$(find "$dir" -type f -mtime +"$age_threshold" 2>/dev/null)

        if [[ -z "$found_files" ]]; then
            echo "  No ancient digital dust bunnies found here! ✨"
        else
            while IFS= read -r file; do
                local file_type=$(get_file_type "$file")
                echo "  - Found a ${file_type} bunny: $(basename "$file")"
                bunny_types["$file_type"]=$((bunny_types["$file_type"] + 1))
                total_dust_bunnies=$((total_dust_bunnies + 1))
            done <<< "$found_files"
        fi
    done

    echo "\n---------------------------------------------------"
    echo "✨ Digital Dust Bunny Hunt Report ✨"
    echo "Total ancient digital dust bunnies found: ${total_dust_bunnies}"

    if [[ "$total_dust_bunnies" -gt 0 ]]; then
        echo "Breakdown by type:"
        for type in "${!bunny_types[@]}"; do
            echo "  - ${type}: ${bunny_types[$type]}"
        done
        echo "\nRecommendation: Consider sweeping these digital corners! (No files were deleted.)"
    else
        echo "Your digital realm is sparkling clean! Keep up the good work. 🌟"
    fi
}

# Parse arguments
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    echo "Usage: $(basename "$0") [DIRECTORY1] [DIRECTORY2] ..."
    echo "Scans specified directories for files older than ${DEFAULT_AGE_DAYS} days."
    echo "If no directories are provided, it defaults to: ${DEFAULT_DIRS[*]}"
    echo "It reports on 'digital dust bunnies' (old files) but does not delete them."
    exit 0
fi

# If arguments are provided, use them as target directories
if [[ "$#" -gt 0 ]]; then
    hunt_dust_bunnies "$@"
else
    hunt_dust_bunnies # Use defaults
fi
