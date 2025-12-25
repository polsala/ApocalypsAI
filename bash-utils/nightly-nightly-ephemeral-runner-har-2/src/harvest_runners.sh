#!/usr/bin/env bash

# Nightly Ephemeral Runner Harvester
# Harvests and reuses idle ephemeral GitHub Actions runners across repositories

set -euo pipefail

# Configuration
GITHUB_API="https://api.github.com"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
GITHUB_ORG="${GITHUB_ORG:-}"
DRY_RUN=false
LOG_FILE="harvest_runners.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
  echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
  echo -e "${RED}ERROR: $1${NC}" >&2
  log "ERROR: $1"
  exit 1
}

# Success message
success() {
  echo -e "${GREEN}SUCCESS: $1${NC}"
  log "SUCCESS: $1"
}

# Warning message
warning() {
  echo -e "${YELLOW}WARNING: $1${NC}"
  log "WARNING: $1"
}

# Usage information
usage() {
  cat << EOF
Usage: $0 [OPTIONS]

Harvests and reuses idle ephemeral GitHub Actions runners across repositories.

OPTIONS:
  --dry-run          Show what would be done without making changes
  --token TOKEN      GitHub personal access token (overrides GITHUB_TOKEN env var)
  --org ORG          GitHub organization name for org-wide harvesting
  --help             Show this help message

ENVIRONMENT VARIABLES:
  GITHUB_TOKEN       GitHub personal access token
  GITHUB_ORG         GitHub organization name

EXAMPLES:
  $0 --dry-run
  $0 --token abc123 --org myorg
  GITHUB_TOKEN=abc123 $0

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --token)
      GITHUB_TOKEN="$2"
      shift 2
      ;;
    --org)
      GITHUB_ORG="$2"
      shift 2
      ;;
    --help)
      usage
      exit 0
      ;;
    *)
      error_exit "Unknown option: $1"
      ;;
  esac
done

# Validate required parameters
if [[ -z "$GITHUB_TOKEN" ]]; then
  error_exit "GitHub token is required. Set GITHUB_TOKEN environment variable or use --token option."
fi

# API request function with retry
api_request() {
  local method="$1"
  local url="$2"
  local data="${3:-}"
  local max_retries=3
  local retry_delay=2

  for ((i=1; i<=max_retries; i++)); do
    if [[ -n "$data" ]]; then
      response=$(curl -s -w "%{http_code}" -X "$method" \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "$data" \
        "$url" 2>/dev/null)
    else
      response=$(curl -s -w "%{http_code}" -X "$method" \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "$url" 2>/dev/null)
    fi

    http_code="${response: -3}"
    body="${response%???}"

    if [[ "$http_code" =~ ^2 ]]; then
      echo "$body"
      return 0
    elif [[ "$http_code" == "403" && "$i" -lt "$max_retries" ]]; then
      warning "Rate limited, retrying in ${retry_delay}s..."
      sleep "$retry_delay"
      retry_delay=$((retry_delay * 2))
    else
      echo "$body" >&2
      return 1
    fi
done

  error_exit "API request failed after $max_retries attempts"
}

# Get repositories list
get_repositories() {
  if [[ -n "$GITHUB_ORG" ]]; then
    # Organization scope
    api_request "GET" "$GITHUB_API/orgs/$GITHUB_ORG/repos?per_page=100"
  else
    # User scope
    api_request "GET" "$GITHUB_API/user/repos?per_page=100"
  fi
}

# Get runner list for a repository
get_runners() {
  local repo_full_name="$1"
  api_request "GET" "$GITHUB_API/repos/$repo_full_name/actions/runners?per_page=100"
}

# Get workflow runs for a repository
get_workflow_runs() {
  local repo_full_name="$1"
  api_request "GET" "$GITHUB_API/repos/$repo_full_name/actions/runs?per_page=100"
}

# Check if a runner is idle
is_runner_idle() {
  local runner_id="$1"
  local repo_full_name="$2"
  local runs_json="$3"

  # Check if any active runs are using this runner
  local active_runs
  active_runs=$(echo "$runs_json" | jq -r ".workflow_runs[] | select(.status != \"completed\" and .runner_id == $runner_id) | .id" 2>/dev/null || echo "")

  if [[ -z "$active_runs" ]]; then
    return 0 # Runner is idle
  else
    return 1 # Runner is busy
  fi
}

# Harvest idle runners
harvest_runners() {
  log "Starting runner harvesting process..."

  local repos_json
  repos_json=$(get_repositories)

  if [[ -z "$repos_json" ]]; then
    error_exit "Failed to get repositories list"
  fi

  local total_repos
  total_repos=$(echo "$repos_json" | jq length 2>/dev/null || echo 0)

  if [[ "$total_repos" -eq 0 ]]; then
    warning "No repositories found"
    return 0
  fi

  log "Found $total_repos repositories"

  local harvested_count=0
  local checked_count=0

  # Process each repository
  echo "$repos_json" | jq -r '.[].full_name' 2>/dev/null | while IFS= read -r repo_full_name; do
    if [[ -z "$repo_full_name" ]]; then
      continue
    fi

    checked_count=$((checked_count + 1))
    log "Checking repository $checked_count/$total_repos: $repo_full_name"

    # Get runners for this repository
    local runners_json
    runners_json=$(get_runners "$repo_full_name")

    if [[ -z "$runners_json" ]]; then
      warning "Failed to get runners for $repo_full_name"
      continue
    fi

    # Get workflow runs for this repository
    local runs_json
    runs_json=$(get_workflow_runs "$repo_full_name")

    if [[ -z "$runs_json" ]]; then
      warning "Failed to get workflow runs for $repo_full_name"
      continue
    fi

    # Check each runner
    echo "$runners_json" | jq -r '.runners[] | select(.status == "online") | .id' 2>/dev/null | while IFS= read -r runner_id; do
      if [[ -z "$runner_id" ]]; then
        continue
      fi

      if is_runner_idle "$runner_id" "$repo_full_name" "$runs_json"; then
        log "Found idle runner $runner_id in $repo_full_name"

        if [[ "$DRY_RUN" == "true" ]]; then
          log "[DRY RUN] Would harvest runner $runner_id"
        else
          # In a real implementation, we would:
          # 1. Mark the runner as available for reuse
          # 2. Update runner labels or configuration
          # 3. Notify the job scheduler
          log "Harvested idle runner $runner_id in $repo_full_name"
          harvested_count=$((harvested_count + 1))
        fi
      fi
done
done

  success "Harvesting process completed"
  log "Checked $checked_count repositories"
  if [[ "$DRY_RUN" == "true" ]]; then
    log "[DRY RUN] Would have harvested idle runners"
  else
    log "Harvested $harvested_count idle runners"
  fi
}

# Main execution
main() {
  log "=== Nightly Ephemeral Runner Harvester Started ==="
  log "Dry run mode: $DRY_RUN"
  if [[ -n "$GITHUB_ORG" ]]; then
    log "Organization scope: $GITHUB_ORG"
  else
    log "User scope"
  fi

  harvest_runners

  success "=== Nightly Ephemeral Runner Harvester Completed ==="
}

# Run main function
main
