#!/bin/bash

# Default values
TARGET_PATH="."
AGE_DAYS=90
MODE="list" # or "move"
ARCHIVE_DIR=".digital_debris_archive"

# Function to display usage
usage() {
    echo "Usage: $0 [-p <path>] [-a <age_days>] [-m <mode>]"
    echo "  -p <path>     : Target directory to scan (default: current directory)"
    echo "  -a <age_days> : Files/directories older than this many days (default: 90)"
    echo "  -m <mode>     : Action mode: 'list' (default) or 'move'"
    echo "                  'list': Lists files/dirs that qualify."
    echo "                  'move': Moves qualifying files/dirs to '$ARCHIVE_DIR' within TARGET_PATH."
    exit 1
}

# Parse arguments
while getopts "p:a:m:h" opt; do
    case ${opt} in
        p ) TARGET_PATH=$OPTARG ;;
        a ) AGE_DAYS=$OPTARG ;;
        m ) MODE=$OPTARG ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done

# Validate mode
if [[ "$MODE" != "list" && "$MODE" != "move" ]]; then
    echo "Error: Invalid mode '$MODE'. Must be 'list' or 'move'."
    usage
fi

echo "--- Nightly Digital Debris Disperser ---"
echo "Scanning '$TARGET_PATH' for digital debris older than $AGE_DAYS days (based on modification time)."

# Find old files
OLD_FILES=$(find "$TARGET_PATH" -type f -mtime +"$AGE_DAYS" 2>/dev/null)
# Find old empty directories
OLD_EMPTY_DIRS=$(find "$TARGET_PATH" -type d -empty -mtime +"$AGE_DAYS" 2>/dev/null)

if [[ -z "$OLD_FILES" && -z "$OLD_EMPTY_DIRS" ]]; then
    echo "No ancient digital debris found. Your digital realm is surprisingly tidy!"
    exit 0
fi

if [[ "$MODE" == "list" ]]; then
    echo ""
    echo "Whispers from the past (files):"
    if [[ -n "$OLD_FILES" ]]; then
        echo "$OLD_FILES" | sed 's/^/  - /'
    else
        echo "  (None)"
    fi

    echo ""
    echo "Echoes of forgotten spaces (empty directories):"
    if [[ -n "$OLD_EMPTY_DIRS" ]]; then
        echo "$OLD_EMPTY_DIRS" | sed 's/^/  - /'
    else
        echo "  (None)"
    fi
    echo ""
    echo "Consider running with '-m move' to relocate this debris to the temporal attic."

elif [[ "$MODE" == "move" ]]; then
    ARCHIVE_FULL_PATH="$TARGET_PATH/$ARCHIVE_DIR"
    echo ""
    echo "Preparing the temporal attic at: $ARCHIVE_FULL_PATH"
    mkdir -p "$ARCHIVE_FULL_PATH"

    if [[ -n "$OLD_FILES" ]]; then
        echo "Relocating ancient files to the temporal attic..."
        echo "$OLD_FILES" | while IFS= read -r file; do
            if [[ -f "$file" ]]; then
                echo "  Moving: $file"
                mv "$file" "$ARCHIVE_FULL_PATH/"
            fi
        done
    else
        echo "No ancient files to relocate."
    fi

    if [[ -n "$OLD_EMPTY_DIRS" ]]; then
        echo "Sweeping away forgotten empty spaces..."
        # Sort in reverse to delete deepest directories first
        echo "$OLD_EMPTY_DIRS" | sort -r | while IFS= read -r dir; do
            # Re-check if directory is empty, as files might have been moved out of it
            if [[ -d "$dir" && -z "$(ls -A "$dir" 2>/dev/null)" ]]; then
                echo "  Removing empty directory: $dir"
                rmdir "$dir"
            elif [[ -d "$dir" ]]; then
                echo "  Skipping non-empty directory: $dir"
            fi
        done
    else
        echo "No forgotten empty spaces to sweep."
    fi
    echo ""
    echo "Digital debris dispersed! Your realm is now a bit tidier."
fi
