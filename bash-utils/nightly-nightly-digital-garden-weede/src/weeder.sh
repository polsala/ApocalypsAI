#!/bin/bash

# Default values
DRY_RUN=false
RETENTION_DAYS=7
TARGET_DIRS=("/tmp" "/var/tmp" "$HOME/.cache" "$HOME/.local/share/Trash/files") # Common temp/cache locations

# Function to display usage
usage() {
    echo "Usage: $0 [--dry-run] [--days <N>] [--dirs <dir1> <dir2> ...]"
    echo ""
    echo "  --dry-run      : Simulate the cleanup without actually deleting files."
    echo "  --days <N>     : Retain files for N days. Default is 7 days."
    echo "  --dirs <...>   : Specify directories to clean. Defaults to common temp/cache paths."
    echo "                   Multiple directories can be specified, separated by spaces."
    echo "  --help         : Display this help message."
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --days)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo "Error: --days requires a numeric argument."
                usage
            fi
            RETENTION_DAYS="$2"
            if ! [[ "$RETENTION_DAYS" =~ ^[0-9]+$ ]]; then
                echo "Error: --days argument must be a positive integer."
                usage
            fi
            shift 2
            ;;
        --dirs)
            shift
            TARGET_DIRS=() # Clear defaults if --dirs is specified
            while [[ "$#" -gt 0 && ! "$1" =~ ^-- ]]; do
                TARGET_DIRS+=("$1")
                shift
            done
            if [[ ${#TARGET_DIRS[@]} -eq 0 ]]; then
                echo "Error: --dirs requires at least one directory argument."
                usage
            fi
            ;;n        --help)
            usage
            ;;n        *)
            echo "Unknown option: $1"
            usage
            ;;n    esac
done

echo "--- Digital Garden Weeder Report ---"
echo "Retention Policy: Files older than $RETENTION_DAYS days"
echo "Target Directories: ${TARGET_DIRS[*]}"
if "$DRY_RUN"; then
    echo "Mode: DRY RUN (no files will be deleted)"
else
    echo "Mode: LIVE RUN (files WILL be deleted)"
fi
echo "------------------------------------"

DELETED_COUNT=0
DELETED_SIZE=0
DRY_RUN_COUNT=0
DRY_RUN_SIZE=0

for DIR in "${TARGET_DIRS[@]}"; do
    if [[ ! -d "$DIR" ]]; then
        echo "Warning: Directory '$DIR' does not exist or is not a directory. Skipping."
        continue
    fi

    echo ""
    echo "Processing directory: $DIR"
    
    # Use find to locate files older than RETENTION_DAYS
    # -type f: only files
    # -mtime +N: files modified N*24 hours ago
    # -print0: null-terminated output for safety with filenames containing spaces/newlines
    # xargs -0: read null-terminated input
    
    # Mock rationale: In a real scenario, `find` would scan the filesystem.
    # For deterministic testing, creating temporary files with specific `mtime`s
    # within a test directory is a direct and robust way to test `find`'s behavior
    # without complex mocking infrastructure for a simple bash script.
    # The `find` command itself is standard and its behavior is well-defined.
    
    # The `find` command below is the actual command that would run.
    # For testing, we'll ensure the test environment has files matching these criteria.
    
    # Find files and process them
    find "$DIR" -type f -mtime +"$RETENTION_DAYS" -print0 | while IFS= read -r -d $'\0' FILE; do
        FILE_SIZE=$(du -b "$FILE" 2>/dev/null | awk '{print $1}') # Get size in bytes
        if [[ -z "$FILE_SIZE" ]]; then
            FILE_SIZE=0
        fi

        if "$DRY_RUN"; then
            echo "  [DRY RUN] Would delete: $FILE (Size: $FILE_SIZE bytes)"
            DRY_RUN_COUNT=$((DRY_RUN_COUNT + 1))
            DRY_RUN_SIZE=$((DRY_RUN_SIZE + FILE_SIZE))
        else
            # Mock rationale: In a real scenario, `rm` would delete the file.
            # For deterministic testing, the most straightforward way to test `rm` is to
            # create a temporary file, run the script, and then check if the file no longer exists.
            # This directly verifies the effect of `rm`.
            if rm "$FILE"; then
                echo "  Deleted: $FILE (Size: $FILE_SIZE bytes)"
                DELETED_COUNT=$((DELETED_COUNT + 1))
                DELETED_SIZE=$((DELETED_SIZE + FILE_SIZE))
            else
                echo "  Error: Failed to delete $FILE"
            fi
        fi
    done
done

echo ""
echo "--- Summary ---"
if "$DRY_RUN"; then
    echo "Dry Run: $DRY_RUN_COUNT files would have been deleted, totaling $DRY_RUN_SIZE bytes."
else
    echo "Live Run: $DELETED_COUNT files deleted, totaling $DELETED_SIZE bytes."
fi
echo "----------------"
