#!/bin/bash

set -euo pipefail

STALE_DAYS=$1
EXCLUDE_BRANCHES_STR=$2

# Convert comma-separated string to an array, handling potential empty string
IFS=',' read -r -a EXCLUDE_BRANCHES <<< "$EXCLUDE_BRANCHES_STR"

# Get current date in seconds since epoch
CURRENT_DATE_SEC=$(date +%s)

STALE_BRANCHES_FOUND=""

# Fetch all remote branches to ensure local git history is up-to-date
# Mock rationale: In a real scenario, this fetches from the actual remote. For testing,
# the 'setup_test_repo.sh' script creates a local 'origin' to simulate this.
git fetch origin --prune > /dev/null 2>&1 || {
    echo "Error: Failed to fetch from origin. Ensure 'actions/checkout' with fetch-depth: 0 is used." >&2
    exit 1
}

# Get all remote branch names, excluding HEAD -> origin/main pointers
# Mock rationale: This queries the local git repository's remote branches.
# The test setup ensures these branches exist with specific histories.
BRANCH_NAMES=$(git branch -r | grep -v '->' | sed 's/origin\///' | xargs)

for BRANCH_NAME in $BRANCH_NAMES; do
    # Skip main/master if they are in the default exclude list or explicitly excluded
    EXCLUDED=false
    for EXCL_BRANCH_PATTERN in "${EXCLUDE_BRANCHES[@]}"; do
        # Use case-insensitive matching for patterns
        if [[ "$BRANCH_NAME" == $EXCL_BRANCH_PATTERN ]]; then
            EXCLUDED=true
            break
        fi
    done
    if $EXCLUDED; then
        echo "Skipping excluded branch: $BRANCH_NAME"
        continue
    fi

    # Get the last commit date for the branch
    # Mock rationale: This command reads the commit date from the local git history.
    # The 'setup_test_repo.sh' script pre-populates this history with specific dates for deterministic testing.
    LAST_COMMIT_DATE_ISO=$(git log -1 --format="%cd" --date=iso-strict "origin/$BRANCH_NAME" 2>/dev/null || echo "")

    if [[ -z "$LAST_COMMIT_DATE_ISO" ]]; then
        echo "Warning: Could not get last commit date for branch 'origin/$BRANCH_NAME'. Skipping." >&2
        continue
    fi

    # Convert ISO date to seconds since epoch
    LAST_COMMIT_DATE_SEC=$(date -d "$LAST_COMMIT_DATE_ISO" +%s)

    # Calculate age in days
    AGE_SECONDS=$((CURRENT_DATE_SEC - LAST_COMMIT_DATE_SEC))
    AGE_DAYS=$((AGE_SECONDS / 86400)) # 60*60*24

    if (( AGE_DAYS > STALE_DAYS )); then
        echo "Branch 'origin/$BRANCH_NAME' is stale ($AGE_DAYS days old)."
        if [[ -z "$STALE_BRANCHES_FOUND" ]]; then
            STALE_BRANCHES_FOUND="$BRANCH_NAME"
        else
            STALE_BRANCHES_FOUND="$STALE_BRANCHES_FOUND,$BRANCH_NAME"
        fi
    else
        echo "Branch 'origin/$BRANCH_NAME' is fresh ($AGE_DAYS days old)."
    fi
done

# Set the action output
echo "stale-branches=$STALE_BRANCHES_FOUND" >> "$GITHUB_OUTPUT"
echo "Stale branches identified: $STALE_BRANCHES_FOUND"
