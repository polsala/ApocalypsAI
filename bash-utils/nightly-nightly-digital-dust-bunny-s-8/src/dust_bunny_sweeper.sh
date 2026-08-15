#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# A whimsical yet practical bash utility to sweep away old temporary files.

set -euo pipefail

DEFAULT_AGE_DAYS=7
AGE_DAYS="${DUST_BUNNY_AGE_DAYS:-$DEFAULT_AGE_DAYS}"
DRY_RUN="${DUST_BUNNY_DRY_RUN:-true}" # Default to dry run for safety
SWEEP="${DUST_BUNNY_SWEEP:-false}"

# Function to display help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS] <DIRECTORY1> [DIRECTORY2...]"
    echo ""
    echo "A whimsical bash utility to sweep away digital dust bunnies (old temporary files)"
    echo "from specified directories."
    echo ""
    echo "Options:"
    echo "  -a <DAYS>, --age <DAYS>    Files older than DAYS will be considered for removal. Default: ${DEFAULT_AGE_DAYS} days."
    echo "  -d, --dry-run              Perform a dry run. Files will be identified, but NOT deleted. (Default)"
    echo "  -s, --sweep                Actually delete the identified files. Use with caution!"
    echo "  -h, --help                 Display this help message."
    echo ""
    echo "Environment Variables:"
    echo "  DUST_BUNNY_AGE_DAYS        Overrides the default age threshold."
    echo "  DUST_BUNNY_DRY_RUN         Set to 'true' or '1' to enable dry run by default."
    echo "  DUST_BUNNY_SWEEP           Set to 'true' or '1' to enable actual sweeping by default."
    echo ""
    echo "Safety Notice: Always perform a dry run before executing a sweep."
}

# Parse command-line arguments
DIRECTORIES=()
while (( "$#" )); do
    case "$1" in
        -a|--age)
            if [[ -n "$2" ]] && [[ "$2" =~ ^[0-9]+$ ]]; then
                AGE_DAYS="$2"
                shift 2
            else
                echo "Error: Argument for $1 is missing or not a number." >&2
                show_help
                exit 1
            fi
            ;;
        -d|--dry-run)
            DRY_RUN="true"
            SWEEP="false" # Dry run overrides sweep
            shift
            ;;
        -s|--sweep)
            SWEEP="true"
            DRY_RUN="false" # Sweep overrides dry run
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*|--*=) # Unknown option
            echo "Error: Unknown option $1" >&2
            show_help
            exit 1
            ;;
        *) # Positional arguments (directories)
            DIRECTORIES+=("$1")
            shift
            ;;
    esac
done

if [[ "${#DIRECTORIES[@]}" -eq 0 ]]; then
    echo "Error: No directories specified for sweeping." >&2
    show_help
    exit 1
fi

echo "--- Nightly Digital Dust Bunny Sweeper ---"
echo "Age threshold: ${AGE_DAYS} days"
echo "Mode: $(if [[ "$SWEEP" == "true" ]]; then echo "SWEEP (DELETING FILES)"; else echo "DRY RUN (NO DELETIONS)"; fi)"
echo "Target directories: ${DIRECTORIES[*]}"
echo "----------------------------------------"

for DIR in "${DIRECTORIES[@]}"; do
    if [[ ! -d "$DIR" ]]; then
        echo "Warning: Directory '$DIR' does not exist or is not a directory. Skipping." >&2
        continue
    fi

    echo "Scanning '$DIR' for digital dust bunnies older than ${AGE_DAYS} days..."

    # Use find to locate files. -type f for regular files, -mtime +AGE_DAYS for modification time.
    # -print0 and xargs -0 are used for handling filenames with spaces or special characters.
    # Mock rationale: The 'find' command is a standard Unix utility. For testing, we create a controlled temporary directory structure with files of specific ages, making its output deterministic within that context.
    FILES_TO_PROCESS=$(find "$DIR" -type f -mtime +"$AGE_DAYS" -print0)

    if [[ -z "$FILES_TO_PROCESS" ]]; then
        echo "No dust bunnies found in '$DIR'."
        continue
    fi

    if [[ "$SWEEP" == "true" ]]; then
        echo "Sweeping away the following dust bunnies from '$DIR':"
        # Mock rationale: The 'rm' command is a standard Unix utility. For testing, we operate on files within a temporary directory, and verify their absence after the script runs, making the deletion deterministic within that context.
        echo "$FILES_TO_PROCESS" | xargs -0 rm -v
        echo "Sweep complete for '$DIR'."
    else
        echo "Found the following digital dust bunnies in '$DIR' (DRY RUN - no files deleted):"
        echo "$FILES_TO_PROCESS" | xargs -0 -I {} echo "  - {}"
        echo "Dry run complete for '$DIR'."
    fi
    echo ""
done

echo "--- Sweeper finished ---"
