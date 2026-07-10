#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

# Default values
DEFAULT_AGE_DAYS=30
DRY_RUN=true
FORCE_DELETE=false
TARGET_DIRS=()

# Whimsical messages
MESSAGES=(
    "Scanning for forgotten digital dust bunnies..."
    "Unearthing ancient byte-fluff..."
    "Dusting off the digital shelves..."
    "Searching for relics of forgotten processes..."
    "The digital broom is ready!"
)

# Function to display help
show_help() {
    echo "Usage: $0 [OPTIONS] <DIRECTORY1> [DIRECTORY2...>"
    echo ""
    echo "A whimsical utility to find and optionally remove old, forgotten files (digital dust bunnies) from specified directories."
    echo ""
    echo "Options:"
    echo "  -a, --age <DAYS>    Files older than <DAYS> will be considered dust bunnies. Default: ${DEFAULT_AGE_DAYS} days."
    echo "  -f, --force         Automatically confirm deletion without prompt (use with caution!)."
    echo "  -c, --clean         Perform actual deletion (default is dry-run)."
    echo "  -h, --help          Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 /tmp /var/log"
    echo "  $0 -a 7 -c /home/user/downloads"
    echo "  $0 --force --clean /var/cache"
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -a|--age)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo "Error: --age requires a numeric argument." >&2
                exit 1
            fi
            if ! [[ "$2" =~ ^[0-9]+$ ]]; then
                echo "Error: --age argument must be a positive integer." >&2
                exit 1
            fi
            DEFAULT_AGE_DAYS="$2"
            shift
            ;;
        -f|--force)
            FORCE_DELETE=true
            ;;
        -c|--clean)
            DRY_RUN=false
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "Error: Unknown option '$1'" >&2
            show_help
            exit 1
            ;;
        *)
            TARGET_DIRS+=("$1")
            ;;
    esac
    shift
done

if [[ ${#TARGET_DIRS[@]} -eq 0 ]]; then
    echo "Error: No directories specified." >&2
    show_help
    exit 1
fi

echo "${MESSAGES[$RANDOM % ${#MESSAGES[@]}]}"
echo "Looking for files older than ${DEFAULT_AGE_DAYS} days in: ${TARGET_DIRS[*]}"
[[ "$DRY_RUN" == "true" ]] && echo "Running in DRY-RUN mode. No files will be deleted."

DUST_BUNNIES=()
for dir in "${TARGET_DIRS[@]}"; do
    if [[ ! -d "$dir" ]]; then
        echo "Warning: Directory '$dir' does not exist or is not a directory. Skipping." >&2
        continue
    fi
    echo "  Entering the dusty corners of '$dir'..."
    # Mock rationale: In tests, `find` is mocked to return predictable paths.
    # In production, this finds files older than N days, excluding directories.
    # The `-print0` and `mapfile -d ''` are for handling filenames with spaces/special characters.
    mapfile -t -d '' found_files < <(find "$dir" -type f -mtime +"$DEFAULT_AGE_DAYS" -print0 2>/dev/null)
    if [[ ${#found_files[@]} -gt 0 ]]; then
        DUST_BUNNIES+=("${found_files[@]}")
    fi
done

if [[ ${#DUST_BUNNIES[@]} -eq 0 ]]; then
    echo "Hooray! No digital dust bunnies found. Your directories are sparkling clean!"
    exit 0
fi

echo ""
echo "Found ${#DUST_BUNNIES[@]} digital dust bunnies:"
for bunny in "${DUST_BUNNIES[@]}"; do
    echo "  - $bunny"
done
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
    echo "Dry-run complete. These files *would* have been swept away."
    exit 0
fi

if [[ "$FORCE_DELETE" == "false" ]]; then
    read -p "Do you wish to sweep these digital dust bunnies away? (y/N): " -n 1 -r
    echo ""
    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
        echo "Phew! Digital dust bunnies spared. They live to gather another day."
        exit 0
    fi
fi

echo "Sweeping away the digital dust bunnies..."
for bunny in "${DUST_BUNNIES[@]}"; do
    # Mock rationale: In tests, `rm` is mocked to log deletions instead of actual removal.
    rm -f "$bunny"
    if [[ $? -eq 0 ]]; then
        echo "  [SWEPT] $bunny"
    else
        echo "  [FAILED] Could not sweep $bunny" >&2
    fi
done

echo "Digital dust bunny sweeping complete! Your directories are now a bit tidier."
