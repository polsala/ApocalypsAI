#!/bin/bash

# Default values
TARGET_DIR="."
AGE_DAYS=30
PATTERNS=("*.tmp" "*.bak" "~*" "#*#") # Default patterns
DRY_RUN=true

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <days>] [-p <pattern1,pattern2,...>] [-c] [-h]"
    echo "  -d <directory> : Target directory to clean (default: current directory)"
    echo "  -a <days>      : Files older than this many days will be considered (default: 30)"
    echo "  -p <patterns>  : Comma-separated list of file patterns (e.g., '*.tmp,*.bak'). Default: '*.tmp,*.bak,~*,#*#'"
    echo "  -c             : Perform cleanup (delete files). By default, it's a dry run."
    echo "  -h             : Display this help message."
    exit 1
}

# Parse arguments
while getopts "d:a:p:ch" opt; do
    case ${opt} in
        d ) TARGET_DIR=$OPTARG ;;
        a ) AGE_DAYS=$OPTARG ;;
        p ) IFS=',' read -r -a PATTERNS <<< "$OPTARG" ;;
        c ) DRY_RUN=false ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done

# Validate AGE_DAYS
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]]; then
    echo "Error: Age must be a positive integer."
    usage
fi

echo "--- Nightly Chrono-Clutter Cleaner ---"
echo "Target Directory: $TARGET_DIR"
echo "Age Threshold: $AGE_DAYS days"
echo "File Patterns: ${PATTERNS[*]}"
echo "Mode: $(if $DRY_RUN; then echo "Dry Run (no files will be deleted)"; else echo "Cleanup (files will be deleted)"; fi)"
echo "--------------------------------------"

# Build find command for listing/identifying
FIND_CMD="find \"$TARGET_DIR\" -type f -mtime +$AGE_DAYS"

# Add patterns to find command
PATTERN_CLAUSE=""
for pattern in "${PATTERNS[@]}"; do
    if [ -n "$PATTERN_CLAUSE" ]; then
        PATTERN_CLAUSE+=" -o "
    fi
    PATTERN_CLAUSE+="-name \"$pattern\""
done

if [ -n "$PATTERN_CLAUSE" ]; then
    FIND_CMD+=" \( $PATTERN_CLAUSE \)"
fi

# Execute find for dry run or listing before deletion
echo "\nSearching for files..."
FOUND_FILES=$(eval $FIND_CMD)

if [ -z "$FOUND_FILES" ]; then
    echo "No chrono-clutter found matching criteria."
else
    echo "Found the following chrono-clutter:"
    echo "$FOUND_FILES"

    if ! $DRY_RUN; then
        echo "\nInitiating cleanup..."
        # Use find -delete for safety and efficiency
        DELETE_CMD="find \"$TARGET_DIR\" -type f -mtime +$AGE_DAYS"
        if [ -n "$PATTERN_CLAUSE" ]; then
            DELETE_CMD+=" \( $PATTERN_CLAUSE \)"
        }
        DELETE_CMD+=" -delete"
        
        echo "Executing: $DELETE_CMD"
        eval $DELETE_CMD
        
        if [ $? -eq 0 ]; then
            echo "Cleanup complete. Digital dust bunnies vanquished!"
        else
            echo "Cleanup failed or encountered issues."
        fi
    else
        echo "\nThis was a dry run. To perform cleanup, run with the -c flag."
    fi
fi

echo "--------------------------------------"
echo "Chrono-Clutter Cleaner finished."
