#!/bin/bash

# Nightly Resource Scavenger

# Default values
AGE_THRESHOLD_DAYS=7
DRY_RUN=true
TARGET_DIRS=()

# Function to display usage
usage() {
    echo "Usage: $0 [-d <days>] [-r] <directory1> [directory2 ...]"
    echo "  -d <days>  : Files older than this many days will be scavenged (default: 7)."
    echo "  -r         : Run in actual scavenging mode (delete files). Default is dry-run."
    echo "  <directory>: One or more directories to scan for old files."
    echo ""
    echo "Example: $0 -d 30 -r /var/log /tmp"
    exit 1
}

# Parse arguments
while getopts "d:r" opt; do
    case ${opt} in
        d )
            AGE_THRESHOLD_DAYS=$OPTARG
            ;;
        r )
            DRY_RUN=false
            ;;
        \? )
            usage
            ;;
    esac
done
shift $((OPTIND -1))

TARGET_DIRS=(${@})

if [ ${#TARGET_DIRS[@]} -eq 0 ]; then
    echo "Error: No target directories specified."
    usage
fi

echo "--- Nightly Resource Scavenger Report ---"
echo "Scavenging for files older than ${AGE_THRESHOLD_DAYS} days."
if [ "$DRY_RUN" = true ]; then
    echo "Mode: Dry Run (no files will be deleted)."
else
    echo "Mode: Actual Scavenge (files WILL be deleted!)."
fi
echo "Target Directories: ${TARGET_DIRS[*]}"
echo "-----------------------------------------"

TOTAL_FOUND=0
TOTAL_SCAVENGED=0

for dir in "${TARGET_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Warning: Directory '$dir' does not exist or is not a directory. Skipping."
        continue
    fi

    echo ""
    echo "Scanning '$dir' for ancient relics..."
    
    # Find files older than AGE_THRESHOLD_DAYS
    # -type f: only files
    # -mtime +N: files modified N*24 hours ago
    FOUND_FILES=$(find "$dir" -type f -mtime +"$AGE_THRESHOLD_DAYS" 2>/dev/null)
    
    if [ -z "$FOUND_FILES" ]; then
        echo "  No ancient relics found in '$dir'. All clear!"
        continue
    fi

    echo "  Found these potential treasures:"
    echo "$FOUND_FILES" | while IFS= read -r file;
    do
        echo "    - $file"
        TOTAL_FOUND=$((TOTAL_FOUND + 1))
    done

    if [ "$DRY_RUN" = false ]; then
        echo "  Initiating reclamation protocol for '$dir'..."
        echo "$FOUND_FILES" | while IFS= read -r file;
        do
            if rm -f "$file"; then
                echo "    Reclaimed: $file"
                TOTAL_SCAVENGED=$((TOTAL_SCAVENGED + 1))
            else
                echo "    Failed to reclaim: $file" >&2
            fi
        done
        echo "  Reclamation complete for '$dir'."
    else
        echo "  (Dry run: no files reclaimed from '$dir'.)"
    fi
done

echo ""
echo "--- Scavenging Summary ---"
echo "Total ancient relics identified: ${TOTAL_FOUND}"
echo "Total relics actually reclaimed: ${TOTAL_SCAVENGED}"
echo "--------------------------"

exit 0
