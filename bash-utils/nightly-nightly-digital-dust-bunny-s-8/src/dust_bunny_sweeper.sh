#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

# Default values
TARGET_DIR="."
AGE_DAYS=90

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <age_in_days>]"
    echo "Scans for old, forgotten files and directories, humorously identifying them as 'digital dust bunnies' for cleanup."
    echo ""
    echo "Options:"
    echo "  -d <directory>  Specify the directory to scan (default: current directory)."
    echo "  -a <age_in_days> Specify the age in days for files/dirs to be considered 'dust bunnies' (default: 90)."
    echo "  -h              Display this help message."
    exit 1
}

# Parse command-line arguments
while getopts "d:a:h" opt; do
    case ${opt} in
        d )
            TARGET_DIR=$OPTARG
            ;;
        a )
            if ! [[ "$OPTARG" =~ ^[0-9]+$ ]]; then
                echo "Error: Age must be a positive integer." >&2
                usage
            fi
            AGE_DAYS=$OPTARG
            ;;
        h )
            usage
            ;;
        \? )
            echo "Invalid option: -$OPTARG" >&2
            usage
            ;;
    esac
done
shift $((OPTIND -1))

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' not found." >&2
    exit 1
fi

echo "Scanning '$TARGET_DIR' for digital dust bunnies older than $AGE_DAYS days..."
echo "---------------------------------------------------------------------"

# Find files and directories older than AGE_DAYS
# Using -print0 and xargs -0 for handling filenames with spaces or special characters
DUST_BUNNIES=$(find "$TARGET_DIR" -maxdepth 1 -type f -mtime +"$AGE_DAYS" -print0; \
               find "$TARGET_DIR" -maxdepth 1 -type d -mtime +"$AGE_DAYS" -not -path "$TARGET_DIR" -print0)

if [ -z "$DUST_BUNNIES" ]; then
    echo "Hooray! No digital dust bunnies found in '$TARGET_DIR'. Your digital space is sparkling!"
else
    echo "Behold! The following digital dust bunnies have been unearthed:"
    echo "$DUST_BUNNIES" | xargs -0 -I {} echo "  - {}" # Simplified output for portability
    echo ""
    echo "Consider sweeping them away with a command like: rm -rf <path/to/dust_bunny>"
    echo "Or for all listed: find '$TARGET_DIR' -maxdepth 1 -mtime +\"$AGE_DAYS\" -delete"
fi

exit 0
