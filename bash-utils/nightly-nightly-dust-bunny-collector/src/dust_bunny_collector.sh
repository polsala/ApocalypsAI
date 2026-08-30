#!/bin/bash

# Nightly Digital Dust Bunny Collector
# Scans for and helps clean up old, large files (digital dust bunnies) in specified directories.

# --- Configuration & Colors ---
COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[0;33m'
COLOR_BLUE='\033[0;34m'
COLOR_PURPLE='\033[0;35m'
COLOR_CYAN='\033[0;36m'
COLOR_NC='\033[0m' # No Color

# --- Functions ---

usage() {
    echo -e "${COLOR_BLUE}Nightly Digital Dust Bunny Collector${COLOR_NC}"
    echo -e "${COLOR_CYAN}------------------------------------${COLOR_NC}"
    echo "Usage: $0 <directory> <age_in_days> <min_size_mb> <action> [archive_dir]"
    echo ""
    echo "Arguments:"
    echo "  <directory>    : Path to the directory to scan (e.g., /var/log, /tmp)"
    echo "  <age_in_days>  : Files older than this many days will be considered (e.g., 30)"
    echo "  <min_size_mb>  : Minimum file size in megabytes. Files smaller than this are ignored (e.g., 100)"
    echo "  <action>       : Action to perform. Choose one of:"
    echo "                   - report : List the identified files."
    echo "                   - archive: Archive files to [archive_dir] and delete originals."
    echo "                   - delete : Permanently delete the identified files."
    echo "  [archive_dir]  : Required for 'archive' action. Directory to store archives."
    echo ""
    echo "Examples:"
    echo "  $0 /var/log 60 50 report"
    echo "  $0 /tmp 90 200 archive ~/archives/dust_bunnies"
    echo "  $0 ~/Downloads 7 10 delete"
    exit 1
}

# --- Main Script ---

# Check arguments
if [ "$#" -lt 4 ]; then
    usage
fi

TARGET_DIR="$1"
AGE_DAYS="$2"
MIN_SIZE_MB="$3"
ACTION="$4"
ARCHIVE_DIR="$5"

# Validate directory
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${COLOR_RED}Error: Directory '$TARGET_DIR' not found or is not a directory.${COLOR_NC}"
    exit 1
fi

# Validate age and size
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || ! [[ "$MIN_SIZE_MB" =~ ^[0-9]+$ ]]; then
    echo -e "${COLOR_RED}Error: Age in days and minimum size must be positive integers.${COLOR_NC}"
    usage
fi

# Validate action
case "$ACTION" in
    report|archive|delete)
        ;;
    *)
        echo -e "${COLOR_RED}Error: Invalid action '$ACTION'. Must be 'report', 'archive', or 'delete'.${COLOR_NC}"
        usage
        ;;
esac

# Validate archive_dir if action is archive
if [ "$ACTION" == "archive" ]; then
    if [ -z "$ARCHIVE_DIR" ]; then
        echo -e "${COLOR_RED}Error: 'archive' action requires an archive directory.${COLOR_NC}"
        usage
    fi
    if [ ! -d "$ARCHIVE_DIR" ]; then
        echo -e "${COLOR_YELLOW}Warning: Archive directory '$ARCHIVE_DIR' not found. Attempting to create it.${COLOR_NC}"
        mkdir -p "$ARCHIVE_DIR" || { echo -e "${COLOR_RED}Error: Could not create archive directory '$ARCHIVE_DIR'.${COLOR_NC}"; exit 1; }
    fi
fi

echo -e "${COLOR_BLUE}Scanning for digital dust bunnies in '${TARGET_DIR}'...${COLOR_NC}"
echo -e "${COLOR_CYAN}Criteria: Older than ${AGE_DAYS} days, larger than ${MIN_SIZE_MB}MB.${COLOR_NC}"

# Find the dust bunnies
# Using -print0 and xargs -0 for safe handling of filenames with spaces or special characters
DUST_BUNNIES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" -size +"$MIN_SIZE_MB"M -print0)

if [ -z "$DUST_BUNNIES" ]; then
    echo -e "${COLOR_GREEN}No digital dust bunnies found matching your criteria. Your system is sparkling clean!${COLOR_NC}"
    exit 0
fi

echo -e "${COLOR_YELLOW}Identified Digital Dust Bunnies:${COLOR_NC}"
echo "$DUST_BUNNIES" | xargs -0 du -h | sort -rh

case "$ACTION" in
    report)
        echo -e "${COLOR_GREEN}Reporting complete. No files were modified.${COLOR_NC}"
        ;;
    archive)
        ARCHIVE_FILENAME="dust_bunnies_$(date +%Y%m%d_%H%M%S).tar.gz"
        ARCHIVE_PATH="$ARCHIVE_DIR/$ARCHIVE_FILENAME"
        echo -e "${COLOR_PURPLE}Archiving identified dust bunnies to '$ARCHIVE_PATH'...${COLOR_NC}"
        # Use tar with --remove-files to delete after archiving
        echo "$DUST_BUNNIES" | xargs -0 tar -czvf "$ARCHIVE_PATH" --remove-files
        if [ $? -eq 0 ]; then
            echo -e "${COLOR_GREEN}Archiving successful! Original dust bunnies swept away.${COLOR_NC}"
        else
            echo -e "${COLOR_RED}Error during archiving. Some dust bunnies might remain.${COLOR_NC}"
            exit 1
        fi
        ;;
    delete)
        echo -e "${COLOR_RED}Deleting identified dust bunnies... This action is irreversible!${COLOR_NC}"
        # Use find with -delete for atomic deletion
        find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" -size +"$MIN_SIZE_MB"M -delete
        if [ $? -eq 0 ]; then
            echo -e "${COLOR_GREEN}Deletion successful! Your system is now lighter.${COLOR_NC}"
        else
            echo -e "${COLOR_RED}Error during deletion. Some stubborn dust bunnies might remain.${COLOR_NC}"
            exit 1
        fi
        ;;
esac

exit 0
