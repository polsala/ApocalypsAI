#!/bin/bash

# Nightly Scavenged Deduplicator
# Identifies and optionally removes duplicate files within specified directories.

set -euo pipefail

# Whimsical flavor text
echo "Initiating Scavenged Deduplicator Protocol..."
echo "Scanning the digital wasteland for redundant data echoes..."

DRY_RUN=true
DELETE_DUPLICATES=false
HASH_ALGO="sha256sum" # Default to sha256sum
MIN_SIZE="0" # Default to 0 bytes

declare -a DIRS # Array to hold directories to scan

# Function to display usage
usage() {
    echo "Usage: $(basename "$0") [OPTIONS] <DIR1> [DIR2...]"
    echo ""
    echo "Identifies and optionally removes duplicate files within specified directories."
    echo "Conserves precious storage in the digital wasteland."
    echo ""
    echo "Options:"
    echo "  --dry-run             (Default) Show duplicates without deleting them."
    echo "  --delete              Actually delete duplicate files. USE WITH CAUTION!"
    echo "  --hash-algo <md5|sha256> Specify hashing algorithm (default: sha256)."
    echo "  --min-size <BYTES>    Only consider files larger than this size (e.g., 1K, 1M, 1G, 100c)."
    echo "  -h, --help            Display this help message."
    echo ""
    echo "Example:"
    echo "  $(basename "$0") --dry-run /path/to/cache /path/to/downloads"
    echo "  $(basename "$0") --delete --hash-algo md5 --min-size 1M /path/to/archive"
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            DELETE_DUPLICATES=false
            ;;
        --delete)
            DELETE_DUPLICATES=true
            DRY_RUN=false
            ;;
        --hash-algo)
            if [[ -n "$2" && ("$2" == "md5" || "$2" == "sha256") ]]; then
                HASH_ALGO="${2}sum"
                shift
            else
                echo "Error: --hash-algo requires 'md5' or 'sha256'." >&2
                usage
            fi
            ;;
        --min-size)
            if [[ -n "$2" && "$2" =~ ^[0-9]+[cKMG]?$ ]]; then
                MIN_SIZE="$2"
                shift
            else
                echo "Error: --min-size requires a size (e.g., 1K, 1M, 1G, 100c)." >&2
                usage
            fi
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "Error: Unknown option '$1'" >&2
            usage
            ;;
        *)
            DIRS+=("$1")
            ;;
    esac
    shift
done

if [ ${#DIRS[@]} -eq 0 ]; then
    echo "Error: No directories specified." >&2
    usage
fi

# Validate directories exist
for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Error: Directory '$dir' not found." >&2
        exit 1
    fi
done

echo "Scanning directories: ${DIRS[*]}"
echo "Using hash algorithm: ${HASH_ALGO}"
if [ "$MIN_SIZE" != "0" ]; then
    echo "Minimum file size: ${MIN_SIZE}"
fi
echo ""

# Determine hash length for parsing
hash_len=0
if [[ "$HASH_ALGO" == "md5sum" ]]; then
    hash_len=32
elif [[ "$HASH_ALGO" == "sha256sum" ]]; then
    hash_len=64
else
    echo "Error: Unsupported hash algorithm '$HASH_ALGO'." >&2
    exit 1
fi

# Use temporary files for hashes and duplicate hashes
HASH_FILE=$(mktemp)
DUPLICATE_HASHES_FILE=$(mktemp)
trap "rm -f '$HASH_FILE' '$DUPLICATE_HASHES_FILE'" EXIT # Clean up temp files on exit

echo "Calculating hashes for files..."

# Construct the find command
find_cmd_base="find "
for dir in "${DIRS[@]}"; do
    find_cmd_base+=" \"$dir\""
done
find_cmd_base+=" -type f"

if [ "$MIN_SIZE" != "0" ]; then
    find_cmd_base+=" -size +${MIN_SIZE}"
fi

# Execute find and hash. Using -print0 and xargs -0 for robust handling of filenames.
# Redirect stderr of xargs/hash_algo to /dev/null to suppress 'No such file or directory' errors
# for files that might disappear during scan, or permission errors, etc. 
# We only care about successful hashes. Errors will be handled by missing entries in HASH_FILE.

eval "$find_cmd_base -print0" | xargs -0 "$HASH_ALGO" 2>/dev/null > "$HASH_FILE"

if [ ! -s "$HASH_FILE" ]; then
    echo "No files found or no hashes generated. Exiting." >&2
    exit 0
fi

# Extract just the hashes and find which ones are duplicates
# The hash is the first field, separated by two spaces from the filename
cut -d ' ' -f 1 "$HASH_FILE" | sort | uniq -d > "$DUPLICATE_HASHES_FILE"

if [ ! -s "$DUPLICATE_HASHES_FILE" ]; then
    echo "No duplicate files found. The wasteland is clean!"
    exit 0
fi

echo "Duplicate files found:"
echo "----------------------"

DUPLICATE_COUNT=0

# Read each duplicate hash and find all files associated with it
while IFS= read -r dup_hash; do
    echo "Group with hash: $dup_hash"
    
    declare -a CURRENT_GROUP_FILES
    # Get all files for this duplicate hash. Filenames can contain spaces.
    # `cut -c $((hash_len + 3))-` extracts everything after the hash and two spaces.
    # `sed 's/^\*//'` removes the leading asterisk if present (e.g., for binary files).
    while IFS= read -r filename_raw; do
        CURRENT_GROUP_FILES+=("$(echo "$filename_raw" | sed 's/^\*//')")
    done < <(grep -F "$dup_hash" "$HASH_FILE" | cut -c $((hash_len + 3))- )

    # The first file in the group is considered the "original" to keep
    PRIMARY_FILE="${CURRENT_GROUP_FILES[0]}"
    echo "  Keeping: $PRIMARY_FILE (Original)"

    for (( i=1; i<${#CURRENT_GROUP_FILES[@]}; i++ )); do
        DUPLICATE_FILE="${CURRENT_GROUP_FILES[$i]}"
        echo "  Duplicate: $DUPLICATE_FILE"
        if $DELETE_DUPLICATES; then
            echo "    Purging: $DUPLICATE_FILE"
            rm "$DUPLICATE_FILE"
            if [ $? -eq 0 ]; then
                echo "    Purged successfully."
            else
                echo "    Failed to purge $DUPLICATE_FILE." >&2
            fi
        else
            echo "    (Dry run: would purge $DUPLICATE_FILE)"
        fi
        DUPLICATE_COUNT=$((DUPLICATE_COUNT + 1))
    done
    echo ""
done < "$DUPLICATE_HASHES_FILE"

echo "Scavenged Deduplicator Report:"
echo "Total duplicate files identified: $DUPLICATE_COUNT"
if $DELETE_DUPLICATES; then
    echo "Total duplicate files purged: $DUPLICATE_COUNT"
else
    echo "Run with --delete to purge identified duplicates."
fi
echo "Protocol complete. Storage optimized for survival."
