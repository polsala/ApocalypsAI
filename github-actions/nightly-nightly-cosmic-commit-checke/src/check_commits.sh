#!/bin/bash

set -euo pipefail

COMMIT_RANGE="${INPUT_COMMIT_RANGE}"
REQUIRED_KEYWORDS_STR="${INPUT_REQUIRED_KEYWORDS}"
FORBIDDEN_KEYWORDS_STR="${INPUT_FORBIDDEN_KEYWORDS}"
FAIL_ON_MISMATCH="${INPUT_FAIL_ON_MISMATCH}"
COMMIT_MESSAGES_FILE="${INPUT_COMMIT_MESSAGES_FILE}"

ALL_COMMIT_MESSAGES=""

# Mock rationale: For testing, we can provide a file with predefined commit messages.
# This allows deterministic and offline execution without actual git history.
if [[ -n "${COMMIT_MESSAGES_FILE}" ]]; then
    echo "Reading commit messages from file: ${COMMIT_MESSAGES_FILE}"
    if [[ ! -f "${COMMIT_MESSAGES_FILE}" ]]; then
        echo "Error: Commit messages file not found at ${COMMIT_MESSAGES_FILE}"
        exit 1
    fi
    ALL_COMMIT_MESSAGES=$(cat "${COMMIT_MESSAGES_FILE}")
else
    echo "Fetching commit messages using git log for range: ${COMMIT_RANGE}"
    # Ensure we have enough history for the commit_range
    # The checkout step in action.yml should handle fetch-depth: 0
    ALL_COMMIT_MESSAGES=$(git log --pretty=format:%s "${COMMIT_RANGE}" || true)
    if [[ -z "${ALL_COMMIT_MESSAGES}" ]]; then
        echo "Warning: No commit messages found for range '${COMMIT_RANGE}'."
    fi
fi

# Convert comma-separated strings to arrays
IFS=',' read -r -a REQUIRED_KEYWORDS <<< "${REQUIRED_KEYWORDS_STR}"
IFS=',' read -r -a FORBIDDEN_KEYWORDS <<< "${FORBIDDEN_KEYWORDS_STR}"

# Initialize status variables
ALIGNMENT_STATUS="aligned"
REQUIRED_FOUND_LIST=""
FORBIDDEN_FOUND_LIST=""

# Track if all required keywords are found
declare -A required_found_map
for keyword in "${REQUIRED_KEYWORDS[@]}"; do
    if [[ -n "$keyword" ]]; then
        required_found_map["$keyword"]="0" # 0 for not found, 1 for found
    fi
done

# Process each commit message
while IFS= read -r line; do
    if [[ -z "$line" ]]; then
        continue
    fi
    echo "Checking commit: '$line'"

    # Check for forbidden keywords
    for keyword in "${FORBIDDEN_KEYWORDS[@]}"; do
        if [[ -n "$keyword" && "$line" == *"$keyword"* ]]; then
            echo "🚫 Misalignment detected: Forbidden keyword '$keyword' found in commit message: '$line'"
            ALIGNMENT_STATUS="misaligned"
            FORBIDDEN_FOUND_LIST+="${keyword},"
        fi
    done

    # Check for required keywords
    for keyword in "${REQUIRED_KEYWORDS[@]}"; do
        if [[ -n "$keyword" && "$line" == *"$keyword"* ]]; then
            required_found_map["$keyword"]="1"
        fi
    done

done <<< "${ALL_COMMIT_MESSAGES}"

# Final check for required keywords
for keyword in "${REQUIRED_KEYWORDS[@]}"; do
    if [[ -n "$keyword" ]]; then
        if [[ "${required_found_map["$keyword"]}" == "1" ]]; then
            REQUIRED_FOUND_LIST+="${keyword},"
        else
            echo "⚠️ Misalignment detected: Required keyword '$keyword' not found in any commit message."
            ALIGNMENT_STATUS="misaligned"
        fi
    fi
done

# Clean up trailing commas
REQUIRED_FOUND_LIST=$(echo "${REQUIRED_FOUND_LIST}" | sed 's/,$//')
FORBIDDEN_FOUND_LIST=$(echo "${FORBIDDEN_FOUND_LIST}" | sed 's/,$//')

# Set outputs
echo "::set-output name=alignment_status::${ALIGNMENT_STATUS}"
echo "::set-output name=required_found::${REQUIRED_FOUND_LIST}"
echo "::set-output name=forbidden_found::${FORBIDDEN_FOUND_LIST}"

# Fail if misaligned and fail_on_mismatch is true
if [[ "${ALIGNMENT_STATUS}" == "misaligned" && "${FAIL_ON_MISMATCH}" == "true" ]]; then
    echo "Cosmic alignment check failed due to mismatch."
    exit 1
else
    echo "Cosmic alignment check completed with status: ${ALIGNMENT_STATUS}"
fi
