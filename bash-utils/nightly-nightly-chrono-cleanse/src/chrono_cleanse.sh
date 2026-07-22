#!/bin/bash

# Nightly Chrono-Cleanse: A whimsical utility to purge ancient digital dust.

set -euo pipefail

# --- Configuration --- 
DEFAULT_AGE_DAYS=30

# --- Functions ---

# Function to display usage information
usage() {
    echo "Usage: $(basename "$0") [OPTIONS] -d <directory1> [-d <directory2> ...]"
    echo "A whimsical Bash utility to purge ancient digital dust (old files) from specified directories."
    echo ""
    echo "Options:"
    echo "  -d <directory>   Specify a directory to cleanse. Can be used multiple times."
    echo "  -a <age_in_days> Files older than this many days will be targeted. Default: ${DEFAULT_AGE_DAYS} days."
    echo "  -n, --dry-run    Perform a dry run. Report what would be deleted, but don't delete."
    echo "  -h, --help       Display this help message."
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") -n -a 60 -d /var/log -d /tmp"
    echo "  $(basename "$0") -a 7 -d ~/downloads"
    exit 1
}

# --- Main Script Logic ---

# Initialize variables
directories=()
age_days="${DEFAULT_AGE_DAYS}"
dry_run=false

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -d)
            if [[ -z "$2" || "$2" == -* ]]; then
                echo "Error: -d requires a directory path." >&2
                usage
            fi
            directories+=("$2")
            shift # past argument
            shift # past value
            ;;
        -a)
            if ! [[ "$2" =~ ^[0-9]+$ ]]; then
                echo "Error: -a requires a positive integer for age in days." >&2
                usage
            fi
            age_days="$2"
            shift # past argument
            shift # past value
            ;;
        -n|--dry-run)
            dry_run=true
            shift # past argument
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage
            ;;
    esac
done

# Validate input
if [[ ${#directories[@]} -eq 0 ]]; then
    echo "Error: At least one directory must be specified with -d." >&2
    usage
fi

echo "\n--- Initiating Chrono-Cleanse Protocol ---"

for dir in "${directories[@]}"; do
    if [[ ! -d "$dir" ]]; then
        echo "Warning: Directory '$dir' does not exist or is not a directory. Skipping." >&2
        continue
    fi

    echo "\nScanning the temporal archives of '$dir' for digital dust older than ${age_days} days..."

    # Construct the find command
    # -type f: Only consider files (not directories)
    # -mtime +${age_days}: Files whose data was last modified N*24 hours ago.
    # -print: Print the full file name (for dry run)
    # -delete: Delete the files (for actual run)
    
    FIND_CMD="find \"$dir\" -type f -mtime +${age_days}"

    if "$dry_run"; then
        echo "  (Dry Run) These files would be swept into the void:"
        # Use -print0 and xargs -0 for filenames with spaces/special chars
        eval "${FIND_CMD} -print0" | xargs -0 -r -I {} echo "    - {}"
        if [[ $? -ne 0 ]]; then
            echo "    No ancient digital dust found in '$dir' for this dry run. All clear!"
        fi
    else
        echo "  Sweeping away ancient digital dust..."
        # Use -print0 and xargs -0 for safe deletion
        # -r: only run rm if there are files to delete
        eval "${FIND_CMD} -print0" | xargs -0 -r rm -v
        if [[ $? -ne 0 ]]; then
            echo "  No ancient digital dust found in '$dir'. The temporal flow is pristine!"
        fi
    fi
done

echo "\n--- Chrono-Cleanse Protocol Complete. The digital realm is a bit tidier. ---"
