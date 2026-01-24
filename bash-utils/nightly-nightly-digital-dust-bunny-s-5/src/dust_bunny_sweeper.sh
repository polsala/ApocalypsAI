#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

# Default configuration
DEFAULT_PATHS=("$HOME/Downloads" "/tmp" "$HOME/.cache" "/var/tmp")
DEFAULT_AGE_DAYS=30
DRY_RUN=false
DELETE_CONFIRMED=false

# Function to display usage
usage() {
    echo "Usage: $0 [-p <path>] [-a <days>] [-d] [-y] [-h]" >&2
    echo "  -p <path>  : Add a path to scan (can be used multiple times). Defaults to common locations." >&2
    echo "  -a <days>  : Age threshold in days. Files/dirs older than this are 'dust bunnies'. Default: $DEFAULT_AGE_DAYS." >&2
    echo "  -d         : Dry run mode. Only list 'dust bunnies', do not delete. (Default: $DRY_RUN)" >&2
    echo "  -y         : Auto-confirm deletion without prompt. USE WITH CAUTION! (Default: $DELETE_CONFIRMED)" >&2
    echo "  -h         : Display this help message." >&2
    exit 1
}

# Parse arguments
PATHS_TO_SCAN=()
while getopts "p:a:dyh" opt; do
    case ${opt} in
        p )
            PATHS_TO_SCAN+=("$OPTARG")
            ;;
        a )
            if [[ "$OPTARG" =~ ^[0-9]+$ ]]; then
                DEFAULT_AGE_DAYS=$OPTARG
            else
                echo "Error: Age must be a positive integer." >&2
                usage
            fi
            ;;
        d )
            DRY_RUN=true
            ;;
        y )
            DELETE_CONFIRMED=true
            ;;
        h )
            usage
            ;;
        \? )
            echo "Invalid option: -$OPTARG" >&2
            usage
            ;;
    esac
done
shift $((OPTIND -1))

# If no paths provided, use defaults
if [ ${#PATHS_TO_SCAN[@]} -eq 0 ]; then
    PATHS_TO_SCAN=("${DEFAULT_PATHS[@]}")
fi

echo "🗑️ Initiating Digital Dust Bunny Sweep..."
echo "Scanning paths: ${PATHS_TO_SCAN[*]}"
echo "Looking for files/directories older than $DEFAULT_AGE_DAYS days."
echo "Dry run mode: $DRY_RUN"

DUST_BUNNIES=()
for scan_path in "${PATHS_TO_SCAN[@]}"; do
    if [ -d "$scan_path" ]; then
        echo "Searching in: $scan_path"
        # Find files and directories older than DEFAULT_AGE_DAYS
        # -mtime +N: files modified N*24 hours ago. +N means more than N days.
        # -print0: print full file name on stdout, followed by a null character.
        # xargs -0: read items from stdin separated by null characters.
        # This handles filenames with spaces or special characters.
        while IFS= read -r -d $'\0' item; do
            DUST_BUNNIES+=("$item")
        done < <(find "$scan_path" -depth -type f -o -type d -mtime +"$DEFAULT_AGE_DAYS" -print0 2>/dev/null)
    else
        echo "Warning: Path '$scan_path' does not exist or is not a directory. Skipping." >&2
    fi
done

if [ ${#DUST_BUNNIES[@]} -eq 0 ]; then
    echo "✨ No digital dust bunnies found! Your system is sparkling clean."
    exit 0
fi

echo ""
echo "Found ${#DUST_BUNNIES[@]} digital dust bunnies:"
for bunny in "${DUST_BUNNIES[@]}"; do
    echo "  - $bunny"
done
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "Dry run complete. No files were deleted."
    exit 0
fi

if [ "$DELETE_CONFIRMED" = false ]; then
    read -p "Do you want to sweep these dust bunnies away? (y/N): " -n 1 -r
    echo "" # Newline after prompt
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Sweep aborted. Digital dust bunnies remain."
        exit 0
    fi
fi

echo "🗑️ Sweeping away digital dust bunnies..."
for bunny in "${DUST_BUNNIES[@]}"; do
    if [ -e "$bunny" ]; then # Check if it still exists before trying to delete
        if rm -rf "$bunny"; then
            echo "  - Swept away: $bunny"
        else
            echo "  - Failed to sweep: $bunny" >&2
        fi
    fi
done

echo "✨ Digital dust bunny sweep complete!"
