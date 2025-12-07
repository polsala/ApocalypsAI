#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# Sweeps away old files from specified directories.

DEFAULT_AGE_DAYS=30
DRY_RUN=false
DIRECTORIES=()
AGE_DAYS=$DEFAULT_AGE_DAYS

# Function to display help message
show_help() {
    echo "Usage: sweeper.sh [DIRECTORY...] [--age <DAYS>] [--dry-run] [--help]"
    echo ""
    echo "A containerized utility to periodically sweep away digital dust bunnies"
    echo "(old log files, temporary data) from specified directories."
    echo ""
    echo "Arguments:"
    echo "  [DIRECTORY...]  One or more paths to directories to clean."
    echo "                  These should correspond to volumes mounted into the container."
    echo "  --age <DAYS>    (Optional) The maximum age (in days) for files to be kept."
    echo "                  Files older than this will be deleted. Defaults to ${DEFAULT_AGE_DAYS} days."
    echo "  --dry-run       (Optional) Perform a dry run, listing files that *would* be deleted"
    echo "                  without actually deleting them."
    echo "  --help          Display this help message."
    echo ""
    echo "Example:"
    echo "  docker run --rm -v /var/log:/var/log:rw digital-dust-bunny-sweeper /var/log --age 7"
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --age)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo "Error: --age requires a numeric value." >&2
                exit 1
            fi
            if ! [[ "$2" =~ ^[0-9]+$ ]]; then
                echo "Error: --age value must be a positive integer." >&2
                exit 1
            fi
            AGE_DAYS="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        -*)
            echo "Error: Unknown option '$1'" >&2
            show_help
            exit 1
            ;;
        *)
            DIRECTORIES+=("$1")
            shift
            ;;
    esac
done

if [ ${#DIRECTORIES[@]} -eq 0 ] && [ "$DRY_RUN" = false ]; then
    echo "Error: No directories specified for cleaning." >&2
    show_help
    exit 1
fi

echo "--- Digital Dust Bunny Sweeper ---"
echo "Target directories: ${DIRECTORIES[*]}"
echo "Files older than: ${AGE_DAYS} days"
if [ "$DRY_RUN" = true ]; then
    echo "Mode: DRY RUN (no files will be deleted)"
else
    echo "Mode: LIVE RUN (files WILL be deleted)"
fi
echo "----------------------------------"

for dir in "${DIRECTORIES[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Warning: Directory '$dir' does not exist or is not a directory. Skipping." >&2
        continue
    fi

    echo "Processing directory: '$dir'"
    if [ "$DRY_RUN" = true ]; then
        # Find files older than AGE_DAYS, excluding directories themselves
        find "$dir" -type f -mtime +"$AGE_DAYS" -print
    else
        # Find and delete files older than AGE_DAYS, excluding directories themselves
        # Use -delete for efficiency and atomicity, but it won't delete non-empty directories.
        # We are specifically targeting files (-type f).
        find "$dir" -type f -mtime +"$AGE_DAYS" -delete
        if [ $? -eq 0 ]; then
            echo "Successfully swept old files from '$dir'."
        else
            echo "Error sweeping files from '$dir'." >&2
        fi
    fi
done

echo "--- Sweeping complete! ---"
