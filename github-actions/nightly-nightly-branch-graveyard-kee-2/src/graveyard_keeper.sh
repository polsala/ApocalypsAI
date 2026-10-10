#!/bin/bash

# This script identifies stale branches based on their last commit date.
# It outputs a JSON array of stale branch names.

STALE_DAYS=${1:-90}
IGNORE_BRANCHES_RAW=${2:-"main,master,develop"}

# Convert comma-separated ignore branches to a bash array for easier checking
IFS=',' read -r -a IGNORE_BRANCHES_ARRAY <<< "$IGNORE_BRANCHES_RAW"

CURRENT_TIMESTAMP=$(date +%s)
STALE_THRESHOLD_SECONDS=$((STALE_DAYS * 24 * 60 * 60))

STALE_BRANCHES=()

# Get all remote branches
# Mock rationale: In a real run, this would interact with the actual git repo.
# For testing, we'll mock `git` to return predefined branch lists and commit dates.
git branch -r | grep -v '\->' | while read -r branch; do
    # Clean up branch name (e.g., "  origin/feature-x" -> "feature-x")
    branch_name=$(echo "$branch" | sed 's/origin\///' | xargs)

    # Skip ignored branches
    SKIP=false
    for ignore_pattern in "${IGNORE_BRANCHES_ARRAY[@]}"; do
        # Use regex matching for ignore patterns
        if [[ "$branch_name" =~ $ignore_pattern ]]; then
            SKIP=true
            break
        fi
    done
    if [ "$SKIP" = true ]; then
        continue
    }

    # Get the last commit timestamp for the branch
    # Mock rationale: For testing, `git log` will be mocked to return specific timestamps.
    LAST_COMMIT_TIMESTAMP=$(git log -1 --format="%ct" "origin/$branch_name" 2>/dev/null)

    if [ -z "$LAST_COMMIT_TIMESTAMP" ]; then
        # This can happen for branches that are just tags or other non-standard refs
        # Or if the branch was deleted remotely but still in local cache (unlikely in CI)
        continue
    fi

    AGE_SECONDS=$((CURRENT_TIMESTAMP - LAST_COMMIT_TIMESTAMP))

    if (( AGE_SECONDS > STALE_THRESHOLD_SECONDS )); then
        STALE_BRANCHES+=("\"$branch_name\"")
    fi
done

# Output as JSON array
echo "["$(IFS=,; echo "${STALE_BRANCHES[*]}")"]"
