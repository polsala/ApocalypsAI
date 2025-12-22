#!/bin/bash

# Default values
TARGET_DIR=""
AGE_DAYS=30
DRY_RUN=true
VERBOSE=false

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS] <directory>"
    echo "A whimsical utility to sweep away temporal dust bunnies (old files)."
    echo ""
    echo "Options:"
    echo "  -d <days>    Files older than <days> will be considered dust bunnies (default: 30)."
    echo "  -x           Execute deletion. By default, it's a dry run."
    echo "  -v           Verbose output."
    echo "  -h           Display this help message."
    echo ""
    echo "Example: $0 -d 60 -x /var/log"
    exit 1
}

# Parse arguments
while getopts "d:xvh" opt; do
    case ${opt} in
        d ) AGE_DAYS=$OPTARG ;;
        x ) DRY_RUN=false ;;
        v ) VERBOSE=true ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done
shift $((OPTIND -1))

# Get target directory
if [ -n "$1" ]; then
    TARGET_DIR="$1"
else
    echo "Error: No target directory specified."
    usage
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' not found."
    exit 1
fi

echo "🌌 Initiating Temporal Dust Bunny Sweeper Protocol for '$TARGET_DIR'..."
echo "⏳ Seeking files older than $AGE_DAYS days..."

# Find files
# Mock rationale: `find` is a standard utility; its behavior with `-mtime` is deterministic
# when operating on files created with `touch -t`. For testing, we control the test
# environment by creating files with specific timestamps, making `find`'s output predictable.
FOUND_FILES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" -print)
NUM_FOUND=$(echo "$FOUND_FILES" | grep -c .)

if [ "$NUM_FOUND" -eq 0 ]; then
    echo "✨ No temporal dust bunnies detected. Your digital realm is pristine!"
    exit 0
fi

echo "🧹 Detected $NUM_FOUND temporal dust bunnies:"
if [ "$VERBOSE" = true ]; then
    echo "$FOUND_FILES"
fi

if [ "$DRY_RUN" = true ]; then
    echo "👁️ This was a dry run. No files were swept away."
    echo "To execute deletion, run with the '-x' option."
else
    echo "🌪️ Sweeping away ancient digital detritus..."
    # Mock rationale: `rm` is a standard utility. For tests, we operate in a
    # temporary directory, so actual deletion is safe and verifiable by checking
    # file existence after the script runs.
    echo "$FOUND_FILES" | xargs -r rm -v
    echo "✅ Temporal dust bunnies successfully swept!"
fi

echo "✨ The digital winds whisper of a cleaner future."
