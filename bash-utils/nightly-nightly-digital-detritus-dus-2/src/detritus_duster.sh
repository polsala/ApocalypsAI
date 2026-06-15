#!/bin/bash

# nightly-digital-detritus-duster
# A whimsical utility to sweep away old files (digital detritus) from specified directories.

# --- Configuration ---
SCRIPT_NAME="Digital Detritus Duster"
VERSION="1.0.0"

# --- Functions ---

display_help() {
    echo "Usage: $0 <directory> <age_in_days> [OPTIONS]"
    echo ""
    echo "Sweeps away digital detritus (old files) from specified directories."
    echo ""
    echo "Arguments:"
    echo "  <directory>    The path to the directory to clean."
    echo "  <age_in_days>  Files older than this many days will be considered 'detritus'."
    echo ""
    echo "Options:"
    echo "  -d, --delete   CAUTION! Actually deletes the identified files. Without this flag,"
    echo "                 the script performs a dry-run, listing files without deleting them."
    echo "  -v, --verbose  Show more detailed output, including each file being considered."
    echo "  -h, --help     Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 /tmp 7"
    echo "  $0 /var/log 30 -v"
    echo "  $0 /home/user/downloads 90 --delete"
    exit 0
}

# --- Main Logic ---

# Parse arguments and options
DELETE_MODE=0
VERBOSE_MODE=0
DIRECTORY=""
AGE_DAYS=""

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d|--delete)
            DELETE_MODE=1
            shift
            ;;
        -v|--verbose)
            VERBOSE_MODE=1
            shift
            ;;
        -h|--help)
            display_help
            ;;
        *)
            if [[ -z "$DIRECTORY" ]]; then
                DIRECTORY="$1"
            elif [[ -z "$AGE_DAYS" ]]; then
                AGE_DAYS="$1"
            else
                echo "Error: Unknown argument or too many arguments: $1" >&2
                display_help
            fi
            shift
            ;;
    esac
done

# Validate arguments
if [[ -z "$DIRECTORY" || -z "$AGE_DAYS" ]]; then
    echo "Error: Missing directory or age_in_days argument." >&2
    display_help
fi

if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]]; then
    echo "Error: Age in days must be a positive integer." >&2
    exit 1
fi

if [[ ! -d "$DIRECTORY" ]]; then
    echo "Error: Directory '$DIRECTORY' does not exist or is not a directory." >&2
    exit 1
fi

echo "--- $SCRIPT_NAME v$VERSION ---"
echo "Scanning '$DIRECTORY' for digital detritus older than $AGE_DAYS days..."

# Construct the find command
FIND_CMD="find \"$DIRECTORY\" -type f -mtime +$AGE_DAYS"

if [[ "$DELETE_MODE" -eq 1 ]]; then
    echo "CAUTION: Delete mode is ENABLED. Files will be permanently removed."
    echo "Proceeding to sweep away the detritus..."
    # Use -print0 and xargs -0 for safe handling of filenames with spaces/special chars
    if [[ "$VERBOSE_MODE" -eq 1 ]]; then
        echo "Identified detritus (and deleting):"
        eval $FIND_CMD -print0 | while IFS= read -r -d $\'\0\' file; do
            echo "  - Sweeping: $file"
            rm -f "$file"
        done
        echo "Sweep complete!"
    else
        # Non-verbose delete
        eval $FIND_CMD -print0 | xargs -0 rm -f
        echo "Digital detritus swept away silently."
    fi
    echo "Cleanup complete for '$DIRECTORY'."
else
    echo "Dry-run mode: No files will be deleted. To delete, run with --delete."
    echo "Identified digital detritus:"
    
    # Collect files first to count them, then print if verbose
    # Using eval for FIND_CMD to correctly handle quoted directory paths
    MAPFILE -d $\'\0\' FILES_TO_REPORT < <(eval $FIND_CMD -print0)

    FOUND_FILES=${#FILES_TO_REPORT[@]}

    if [[ "$FOUND_FILES" -eq 0 ]]; then
        echo "  No ancient scrolls or forgotten bits found. Your digital realm is pristine!"
    else
        if [[ "$VERBOSE_MODE" -eq 1 ]]; then
            for file in "${FILES_TO_REPORT[@]}"; do
                echo "  - Found: $file"
            done
        else
            echo "  (Use -v for detailed list)"
        fi
        echo "Found $FOUND_FILES pieces of digital detritus."
        echo "Consider running with --delete to tidy up."
    fi
    echo "Dry-run complete for '$DIRECTORY'."
fi

echo "--- $SCRIPT_NAME finished its nightly rounds. ---"
