#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# A whimsical utility to find and manage old, unused files.

DEFAULT_AGE_DAYS=90
MODE="report"
DRY_RUN=0
TARGET_DIR=""

# Whimsical ASCII art header
print_header() {
    echo -e "\n  _   _ _ _   _       _ _ _             _
 | | | (_) | | |     | (_) |           | |
 | | | |_| |_| | __ _| |_| |__  _ __ __| | ___ _ __
 | | | | | __| |/ _\` | | | '_ \\| '__/ _\` |/ _ \\ '__|
 | |_| | | |_| | (_| | | | |_) | | | (_| |  __/ |
  \\___/|_|\\__|\\__\\__,_|_|_|_.__/|_|  \\__,_|\\___|_|\n\n  Sweeping for Digital Dust Bunnies...\n"
}

# Usage message
usage() {
    echo "Usage: $0 [OPTIONS] <directory>"
    echo ""
    echo "A whimsical shell script to identify and report on old, unused files (digital dust bunnies)"
    echo "in specified directories, suggesting cleanup actions."
    echo ""
    echo "Options:"
    echo "  -a <days>, --age <days>    Files older than this many days will be considered dust bunnies. Default: ${DEFAULT_AGE_DAYS}."
    echo "  -m <mode>, --mode <mode>   Action to perform: 'report' (default), 'archive', or 'delete'."
    echo "  -d, --dry-run              Show what *would* happen without performing any actions."
    echo "  -h, --help                 Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 --age 120 --dry-run ~/my_documents/"
    echo "  $0 --mode archive ~/downloads/"
    echo "  $0 --age 365 --mode delete --dry-run /tmp/old_cache/"
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -a|--age)
            if [[ "$2" =~ ^[0-9]+$ ]]; then
                AGE_DAYS="$2"
                shift
            else
                echo "Error: --age requires a numeric value."
                usage
            fi
            ;;
        -m|--mode)
            case "$2" in
                report|archive|delete)
                    MODE="$2"
                    shift
                    ;;
                *)
                    echo "Error: Invalid mode '$2'. Must be 'report', 'archive', or 'delete'."
                    usage
                    ;;
            esac
            ;;
        -d|--dry-run)
            DRY_RUN=1
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "Error: Unknown option '$1'"
            usage
            ;;
        *)
            if [ -z "$TARGET_DIR" ]; then
                TARGET_DIR="$1"
            else
                echo "Error: Too many directories specified. Only one target directory allowed."
                usage
            fi
            ;;
    esac
    shift
done

# Validate target directory
if [ -z "$TARGET_DIR" ]; then
    echo "Error: No target directory specified."
    usage
elif [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist or is not a directory."
    exit 1
fi

# Ensure AGE_DAYS is set
AGE_DAYS=${AGE_DAYS:-$DEFAULT_AGE_DAYS}

print_header
echo "Scanning '$TARGET_DIR' for digital dust bunnies older than ${AGE_DAYS} days..."
echo "Mode: ${MODE} | Dry Run: $(if [ "$DRY_RUN" -eq 1 ]; then echo "Yes"; else echo "No"; fi)"
echo "---------------------------------------------------------------------"

# Find files
# Mock rationale: In tests, we will mock the 'find' command to control its output
# without actually touching the filesystem or relying on real file ages.
DUST_BUNNIES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" 2>/dev/null)

if [ -z "$DUST_BUNNIES" ]; then
    echo "✨ Hooray! No digital dust bunnies found. Your digital space is sparkling clean! ✨"
    exit 0
fi

echo "A colony of ancient bits has been detected! (${MODE} mode)"
echo "---------------------------------------------------------------------"

COUNT=0
for FILE_PATH in $DUST_BUNNIES; do
    COUNT=$((COUNT + 1))
    RELATIVE_PATH="${FILE_PATH#$TARGET_DIR/}" # Make path relative for cleaner output
    echo "  [${COUNT}] Found: ${RELATIVE_PATH}"

    if [ "$DRY_RUN" -eq 1 ]; then
        case "$MODE" in
            archive)
                echo "      (Dry Run) Would move to: $(dirname "$FILE_PATH")/.dust_bunnies_archive/"
                ;;
            delete)
                echo "      (Dry Run) Would delete: ${FILE_PATH}"
                ;;
        esac
    else
        case "$MODE" in
            archive)
                ARCHIVE_DIR="$(dirname "$FILE_PATH")/.dust_bunnies_archive"
                # Mock rationale: In tests, we will mock 'mkdir -p' and 'mv' to prevent
                # actual filesystem changes and verify the commands would be called correctly.
                mkdir -p "$ARCHIVE_DIR" && mv "$FILE_PATH" "$ARCHIVE_DIR/"
                if [ $? -eq 0 ]; then
                    echo "      🧹 Archived to: ${ARCHIVE_DIR}/$(basename "$FILE_PATH")"
                else
                    echo "      ❌ Failed to archive: ${FILE_PATH}"
                fi
                ;;
            delete)
                # Mock rationale: In tests, we will mock 'rm' to prevent actual deletion
                # and verify the command would be called correctly.
                rm "$FILE_PATH"
                if [ $? -eq 0 ]; then
                    echo "      🗑️ Evicted: ${FILE_PATH}"
                else
                    echo "      ❌ Failed to delete: ${FILE_PATH}"
                fi
                ;;
        esac
    fi
done

echo "---------------------------------------------------------------------"
echo "Cleanup complete! Processed ${COUNT} digital dust bunnies."
echo "May your digital realm remain ever tidy!"
