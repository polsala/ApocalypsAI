#!/bin/bash

# Nightly Cosmic Dust Collector
# Sweeps away old files from a specified directory.

# --- Configuration ---
# No direct configuration needed, all parameters are passed via CLI arguments.

# --- Functions ---

# Function to display usage information
usage() {
    echo "Usage: $0 <directory_path> <age_in_days> [--dry-run] [--verbose]"
    echo ""
    echo "  <directory_path> : The path to the directory to clean."
    echo "  <age_in_days>    : Files older than this many days will be targeted."
    echo "  --dry-run        : Simulate deletion, list files but do not remove them."
    echo "  --verbose        : Provide more detailed output."
    echo ""
    echo "Example: $0 /var/log 30 --dry-run --verbose"
    exit 1
}

# --- Main Script ---

# Parse arguments
DIRECTORY=""
AGE=""
DRY_RUN=0
VERBOSE=0

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        --verbose)
            VERBOSE=1
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            if [[ -z "$DIRECTORY" ]]; then
                DIRECTORY="$1"
            elif [[ -z "$AGE" ]]; then
                AGE="$1"
            else
                echo "Error: Unknown argument or too many arguments: $1"
                usage
            fi
            shift
            ;;
    esac
done

# Validate arguments
if [[ -z "$DIRECTORY" || -z "$AGE" ]]; then
    echo "Error: Missing required arguments."
    usage
fi

if ! [[ "$AGE" =~ ^[0-9]+$ ]]; then
    echo "Error: Age must be a positive integer."
    exit 1
fi

if [[ ! -d "$DIRECTORY" ]]; then
    echo "Error: Directory '$DIRECTORY' does not exist or is not a directory."
    exit 1
fi

if [[ "$VERBOSE" -eq 1 ]]; then
    echo "--- Cosmic Dust Collection Initiated ---"
    echo "Target Directory: '$DIRECTORY'"
    echo "Files older than: '$AGE' days"
    if [[ "$DRY_RUN" -eq 1 ]]; then
        echo "Mode: DRY RUN (no files will be deleted)"
    else
        echo "Mode: LIVE RUN (files WILL be deleted)"
    fi
    echo "----------------------------------------"
fi

# Find and process files
# -type f: only regular files
# -mtime +AGE: files modified more than AGE*24 hours ago
# -print0: print full file name on stdout, followed by a null character (for xargs -0)
# xargs -0: read items from standard input, delimited by null characters
# rm --: ensures that filenames starting with '-' are not interpreted as options
# || true: prevents xargs from exiting if rm fails on some files (e.g., permissions)
# Mock rationale: The `find` and `rm` commands are standard system utilities.
# For testing, we create a controlled temporary file system environment.
# The `find` command will operate on these temporary files, and `rm` will delete them.
# No external services or complex system states are involved, making it deterministic.

if [[ "$DRY_RUN" -eq 1 ]]; then
    if [[ "$VERBOSE" -eq 1 ]]; then
        echo "Files that would be collected (deleted):"
        find "$DIRECTORY" -type f -mtime +"$AGE" -print
    else
        find "$DIRECTORY" -type f -mtime +"$AGE" -print > /dev/null # Suppress output if not verbose
    fi
    echo "Dry run complete. No files were deleted."
else
    if [[ "$VERBOSE" -eq 1 ]]; then
        echo "Collecting (deleting) the following files:"
        find "$DIRECTORY" -type f -mtime +"$AGE" -print -exec rm -v {} \;
        # Using -exec rm -v {} \; for verbose output during deletion
    else
        find "$DIRECTORY" -type f -mtime +"$AGE" -print0 | xargs -0 rm -- || true
    fi
    echo "Cosmic dust collection complete."
fi

exit 0
