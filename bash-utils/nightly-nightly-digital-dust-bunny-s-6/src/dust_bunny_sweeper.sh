#!/bin/bash

# Configuration defaults
DEFAULT_AGE_DAYS=30
DEFAULT_ACTION="report" # "report", "archive", "delete"
DEFAULT_ARCHIVE_DIR="$HOME/.digital_void_archive"
EXCLUDE_EXTENSIONS=("log" "tmp" "bak" "swp") # Example extensions to exclude from deletion/archiving suggestions

# Function to display usage
usage() {
    echo "Usage: $0 <directory> [options]"
    echo "Sweeps away digital dust bunnies (old, forgotten files) from your directories."
    echo ""
    echo "Arguments:"
    echo "  <directory>     The path to scan for old files."
    echo ""
    echo "Options:"
    echo "  -a <days>       Files older than <days> will be considered dust bunnies. Default: ${DEFAULT_AGE_DAYS} days."
    echo "  -x <ext1,ext2>  Comma-separated list of file extensions to EXCLUDE from sweeping actions."
    echo "                  (e.g., 'log,tmp'). Default: ${EXCLUDE_EXTENSIONS[*]}"
    echo "  -m <mode>       Action mode: 'report' (default), 'archive', 'delete'."
    echo "                  'report': Just list the files."
    echo "                  'archive': Move files to the archive directory."
    echo "                  'delete': Permanently delete files."
    echo "  -o <path>       Specify a custom archive directory for 'archive' mode. Default: ${DEFAULT_ARCHIVE_DIR}"
    echo "  -f              Force action without confirmation (use with caution for 'archive'/'delete')."
    echo "  -h              Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 /path/to/downloads -a 90"
    echo "  $0 /path/to/logs -m delete -x 'gz,zip' -f"
    echo "  $0 /path/to/documents -m archive -o /mnt/cold_storage/digital_void"
}

# Parse arguments
SCAN_DIR=""
AGE_DAYS=${DEFAULT_AGE_DAYS}
ACTION=${DEFAULT_ACTION}
ARCHIVE_DIR=${DEFAULT_ARCHIVE_DIR}
FORCE_ACTION="false"
EXCLUDE_PATTERN=""

while getopts ":a:x:m:o:fh" opt; do
    case ${opt} in
        a ) AGE_DAYS=$OPTARG ;;
        x ) EXCLUDE_EXTENSIONS=(${OPTARG//,/ }) ;;
        m ) ACTION=$OPTARG ;;
        o ) ARCHIVE_DIR=$OPTARG ;;
        f ) FORCE_ACTION="true" ;;
        h ) usage; exit 0 ;;
        \? ) echo "Invalid option: -$OPTARG" >&2; usage; exit 1 ;;
        : ) echo "Invalid option: -$OPTARG requires an argument" >&2; usage; exit 1 ;;
    esac
done
shift $((OPTIND -1))

SCAN_DIR=$1

if [[ -z "$SCAN_DIR" ]]; then
    echo "Error: Please specify a directory to scan." >&2
    usage
    exit 1
fi

if [[ ! -d "$SCAN_DIR" ]]; then
    echo "Error: Directory '$SCAN_DIR' does not exist or is not a directory." >&2
    exit 1
fi

# Validate action mode
if [[ "$ACTION" != "report" && "$ACTION" != "archive" && "$ACTION" != "delete" ]]; then
    echo "Error: Invalid action mode '$ACTION'. Must be 'report', 'archive', or 'delete'." >&2
    usage
    exit 1
fi

# Prepare exclude pattern for find
if [[ ${#EXCLUDE_EXTENSIONS[@]} -gt 0 ]]; then
    EXCLUDE_PATTERN=$(printf "! -name '*.%s' " "${EXCLUDE_EXTENSIONS[@]}")
fi

echo "--- Digital Dust Bunny Sweeper ---"
echo "Scanning directory: '$SCAN_DIR'"
echo "Looking for files older than: ${AGE_DAYS} days"
echo "Action mode: ${ACTION}"
if [[ "$ACTION" == "archive" ]]; then
    echo "Archive directory: '$ARCHIVE_DIR'"
fi
if [[ ${#EXCLUDE_EXTENSIONS[@]} -gt 0 ]]; then
    echo "Excluding extensions: ${EXCLUDE_EXTENSIONS[*]}"
fi
echo "----------------------------------"

# Find old files
# Mock rationale: In a real scenario, `find` would interact with the filesystem.
# For testing, we rely on `find`'s behavior with a controlled test environment.
# The test script will create specific files with specific modification times.
# The `find` command itself is not mocked, but its input (the filesystem) is.
OLD_FILES=$(find "$SCAN_DIR" -type f -mtime +"$AGE_DAYS" $EXCLUDE_PATTERN -print0)

if [[ -z "$OLD_FILES" ]]; then
    echo "No digital dust bunnies found. Your directory is sparkling clean!"
    exit 0
fi

echo ""
echo "Found the following digital dust bunnies:"
echo "----------------------------------------"
echo "$OLD_FILES" | xargs -0 -I {} echo "  - {}"
echo "----------------------------------------"
echo ""

if [[ "$ACTION" == "report" ]]; then
    echo "Report complete. No actions taken."
    exit 0
fi

if [[ "$FORCE_ACTION" == "false" ]]; then
    read -p "Proceed with '${ACTION}' action? (y/N): " -n 1 -r
    echo ""
    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
        echo "Action cancelled by user."
        exit 0
    fi
fi

case "$ACTION" in
    archive)
        mkdir -p "$ARCHIVE_DIR" || { echo "Error: Could not create archive directory '$ARCHIVE_DIR'." >&2; exit 1; }
        echo "Sweeping dust bunnies to the Digital Void (archiving)..."
        echo "$OLD_FILES" | xargs -0 -I {} mv -v "{}" "$ARCHIVE_DIR/"
        echo "Archiving complete. The Digital Void grows..."
        ;;
    delete)
        echo "Vaporizing dust bunnies (deleting permanently)..."
        echo "$OLD_FILES" | xargs -0 -I {} rm -v "{}"
        echo "Deletion complete. Poof! They're gone."
        ;;
esac

echo "Digital Dust Bunny Sweeper finished its rounds."
