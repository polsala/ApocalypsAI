#!/bin/bash

# Nightly Ephemeral Runner Ghost Buster
# Detects and cleans up orphaned GitHub Actions runners

set -euo pipefail

# Script metadata
SCRIPT_NAME="$(basename "$0")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="1.0.0"

# Default configuration
DEFAULT_RETENTION_DAYS=3
DEFAULT_DRY_RUN=false
DEFAULT_VERBOSE=false
DEFAULT_OUTPUT="ghost_report_$(date +%Y%m%d_%H%M%S).json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
GITHUB_TOKEN=""
API_BASE_URL="https://api.github.com"
REPOSITORIES=()
RETENTION_DAYS=$DEFAULT_RETENTION_DAYS
DRY_RUN=$DEFAULT_DRY_RUN
VERBOSE=$DEFAULT_VERBOSE
OUTPUT_FILE="$DEFAULT_OUTPUT"

# Logging functions
log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_debug() {
  if [[ $VERBOSE == true ]]; then
    echo -e "${BLUE}[DEBUG]${NC} $1"
  fi
}

# Utility functions
print_usage() {
  cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

Detects and cleans up orphaned ephemeral GitHub Actions runners.

OPTIONS:
  --repos <list>          Comma-separated list of repositories to scan
  --retention-days <days> Keep runners registered within this many days (default: $DEFAULT_RETENTION_DAYS)
  --dry-run               Show what would be deleted without actually deleting
  --output <file>         Write report to specified file (default: $DEFAULT_OUTPUT)
  --verbose               Enable detailed logging
  --help                  Show this help message

ENVIRONMENT VARIABLES:
  GITHUB_TOKEN            Personal access token for GitHub API
  GITHUB_API_URL          Custom API base URL (for GitHub Enterprise)

EXAMPLES:
  $SCRIPT_NAME
  $SCRIPT_NAME --dry-run
  $SCRIPT_NAME --repos "owner/repo1,owner/repo2" --retention-days 7
  $SCRIPT_NAME --output report.json --verbose

EOF
}

load_config() {
  local config_file="$SCRIPT_DIR/config.json"
  
  if [[ -f "$config_file" ]]; then
    log_info "Loading configuration from $config_file"
    
    # Load GitHub token
    if command -v jq >/dev/null 2>&1; then
      local token=$(jq -r '.github_token // empty' "$config_file" 2>/dev/null || echo "")
      if [[ -n "$token" && "$token" != "null" ]]; then
        GITHUB_TOKEN="$token"
      fi
      
      # Load API URL
      local api_url=$(jq -r '.api_base_url // empty' "$config_file" 2>/dev/null || echo "")
      if [[ -n "$api_url" && "$api_url" != "null" ]]; then
        API_BASE_URL="$api_url"
      fi
      
      # Load repositories
      local repos=$(jq -r '.repositories[] // empty' "$config_file" 2>/dev/null || echo "")
      if [[ -n "$repos" ]]; then
        IFS=$'\n' read -d '' -r -a REPOSITORIES <<< "$repos"
      fi
      
      # Load retention days
      local retention=$(jq -r '.retention_days // empty' "$config_file" 2>/dev/null || echo "")
      if [[ -n "$retention" && "$retention" != "null" ]]; then
        RETENTION_DAYS="$retention"
      fi
      
      # Load dry run setting
      local dry_run=$(jq -r '.dry_run // empty' "$config_file" 2>/dev/null || echo "")
      if [[ "$dry_run" == "true" ]]; then
        DRY_RUN=true
      fi
      
      # Load verbose setting
      local verbose=$(jq -r '.verbose // empty' "$config_file" 2>/dev/null || echo "")
      if [[ "$verbose" == "true" ]]; then
        VERBOSE=true
      fi
    else
      log_warn "jq not found, skipping config file parsing"
    fi
  fi
}

validate_prerequisites() {
  local missing_tools=()
  
  if ! command -v curl >/dev/null 2>&1; then
    missing_tools+=("curl")
  fi
  
  if ! command -v jq >/dev/null 2>&1; then
    missing_tools+=("jq")
  fi
  
  if [[ ${#missing_tools[@]} -gt 0 ]]; then
    log_error "Missing required tools: ${missing_tools[*]}"
    log_info "Please install the missing tools and try again."
    exit 1
  fi
}

validate_token() {
  if [[ -z "$GITHUB_TOKEN" ]]; then
    if [[ -n "${GITHUB_TOKEN:-}" ]]; then
      GITHUB_TOKEN="$GITHUB_TOKEN"
    else
      log_error "GitHub token not found."
      log_info "Please set the GITHUB_TOKEN environment variable or add it to config.json"
      exit 1
    fi
  fi
  
  # Test token validity
  log_debug "Testing GitHub token validity"
  local test_response
  if test_response=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "$API_BASE_URL/user"); then
    
    if echo "$test_response" | jq -e '.login' >/dev/null 2>&1; then
      local username=$(echo "$test_response" | jq -r '.login')
      log_success "Authenticated as $username"
    else
      log_error "Invalid GitHub token or API response"
      log_debug "Response: $test_response"
      exit 1
    fi
  else
    log_error "Failed to authenticate with GitHub API"
    exit 1
  fi
}

parse_arguments() {
  while [[ $# -gt 0 ]]; do
    case $1 in
      --repos)
        IFS=',' read -ra REPO_ARRAY <<< "$2"
        REPOSITORIES+=("${REPO_ARRAY[@]}")
        shift 2
        ;;
      --retention-days)
        if [[ $2 =~ ^[0-9]+$ ]]; then
          RETENTION_DAYS="$2"
          shift 2
        else
          log_error "--retention-days must be a positive integer"
          exit 1
        fi
        ;;
      --dry-run)
        DRY_RUN=true
        shift
        ;;
      --output)
        OUTPUT_FILE="$2"
        shift 2
        ;;
      --verbose)
        VERBOSE=true
        shift
        ;;
      --help)
        print_usage
        exit 0
        ;;
      *)
        log_error "Unknown option: $1"
        print_usage
        exit 1
        ;;
    esac
  done
}

get_repositories() {
  # If no repositories specified, try to get from GitHub API
  if [[ ${#REPOSITORIES[@]} -eq 0 ]]; then
    log_info "No repositories specified, attempting to fetch user repositories"
    
    local repos_response
    if repos_response=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github.v3+json" \
      "$API_BASE_URL/user/repos?per_page=100"); then
      
      local repo_count=$(echo "$repos_response" | jq length)
      log_info "Found $repo_count repositories"
      
      # Extract repository names
      while IFS= read -r repo; do
        REPOSITORIES+=("$repo")
      done < <(echo "$repos_response" | jq -r '.[].full_name')
      
    else
      log_error "Failed to fetch repositories from GitHub API"
      exit 1
    fi
  fi
  
  if [[ ${#REPOSITORIES[@]} -eq 0 ]]; then
    log_error "No repositories to scan. Please specify repositories with --repos option."
    exit 1
  fi
  
  log_info "Will scan ${#REPOSITORIES[@]} repositories"
}

get_runner_registration_time() {
  local repo="$1"
  local runner_id="$2"
  
  local response
  if response=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "$API_BASE_URL/repos/$repo/actions/runners/$runner_id"); then
    
    if echo "$response" | jq -e '.created_at' >/dev/null 2>&1; then
      echo "$response" | jq -r '.created_at'
    else
      echo ""
    fi
  else
    echo ""
  fi
}

is_runner_orphaned() {
  local repo="$1"
  local runner_id="$2"
  
  # Get runner registration time
  local registration_time=$(get_runner_registration_time "$repo" "$runner_id")
  
  if [[ -z "$registration_time" ]]; then
    log_debug "Could not get registration time for runner $runner_id in $repo"
    return 1
  fi
  
  # Convert to timestamp
  local registration_timestamp
  if registration_timestamp=$(date -d "$registration_time" +%s 2>/dev/null); then
    local current_timestamp=$(date +%s)
    local retention_seconds=$((RETENTION_DAYS * 24 * 3600))
    local age_seconds=$((current_timestamp - registration_timestamp))
    
    if [[ $age_seconds -gt $retention_seconds ]]; then
      log_debug "Runner $runner_id in $repo is orphaned (age: $((age_seconds / 3600)) hours)"
      return 0
    else
      log_debug "Runner $runner_id in $repo is not orphaned (age: $((age_seconds / 3600)) hours)"
      return 1
    fi
  else
    log_debug "Could not parse registration time for runner $runner_id in $repo"
    return 1
  fi
}

scan_repository() {
  local repo="$1"
  local repo_results=()
  
  log_info "Scanning repository: $repo"
  
  # Get registered runners
  local runners_response
  if ! runners_response=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "$API_BASE_URL/repos/$repo/actions/runners"); then
    log_warn "Failed to fetch runners for $repo"
    return 1
  fi
  
  # Check if response is valid
  if ! echo "$runners_response" | jq -e '.runners' >/dev/null 2>&1; then
    log_warn "Invalid response for $repo: $runners_response"
    return 1
  fi
  
  local runner_count=$(echo "$runners_response" | jq '.runners | length')
  log_debug "Found $runner_count registered runners in $repo"
  
  # Process each runner
  local orphaned_count=0
  local total_count=0
  
  while IFS= read -r runner; do
    local runner_id=$(echo "$runner" | jq -r '.id')
    local runner_name=$(echo "$runner" | jq -r '.name')
    local runner_status=$(echo "$runner" | jq -r '.status')
    
    total_count=$((total_count + 1))
    
    log_debug "Checking runner $runner_id ($runner_name) with status $runner_status"
    
    # Only check offline runners
    if [[ "$runner_status" == "offline" ]]; then
      if is_runner_orphaned "$repo" "$runner_id"; then
        orphaned_count=$((orphaned_count + 1))
        
        # Build runner info
        local runner_info=$(cat << EOF
{
  "id": $runner_id,
  "name": "$runner_name",
  "status": "$runner_status",
  "repository": "$repo",
  "registration_time": "$(get_runner_registration_time "$repo" "$runner_id")"
}
EOF
)
        
        repo_results+=("$runner_info")
      fi
    fi
  done < <(echo "$runners_response" | jq -c '.runners[]')
  
  # Build repository result
  local repo_result=$(cat << EOF
{
  "repository": "$repo",
  "total_runners": $total_count,
  "orphaned_runners": $orphaned_count,
  "runners": [$(IFS=,; echo "${repo_results[*]}")]
}
EOF
)

  echo "$repo_result"
}

delete_runner() {
  local repo="$1"
  local runner_id="$2"
  
  log_info "Deleting runner $runner_id from $repo"
  
  if [[ $DRY_RUN == true ]]; then
    log_warn "[DRY RUN] Would delete runner $runner_id from $repo"
    return 0
  fi
  
  local response
  if response=$(curl -s -X DELETE -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "$API_BASE_URL/repos/$repo/actions/runners/$runner_id"); then
    
    if [[ -z "$response" ]] || echo "$response" | jq -e 'empty' >/dev/null 2>&1; then
      log_success "Successfully deleted runner $runner_id from $repo"
      return 0
    else
      log_error "Failed to delete runner $runner_id from $repo: $response"
      return 1
    fi
  else
    log_error "API request failed for deleting runner $runner_id from $repo"
    return 1
  fi
}

process_orphaned_runners() {
  local all_results=()
  local total_orphaned=0
  local total_deleted=0
  local errors=()
  
  log_info "Starting scan of ${#REPOSITORIES[@]} repositories"
  
  for repo in "${REPOSITORIES[@]}"; do
    local repo_result
    if repo_result=$(scan_repository "$repo"); then
      all_results+=("$repo_result")
      
      local orphaned_count=$(echo "$repo_result" | jq '.orphaned_runners')
      total_orphaned=$((total_orphaned + orphaned_count))
      
      # Process orphaned runners for deletion
      while IFS= read -r runner; do
        local runner_id=$(echo "$runner" | jq -r '.id')
        
        if delete_runner "$repo" "$runner_id"; then
          total_deleted=$((total_deleted + 1))
        else
          errors+=("Failed to delete runner $runner_id from $repo")
        fi
      done < <(echo "$repo_result" | jq -c '.runners[]')
    else
      errors+=("Failed to scan repository $repo")
    fi
  done
  
  # Generate report
  generate_report "$total_orphaned" "$total_deleted" "${errors[@]}"
}

generate_report() {
  local total_orphaned="$1"
  local total_deleted="$2"
  shift 2
  local errors=("$@")
  
  log_info "Generating report: $OUTPUT_FILE"
  
  local report=$(cat << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "version": "$VERSION",
  "configuration": {
    "retention_days": $RETENTION_DAYS,
    "dry_run": $DRY_RUN,
    "repositories_scanned": ${#REPOSITORIES[@]},
    "repositories": [$(printf '%s\n' "${REPOSITORIES[@]}" | jq -R . | jq -s .)]
  },
  "summary": {
    "total_orphaned_runners": $total_orphaned,
    "total_deleted_runners": $total_deleted,
    "errors_count": ${#errors[@]}
  },
  "results": [$(IFS=,; echo "${all_results[*]}")],
  "errors": [$(printf '%s\n' "${errors[@]}" | jq -R . | jq -s .)]
}
EOF
)
  
  echo "$report" | jq . > "$OUTPUT_FILE"
  
  log_success "Report generated: $OUTPUT_FILE"
  log_info "Summary: $total_orphaned orphaned runners found, $total_deleted deleted, ${#errors[@]} errors"
  
  if [[ $DRY_RUN == true ]]; then
    log_warn "DRY RUN mode - no runners were actually deleted"
  fi
}

main() {
  log_info "Starting Nightly Ephemeral Runner Ghost Buster v$VERSION"
  
  # Load configuration
  load_config
  
  # Parse command line arguments
  parse_arguments "$@"
  
  # Validate prerequisites
  validate_prerequisites
  
  # Validate GitHub token
  validate_token
  
  # Get repositories to scan
  get_repositories
  
  # Process orphaned runners
  process_orphaned_runners
  
  log_success "Ghost Buster completed successfully"
}

# Run main function with all arguments
main "$@"
