#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

TARGET_DIR=""
AGE_DAYS=""
SIZE_MB=""
ARCHIVE_DIR=""
FORCE_SWEEP=0

display_help() {
    echo "Usage: $0 -d <directory> [-a <days> | -s <size_mb>] [-o <archive_dir>] [-f]"
    echo ""
    echo "Identifies and optionally archives old or large files, treating them as 'digital dust bunnies'."
    echo ""
    echo "Options:"
    echo "  -d <directory>    : The target directory to scan for dust bunnies."
    echo "  -a <days>         : Find files older than N days."
    echo "  -s <size_mb>      : Find files larger than N megabytes."
    echo "  -o <archive_dir>  : Optional. Directory to move found files to. If not specified, files are only listed."
    echo "  -f                : Force sweep. Do not ask for confirmation before archiving."
    echo "  -h                : Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 -d /var/log -a 30 -o /tmp/void_archive"
    echo "  $0 -d ~/Downloads -s 100"
    exit 0
}

# Parse arguments
while getopts "d:a:s:o:fh" opt; do
    case ${opt} in
        d ) TARGET_DIR=$OPTARG ;;
        a ) AGE_DAYS=$OPTARG ;;
        s ) SIZE_MB=$OPTARG ;;
        o ) ARCHIVE_DIR=$OPTARG ;;
        f ) FORCE_SWEEP=1 ;;
        h ) display_help ;;
        \? ) echo "Invalid option: -$OPTARG" >&2; display_help ;;
    esac
done

if [[ -z "$TARGET_DIR" ]]; then
    echo "Error: Target directory (-d) is required." >&2
    display_help
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist or is not a directory." >&2
    exit 1
fi

if [[ -z "$AGE_DAYS" && -z "$SIZE_MB" ]]; then
    echo "Error: Either age (-a) or size (-s) criteria must be specified." >&2
    display_help
fi

if [[ -n "$AGE_DAYS" && -n "$SIZE_MB" ]]; then
    echo "Warning: Both age and size criteria specified. Files matching EITHER will be considered." >&2
fi

if [[ -n "$ARCHIVE_DIR" && ! -d "$ARCHIVE_DIR" ]]; then
    echo "Void Archive '$ARCHIVE_DIR' does not exist. Creating it..."
    mkdir -p "$ARCHIVE_DIR" || { echo "Error: Could not create archive directory '$ARCHIVE_DIR'." >&2; exit 1; }
fi

echo "Scanning '$TARGET_DIR' for digital dust bunnies..."
echo "Criteria: $([[ -n "$AGE_DAYS" ]] && echo "Older than $AGE_DAYS days") $([[ -n "$SIZE_MB" ]] && echo "Larger than $SIZE_MB MB")"

FIND_CMD="find \"$TARGET_DIR\" -type f"

if [[ -n "$AGE_DAYS" ]]; then
    FIND_CMD+=" -mtime +$AGE_DAYS"
fi

if [[ -n "$SIZE_MB" ]]; then
    # find uses +N for > N, -N for < N, N for = N
    FIND_CMD+=" -size +${SIZE_MB}M"
fi

# Execute find command and store results
mapfile -t DUST_BUNNIES < <(eval "$FIND_CMD")

if [[ ${#DUST_BUNNIES[@]} -eq 0 ]]; then
    echo "No digital dust bunnies found. Your system is sparkling clean!"
    exit 0
fi

echo ""
echo "Found ${#DUST_BUNNIES[@]} digital dust bunnies:"
for bunny in "${DUST_BUNNIES[@]}"; do
    echo "  - $bunny"
done
echo ""

if [[ -n "$ARCHIVE_DIR" ]]; then
    if [[ "$FORCE_SWEEP" -eq 0 ]]; then
        read -p "Do you want to sweep these dust bunnies into the Void Archive '$ARCHIVE_DIR'? (y/N): " -n 1 -r
        echo ""
        if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
            echo "Sweep aborted. Dust bunnies remain."
            exit 0
        fi
    fi

    echo "Sweeping dust bunnies into '$ARCHIVE_DIR'..."
    for bunny in "${DUST_BUNNIES[@]}"; do
        if [[ -f "$bunny" ]]; then
            mv "$bunny" "$ARCHIVE_DIR/"
            if [[ $? -eq 0 ]]; then
                echo "  Moved: $bunny"
            else
                echo "  Failed to move: $bunny" >&2
            fi
        else
            echo "  Skipped (not a file or already moved): $bunny"
        fi
    done
    echo "Sweep complete. The Void Archive holds your digital debris."
else
    echo "To sweep these dust bunnies, specify an archive directory with -o <archive_dir>."
fi

exit 0
