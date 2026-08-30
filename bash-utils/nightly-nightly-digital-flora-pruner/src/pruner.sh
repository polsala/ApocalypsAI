#!/bin/bash

# Nightly Digital Flora Pruner - Tending to your digital garden

# Function to display usage instructions
usage() {
    echo "Usage: $0 -d <directory> -a <age_in_days> [-n] [-f]"
    echo "  -d <directory>: The digital garden path to tend." >&2
    echo "  -a <age_in_days>: Files older than this many days (by last access time) will be considered withered." >&2
    echo "  -n: Dry run. Show what would be pruned without actually doing it." >&2
    echo "  -f: Force pruning without confirmation." >&2
    exit 1
}

# --- Argument Parsing ---
DIRECTORY=""
AGE_DAYS=""
DRY_RUN=0
FORCE=0

while getopts "d:a:nf" opt; do
    case ${opt} in
        d ) DIRECTORY=$OPTARG ;;
        a ) AGE_DAYS=$OPTARG ;;
        n ) DRY_RUN=1 ;;
        f ) FORCE=1 ;;
        \? ) usage ;;
    esac
done

# Validate required arguments
if [ -z "$DIRECTORY" ] || [ -z "$AGE_DAYS" ]; then
    echo "Error: Both -d (directory) and -a (age) are required." >&2
    usage
fi

# Validate directory existence
if [ ! -d "$DIRECTORY" ]; then
    echo "Error: Digital garden path '$DIRECTORY' not found. Please provide a valid directory." >&2
    exit 1
fi

# Validate age is a positive integer
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [ "$AGE_DAYS" -lt 0 ]; then
    echo "Error: Age must be a non-negative integer." >&2
    exit 1
fi

# --- Pruning Logic ---

echo "🌿 Tending to the digital garden at '$DIRECTORY'..."
echo "🔍 Identifying withered digital flora older than $AGE_DAYS days (by last access time)..."

# Find files older than AGE_DAYS by access time
# Using -print0 and xargs -0 for safe handling of filenames with spaces or special characters.
PRUNABLE_FLORA_LIST=$(find "$DIRECTORY" -type f -atime +"$AGE_DAYS" -print0)

# Count the number of files found
NUM_FLORA=0
if [ -n "$PRUNABLE_FLORA_LIST" ]; then
    NUM_FLORA=$(echo "$PRUNABLE_FLORA_LIST" | tr -d '\0' | wc -l)
fi

if [ "$NUM_FLORA" -eq 0 ]; then
    echo "✨ No withered digital flora found. Your garden is pristine!"
    exit 0
fi

echo "Found $NUM_FLORA withered digital leaves to consider for pruning:"
# Display the list of files, replacing null terminators with newlines for readability
echo "$PRUNABLE_FLORA_LIST" | tr '\0' '\n'

if [ "$DRY_RUN" -eq 1 ]; then
    echo "🌳 This was a dry run. No digital flora were pruned. The garden remains untouched."
    exit 0
fi

if [ "$FORCE" -eq 0 ]; then
    read -p "Proceed with pruning these digital leaves? (y/N): " CONFIRM
    if [[ ! "$CONFIRM" =~ ^[yY]$ ]]; then
        echo "🚫 Pruning cancelled. The digital garden remains as is." >&2
        exit 0
    fi
fi

echo "✂️ Pruning withered digital leaves..."
# Use xargs -0 with rm -v for verbose and safe deletion
echo "$PRUNABLE_FLORA_LIST" | xargs -0 rm -v

echo "✅ Digital garden tended. May your bits flourish!"
