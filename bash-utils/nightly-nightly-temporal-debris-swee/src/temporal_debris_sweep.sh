#!/bin/bash

# Default values
TARGET_DIR="."
AGE_DAYS=7
DRY_RUN=true

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <age_days>] [-c] [-h]"
    echo "  -d <directory> : Target directory to sweep (default: current directory)"
    echo "  -a <age_days>  : Files older than this many days will be considered temporal debris (default: 7)"
    echo "  -c             : Commit to sweeping (delete files). By default, it's a dry run (list only)."
    echo "  -h             : Display this help message."
    exit 1
}

# Parse command-line options
while getopts "d:a:ch" opt; do
    case "${opt}" in
        d) TARGET_DIR="${OPTARG}" ;;
        a) AGE_DAYS="${OPTARG}" ;;
        c) DRY_RUN=false ;;
        h) usage ;;
        *) usage ;;
    esac
done
shift $((OPTIND-1))

# Validate directory
if [ ! -d "${TARGET_DIR}" ]; then
    echo "Error: Target directory '${TARGET_DIR}' does not exist or is not a directory." >&2
    exit 1
fi

echo "-- ApocalypsAI Temporal Debris Sweeper --"
echo "Scanning for temporal anomalies (files older than ${AGE_DAYS} days) in: ${TARGET_DIR}"
echo ""

# Find files
# Using -type f to only target regular files, not directories
# Using -mtime +N for files modified N*24 hours ago
# Using -print0 and xargs -0 for safe handling of filenames with spaces/special chars
FILES_TO_SWEEP=$(find "${TARGET_DIR}" -type f -mtime +${AGE_DAYS} -print0)

if [ -z "$FILES_TO_SWEEP" ]; then
    echo "No significant temporal debris detected. Your timeline is remarkably clean!"
else
    echo "Detected temporal debris:"
    echo "${FILES_TO_SWEEP}" | xargs -0 -I {} echo "  - {}"
    echo ""

    if ${DRY_RUN}; then
        echo "This was a dry run. To commit to sweeping, run with the '-c' flag."
        echo "No temporal anomalies were purged."
    else
        echo "Initiating temporal debris purge..."
        echo "${FILES_TO_SWEEP}" | xargs -0 rm -f
        echo "Temporal debris successfully swept away. The timeline is now clearer."
    fi
fi

echo ""
echo "-- Sweep Complete --"
