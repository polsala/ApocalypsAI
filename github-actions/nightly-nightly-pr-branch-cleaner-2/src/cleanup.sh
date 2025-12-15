#!/usr/bin/env bash
set -euo pipefail

# Parameters
TOKEN="${GITHUB_TOKEN}"
DAYS_OLD="${DAYS_OLD:-30}"
REPO="${GITHUB_REPOSITORY}"
API_URL="https://api.github.com"

# Helper to get ISO date cutoff
CUTOFF_DATE=$(date -u -d "-${DAYS_OLD} days" +"%Y-%m-%dT%H:%M:%SZ")

# Function to fetch branches (mockable)
fetch_branches() {
  if [[ "${MOCK_MODE:-}" == "1" ]]; then
    echo "${MOCK_BRANCHES}"
  else
    curl -s -H "Authorization: token $TOKEN" "$API_URL/repos/$REPO/branches?per_page=100"
  fi
}

# Function to fetch PR for a branch (mockable)
fetch_pr_for_branch() {
  local branch="$1"
  if [[ "${MOCK_MODE:-}" == "1" ]]; then
    echo "${MOCK_PR_RESPONSE}"
  else
    curl -s -H "Authorization: token $TOKEN" "$API_URL/search/issues?q=repo:$REPO+type:pr+head:$branch+state:closed"
  fi
}

# Function to delete branch (mockable)
delete_branch() {
  local branch="$1"
  if [[ "${MOCK_MODE:-}" == "1" ]]; then
    echo "MOCK DELETE $branch"
  else
    curl -s -X DELETE -H "Authorization: token $TOKEN" "$API_URL/repos/$REPO/git/refs/heads/$branch"
  fi
}

# Main logic
branches_json=$(fetch_branches)
branch_names=$(echo "$branches_json" | jq -r '.[].name')

for branch in $branch_names; do
  # Skip default branches
  if [[ "$branch" == "main" || "$branch" == "master" ]]; then
    continue
  fi

  pr_json=$(fetch_pr_for_branch "$branch")
  # Find merged PRs
  merged_pr=$(echo "$pr_json" | jq -r '.items[] | select(.state=="closed" and .pull_request.merged_at != null) | .pull_request.merged_at' | head -n1 || true)
  if [[ -z "$merged_pr" ]]; then
    continue
  fi

  # Compare dates (ISO 8601 strings compare lexicographically)
  if [[ "$merged_pr" < "$CUTOFF_DATE" ]]; then
    delete_branch "$branch"
    echo "🗑️ Farewell, \`$branch\`! May your code rest in peace."
  fi
done
