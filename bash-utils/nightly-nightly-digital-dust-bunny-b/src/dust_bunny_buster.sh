#!/bin/bash

# Nightly Digital Dust Bunny Buster

# Default values
TARGET_DIR="."
AGE_DAYS=7
DRY_RUN=true
FORCE_DELETE=false

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <days>] [-p] [-f]"
    echo ""
    echo "A whimsical Bash script to identify and optionally purge old, unused files and directories,"
    echo "metaphorically busting digital 'dust bunnies' from your system."
    echo ""
    echo "Options:"
    echo "  -d <directory>  Specify the target directory to scan (default: current directory)."
    echo "  -a <days>       Specify the age in days for files/directories to be considered 'dust bunnies' (default: 7 days)."
    echo "  -p              Perform the purge (delete files/directories). By default, it's a dry run."
    echo "  -f              Force deletion without confirmation (use with caution, implies -p)."
    echo "  -h              Display this help message."
    echo ""
    echo "Example:"
    echo "  $0 -d /tmp -a 30          # Dry run: find files/dirs in /tmp older than 30 days."
    echo "  $0 -d /var/log -a 90 -p  # Purge: delete files/dirs in /var/log older than 90 days (with confirmation)."
    echo "  $0 -d ~/Downloads -a 180 -f # Force purge: delete files/dirs in ~/Downloads older than 180 days (no confirmation)."
    exit 1
}

# Parse command-line options
while getopts "d:a:pfh" opt; do
    case ${opt} in
        d ) TARGET_DIR=$OPTARG ;;
        a ) AGE_DAYS=$OPTARG ;;
        p ) DRY_RUN=false ;;
        f ) DRY_RUN=false; FORCE_DELETE=true ;;
        h ) usage ;;
        \? ) echo "Invalid option: -$OPTARG" >&2; usage ;;
    esac
done
shift $((OPTIND -1))

# Validate AGE_DAYS
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]]; then
    echo "Error: Age must be a positive integer." >&2
    usage
fi

# Validate TARGET_DIR
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist or is not a directory." >&2
    exit 1
fi

echo "Scanning for Digital Dust Bunnies in: '$TARGET_DIR'"
echo "Looking for files/directories older than: $AGE_DAYS days"
echo ""

# Find files and directories
# Using -print0 and xargs -0 for safety with filenames containing spaces or special characters
# -mindepth 1 -maxdepth 1 ensures only direct children of TARGET_DIR are considered.
DUST_BUNNIES=$(find "$TARGET_DIR" -mindepth 1 -maxdepth 1 -mtime +"$AGE_DAYS" -print0)

if [ -z "$DUST_BUNNIES" ]; then
    echo "No digital dust bunnies found! Your system is sparkling clean."
    exit 0
fi

echo "Identified the following digital dust bunnies:"
echo "$DUST_BUNNIES" | xargs -0 -I {} echo "  - {}"
echo ""

if $DRY_RUN; then
    echo "This was a dry run. No files were deleted."
    echo "To perform the purge, run with the '-p' option."
else
    if ! $FORCE_DELETE; then
        read -p "Do you wish to purge these digital dust bunnies? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Purge cancelled. The dust bunnies live another day."
            exit 0
        fi
    fi

    echo "Initiating Digital Dust Bunny Purge..."
    # xargs -0 rm -rf will handle both files and non-empty directories safely.
    echo "$DUST_BUNNIES" | xargs -0 rm -rf
    
    if [ $? -eq 0 ]; then
        echo "Digital Dust Bunny Purge complete! Your system feels lighter."
    else
        echo "Error during purge. Some dust bunnies might have escaped!" >&2
        exit 1
    fi
fi
