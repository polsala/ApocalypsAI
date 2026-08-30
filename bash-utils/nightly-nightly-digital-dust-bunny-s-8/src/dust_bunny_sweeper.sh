#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# A whimsical Bash utility to identify and sweep away old, unaccessed files.

# --- Configuration ---
# Default archive directory name if not specified
DEFAULT_ARCHIVE_SUBDIR="digital_dust_bunnies_archive"

# --- Functions ---

# Display usage information
usage() {
    echo "Usage: $0 <target_directory> <days_old> [archive_directory] [--dry-run]"
    echo ""
    echo "  <target_directory> : The directory to scan for digital dust bunnies."
    echo "  <days_old>         : Minimum age (in days, based on last access time) for a file to be considered a dust bunny."
    echo "  [archive_directory]: Optional. If provided, identified files will be moved here. If omitted, only lists files."
    echo "  --dry-run          : Optional. If present, only lists files and reports what *would* happen, no actual moves."
    echo ""
    echo "Examples:"
    echo "  $0 /var/log 30"
    echo "  $0 ~/Downloads 90 --dry-run"
    echo "  $0 /tmp/old_stuff 7 /tmp/archive"
    exit 1
}

# Log messages with a whimsical touch
log_whimsical() {
    local message="$1"
    echo "✨🧹 ApocalypsAI Sweeper: $message"
}

# --- Main Script ---

# Parse arguments
TARGET_DIR="$1"
DAYS_OLD="$2"
ARCHIVE_DIR=""
DRY_RUN=0

# Shift arguments to handle optional archive_directory and --dry-run
shift 2
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=1
            ;;
        *)
            if [[ -z "$ARCHIVE_DIR" ]]; then
                ARCHIVE_DIR="$1"
            else
                log_whimsical "Error: Too many arguments. Unexpected: '$1'"
                usage
            fi
            ;;
    esac
    shift
done

# Validate inputs
if [[ -z "$TARGET_DIR" || -z "$DAYS_OLD" ]]; then
    log_whimsical "Error: Missing required arguments."
    usage
fi

if ! [[ "$DAYS_OLD" =~ ^[0-9]+$ ]] || [[ "$DAYS_OLD" -lt 0 ]]; then
    log_whimsical "Error: <days_old> must be a non-negative integer."
    usage
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    log_whimsical "Error: Target directory '$TARGET_DIR' does not exist or is not a directory."
    exit 1
fi

# Determine if it's a dry run or actual sweep
if [[ -z "$ARCHIVE_DIR" ]]; then
    DRY_RUN=1 # If no archive directory is specified, it's implicitly a dry run
    log_whimsical "No archive directory specified. Performing a dry run to list digital dust bunnies."
elif [[ "$DRY_RUN" -eq 1 ]]; then
    log_whimsical "Dry run requested. Will only list digital dust bunnies, no files will be moved."
else
    log_whimsical "Preparing to sweep digital dust bunnies into '$ARCHIVE_DIR'."
    # Create archive directory if it doesn't exist
    if [[ ! -d "$ARCHIVE_DIR" ]]; then
        log_whimsical "Creating archive directory: '$ARCHIVE_DIR'"
        mkdir -p "$ARCHIVE_DIR" || { log_whimsical "Error: Could not create archive directory '$ARCHIVE_DIR'. Check permissions."; exit 1; }
    fi
fi

log_whimsical "Scanning '$TARGET_DIR' for files not accessed in the last $DAYS_OLD days..."

# Find files older than DAYS_OLD based on access time
# Using -print0 and xargs -0 for robust handling of filenames with spaces/special characters
# Mock rationale: In tests, 'find' will be mocked to return predefined paths.
# In production, this uses the real 'find' command.
FOUND_FILES=$(find "$TARGET_DIR" -type f -atime +"$DAYS_OLD" -print0)

if [[ -z "$FOUND_FILES" ]]; then
    log_whimsical "No digital dust bunnies found in '$TARGET_DIR' older than $DAYS_OLD days. Your digital space is sparkling clean!"
    exit 0
fi

log_whimsical "Found the following digital dust bunnies:"
echo "$FOUND_FILES" | xargs -0 -I {} echo "  - {}"

if [[ "$DRY_RUN" -eq 1 ]]; then
    log_whimsical "Dry run complete. No files were moved. To sweep them, provide an archive directory without --dry-run."
else
    log_whimsical "Initiating sweep! Moving digital dust bunnies to '$ARCHIVE_DIR/'..."
    echo "$FOUND_FILES" | xargs -0 -I {} mv "{}" "$ARCHIVE_DIR/" || { log_whimsical "Error: Failed to move some files. Check permissions or disk space."; exit 1; }
    log_whimsical "Sweep complete! All identified digital dust bunnies have been moved to '$ARCHIVE_DIR'."
fi

exit 0
