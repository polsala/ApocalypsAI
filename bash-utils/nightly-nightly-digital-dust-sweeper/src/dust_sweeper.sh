#!/bin/bash

# Nightly Digital Dust Sweeper
# Scans for old files, temporary files, and empty directories.

# Default values
SCAN_PATH="."
OLD_DAYS=30

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -p|--path)
            if [[ -z "$2" ]]; then
                echo "Error: --path requires a directory argument."
                exit 1
            fi
            SCAN_PATH="$2"
            shift # Shift past argument and value
            ;;
        -d|--days)
            if ! [[ "$2" =~ ^[0-9]+$ ]]; then
                echo "Error: --days requires a numeric argument."
                exit 1
            fi
            OLD_DAYS="$2"
            shift # Shift past argument and value
            ;;
        -h|--help)
            echo "Usage: $0 [-p|--path <DIRECTORY>] [-d|--days <NUMBER>]"
            echo "  -p, --path <DIRECTORY>  : The directory to scan. Defaults to current directory."
            echo "  -d, --days <NUMBER>     : Files older than this many days will be considered 'old'. Defaults to 30."
            exit 0
            ;;
        *)
            echo "Unknown parameter or missing value: $1"
            echo "Use -h or --help for usage information."
            exit 1
            ;;
    esac
    shift # Shift past the argument
done

# Validate SCAN_PATH
if [[ ! -d "$SCAN_PATH" ]]; then
    echo "Error: Directory '$SCAN_PATH' not found or is not a directory."
    exit 1
fi

echo "Scanning '$SCAN_PATH' for digital dust bunnies older than $OLD_DAYS days..."
echo "--------------------------------------------------"

echo "\n--- Empty Directories ---"
# Find empty directories
find "$SCAN_PATH" -type d -empty -print

echo "\n--- Old Files (older than $OLD_DAYS days) ---"
# Find regular files modified more than OLD_DAYS ago
find "$SCAN_PATH" -type f -mtime +"$OLD_DAYS" -print

echo "\n--- Temporary/Backup Files ---"
# Find files with common temporary/backup extensions
find "$SCAN_PATH" -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*~" -o -name "*.log" -o -name "*.old" \) -print

echo "\n--------------------------------------------------"
echo "Scan complete. Review the listed 'dust bunnies' for potential cleanup."
