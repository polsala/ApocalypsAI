#!/bin/bash

# Wasteland Cache Cleaner - Identify and manage digital relics and resource hogs.

# Default values
TARGET_DIR="."
MODE="old" # 'old' or 'large'
THRESHOLD="" # e.g., '30d' for old, '100M' for large
ACTION="list" # 'list' or 'delete'

# Whimsical messages
MSG_HEADER="=== ApocalypsAI Wasteland Cache Report ==="
MSG_NO_FILES="No forgotten relics or resource hogs found in the cache. All clear, survivor!"
MSG_LISTING_OLD="Scanning for ancient relics (older than %s) in %s..."
MSG_LISTING_LARGE="Scanning for resource hogs (larger than %s) in %s..."
MSG_DELETING_OLD="Purging ancient relics (older than %s) from %s..."
MSG_DELETING_LARGE="Purging resource hogs (larger than %s) from %s..."
MSG_FILE_FOUND_OLD="  [RELIC] %s (Modified: %s)"
MSG_FILE_FOUND_LARGE="  [HOG] %s (Size: %s)"
MSG_FILE_DELETED="  [PURGED] %s"
MSG_SUMMARY_LIST="Found %d items. Use --action delete to purge them."
MSG_SUMMARY_DELETED="Purged %d items from the wasteland cache."
MSG_ERROR_DIR="ERROR: Target directory '%s' does not exist or is not a directory."
MSG_ERROR_THRESHOLD="ERROR: Invalid threshold for mode '%s'. Expected format: 'Nd' (days) for 'old', 'NM'/'NG' (MB/GB) for 'large'."
MSG_USAGE="Usage: $0 <directory> [--mode old|large] [--threshold <value>] [--action list|delete]\n\n  <directory>   : The path to the cache to scan.\n  --mode        : 'old' to find files by age (default), 'large' to find by size.\n  --threshold   : For 'old': e.g., '30d' (30 days). For 'large': e.g., '100M' (100 MB), '1G' (1 GB).\n  --action      : 'list' to show files (default), 'delete' to remove them."

# Function to display usage
usage() {
    echo -e "$MSG_USAGE"
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --mode)
            MODE="$2"
            shift
            ;;
        --threshold)
            THRESHOLD="$2"
            shift
            ;;
        --action)
            ACTION="$2"
            ;;
        -h|--help)
            usage
            ;;
        *)
            if [[ -z "$TARGET_DIR" || "$TARGET_DIR" == "." ]]; then
                TARGET_DIR="$1"
            else
                echo "ERROR: Unknown argument or multiple directories specified: $1"
                usage
            fi
            ;;
    esac
    shift
done

# Validate target directory
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "$(printf "$MSG_ERROR_DIR" "$TARGET_DIR")"
    usage
fi

# Validate threshold
if [[ -z "$THRESHOLD" ]]; then
    # Set default thresholds if not provided
    if [[ "$MODE" == "old" ]]; then
        THRESHOLD="30d" # Default to 30 days
    elif [[ "$MODE" == "large" ]]; then
        THRESHOLD="100M" # Default to 100 MB
    fi
fi

FIND_ARGS=()
if [[ "$MODE" == "old" ]]; then
    if [[ "$THRESHOLD" =~ ^([0-9]+)d$ ]]; then
        DAYS="${BASH_REMATCH[1]}"
        FIND_ARGS+=("-mtime" "+$DAYS")
        echo "$(printf "$MSG_LISTING_OLD" "${DAYS} days" "$TARGET_DIR")"
    else
        echo "$(printf "$MSG_ERROR_THRESHOLD" "$MODE")"
        usage
    fi
elif [[ "$MODE" == "large" ]]; then
    if [[ "$THRESHOLD" =~ ^([0-9]+)([MG])$ ]]; then
        SIZE_VAL="${BASH_REMATCH[1]}"
        SIZE_UNIT="${BASH_REMATCH[2]}"
        # find -size uses 512-byte blocks. Convert M/G to blocks.
        if [[ "$SIZE_UNIT" == "M" ]]; then
            BLOCKS=$((SIZE_VAL * 1024 * 1024 / 512))
        elif [[ "$SIZE_UNIT" == "G" ]]; then
            BLOCKS=$((SIZE_VAL * 1024 * 1024 * 1024 / 512))
        fi
        FIND_ARGS+=("-size" "+${BLOCKS}c") # +N for greater than N bytes, c for bytes
        echo "$(printf "$MSG_LISTING_LARGE" "${SIZE_VAL}${SIZE_UNIT}" "$TARGET_DIR")"
    else
        echo "$(printf "$MSG_ERROR_THRESHOLD" "$MODE")"
        usage
    fi
else
    echo "ERROR: Invalid mode '$MODE'. Use 'old' or 'large'."
    usage
fi

echo "$MSG_HEADER"

# Find files
FOUND_FILES=()
while IFS= read -r -d $'\0' file; do
    FOUND_FILES+=("$file")
done < <(find "$TARGET_DIR" -type f "${FIND_ARGS[@]}" -print0)

if [[ ${#FOUND_FILES[@]} -eq 0 ]]; then
    echo "$MSG_NO_FILES"
else
    COUNT=0
    for file in "${FOUND_FILES[@]}"; do
        if [[ "$ACTION" == "list" ]]; then
            if [[ "$MODE" == "old" ]]; then
                MOD_TIME=$(stat -c %y "$file" | cut -d'.' -f1)
                echo "$(printf "$MSG_FILE_FOUND_OLD" "$file" "$MOD_TIME")"
            elif [[ "$MODE" == "large" ]]; then
                FILE_SIZE=$(du -h "$file" | cut -f1)
                echo "$(printf "$MSG_FILE_FOUND_LARGE" "$file" "$FILE_SIZE")"
            fi
        elif [[ "$ACTION" == "delete" ]]; then
            rm -f "$file"
            echo "$(printf "$MSG_FILE_DELETED" "$file")"
        fi
        COUNT=$((COUNT + 1))
    done

    if [[ "$ACTION" == "list" ]]; then
        echo "$(printf "$MSG_SUMMARY_LIST" "$COUNT")"
    elif [[ "$ACTION" == "delete" ]]; then
        echo "$(printf "$MSG_SUMMARY_DELETED" "$COUNT")"
    fi
fi
