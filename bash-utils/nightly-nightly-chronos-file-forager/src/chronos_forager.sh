#!/bin/bash

# Chronos's File Forager
# Finds and optionally removes files older than a specified number of days.

set -euo pipefail

# Function to display usage information
usage() {
    echo "Usage: $(basename "$0") <directory> <age_in_days> [dry-run|delete]"
    echo ""
    echo "  <directory>    : The path to the directory to forage."
    echo "  <age_in_days>  : Minimum age in full days for files to be considered old."
    echo "  [dry-run|delete]: Action to perform. 'dry-run' (default) lists files, 'delete' removes them."
    echo ""
    echo "Example: $(basename "$0") /var/log 7 dry-run"
    echo "Example: $(basename "$0") /tmp/my_app_cache 30 delete"
    exit 1
}

# Validate arguments
if [[ "$#" -lt 2 || "$#" -gt 3 ]]; then
    usage
fi

DIRECTORY="$1"
AGE_DAYS="$2"
ACTION="${3:-dry-run}" # Default to dry-run if no action specified

# Validate directory exists
if [[ ! -d "$DIRECTORY" ]]; then
    echo "Error: Directory '$DIRECTORY' not found or is not a directory." >&2
    exit 1
fi

# Validate age is a positive integer
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [[ "$AGE_DAYS" -lt 0 ]]; then
    echo "Error: Age in days must be a non-negative integer." >&2
    exit 1
fi

# Validate action
if [[ "$ACTION" != "dry-run" && "$ACTION" != "delete" ]]; then
    echo "Error: Invalid action specified. Must be 'dry-run' or 'delete'." >&2
    usage
fi

echo "Chronos is foraging in: '$DIRECTORY' for files older than $AGE_DAYS day(s)."

# Find files older than AGE_DAYS
# -type f: only regular files
# -mtime +AGE_DAYS: files modified more than AGE_DAYS ago
# -print0: null-terminated output for safety with filenames containing spaces/newlines
# xargs -0: reads null-terminated input

# Mock rationale: For testing, we don't want to actually delete files on the system.
# The test script creates a temporary directory and files, and then runs this script against it.
# The 'rm' command is only executed if ACTION is 'delete' and the test environment is controlled.

if [[ "$ACTION" == "dry-run" ]]; then
    echo "(Dry-run mode: no files will be deleted)"
    find "$DIRECTORY" -type f -mtime +"$AGE_DAYS" -print
    echo "Dry-run complete. No changes made."
elif [[ "$ACTION" == "delete" ]]; then
    echo "(Delete mode: files will be permanently removed!)"
    read -p "Are you sure you want to delete files older than $AGE_DAYS days in '$DIRECTORY'? (y/N): " -n 1 -r
    echo # Move to a new line
    if [[ "$REPLY" =~ ^[Yy]$ ]]; then
        find "$DIRECTORY" -type f -mtime +"$AGE_DAYS" -print0 | xargs -0 rm -v
        echo "Deletion complete."
    else
        echo "Deletion cancelled."
    fi
fi
