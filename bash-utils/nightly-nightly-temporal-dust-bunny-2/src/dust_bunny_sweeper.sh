#!/bin/bash

# Nightly Temporal Dust Bunny Sweeper
# Identifies and helps manage old, unaccessed files (digital dust bunnies) in specified directories.

# --- Configuration ---
ARCHIVE_DIR_NAME=".dust_bunnies_archive"

# --- Functions ---
show_help() {
    echo "Usage: $0 <directory> <age_in_days> [--sweep]"
    echo ""
    echo "  <directory>   : The path to the directory to scan."
    echo "  <age_in_days> : Files not accessed for this many days (or more) will be considered 'dust bunnies'."
    echo "  --sweep       : (Optional) If provided, identified dust bunnies will be moved to a"
    echo "                  '.dust_bunnies_archive' subdirectory within the scanned directory."
    echo "                  If this directory doesn't exist, it will be created."
    echo ""
    echo "Examples:"
    echo "  $0 /var/log 90"
    echo "  $0 ~/old_projects 365 --sweep"
    exit 1
}

# --- Main Logic ---

# Check for minimum arguments
if [ "$#" -lt 2 ]; then
    show_help
fi

TARGET_DIR="$1"
AGE_DAYS="$2"
SWEEP_MODE=false

# Check for --sweep argument
if [ "$#" -ge 3 ] && [ "$3" == "--sweep" ]; then
    SWEEP_MODE=true
fi

# Validate directory
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' not found."
    exit 1
fi

# Validate age_in_days is a positive integer
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [ "$AGE_DAYS" -lt 0 ]; then
    echo "Error: Age in days must be a non-negative integer."
    exit 1
fi

echo "Scanning '$TARGET_DIR' for files not accessed in the last $AGE_DAYS days..."

# Find files
# Using -print0 and xargs -0 for handling filenames with spaces or special characters
DUST_BUNNIES=$(find "$TARGET_DIR" -type f -atime +"$AGE_DAYS" -print0)

if [ -z "$DUST_BUNNIES" ]; then
    echo "No temporal dust bunnies found. Your digital space is sparkling clean!"
    exit 0
fi

if $SWEEP_MODE; then
    ARCHIVE_PATH="$TARGET_DIR/$ARCHIVE_DIR_NAME"
    echo "Sweep mode activated. Moving identified files to '$ARCHIVE_PATH/'..."
    mkdir -p "$ARCHIVE_PATH" || { echo "Error: Could not create archive directory '$ARCHIVE_PATH'."; exit 1; }

    echo "$DUST_BUNNIES" | xargs -0 -I {} mv "{}" "$ARCHIVE_PATH/"
    echo "Moved the following files to '$ARCHIVE_PATH':"
    echo "$DUST_BUNNIES" | tr '\0' '\n' # Print the list of moved files
else
    echo "Found the following temporal dust bunnies (use --sweep to move them):"
    echo "$DUST_BUNNIES" | tr '\0' '\n' # Print the list of found files
fi

exit 0
