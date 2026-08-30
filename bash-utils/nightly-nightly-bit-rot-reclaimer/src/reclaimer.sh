#!/bin/bash

# Nightly Bit Rot Reclaimer
# A utility to identify and suggest 'reclaiming' digital space by listing files
# susceptible to 'bit rot' (old or large files) for review.

DEFAULT_PATH="."
DEFAULT_AGE=365 # days
DEFAULT_SIZE=100 # MB

SCAN_PATH="$DEFAULT_PATH"
MIN_AGE_DAYS="$DEFAULT_AGE"
MIN_SIZE_MB="$DEFAULT_SIZE"
DRY_RUN=0

# Function to display help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo "A utility to identify and suggest 'reclaiming' digital space by listing files"
    echo "susceptible to 'bit rot' (old or large files) for review."
    echo "\nOptions:"
    echo "  --path <directory>  The directory to scan. Defaults to '$DEFAULT_PATH'."
    echo "  --age <days>        Files older than this many days (based on modification time) will be considered. Defaults to '$DEFAULT_AGE' days."
    echo "  --size <MB>         Files larger than this many megabytes will be considered. Defaults to '$DEFAULT_SIZE' MB."
    echo "  --dry-run           Only print the command that would be executed, without running find."
    echo "  --help              Display this help message."
    exit 0
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        --path)
        SCAN_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        --age)
        MIN_AGE_DAYS="$2"
        shift # past argument
        shift # past value
        ;;
        --size)
        MIN_SIZE_MB="$2"
        shift # past argument
        shift # past value
        ;;
        --dry-run)
        DRY_RUN=1
        shift # past argument
        ;;
        --help)
        show_help
        ;;
        *)
        echo "Unknown option: $1"
        show_help
        ;;
    esac
done

# Validate path
if [ ! -d "$SCAN_PATH" ]; then
    echo "Error: Directory '$SCAN_PATH' not found." >&2
    exit 1
fi

# Construct the find command
# Using -mtime for modification time, +N means older than N days
# Using -size for file size, +NC means larger than N*C bytes (e.g., +100M for 100MB)
FIND_CMD="find \"$SCAN_PATH\" -type f \( -mtime +${MIN_AGE_DAYS} -o -size +${MIN_SIZE_MB}M \) -print0"

if [ "$DRY_RUN" -eq 1 ]; then
    echo "Dry run: The following command would be executed:"
    echo "  $FIND_CMD"
    exit 0
fi

echo "Reclamation Report for '$SCAN_PATH':"
echo "--------------------------------------"
echo "Potential Bit Rot Candidates (Older than ${MIN_AGE_DAYS} days OR Larger than ${MIN_SIZE_MB} MB):\n"

# Execute the find command and process results
# Using -print0 and read -d '' for safe handling of filenames with spaces or special characters
# Mock rationale: `stat` command output format can vary slightly between systems (e.g., Linux vs macOS).
# For deterministic tests, we will mock the `stat` output or rely on `find`'s output directly
# and verify file paths, assuming `stat` would provide correct info in a real environment.

# Execute find and process results directly
# Using process substitution to feed null-separated output to while loop
while IFS= read -r -d '' file; do
    if [ -f "$file" ]; then
        # Check if GNU stat is available (for --format option)
        if stat --version >/dev/null 2>&1; then
            # GNU stat (Linux)
            FILE_SIZE_BYTES=$(stat -c "%s" "$file")
            MOD_DATE=$(stat -c "%y" "$file" | cut -d' ' -f1)
        else
            # BSD stat (macOS)
            FILE_SIZE_BYTES=$(stat -f "%z" "$file")
            MOD_DATE=$(stat -f "%m" "$file" | xargs -I {} date -r {} +%Y-%m-%d)
        fi

        # Convert bytes to human-readable format (simplified for MB/GB)
        if (( FILE_SIZE_BYTES > 1024*1024*1024 )); then
            HUMAN_SIZE=$(awk "BEGIN {printf \"%.1fG\", $FILE_SIZE_BYTES / (1024*1024*1024)}")
        elif (( FILE_SIZE_BYTES > 1024*1024 )); then
            HUMAN_SIZE=$(awk "BEGIN {printf \"%.1fM\", $FILE_SIZE_BYTES / (1024*1024)}")
        else
            HUMAN_SIZE=$(awk "BEGIN {printf \"%.1fK\", $FILE_SIZE_BYTES / 1024}")
        fi

        echo "[ ] $file (${HUMAN_SIZE}, last modified ${MOD_DATE})"
    fi
done < <(eval "$FIND_CMD")

echo "\nTo reclaim space, consider archiving or deleting checked files."
