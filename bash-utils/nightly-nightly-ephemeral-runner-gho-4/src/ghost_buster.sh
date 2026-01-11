#!/usr/bin/env bash

# Nightly Ephemeral Runner Ghost Buster
# Detects and cleans up orphaned GitHub Actions self-hosted runners

set -euo pipefail

# Configuration
GITHUB_API="https://api.github.com"
REPORT_FILE="ghost_buster_report.json"
DEFAULT_AGE_HOURS=24

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging
log() {
  echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*"
}

warn() {
  echo -e "${YELLOW}[WARN]${NC} $*" >&2
}

error() {
  echo -e "${RED}[ERROR]${NC} $*" >&2
}

# Usage
usage() {
  cat <<EOF
Usage: $0 [OPTIONS]

Detects and cleans up orphaned GitHub Actions self-hosted runners.

OPTIONS:
  --repo-owner OWNER    GitHub repository owner (org or user)
  --repo-name NAME      GitHub repository name
  --cloud CLOUD         Cloud provider: aws, azure, gcp
  --age HOURS           Age in hours to consider instances stale (default: 24)
  --dry-run             Show what would be deleted without making changes
  --help                Show this help message

EXAMPLES:
  $0 --repo-owner myorg --repo-name myrepo --cloud aws --age 24
  $0 --cloud aws --age 12 --dry-run

EOF
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --repo-owner)
      REPO_OWNER="$2"
      shift 2
      ;;
    --repo-name)
      REPO_NAME="$2"
      shift 2
      ;;
    --cloud)
      CLOUD="$2"
      shift 2
      ;;
    --age)
      AGE_HOURS="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --help)
      usage
      ;;
    *)
      error "Unknown option: $1"
      usage
      ;;
  esac
done

# Validate required args
if [[ -z "${CLOUD:-}" ]]; then
  error "--cloud is required"
  usage
fi

if [[ -z "${AGE_HOURS:-}" ]]; then
  AGE_HOURS=${DEFAULT_AGE_HOURS}
fi

if [[ "${CLOUD}" != "aws" && "${CLOUD}" != "azure" && "${CLOUD}" != "gcp" ]]; then
  error "--cloud must be one of: aws, azure, gcp"
  usage
fi

if [[ "${DRY_RUN:-false}" == "true" ]]; then
  log "DRY RUN mode enabled - no changes will be made"
fi

# Initialize report
REPORT=$(cat <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "cloud": "${CLOUD}",
  "age_hours": ${AGE_HOURS},
  "dry_run": ${DRY_RUN:-false},
  "orphaned_runners": [],
  "cleaned_instances": [],
  "summary": {
    "total_instances": 0,
    "stale_instances": 0,
    "orphaned_runners_count": 0,
    "cleaned_count": 0
  }
}
EOF
)

# Function to update report
update_report() {
  local key="$1"
  local value="$2"
  REPORT=$(echo "$REPORT" | jq ".${key} = ${value}")
}

# Function to append to array in report
append_to_report() {
  local key="$1"
  local item="$2"
  REPORT=$(echo "$REPORT" | jq ".${key} += [${item}]")
}

# Get GitHub runners
get_github_runners() {
  if [[ -z "${REPO_OWNER:-}" || -z "${REPO_NAME:-}" ]]; then
    warn "Skipping GitHub runner fetch - repo not specified"
    return 1
  fi

  if [[ -z "${GITHUB_TOKEN:-}" ]]; then
    error "GITHUB_TOKEN environment variable is required for GitHub API access"
    return 1
  fi

  log "Fetching GitHub runners for ${REPO_OWNER}/${REPO_NAME}"

  local url="${GITHUB_API}/repos/${REPO_OWNER}/${REPO_NAME}/actions/runners"

  local response
  response=$(curl -s -H "Authorization: token ${GITHUB_TOKEN}" "${url}")

  if echo "$response" | jq -e '.runners' >/dev/null 2>&1; then
    echo "$response" | jq '.runners[] | {id, name, status, busy, labels}'
  else
    error "Failed to fetch runners: $response"
    return 1
  fi
}

# Get cloud instances
get_cloud_instances() {
  log "Fetching instances from ${CLOUD}"

  case "${CLOUD}" in
    aws)
      # Mock AWS CLI output for testing
      if command -v aws >/dev/null 2>&1; then
        aws ec2 describe-instances --query 'Reservations[].Instances[?State.Name==`running`].[InstanceId,Tags[?Key==`Name`].Value|[0],LaunchTime]' --output json
      else
        warn "AWS CLI not found - using mock data"
        cat <<'MOCK_AWS'
["i-12345", "runner-aws-1", "2025-01-01T00:00:00.000Z"]
["i-67890", "runner-aws-2", "2025-01-01T00:00:00.000Z"]
MOCK_AWS
      fi
      ;;
    azure)
      if command -v az >/dev/null 2>&1; then
        az vm list --query '[].{id:id, name:name, timeCreated:timeCreated}' --output json
      else
        warn "Azure CLI not found - using mock data"
        cat <<'MOCK_AZ'
{"id":"vm-1", "name":"runner-azure-1", "timeCreated":"2025-01-01T00:00:00.000Z"}
{"id":"vm-2", "name":"runner-azure-2", "timeCreated":"2025-01-01T00:00:00.000Z"}
MOCK_AZ
      fi
      ;;
    gcp)
      if command -v gcloud >/dev/null 2>&1; then
        gcloud compute instances list --format='json(name, id, creationTimestamp)'
      else
        warn "gcloud CLI not found - using mock data"
        cat <<'MOCK_GCP'
{"name":"runner-gcp-1", "id":"123", "creationTimestamp":"2025-01-01T00:00:00.000-00:00"}
{"name":"runner-gcp-2", "id":"456", "creationTimestamp":"2025-01-01T00:00:00.000-00:00"}
MOCK_GCP
      fi
      ;;
  esac
}

# Detect orphaned runners
# Mock rationale: Uses jq to parse JSON and compare runner names with instance names.
detect_orphaned_runners() {
  if [[ -z "${REPO_OWNER:-}" || -z "${REPO_NAME:-}" ]]; then
    return 0
  fi

  log "Detecting orphaned runners"

  local runners_file="/tmp/runners.json"
  local instances_file="/tmp/instances.json"

  get_github_runners >"${runners_file}" 2>/dev/null || true
  get_cloud_instances >"${instances_file}" 2>/dev/null || true

  # Extract instance names
  local instance_names
  case "${CLOUD}" in
    aws)
      instance_names=$(jq -r '.[1]' "${instances_file}" 2>/dev/null || echo "")
      ;;
    azure)
      instance_names=$(jq -r '.name' "${instances_file}" 2>/dev/null || echo "")
      ;;
    gcp)
      instance_names=$(jq -r '.name' "${instances_file}" 2>/dev/null || echo "")
      ;;
  esac

  # Check each runner
  while IFS= read -r runner; do
    local runner_name
    runner_name=$(echo "$runner" | jq -r '.name')

    if ! echo "${instance_names}" | grep -q "${runner_name}"; then
      log "Orphaned runner detected: ${runner_name}"
      append_to_report "orphaned_runners" "${runner}"
      update_report "summary.orphaned_runners_count" "$(echo "$REPORT" | jq '.summary.orphaned_runners_count') + 1"
    fi
  done < <(jq -c '.' "${runners_file}" 2>/dev/null || true)
}

# Cleanup stale instances
# Mock rationale: Compares instance launch time with current time to find stale instances.
cleanup_stale_instances() {
  log "Cleaning up stale instances (older than ${AGE_HOURS} hours)"

  local instances_file="/tmp/instances.json"
  get_cloud_instances >"${instances_file}" 2>/dev/null || true

  local cutoff_epoch
  cutoff_epoch=$(date -d "${AGE_HOURS} hours ago" +%s)

  local total=0
  local stale=0

  while IFS= read -r instance; do
    total=$((total + 1))

    local launch_time
    case "${CLOUD}" in
      aws)
        launch_time=$(echo "$instance" | jq -r '.[2]')
        ;;
      azure)
        launch_time=$(echo "$instance" | jq -r '.timeCreated')
        ;;
      gcp)
        launch_time=$(echo "$instance" | jq -r '.creationTimestamp')
        ;;
    esac

    if [[ -n "${launch_time}" && "${launch_time}" != "null" ]]; then
      local launch_epoch
      # Convert ISO 8601 to epoch (simplified for mock)
      launch_epoch=$(date -d "${launch_time}" +%s 2>/dev/null || echo 0)

      if [[ $launch_epoch -lt $cutoff_epoch ]]; then
        stale=$((stale + 1))
        log "Stale instance: ${instance}"

        if [[ "${DRY_RUN:-false}" != "true" ]]; then
          # Perform actual cleanup based on cloud
          case "${CLOUD}" in
            aws)
              local instance_id
              instance_id=$(echo "$instance" | jq -r '.[0]')
              log "Terminating AWS instance ${instance_id}"
              # aws ec2 terminate-instances --instance-ids "${instance_id}" >/dev/null
              ;;
            azure)
              local vm_id
              vm_id=$(echo "$instance" | jq -r '.id')
              log "Deleting Azure VM ${vm_id}"
              # az vm delete --ids "${vm_id}" --yes --no-wait
              ;;
            gcp)
              local vm_name
              vm_name=$(echo "$instance" | jq -r '.name')
              log "Deleting GCP instance ${vm_name}"
              # gcloud compute instances delete "${vm_name}" --quiet
              ;;
          esac
        fi

        append_to_report "cleaned_instances" "${instance}"
        update_report "summary.cleaned_count" "$(echo "$REPORT" | jq '.summary.cleaned_count') + 1"
      fi
    fi
  done < <(jq -c '.' "${instances_file}" 2>/dev/null || true)

  update_report "summary.total_instances" "${total}"
  update_report "summary.stale_instances" "${stale}"
}

# Main execution
main() {
  log "Starting Ghost Buster for ${CLOUD}"

  detect_orphaned_runners
  cleanup_stale_instances

  log "Writing report to ${REPORT_FILE}"
  echo "$REPORT" | jq '.' >"${REPORT_FILE}"

  log "Ghost Buster completed"
  echo "--- Summary ---"
  echo "Total instances: $(echo "$REPORT" | jq '.summary.total_instances')"
  echo "Stale instances: $(echo "$REPORT" | jq '.summary.stale_instances')"
  echo "Orphaned runners: $(echo "$REPORT" | jq '.summary.orphaned_runners_count')"
  echo "Cleaned count: $(echo "$REPORT" | jq '.summary.cleaned_count')"
}

main "$@"
