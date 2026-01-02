#!/bin/bash

# Nightly Digital Debris Detector

# Default values
TARGET_DIR="."
AGE_DAYS=30
ACTION="report" # Can be 'report', 'archive', 'vaporize'
DEBRIS_VAULT=".digital_debris_vault"

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS] <directory>"
    echo ""
    echo "Scans specified directories for digital debris (old, large, or unused files) and helps manage them."
    echo ""
    echo "Options:"
    echo "  -d, --days <N>     Files older than N days (default: 30)."
    echo "  -r, --report       Report debris found (default action)."
    echo "  -a, --archive      Move debris to a '.digital_debris_vault' subdirectory."
    echo "  -v, --vaporize     Permanently delete debris."
    echo "  -h, --help         Display this help message."
    echo ""
    echo "Example: $0 --days 60 --archive /var/log"
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d|--days)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo "Error: --days requires a numeric argument."
                usage
            fi
            AGE_DAYS="$2"
            shift
            ;;
        -r|--report)
            ACTION="report"
            ;;
        -a|--archive)
            ACTION="archive"
            ;;
        -v|--vaporize)
            ACTION="vaporize"
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "Error: Unknown option '$1'"
            usage
            ;;
        *)
            if [[ -z "$TARGET_DIR" || "$TARGET_DIR" == "." ]]; then
                TARGET_DIR="$1"
            else
                echo "Error: Multiple target directories specified. Please provide only one."
                usage
            fi
            ;;
    esac
    shift
done

# Validate target directory
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist or is not a directory."
    exit 1
fi

# Ensure AGE_DAYS is a positive integer
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [[ "$AGE_DAYS" -le 0 ]]; then
    echo "Error: Days must be a positive integer."
    exit 1
fi

echo "Nightly Digital Debris Detector Initiated."
echo "Scanning '$TARGET_DIR' for files older than $AGE_DAYS days..."

# Find debris
# Using -print0 and xargs -0 for safe handling of filenames with spaces/special characters
DEBRIS_FILES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" -print0)

if [[ -z "$DEBRIS_FILES" ]]; then
    echo "No digital debris detected. All clear!"
    exit 0
fi

echo "Digital debris detected:"

case "$ACTION" in
    report)
        echo "$DEBRIS_FILES" | xargs -0 -I {} echo "  - {}"
        echo "Debris reported. Use --archive or --vaporize to manage."
        ;;
    archive)
        DEBRIS_VAULT_PATH="$TARGET_DIR/$DEBRIS_VAULT"
        mkdir -p "$DEBRIS_VAULT_PATH"
        echo "$DEBRIS_FILES" | xargs -0 -I {} mv "{}" "$DEBRIS_VAULT_PATH/"
        echo "Debris moved to '$DEBRIS_VAULT_PATH'."
        ;;
    vaporize)
        echo "$DEBRIS_FILES" | xargs -0 rm -f
        echo "Debris vaporized. Poof!"
        ;;
esac

echo "Nightly Digital Debris Detector Complete."
