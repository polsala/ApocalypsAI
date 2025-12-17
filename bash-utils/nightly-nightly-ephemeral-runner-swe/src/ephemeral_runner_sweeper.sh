#!/bin/bash

# Nightly Ephemeral Runner Sweeper
# Discovers and cleans up orphaned ephemeral GitHub self-hosted runners

set -euo pipefail

# Configuration
GITHUB_API_URL="${GITHUB_API_URL:-https://api.github.com}"
DEFAULT_THRESHOLD_HOURS=24
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Help function
show_help() {
  cat << EOF
Nightly Ephemeral Runner Sweeper

Usage: $0 [OPTIONS]

Options:
  --org ORG_NAME        GitHub organization name (required)
  --threshold HOURS     Inactivity threshold in hours (default: 24)
  --dry-run            Show what would be removed without making changes
  --cleanup            Remove orphaned runners (requires --org)
  --help               Show this help message

Environment Variables:
  GITHUB_TOKEN         GitHub API token with admin:org scope
  GITHUB_API_URL       GitHub API URL (default: https://api.github.com)

Examples:
  $0 --org my-org --dry-run
  $0 --org my-org --cleanup
  $0 --org my-org --threshold 48 --cleanup

EOF
}

# Validate GitHub token
validate_token() {
  if [[ -z "${GITHUB_TOKEN:-}" ]]; then
    log_error "GITHUB_TOKEN environment variable is required"
    log_info "Set it with: export GITHUB_TOKEN=your_token_here"
    exit 1
  fi

  # Test token validity
  local response
  response=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github.v3+json" \
    "${GITHUB_API_URL}/user")

  if [[ "$response" != "200" ]]; then
    log_error "Invalid GitHub token or API request failed (HTTP $response)"
    exit 1
  fi

  log_success "GitHub token validated"
}

# Get all runners for an organization
get_runners() {
  local org_name="$1"
  local page=1
  local per_page=100
  local all_runners=""

  log_info "Fetching runners for organization: $org_name"

  while true; do
    local response
    response=$(curl -s \
      -H "Authorization: token ${GITHUB_TOKEN}" \
      -H "Accept: application/vnd.github.v3+json" \
      "${GITHUB_API_URL}/orgs/${org_name}/actions/runners?page=${page}&per_page=${per_page}")

    local runners_page
    runners_page=$(echo "$response" | jq -r '.runners[] | @base64' 2>/dev/null || true)

    if [[ -z "$runners_page" ]]; then
      break
    fi

    all_runners+="$runners_page\n"

    local total_count
    total_count=$(echo "$response" | jq -r '.total_count // 0')
    local current_count
    current_count=$(echo "$runners_page" | wc -l)

    if [[ $((page * per_page)) -ge $total_count ]]; then
      break
    fi

    page=$((page + 1))
  done

  echo "$all_runners" | base64 -d 2>/dev/null || echo ""
}

# Parse runner information
parse_runner_info() {
  local runner_json="$1"
  local runner_id name status busy created_at updated_at last_contacted_at

  runner_id=$(echo "$runner_json" | jq -r '.id // "unknown"')
  name=$(echo "$runner_json" | jq -r '.name // "unknown"')
  status=$(echo "$runner_json" | jq -r '.status // "unknown"')
  busy=$(echo "$runner_json" | jq -r '.busy // false')
  created_at=$(echo "$runner_json" | jq -r '.created_at // "unknown"')
  updated_at=$(echo "$runner_json" | jq -r '.updated_at // "unknown"')
  last_contacted_at=$(echo "$runner_json" | jq -r '.last_contacted_at // "unknown"')

  echo "$runner_id|$name|$status|$busy|$created_at|$updated_at|$last_contacted_at"
}

# Calculate hours since last contact
hours_since_contact() {
  local last_contact="$1"

  if [[ "$last_contact" == "unknown" || -z "$last_contact" ]]; then
    echo "99999"
    return
  fi

  local last_contact_epoch current_epoch hours_diff
  last_contact_epoch=$(date -d "$last_contact" +%s 2>/dev/null || echo "0")
  current_epoch=$(date +%s)
  hours_diff=$(( (current_epoch - last_contact_epoch) / 3600 ))

  echo "$hours_diff"
}

# Check if runner should be considered orphaned
is_orphaned_runner() {
  local status="$1"
  local busy="$2"
  local hours_inactive="$3"
  local threshold="$4"

  # Runner is orphaned if:
  # 1. It's offline OR
  # 2. It's online but not busy and has been inactive for threshold hours
  if [[ "$status" == "offline" ]]; then
    return 0
  elif [[ "$status" == "online" && "$busy" == "false" && $hours_inactive -gt $threshold ]]; then
    return 0
  fi
  return 1
}

# Remove a runner
remove_runner() {
  local org_name="$1"
  local runner_id="$2"
  local runner_name="$3"

  log_info "Removing runner $runner_name (ID: $runner_id)"

  local response_code
  response_code=$(curl -s -o /dev/null -w "%{http_code}" \
    -X DELETE \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github.v3+json" \
    "${GITHUB_API_URL}/orgs/${org_name}/actions/runners/${runner_id}")

  if [[ "$response_code" == "204" ]]; then
    log_success "Successfully removed runner $runner_name (ID: $runner_id)"
    return 0
  else
    log_error "Failed to remove runner $runner_name (ID: $runner_id). HTTP $response_code"
    return 1
  fi
}

# Generate cleanup report
generate_report() {
  local org_name="$1"
  local threshold="$2"
  local all_runners_json="$3"
  local orphaned_runners_json="$4"
  local dry_run="$5"
  local removed_count="$6"
  local failed_count="$7"

  local report_file="${SCRIPT_DIR}/cleanup_report.md"
  local timestamp
  timestamp=$(date -u '+%Y-%m-%d %H:%M:%S UTC')

  cat > "$report_file" << EOF
# Ephemeral Runner Cleanup Report

**Organization:** $org_name
**Threshold:** $threshold hours
**Mode:** $([ "$dry_run" == "true" ] && echo "DRY RUN" || echo "CLEANUP")
**Timestamp:** $timestamp
**GitHub API:** $GITHUB_API_URL

## Summary

EOF

  if [[ -n "$orphaned_runners_json" ]]; then
    cat >> "$report_file" << EOF
### Orphaned Runners Found

| Runner ID | Name | Status | Busy | Last Contacted | Hours Inactive |
|-----------|------|--------|------|----------------|----------------|
EOF

    echo "$orphaned_runners_json" | while IFS='|' read -r runner_id name status busy created_at updated_at last_contacted_at; do
      local hours_inactive
      hours_inactive=$(hours_since_contact "$last_contacted_at")
      cat >> "$report_file" << EOF
| $runner_id | $name | $status | $busy | $last_contacted_at | $hours_inactive |
EOF
    done
  else
    cat >> "$report_file" << EOF
No orphaned runners found.

EOF
  fi

  cat >> "$report_file" << EOF
### All Runners Status

| Runner ID | Name | Status | Busy | Last Contacted | Hours Inactive |
|-----------|------|--------|------|----------------|----------------|
EOF

  echo "$all_runners_json" | while IFS='|' read -r runner_id name status busy created_at updated_at last_contacted_at; do
    local hours_inactive
    hours_inactive=$(hours_since_contact "$last_contacted_at")
    cat >> "$report_file" << EOF
| $runner_id | $name | $status | $busy | $last_contacted_at | $hours_inactive |
EOF
  done

  if [[ "$dry_run" != "true" ]]; then
    cat >> "$report_file" << EOF

### Cleanup Results

- Runners removed: $removed_count
- Failed removals: $failed_count

EOF
  fi

  cat >> "$report_file" << EOF

---
*Generated by Nightly Ephemeral Runner Sweeper*
EOF

  log_success "Report generated: $report_file"
}

# Main execution function
main() {
  local org_name=""
  local threshold="$DEFAULT_THRESHOLD_HOURS"
  local dry_run="false"
  local cleanup="false"

  # Parse command line arguments
  while [[ $# -gt 0 ]]; do
    case $1 in
      --org)
        org_name="$2"
        shift 2
        ;;
      --threshold)
        threshold="$2"
        shift 2
        ;;
      --dry-run)
        dry_run="true"
        shift
        ;;
      --cleanup)
        cleanup="true"
        shift
        ;;
      --help)
        show_help
        exit 0
        ;;
      *)
        log_error "Unknown option: $1"
        show_help
        exit 1
        ;;
    esac
  done

  # Validate inputs
  if [[ -z "$org_name" ]]; then
    log_error "Organization name is required (--org ORG_NAME)"
    show_help
    exit 1
  fi

  if [[ ! "$threshold" =~ ^[0-9]+$ ]]; then
    log_error "Threshold must be a positive integer"
    exit 1
  fi

  if [[ "$cleanup" == "false" && "$dry_run" == "false" ]]; then
    log_error "Must specify either --dry-run or --cleanup"
    show_help
    exit 1
  fi

  # Validate GitHub token
  validate_token

  # Get all runners
  local all_runners_json
  all_runners_json=$(get_runners "$org_name")

  if [[ -z "$all_runners_json" ]]; then
    log_warn "No runners found for organization: $org_name"
    generate_report "$org_name" "$threshold" "" "" "$dry_run" 0 0
    exit 0
  fi

  log_info "Found $(echo "$all_runners_json" | wc -l) runners"

  # Process runners
  local orphaned_runners=""
  local removed_count=0
  local failed_count=0
  local all_runners_formatted=""

  echo "$all_runners_json" | while IFS='\n' read -r runner_json; do
    if [[ -n "$runner_json" ]]; then
      local runner_info
      runner_info=$(parse_runner_info "$runner_json")
      all_runners_formatted+="$runner_info\n"

      IFS='|' read -r runner_id name status busy created_at updated_at last_contacted_at <<< "$runner_info"
      local hours_inactive
      hours_inactive=$(hours_since_contact "$last_contacted_at")

      if is_orphaned_runner "$status" "$busy" "$hours_inactive" "$threshold"; then
        log_warn "Orphaned runner found: $name (ID: $runner_id, Status: $status, Inactive: ${hours_inactive}h)"
        orphaned_runners+="$runner_info\n"

        if [[ "$cleanup" == "true" ]]; then
          if remove_runner "$org_name" "$runner_id" "$name"; then
            removed_count=$((removed_count + 1))
          else
            failed_count=$((failed_count + 1))
          fi
        fi
      else
        log_info "Active runner: $name (ID: $runner_id, Status: $status, Inactive: ${hours_inactive}h)"
      fi
    fi
  done

  # Generate final report
  generate_report "$org_name" "$threshold" "$all_runners_formatted" "$orphaned_runners" "$dry_run" "$removed_count" "$failed_count"

  if [[ "$cleanup" == "true" ]]; then
    log_success "Cleanup completed. Removed: $removed_count, Failed: $failed_count"
  else
    log_success "Dry run completed. Use --cleanup to remove orphaned runners."
  fi
}

# Run main function with all arguments
main "$@"
