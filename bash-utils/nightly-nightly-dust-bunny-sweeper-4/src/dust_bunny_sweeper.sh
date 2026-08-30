#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

# Default age for dust bunnies (in days)
DEFAULT_AGE_DAYS=7
DRY_RUN=false
DIRECTORIES=()

# Function to display usage
usage() {
    echo "Usage: $0 <age_in_days> [directory1] [directory2] ... [--dry-run]"
    echo ""
    echo "Sweeps away old, forgotten files (digital dust bunnies) from specified directories."
    echo "Files older than <age_in_days> will be considered dust bunnies."
    echo "If no directories are specified, the current directory will be swept."
    echo ""
    echo "Options:"
    echo "  --dry-run   : Simulate the sweep without actually deleting files."
    echo ""
    echo "Example:"
    echo "  $0 30 /var/log /tmp --dry-run"
    echo "  $0 7 ~/Downloads"
    exit 1
}

# Parse arguments
if [[ "$#" -eq 0 ]]; then
    usage
fi

AGE_DAYS="$1"
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]]; then
    echo "Error: <age_in_days> must be a positive integer."
    usage
fi
shift

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            if [[ -d "$1" ]]; then
                DIRECTORIES+=("$1")
            else
                echo "Warning: Directory '$1' does not exist or is not a directory. Skipping."
            fi
            shift
            ;;
    esac
done

# If no directories were specified after parsing, use current directory
if [[ "${#DIRECTORIES[@]}" -eq 0 ]]; then
    DIRECTORIES+=(".")
fi

echo "✨ Initiating Nightly Digital Dust Bunny Sweep! ✨"
echo "Targeting files older than $AGE_DAYS days."
if "$DRY_RUN"; then
    echo "--- DRY RUN MODE: No files will be deleted. ---"
fi
echo ""

TOTAL_FILES_SWEPT=0
TOTAL_SPACE_RECLAIMED=0

for DIR in "${DIRECTORIES[@]}"; do
    echo "🗑️ Sweeping through the digital corners of: $DIR"

    # Find files older than AGE_DAYS
    # Using -type f to only target files, not directories
    # Using -print0 for safe handling of filenames with spaces/special chars
    # Mock rationale: In tests, 'find' will be mocked to return predefined file paths.
    FILES_TO_SWEEP=$(find "$DIR" -type f -mtime +"$AGE_DAYS" -print0)

    if [[ -z "$FILES_TO_SWEEP" ]]; then
        echo "  No ancient digital dust bunnies found here. All clear! 🌟"
        continue
    fi

    DIR_FILES_SWEPT=0
    DIR_SPACE_RECLAIMED=0

    # Read null-separated filenames
    while IFS= read -r -d $'\0' FILE; do
        if [[ -f "$FILE" ]]; then # Double check if it's still a file (might be deleted by another process)
            FILE_SIZE=$(du -b "$FILE" 2>/dev/null | awk '{print $1}') # Mock rationale: 'du' will be mocked to return a fixed size.
            if [[ -n "$FILE_SIZE" ]]; then
                DIR_SPACE_RECLAIMED=$((DIR_SPACE_RECLAIMED + FILE_SIZE))
            fi

            echo "  Found a dusty relic: $FILE (Size: $(numfmt --to=iec-i --suffix=B --format="%.1f" "$FILE_SIZE"))"
            if ! "$DRY_RUN"; then
                # Mock rationale: 'rm' will be mocked to prevent actual deletion during tests.
                rm "$FILE"
                if [[ "$?" -eq 0 ]]; then
                    echo "    -> Gently ushered into the void. ✨"
                    DIR_FILES_SWEPT=$((DIR_FILES_SWEPT + 1))
                else
                    echo "    -> Failed to usher into the void. 🚧"
                fi
            fi
        fi
    done <<< "$FILES_TO_SWEEP"

    echo "--- Sweep Summary for $DIR ---"
    echo "  Digital dust bunnies found and processed: $DIR_FILES_SWEPT"
    echo "  Digital fluff reclaimed: $(numfmt --to=iec-i --suffix=B --format="%.1f" "$DIR_SPACE_RECLAIMED")"
    echo ""

    TOTAL_FILES_SWEPT=$((TOTAL_FILES_SWEPT + DIR_FILES_SWEPT))
    TOTAL_SPACE_RECLAIMED=$((TOTAL_SPACE_RECLAIMED + DIR_SPACE_RECLAIMED))
done

echo "--- Grand Sweep Finale! ---"
echo "Total digital dust bunnies swept across all realms: $TOTAL_FILES_SWEPT"
echo "Total digital fluff (disk space) reclaimed: $(numfmt --to=iec-i --suffix=B --format="%.1f" "$TOTAL_SPACE_RECLAIMED")"
echo "May your digital spaces remain pristine! 💖"
