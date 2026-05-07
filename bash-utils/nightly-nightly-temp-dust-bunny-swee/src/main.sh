#!/bin/bash

# Default values
TARGET_DIR="/tmp"
AGE_DAYS=7
DRY_RUN=false
VERBOSE=false

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <days>] [-n] [-v] [-h]"
    echo "  -d <directory> : Target directory to sweep (default: $TARGET_DIR)"
    echo "  -a <days>      : Age in days for files/dirs to be considered 'dust bunnies' (default: $AGE_DAYS)"
    echo "  -n             : Dry run (show what would be deleted without deleting)"
    echo "  -v             : Verbose output"
    echo "  -h             : Display this help message"
    exit 1
}

# Parse arguments
while getopts "d:a:nvh" opt; do
    case ${opt} in
        d ) TARGET_DIR=$OPTARG ;;
        a ) AGE_DAYS=$OPTARG ;;
        n ) DRY_RUN=true ;;
        v ) VERBOSE=true ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done
shift $((OPTIND -1))

# Input validation
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist." >&2
    exit 1
fi

if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || (( AGE_DAYS < 0 )); then
    echo "Error: Age in days must be a non-negative integer." >&2
    exit 1
fi

# Safety warning for critical directories
case "$TARGET_DIR" in
    "/" | "/home" | "/etc" | "/usr" | "/var" | "/bin" | "/sbin" | "/lib" | "/boot" | "/dev" | "/proc" | "/sys" )
        echo "Warning: Sweeping critical system directory '$TARGET_DIR' is not recommended. Proceed with extreme caution." >&2
        ;;
esac

echo "--- Nightly Temporal Dust Bunny Sweeper ---"
echo "Targeting directory: $TARGET_DIR"
echo "Sweeping files/directories older than: $AGE_DAYS days"
if $DRY_RUN; then
    echo "Mode: DRY RUN (no files will be deleted)"
else
    echo "Mode: LIVE SWEEP (files WILL be deleted)"
fi
echo "------------------------------------------"

# Find and delete old files/directories
# Using -mtime +N means files/dirs modified more than N*24 hours ago.
# -type f -o -type d finds both files and directories.
# -mindepth 1 -maxdepth 1 ensures only direct children of TARGET_DIR are considered.
# -print0 and xargs -0 handle filenames with spaces or special characters (though -delete is safer).

# Construct the find command base
FIND_BASE_CMD="find \"$TARGET_DIR\" -mindepth 1 -maxdepth 1 -mtime +$AGE_DAYS \( -type f -o -type d \)"

if $DRY_RUN; then
    echo "Files/directories that would be swept:"
    eval "$FIND_BASE_CMD" -print
else
    if $VERBOSE; then
        echo "Sweeping the following temporal dust bunnies:"
        # Using -exec rm -rf {} + for better handling of many files than individual -delete
        eval "$FIND_BASE_CMD" -print -exec rm -rf {} +
    else
        # No verbose output, just delete silently
        eval "$FIND_BASE_CMD" -exec rm -rf {} +
        echo "Temporal dust bunnies swept away!"
    fi
fi

echo "Sweep complete."
