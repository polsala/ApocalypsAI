#!/bin/bash

# Nightly Digital Debris Scavenger

# Default values
TARGET_DIR=""
AGE_DAYS=30
QUARANTINE_MODE=0
QUARANTINE_DIR=""

# Function to display usage
usage() {
    echo "Usage: $0 -d <directory> [-a <age_in_days>] [-q]"
    echo "  -d <directory>    : The directory to scan for digital debris."
    echo "  -a <age_in_days>  : Files older than this many days will be considered debris (default: 30)."
    echo "  -q                : Enable quarantine mode. Moves debris to a temporary quarantine directory."
    echo "  -h                : Display this help message."
    exit 1
}

# Parse command-line arguments
while getopts "d:a:qh" opt; do
    case "${opt}" in
        d) TARGET_DIR="${OPTARG}" ;;
        a) AGE_DAYS="${OPTARG}" ;;
        q) QUARANTINE_MODE=1 ;;
        h) usage ;;
        *) usage ;;
    esac
done
shift $((OPTIND-1))

# Validate TARGET_DIR
if [[ -z "${TARGET_DIR}" ]]; then
    echo "Error: Target directory must be specified." >&2
    usage
fi

if [[ ! -d "${TARGET_DIR}" ]]; then
    echo "Error: Target directory '${TARGET_DIR}' does not exist or is not a directory." >&2
    exit 1
}

# Validate AGE_DAYS
if ! [[ "${AGE_DAYS}" =~ ^[0-9]+$ ]] || [[ "${AGE_DAYS}" -le 0 ]]; then
    echo "Error: Age in days must be a positive integer." >&2
    exit 1
}

echo "Scanning '${TARGET_DIR}' for digital debris older than ${AGE_DAYS} days..."

# Find old files
# Mock rationale: In tests, we will create specific files with specific modification times
# and ensure `find` correctly identifies them.
# For actual execution, `find` is a standard utility and doesn't need mocking beyond
# ensuring the test environment has files matching the criteria.
DEBRIS_FILES=$(find "${TARGET_DIR}" -type f -mtime +"${AGE_DAYS}" -print)

if [[ -z "${DEBRIS_FILES}" ]]; then
    echo "No digital debris found. All clear, scavenger!"
    exit 0
}

echo "--- Digital Debris Detected ---"
echo "${DEBRIS_FILES}" | while IFS= read -r file; do
    echo "  - ${file}"
done
echo "-------------------------------"

if [[ "${QUARANTINE_MODE}" -eq 1 ]]; then
    QUARANTINE_DIR=$(mktemp -d "${TARGET_DIR}/.scavenger_quarantine_XXXXXX")
    if [[ ! -d "${QUARANTINE_DIR}" ]]; then
        echo "Error: Failed to create quarantine directory." >&2
        exit 1
    fi
    echo "Quarantining debris to: '${QUARANTINE_DIR}'"
    echo "${DEBRIS_FILES}" | while IFS= read -r file; do
        # Mock rationale: In tests, we will verify that files are moved to the correct
        # quarantine directory. The `mv` command itself is a standard utility.
        mv "${file}" "${QUARANTINE_DIR}/"
        if [[ $? -ne 0 ]]; then
            echo "Warning: Failed to quarantine '${file}'." >&2
        else
            echo "  - Quarantined: ${file}"
        fi
    done
    echo "Digital debris successfully quarantined. Remember to inspect and purge the quarantine zone!"
else
    echo "To quarantine this debris, run with the '-q' flag."
fi

exit 0
