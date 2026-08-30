#!/bin/bash
set -euo pipefail

# Inputs from action.yml (passed as environment variables)
DAYS_STALE="${INPUT_DAYS_STALE}"
COMMIT_MESSAGE_PREFIX="${INPUT_COMMIT_MESSAGE_PREFIX}"
EXCLUDE_BRANCHES_RAW="${INPUT_EXCLUDE_BRANCHES}"
GITHUB_TOKEN="${INPUT_GITHUB_TOKEN}"
GITHUB_REPOSITORY="${GITHUB_REPOSITORY}"

# Convert comma-separated string to an array for easier checking
IFS=',' read -r -a EXCLUDE_BRANCHES_ARRAY <<< "${EXCLUDE_BRANCHES_RAW}"

# Set Git user for the commit
git config user.name "ApocalypsAI Nightly Integrator"
git config user.email "apocalypsai@example.com"

# Configure git to use the GITHUB_TOKEN for authentication
# This is crucial for pushing back to the repository
git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"

CURRENT_TIMESTAMP=$(date +%s)
STALE_THRESHOLD_SECONDS=$((DAYS_STALE * 24 * 60 * 60))

REJUVENATED_BRANCHES=()

echo "Scanning for branches older than ${DAYS_STALE} days..."

# Fetch all remote branches
git fetch origin '+refs/heads/*:refs/remotes/origin/*'

# List all remote branches, excluding HEAD
git branch -r | grep -v 'HEAD' | while read -r remote_branch; do
    branch_name=$(echo "${remote_branch}" | sed 's/origin\///')

    # Skip excluded branches
    EXCLUDED=false
    for excluded in "${EXCLUDE_BRANCHES_ARRAY[@]}"; do
        if [[ "${branch_name}" == "${excluded}" ]]; then
            echo "Skipping excluded branch: ${branch_name}"
            EXCLUDED=true
            break
        fi
    done
    if ${EXCLUDED}; then
        continue
    fi

    # Get the last commit timestamp for the branch
    LAST_COMMIT_TIMESTAMP=$(git log -1 --format="%at" "origin/${branch_name}")

    if [[ -z "${LAST_COMMIT_TIMESTAMP}" ]]; then
        echo "Warning: Could not get last commit timestamp for ${branch_name}. Skipping."
        continue
    fi

    TIME_DIFFERENCE=$((CURRENT_TIMESTAMP - LAST_COMMIT_TIMESTAMP))

    if (( TIME_DIFFERENCE > STALE_THRESHOLD_SECONDS )); then
        echo "Branch '${branch_name}' is stale (last commit: $(date -d "@${LAST_COMMIT_TIMESTAMP}")). Rejuvenating..."

        # Checkout the branch
        git checkout "${branch_name}"

        # Create a whimsical commit message
        WHIMSICAL_MESSAGE_SUFFIX=$(shuf -n 1 <<EOF
You've been missed! Time to shine again.
A little nudge from the void.
Still here, still fabulous!
Don't worry, I've got your back (and your branch).
Dusting off the digital cobwebs.
Awakening from slumber!
EOF
)
        COMMIT_MESSAGE="${COMMIT_MESSAGE_PREFIX} ${WHIMSICAL_MESSAGE_SUFFIX}"

        # Create an empty commit
        git commit --allow-empty -m "${COMMIT_MESSAGE}"

        # Push the empty commit
        git push origin "${branch_name}"

        REJUVENATED_BRANCHES+=("${branch_name}")
        echo "Rejuvenated branch: ${branch_name}"
    else
        echo "Branch '${branch_name}' is active enough (last commit: $(date -d "@${LAST_COMMIT_TIMESTAMP}")). Skipping."
    fi
done

# Set output for rejuvenated branches
if [[ ${#REJUVENATED_BRANCHES[@]} -gt 0 ]]; then
    JSON_OUTPUT=$(printf '%s\n' "${REJUVENATED_BRANCHES[@]}" | jq -R . | jq -s .)
    echo "rejuvenated-branches=${JSON_OUTPUT}" >> "${GITHUB_OUTPUT}"
    echo "Successfully rejuvenated ${#REJUVENATED_BRANCHES[@]} branches."
else
    echo "No branches needed rejuvenation."
    echo "rejuvenated-branches=[]" >> "${GITHUB_OUTPUT}"
fi
