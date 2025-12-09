#!/bin/bash

# Nightly Git Branch Pruner
# Automatically closes stale branches based on configurable inactivity and naming rules.

set -euo pipefail

# Configuration
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
DAYS_INACTIVE="${DAYS_INACTIVE:-30}"
PROTECTED_BRANCHES="${PROTECTED_BRANCHES:-main,master,develop,dev,release/*}"
DRY_RUN="${DRY_RUN:-false}"
REPO="${GITHUB_REPOSITORY:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging
log() {
  echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
  echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

error() {
  echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" >&2
}

# Validation
if [[ -z "$GITHUB_TOKEN" ]]; then
  error "GITHUB_TOKEN is required"
  exit 1
fi

if [[ -z "$REPO" ]]; then
  error "GITHUB_REPOSITORY environment variable is required"
  exit 1
fi

# Convert comma-separated protected branches to array
IFS=',' read -ra PROTECTED_ARRAY <<< "$PROTECTED_BRANCHES"

# Function to check if branch matches protected patterns
is_protected() {
  local branch_name="$1"
  for pattern in "${PROTECTED_ARRAY[@]}"; do
    if [[ "$branch_name" == $pattern ]]; then
      return 0
    fi
  done
  return 1
}

# Function to check if branch is stale
is_stale() {
  local branch_name="$1"
  local last_commit_date="$2"
  
  # Convert last commit date to timestamp
  local last_commit_timestamp
  last_commit_timestamp=$(date -d "$last_commit_date" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$last_commit_date" +%s 2>/dev/null || echo "0")
  
  if [[ "$last_commit_timestamp" == "0" ]]; then
    warn "Could not parse date for branch $branch_name, skipping"
    return 1
  fi
  
  # Calculate days since last commit
  local current_timestamp
  current_timestamp=$(date +%s)
  local days_since_commit
  days_since_commit=$(( (current_timestamp - last_commit_timestamp) / 86400 ))
  
  if [[ $days_since_commit -gt $DAYS_INACTIVE ]]; then
    return 0
  else
    return 1
  fi
}

# Function to close a branch (create a pull request to close it)
close_branch() {
  local branch_name="$1"
  local reason="$2"
  
  log "Processing branch: $branch_name ($reason)"
  
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[DRY RUN] Would close branch: $branch_name"
    return 0
  fi
  
  # Create a pull request to close the branch
  local pr_body="This branch is being closed due to inactivity.\n\nReason: $reason\n\nPlease merge or rebase any necessary changes before this PR is merged."
  
  local pr_response
  pr_response=$(curl -s -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/repos/$REPO/pulls \
    -d "$(cat <<EOF
{
  "title": "Close stale branch: $branch_name",
  "body": "$pr_body",
  "head": "$branch_name",
  "base": "main"
}
EOF
)")
  
  if [[ $(echo "$pr_response" | jq -r '.message // empty') == "Not Found" ]]; then
    warn "Could not create PR for branch $branch_name (possibly already closed)"
    return 0
  fi
  
  local pr_number
  pr_number=$(echo "$pr_response" | jq -r '.number // empty')
  
  if [[ -n "$pr_number" && "$pr_number" != "null" ]]; then
    log "Successfully created PR #$pr_number to close branch: $branch_name"
  else
    error "Failed to create PR for branch $branch_name"
    error "Response: $pr_response"
    return 1
  fi
}

# Main execution
log "Starting branch pruning process"
log "Repository: $REPO"
log "Days inactive threshold: $DAYS_INACTIVE"
log "Protected branches: $PROTECTED_BRANCHES"
log "Dry run mode: $DRY_RUN"

# Get all branches
log "Fetching all branches..."
local branches_response
branches_response=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$REPO/branches?per_page=100")

# Parse branches
local branch_count
branch_count=$(echo "$branches_response" | jq length)

log "Found $branch_count branches"

# Process each branch
local processed=0
local closed=0
local skipped=0

for ((i=0; i<branch_count; i++)); do
  local branch_name
  branch_name=$(echo "$branches_response" | jq -r ".[$i].name")
  
  local last_commit_sha
  last_commit_sha=$(echo "$branches_response" | jq -r ".[$i].commit.sha")
  
  local last_commit_date
  last_commit_date=$(echo "$branches_response" | jq -r ".[$i].commit.commit.author.date")
  
  processed=$((processed + 1))
  
  # Skip protected branches
  if is_protected "$branch_name"; then
    skipped=$((skipped + 1))
    log "Skipping protected branch: $branch_name"
    continue
  fi
  
  # Check if branch is stale
  if is_stale "$branch_name" "$last_commit_date"; then
    close_branch "$branch_name" "Inactive for more than $DAYS_INACTIVE days"
    closed=$((closed + 1))
  else
    skipped=$((skipped + 1))
    log "Branch $branch_name is still active (last commit: $last_commit_date)"
  fi
done

log "Branch pruning complete!"
log "Processed: $processed, Closed: $closed, Skipped: $skipped"

# Exit with error if no branches were processed (possible API error)
if [[ $processed -eq 0 ]]; then
  error "No branches were processed. Check API access and repository permissions."
  exit 1
fi
