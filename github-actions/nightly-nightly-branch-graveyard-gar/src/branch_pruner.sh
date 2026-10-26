#!/bin/bash

set -euo pipefail

STALE_DAYS=${1:-90}
IGNORE_BRANCHES_CSV=${2:-"main,master,develop"}
TEST_MODE_FILE=${3:-""} # Optional: path to a file for test mode

# Convert ignore branches CSV to an array
IFS=',' read -r -a IGNORE_BRANCHES_ARRAY <<< "$IGNORE_BRANCHES_CSV"

# Function to check if a branch should be ignored based on patterns
should_ignore() {
    local branch_name="$1" # This is already cleaned (no "origin/")
    for ignore_pattern in "${IGNORE_BRANCHES_ARRAY[@]}"; do
        # Use bash pattern matching for wildcards
        if [[ "$branch_name" == $ignore_pattern ]]; then
            return 0 # True, ignore
        fi
    done
    return 1 # False, do not ignore
}

STALE_BRANCHES=()
CURRENT_TIMESTAMP=$(date +%s)
THRESHOLD_TIMESTAMP=$((CURRENT_TIMESTAMP - (STALE_DAYS * 24 * 60 * 60)))

if [[ -n "$TEST_MODE_FILE" ]]; then
    # Test mode: read from file (format: branch_name|timestamp)
    while IFS='|' read -r branch_name commit_timestamp; do
        # Remove "origin/" prefix for consistent comparison with ignore patterns
        CLEAN_BRANCH_NAME="${branch_name#origin/}"
        if should_ignore "$CLEAN_BRANCH_NAME"; then
            continue
        fi

        if (( commit_timestamp < THRESHOLD_TIMESTAMP )); then
            STALE_BRANCHES+=("$CLEAN_BRANCH_NAME")
        fi
    done < "$TEST_MODE_FILE"
else
    # Live mode: use git
    git fetch origin --prune > /dev/null 2>&1
    # Get all remote branches, remove "origin/" prefix, and trim whitespace
    ALL_REMOTE_BRANCHES=$(git branch -r | grep -v HEAD | sed 's/origin\///g' | sed 's/^[[:space:]]*//')

    for branch in $ALL_REMOTE_BRANCHES; do
        if should_ignore "$branch"; then
            continue
        fi

        LAST_COMMIT_DATE_ISO=$(git show -s --format=%ci "origin/$branch")
        LAST_COMMIT_TIMESTAMP=$(date -d "$LAST_COMMIT_DATE_ISO" +%s)

        if (( LAST_COMMIT_TIMESTAMP < THRESHOLD_TIMESTAMP )); then
            STALE_BRANCHES+=("$branch")
        fi
    done
fi

# Output results to GITHUB_OUTPUT
STALE_BRANCHES_JSON=$(printf '%s\n' "${STALE_BRANCHES[@]}" | jq -R . | jq -s .)
echo "stale-branches=$STALE_BRANCHES_JSON" >> "$GITHUB_OUTPUT"
echo "stale-branches-count=${#STALE_BRANCHES[@]}" >> "$GITHUB_OUTPUT"

if [[ ${#STALE_BRANCHES[@]} -gt 0 ]]; then
    echo "::warning::Found ${#STALE_BRANCHES[@]} stale branches:"
    printf '%s\n' "${STALE_BRANCHES[@]}" | while read -r b; do echo "  - $b"; done
else
    echo "No stale branches found. Repository is spick and span!"
fi
