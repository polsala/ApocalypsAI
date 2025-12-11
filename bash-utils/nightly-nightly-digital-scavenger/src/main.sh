#!/bin/bash

# Whimsical ASCII art for the scavenger
echo "
  _  _
 /_\\/ \\
( o.o )  Nightly Digital Scavenger
 > ^ <   Initiating digital salvage operation...
"

# Default values
TARGET_DIR=""
STALE_AGE_DAYS=30
DRY_RUN=false
FORCE_DELETE=false

# Function to display usage
usage() {
    echo "Usage: $0 -d <directory> [-a <age_in_days>] [--dry-run] [--force]"
    echo "  -d <directory>   : The directory to scavenge for stale files."
    echo "  -a <age_in_days> : Files older than this many days will be considered stale. Default: 30."
    echo "  --dry-run        : Simulate the scavenging without deleting any files."
    echo "  --force          : Skip confirmation prompt when deleting files (use with caution!)."
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d|--directory)
            TARGET_DIR="$2"
            shift
            ;;
        -a|--age)
            STALE_AGE_DAYS="$2"
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            ;;
        --force)
            FORCE_DELETE=true
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown parameter: $1"
            usage
            ;;
    esac
    shift
done

# Validate TARGET_DIR
if [ -z "$TARGET_DIR" ]; then
    echo "Error: Target directory must be specified."
    usage
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist or is not a directory."
    exit 1
fi

echo "Scavenging for digital relics older than $STALE_AGE_DAYS days in: $TARGET_DIR"

# Find stale files
# Mock rationale: For testing, `find` is a core utility and its behavior is predictable.
# We will create temporary files with specific modification times in the test script.
STALE_FILES=$(find "$TARGET_DIR" -type f -mtime +"$STALE_AGE_DAYS" -print)
FILE_COUNT=$(echo "$STALE_FILES" | wc -l)
if [ -z "$STALE_FILES" ]; then
    FILE_COUNT=0
fi

if [ "$FILE_COUNT" -eq 0 ]; then
    echo "No ancient digital artifacts found. Your archives are surprisingly fresh!"
    exit 0
fi

echo "Found $FILE_COUNT potential relics:"
echo "$STALE_FILES"

if "$DRY_RUN"; then
    echo "--- DRY RUN COMPLETE ---"
    echo "No files were deleted. This was just a reconnaissance mission."
else
    if "$FORCE_DELETE"; then
        echo "Initiating forced salvage operation. No time for pleasantries!"
        # Mock rationale: `rm` is a core utility. In tests, we operate on a temporary directory
        # so actual deletion is safe and verifiable.
        echo "$STALE_FILES" | xargs rm -f
        echo "Salvage complete! $FILE_COUNT digital relics reclaimed."
    else
        echo -n "Proceed with actual salvage (delete these files)? (y/N): "
        # Mock rationale: `read` is a core utility. In tests, we can pipe 'y' or 'N' to stdin
        # to simulate user input deterministically.
        read -r CONFIRMATION
        if [[ "$CONFIRMATION" =~ ^[Yy]$ ]]; then
            echo "Commencing digital reclamation..."
            echo "$STALE_FILES" | xargs rm -f
            echo "Salvage complete! $FILE_COUNT digital relics reclaimed."
        else
            echo "Salvage aborted. The relics remain, for now."
        fi
    fi
fi
