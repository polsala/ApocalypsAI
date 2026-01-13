#!/bin/bash

set -euo pipefail

DAYS_STALE=${1:-90}
CURRENT_TIMESTAMP=$(date +%s)
STALE_THRESHOLD_SECONDS=$((CURRENT_TIMESTAMP - DAYS_STALE * 24 * 60 * 60))

STALE_BRANCHES=()

# Mock rationale: We mock 'git' to control the output of branch information
# and commit times, ensuring deterministic tests without actual git repository access.
# This allows testing the script's logic independently of a live git repository.
BRANCH_INFO=$(git for-each-ref --sort=-committerdate refs/remotes/origin/ --format='%(refname:short) %(committerdate:unix)')

echo "$BRANCH_INFO" | while IFS= read -r line; do
    BRANCH_NAME=$(echo "$line" | awk '{print $1}')
    COMMIT_TIMESTAMP=$(echo "$line" | awk '{print $2}')

    # Skip HEAD, main, and master branches from being considered stale for pruning
    if [[ "$BRANCH_NAME" == "origin/HEAD" || "$BRANCH_NAME" == "origin/main" || "$BRANCH_NAME" == "origin/master" ]]; then
        continue
    }

    # Remove "origin/" prefix for cleaner output
    CLEAN_BRANCH_NAME="${BRANCH_NAME#origin/}"

    if (( COMMIT_TIMESTAMP < STALE_THRESHOLD_SECONDS )); then
        STALE_BRANCHES+=("\"$CLEAN_BRANCH_NAME\"")
    fi
done

# Output as JSON array to GITHUB_OUTPUT
echo "stale-branches=[$(IFS=,; echo "${STALE_BRANCHES[*]}") ]" >> "$GITHUB_OUTPUT"
