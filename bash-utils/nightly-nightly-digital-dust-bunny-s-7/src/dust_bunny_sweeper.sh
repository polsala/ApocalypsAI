#!/bin/bash

# Default configuration
TARGET_DIRS=("/tmp" "/var/log" "$HOME/.cache") # Directories to scan
MAX_AGE_DAYS=7                                 # Files older than this will be considered dust bunnies
DRY_RUN=true                                   # Default to dry run
VERBOSE=false                                  # Verbose output

# --- Internal functions (can be overridden for testing) ---

# Mock rationale: This function wraps the 'find' command. In tests, it will be overridden
# to return predefined file paths, avoiding actual filesystem scans and ensuring determinism.
_find_old_files() {
    local dir="$1"
    local age="$2"
    find "$dir" -type f -mtime +"$age" -print 2>/dev/null
}

# Mock rationale: This function wraps the 'rm' command. In tests, it will be overridden
# to log deletion attempts to a mock file instead of actually deleting files, ensuring
# tests are non-destructive and deterministic.
_delete_file() {
    local file="$1"
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "DRY RUN: Would delete: $file"
    else
        if [[ "$VERBOSE" == "true" ]]; then
            echo "Deleting: $file"
        fi
        rm "$file"
    fi
}

# --- Main script logic ---

usage() {
    echo "Usage: $0 [-d <dir>] [-a <days>] [-r] [-v] [-h]"
    echo "  -d <dir>  : Add a directory to scan (can be used multiple times). Defaults: ${TARGET_DIRS[*]}"
    echo "  -a <days> : Max age in days for files to be considered dust bunnies. Defaults: $MAX_AGE_DAYS"
    echo "  -r        : Run for real (perform deletions). Default is dry run."
    echo "  -v        : Verbose output."
    echo "  -h        : Show this help message."
    echo ""
    echo "Environment variables can also configure defaults:"
    echo "  DUST_BUNNY_DIRS     : Space-separated list of directories."
    echo "  DUST_BUNNY_MAX_AGE  : Max age in days."
    echo "  DUST_BUNNY_REAL_RUN : Set to 'true' to enable real deletions."
    exit 1
}

# Parse command line arguments
while getopts "d:a:rvh" opt; do
    case "$opt" in
        d)
            if [[ -z "$_CUSTOM_DIRS_SET" ]]; then
                TARGET_DIRS=() # Clear defaults if -d is used
                _CUSTOM_DIRS_SET=true
            fi
            TARGET_DIRS+=("$OPTARG")
            ;;
        a)
            MAX_AGE_DAYS="$OPTARG"
            ;;
        r)
            DRY_RUN=false
            ;;
        v)
            VERBOSE=true
            ;;
        h)
            usage
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

# Apply environment variable overrides if not set by command line
if [[ -n "$DUST_BUNNY_DIRS" && -z "$_CUSTOM_DIRS_SET" ]]; then
    TARGET_DIRS=($DUST_BUNNY_DIRS)
fi
if [[ -n "$DUST_BUNNY_MAX_AGE" ]]; then
    MAX_AGE_DAYS="$DUST_BUNNY_MAX_AGE"
fi
if [[ "$DUST_BUNNY_REAL_RUN" == "true" ]]; then
    DRY_RUN=false
fi

echo "--- Digital Dust Bunny Sweeper ---"
echo "Scanning directories: ${TARGET_DIRS[*]}"
echo "Files older than: $MAX_AGE_DAYS days"
echo "Mode: $(if [[ "$DRY_RUN" == "true" ]]; then echo "DRY RUN (no files will be deleted)"; else echo "REAL RUN (files will be deleted)"; fi)"
if [[ "$VERBOSE" == "true" ]]; then
    echo "Verbose output enabled."
fi
echo "----------------------------------"

TOTAL_DELETED_COUNT=0
TOTAL_DELETED_SIZE=0

for dir in "${TARGET_DIRS[@]}"; do
    if [[ ! -d "$dir" ]]; then
        echo "Warning: Directory not found or not accessible: $dir. Skipping."
        continue
    fi

    echo "Processing directory: $dir"
    OLD_FILES=$(_find_old_files "$dir" "$MAX_AGE_DAYS")

    if [[ -z "$OLD_FILES" ]]; then
        echo "  No digital dust bunnies found in $dir older than $MAX_AGE_DAYS days."
        continue
    fi

    DIR_DELETED_COUNT=0
    DIR_DELETED_SIZE=0

    while IFS= read -r file; do
        if [[ -f "$file" ]]; then # Ensure it's still a file
            FILE_SIZE=$(du -b "$file" 2>/dev/null | awk '{print $1}')
            if [[ -z "$FILE_SIZE" ]]; then
                FILE_SIZE=0
            fi

            _delete_file "$file"

            if [[ "$DRY_RUN" == "false" ]]; then
                # Only count if actually deleted (or attempted to delete)
                TOTAL_DELETED_COUNT=$((TOTAL_DELETED_COUNT + 1))
                TOTAL_DELETED_SIZE=$((TOTAL_DELETED_SIZE + FILE_SIZE))
                DIR_DELETED_COUNT=$((DIR_DELETED_COUNT + 1))
                DIR_DELETED_SIZE=$((DIR_DELETED_SIZE + FILE_SIZE))
            fi
        fi
    done <<< "$OLD_FILES"

    if [[ "$DRY_RUN" == "false" ]]; then
        echo "  Swept away $DIR_DELETED_COUNT dust bunnies, freeing $(numfmt --to=iec-i --suffix=B --format="%.1f" "$DIR_DELETED_SIZE") in $dir."
    fi
done

echo "----------------------------------"
if [[ "$DRY_RUN" == "true" ]]; then
    echo "DRY RUN complete. No files were deleted."
    echo "To perform actual deletions, run with the -r flag or set DUST_BUNNY_REAL_RUN=true."
else
    echo "Sweeping complete! Total digital dust bunnies swept: $TOTAL_DELETED_COUNT"
    echo "Total space freed: $(numfmt --to=iec-i --suffix=B --format="%.1f" "$TOTAL_DELETED_SIZE")"
fi
echo "----------------------------------"
