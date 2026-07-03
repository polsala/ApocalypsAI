#!/bin/bash

set -euo pipefail

OWNER=$(echo "$GITHUB_REPOSITORY" | cut -d'/' -f1)
REPO_NAME=$(echo "$GITHUB_REPOSITORY" | cut -d'/' -f2)
BASE_BRANCH=${BASE_BRANCH:-main}
STALE_DAYS=${STALE_DAYS:-30}

# Set GitHub token for gh CLI
export GH_TOKEN="${GITHUB_TOKEN}"

# Calculate stale date threshold in UTC seconds
STALE_THRESHOLD_SECONDS=$(date -u -d "${STALE_DAYS} days ago" +%s)

echo "🔍 Gardening the repository for stale branches..."
echo "  Base branch: ${BASE_BRANCH}"
echo "  Stale threshold: ${STALE_DAYS} days ago (UTC)"

STALE_UNMERGED_BRANCHES=()

# Fetch all branch names
BRANCH_NAMES=$(gh api "repos/${OWNER}/${REPO_NAME}/branches" --jq '.[].name' -H "Accept: application/vnd.github.v3+json")

if [ -z "$BRANCH_NAMES" ]; then
  echo "No branches found or API call failed."
  echo "stale_branches=[]" >> "$GITHUB_OUTPUT"
  exit 0
fi

echo "Found branches: ${BRANCH_NAMES}"

for BRANCH_NAME in $BRANCH_NAMES; do
  if [[ "$BRANCH_NAME" == "$BASE_BRANCH" ]]; then
    echo "Skipping base branch: ${BRANCH_NAME}"
    continue
  }

  echo "Checking branch: ${BRANCH_NAME}"

  # Get last commit date
  BRANCH_DETAILS=$(gh api "repos/${OWNER}/${REPO_NAME}/branches/${BRANCH_NAME}" -H "Accept: application/vnd.github.v3+json")
  LAST_COMMIT_DATE=$(echo "$BRANCH_DETAILS" | jq -r '.commit.commit.author.date')
  LAST_COMMIT_SECONDS=$(date -u -d "$LAST_COMMIT_DATE" +%s) # Convert API date (UTC) to UTC seconds

  if (( LAST_COMMIT_SECONDS > STALE_THRESHOLD_SECONDS )); then
    echo "  Branch '${BRANCH_NAME}' is fresh (last commit: ${LAST_COMMIT_DATE}). Skipping."
    continue
  }

  echo "  Branch '${BRANCH_NAME}' is stale (last commit: ${LAST_COMMIT_DATE}). Checking merge status..."

  # Check merge status against base branch
  # Status can be 'ahead', 'behind', 'diverged', 'identical'
  # We care about 'ahead' or 'diverged' as unmerged
  COMPARE_STATUS=$(gh api "repos/${OWNER}/${REPO_NAME}/compare/${BASE_BRANCH}...${BRANCH_NAME}" -H "Accept: application/vnd.github.v3+json" | jq -r '.status')

  if [[ "$COMPARE_STATUS" == "ahead" || "$COMPARE_STATUS" == "diverged" ]]; then
    echo "  Branch '${BRANCH_NAME}' is stale AND unmerged (status: ${COMPARE_STATUS}). Adding to list."
    STALE_UNMERGED_BRANCHES+=("$BRANCH_NAME")
  else
    echo "  Branch '${BRANCH_NAME}' is stale but appears merged or behind (status: ${COMPARE_STATUS}). Skipping."
  fi
done

# Format output as JSON array
JSON_OUTPUT=$(printf '%s\n' "${STALE_UNMERGED_BRANCHES[@]}" | jq -R . | jq -s .)

echo "🌿 Gardener's Report:"
if [ ${#STALE_UNMERGED_BRANCHES[@]} -eq 0 ]; then
  echo "  All branches are blooming! No stale, unmerged branches found."
else
  echo "  The following branches need pruning:"
  for branch in "${STALE_UNMERGED_BRANCHES[@]}"; do
    echo "    - ${branch}"
  done
fi

echo "stale_branches=${JSON_OUTPUT}" >> "$GITHUB_OUTPUT"
