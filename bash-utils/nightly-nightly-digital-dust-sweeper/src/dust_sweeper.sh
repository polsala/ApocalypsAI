#!/bin/bash

# Nightly Digital Dust Sweeper - Scavenging for lost bytes in the digital wasteland

DEFAULT_PATH="."
DEFAULT_AGE_DAYS=365 # Files older than 1 year
DEFAULT_SIZE_MB=100  # Files larger than 100MB

# --- Whimsical Messages ---
MSG_HEADER="=== Initiating Digital Dust Bunny Sweep ==="
MSG_NO_DUST="The digital winds whisper... no significant dust bunnies found. Your storage is surprisingly pristine!"
MSG_FOUND_FILES="Found some ancient byte-piles (files) that might be digital dust bunnies:"
MSG_FOUND_DIRS="Discovered some forgotten data-caverns (directories) that could be hoarding dust:"
MSG_FOOTER="=== Digital Dust Sweep Complete! Reclaim your precious bytes! ==="
MSG_SUGGESTION="Consider these for archiving or deletion to free up space. Use with caution!"

# --- Helper Functions ---

show_help() {
    echo "Usage: $0 [OPTIONS] [PATH]"
    echo ""
    echo "Scans for and reports on large, old, or unused files and directories,"
    echo "presenting them as 'digital dust bunnies' ready for sweeping."
    echo ""
    echo "Options:"
    echo "  -p, --path <PATH>      Specify the starting path for the sweep (default: $DEFAULT_PATH)"
    echo "  -a, --age <DAYS>       Minimum age in days for a file/dir to be considered old (default: $DEFAULT_AGE_DAYS)"
    echo "  -s, --size <MB>        Minimum size in MB for a file/dir to be considered large (default: $DEFAULT_SIZE_MB)"
    echo "  -h, --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 -p /var/log -a 90 -s 50"
    echo "  $0 --path /home/user/downloads --age 180"
}

# --- Main Logic ---

PATH_TO_SWEEP="$DEFAULT_PATH"
AGE_DAYS="$DEFAULT_AGE_DAYS"
SIZE_MB="$DEFAULT_SIZE_MB"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -p|--path)
            PATH_TO_SWEEP="$2"
            shift
            ;;
        -a|--age)
            AGE_DAYS="$2"
            shift
            ;;
        -s|--size)
            SIZE_MB="$2"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "Error: Unknown option '$1'"
            show_help
            exit 1
            ;;
        *)
            # If it's not an option, assume it's the path
            if [[ "$PATH_TO_SWEEP" == "$DEFAULT_PATH" ]]; then
                PATH_TO_SWEEP="$1"
            else
                echo "Error: Multiple paths specified. Please use -p or --path for a single path."
                show_help
                exit 1
            fi
            ;;
    esac
    shift
done

if [[ ! -d "$PATH_TO_SWEEP" ]]; then
    echo "Error: Path '$PATH_TO_SWEEP' does not exist or is not a directory."
    exit 1
fi

echo "$MSG_HEADER"
echo "Scanning '$PATH_TO_SWEEP' for digital dust bunnies (older than $AGE_DAYS days, larger than $SIZE_MB MB)..."
echo ""

found_any=false

# Find large, old files
echo "$MSG_FOUND_FILES"
find "$PATH_TO_SWEEP" -type f -mtime +"$AGE_DAYS" -size +"$SIZE_MB"M -print0 | while IFS= read -r -d $'\0' file; do
    if [[ -f "$file" ]]; then # Double check it's a file (find might return broken symlinks etc.)
        size=$(du -h "$file" | awk '{print $1}')
        mod_time=$(stat -c %y "$file" | cut -d' ' -f1)
        echo "  [FILE] $size ($mod_time) - $file"
        found_any=true
    fi
done

echo ""

# Find large, old directories
echo "$MSG_FOUND_DIRS"
# Find directories, then calculate their total size, filter by size and age
# This is more complex for directories as `find -size` applies to individual files within, not total dir size.
# We'll find directories, then use du -sh to get their size, and stat to get their modification time.
# This approach is less efficient for very deep hierarchies but more accurate for total dir size.
find "$PATH_TO_SWEEP" -type d -mtime +"$AGE_DAYS" -print0 | while IFS= read -r -d $'\0' dir; do
    if [[ -d "$dir" ]]; then
        dir_size_bytes=$(du -s "$dir" | awk '{print $1}') # Size in KB
        dir_size_mb=$((dir_size_bytes / 1024)) # Convert KB to MB
        if [[ "$dir_size_mb" -ge "$SIZE_MB" ]]; then
            size_human=$(du -sh "$dir" | awk '{print $1}')
            mod_time=$(stat -c %y "$dir" | cut -d' ' -f1)
            echo "  [DIR]  $size_human ($mod_time) - $dir"
            found_any=true
        fi
    fi
done

echo ""

if ! $found_any; then
    echo "$MSG_NO_DUST"
else
    echo "$MSG_SUGGESTION"
fi

echo "$MSG_FOOTER"
