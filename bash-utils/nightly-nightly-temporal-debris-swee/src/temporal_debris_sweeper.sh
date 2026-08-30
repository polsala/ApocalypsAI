#!/bin/bash

# Nightly Temporal Debris Sweeper
# Sweeps away old, temporary files and directories.

# Default values
DEFAULT_PATH="/tmp"
DEFAULT_AGE_DAYS=7
DRY_RUN=true
CONFIRM=false

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS] [PATH]"
    echo ""
    echo "Whimsically identifies and optionally sweeps away old, temporary files and directories."
    echo "Treats old files as 'temporal debris' that accumulates over time."
    echo ""
    echo "Options:"
    echo "  -p, --path <PATH>     Specify the directory to scan (default: $DEFAULT_PATH)"
    echo "  -a, --age <DAYS>      Files/directories older than <DAYS> will be considered debris (default: $DEFAULT_AGE_DAYS days)"
    echo "  -f, --force           Perform actual deletion without confirmation (USE WITH CAUTION!)"
    echo "  -c, --confirm         Require confirmation before deletion (overrides -f if both present)"
    echo "  -s, --sweep           Perform actual deletion (disables dry run, requires confirmation unless -f is used)"
    echo "  -h, --help            Display this help message"
    echo ""
    echo "By default, the script runs in dry-run mode, only listing files that would be swept."
    echo "Use -s to enable actual sweeping. It will prompt for confirmation unless -f is also used."
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -p|--path)
            SCAN_PATH="$2"
            shift
            ;;
        -a|--age)
            AGE_DAYS="$2"
            shift
            ;;
        -f|--force)
            DRY_RUN=false
            CONFIRM=false
            ;;
        -c|--confirm)
            CONFIRM=true
            DRY_RUN=false # If confirmation is requested, it implies a real sweep
            ;;
        -s|--sweep)
            DRY_RUN=false
            CONFIRM=true # Default to confirmation for safety
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            echo "Error: Unknown option '$1'"
            usage
            exit 1
            ;;
        *) # Positional argument for path
            if [ -z "$SCAN_PATH" ]; then
                SCAN_PATH="$1"
            else
                echo "Error: Multiple paths specified. Please use -p for explicit path."
                usage
                exit 1
            fi
            ;;
    esac
    shift
done

# Set defaults if not provided
SCAN_PATH="${SCAN_PATH:-$DEFAULT_PATH}"
AGE_DAYS="${AGE_DAYS:-$DEFAULT_AGE_DAYS}"

# Validate inputs
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [ "$AGE_DAYS" -lt 0 ]; then
    echo "Error: Age must be a non-negative integer."
    exit 1
fi

if [ ! -d "$SCAN_PATH" ]; then
    echo "Error: Path '$SCAN_PATH' is not a valid directory."
    exit 1
fi

echo "--- Nightly Temporal Debris Sweeper ---"
echo "Scanning for temporal debris in: '$SCAN_PATH'"
echo "Debris defined as files/directories older than: $AGE_DAYS days"
echo ""

# Find files/directories
# Using -depth to process contents before directory itself, important for -delete
# Using -print0 and xargs -0 for safe handling of filenames with spaces/special chars
DEBRIS_LIST=$(find "$SCAN_PATH" -depth -mindepth 1 -type f -o -type d -mtime +"$AGE_DAYS" -print0)

if [ -z "$DEBRIS_LIST" ]; then
    echo "No temporal debris found. Your digital space is sparkling clean!"
    exit 0
fi

echo "Identified temporal debris:"
echo "$DEBRIS_LIST" | xargs -0 -I {} echo "  - {}"
echo ""

if $DRY_RUN; then
    echo "This was a dry run. No files were swept away."
    echo "To perform an actual sweep, run with the -s or --sweep option."
    exit 0
fi

if $CONFIRM; then
    read -p "Are you sure you want to sweep away this temporal debris? (y/N): " -n 1 -r
    echo ""
    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
        echo "Sweeping aborted. Temporal debris remains for now."
        exit 0
    fi
fi

echo "Sweeping away temporal debris..."
echo "$DEBRIS_LIST" | xargs -0 rm -rf
echo "Temporal debris swept! Your digital space feels lighter."
