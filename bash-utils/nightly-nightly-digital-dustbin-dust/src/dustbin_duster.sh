#!/bin/bash

# Default values
TARGET_DIR="${1:-/tmp}" # Use first argument, or /tmp if none
DAYS_OLD="${2:-7}"      # Use second argument, or 7 days if none
DRY_RUN=false
EULOGIES=(
    "Farewell, digital dust bunny. May your bits find peace in the great beyond."
    "Into the void you go, little file. May your next incarnation be more useful."
    "A silent whisper, a forgotten byte. Your time has come, goodnight, goodnight."
    "Your purpose served, your data spent. Adieu, digital transient."
    "May your inodes rest in peace, and your blocks find release."
)

# Function to display usage
usage() {
    echo "Usage: $0 [DIRECTORY] [DAYS_OLD] [--dry-run]"
    echo "  DIRECTORY: The directory to scan for old files (default: /tmp)"
    echo "  DAYS_OLD: Files older than this many days will be considered (default: 7)"
    echo "  --dry-run: Simulate deletion without actually removing files."
    exit 1
}

# Parse arguments
for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            # Positional arguments
            if [[ -z "$TARGET_DIR_SET" ]]; then
                TARGET_DIR="$arg"
                TARGET_DIR_SET=true
            elif [[ -z "$DAYS_OLD_SET" ]]; then
                DAYS_OLD="$arg"
                DAYS_OLD_SET=true
            else
                echo "Unknown argument: $arg"
                usage
            fi
            shift
            ;;
    esac
done

# Validate inputs
if ! [[ "$DAYS_OLD" =~ ^[0-9]+$ ]]; then
    echo "Error: DAYS_OLD must be a positive integer."
    usage
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Directory '$TARGET_DIR' not found."
    exit 1
fi

echo "--- Nightly Digital Dustbin Duster ---"
echo "Scanning '$TARGET_DIR' for files older than $DAYS_OLD days..."
echo ""

# Find old files, excluding directories themselves
# Mock rationale: `find` is a standard utility; its behavior is predictable.
# We will mock its output in tests to control which files are "found".
OLD_FILES=$(find "$TARGET_DIR" -type f -mtime +"$DAYS_OLD" 2>/dev/null)

if [[ -z "$OLD_FILES" ]]; then
    echo "No digital dust bunnies found. Your system is remarkably tidy!"
    exit 0
fi

echo "Found the following forgotten digital artifacts:"
echo "$OLD_FILES" | while IFS= read -r file; do
    # Mock rationale: `shuf` is used for random selection. In tests, we will mock `shuf`
    # to always return the first eulogy for deterministic output.
    EULOGY=$(printf "%s\n" "${EULOGIES[@]}" | shuf -n 1)
    echo ""
    echo "  File: $file"
    echo "  Whisper: \"$EULOGY\""
    echo "  Action: $(if $DRY_RUN; then echo "Would delete"; else echo "Pending deletion"; fi)"
done

echo ""
if $DRY_RUN; then
    echo "This was a dry run. No files were actually deleted."
    exit 0
fi

read -p "Proceed with deletion of these files? (y/N): " -n 1 -r
echo "" # Newline after input

if [[ "$REPLY" =~ ^[Yy]$ ]]; then
    echo "Initiating digital cleansing..."
    echo "$OLD_FILES" | while IFS= read -r file; do
        # Mock rationale: `rm` is the core action. In tests, we will mock `rm`
        # to verify it's called with the correct arguments without actual deletion.
        if rm "$file"; then
            echo "  [DELETED] $file"
        else
            echo "  [FAILED]  $file (Permission denied or other error)"
        fi
    done
    echo "Digital dustbin dusted!"
else
    echo "Aborting. The digital ghosts live to see another day."
fi
