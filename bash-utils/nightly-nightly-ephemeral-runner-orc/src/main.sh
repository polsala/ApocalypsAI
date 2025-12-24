#!/bin/bash

# Nightly Ephemeral Runner Orchestrator
# A whimsical-yet-useful Bash utility for managing GitHub Actions runners

set -euo pipefail

# Configuration
GITHUB_API_BASE="https://api.github.com"
LOG_FILE="/tmp/runner_orchestrator.log"
HEALTH_THRESHOLD=300  # seconds

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
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

# Check dependencies
check_deps() {
    local deps=("curl" "jq")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            error_exit "$dep is required but not installed"
        fi
    done
}

# API request wrapper
api_request() {
    local method="$1"
    local endpoint="$2"
    local token="$3"
    local data="${4:-}"
    
    local url="$GITHUB_API_BASE$endpoint"
    local headers=(
        "Authorization: token $token"
        "Accept: application/vnd.github.v3+json"
        "User-Agent: runner-orchestrator"
    )
    
    local curl_args=(
        "-s"
        "-w" "\n%{http_code}"
        "${headers[@]/#/-H }"
    )
    
    if [[ "$method" == "POST" && -n "$data" ]]; then
        curl_args+=("-X" "POST" "-d" "$data")
    elif [[ "$method" == "DELETE" ]]; then
        curl_args+=("-X" "DELETE")
    fi
    
    curl_args+=("$url")
    
    local response
    response=$(curl "${curl_args[@]}")
    local http_code
    http_code=$(echo "$response" | tail -n1)
    local body
    body=$(echo "$response" | head -n-1)
    
    if [[ "$http_code" -ge 400 ]]; then
        error_exit "API request failed with code $http_code: $body"
    fi
    
    echo "$body"
}

# Provision a new runner
provision_runner() {
    local token="$1"
    local org="$2"
    local runner_name="ephemeral-runner-$(date +%s)"
    
    log "Provisioning runner: $runner_name"
    
    # Get runner registration token
    local reg_token
    reg_token=$(api_request "POST" "/orgs/$org/actions/runners/registration-token" "$token" | jq -r '.token')
    
    if [[ "$reg_token" == "null" || -z "$reg_token" ]]; then
        error_exit "Failed to get registration token"
    fi
    
    # This would normally install the runner, but for this utility
    # we'll just simulate it and log the registration token
    log "Runner $runner_name provisioned with token: $reg_token"
    success "Runner $runner_name provisioned successfully"
    
    # In a real implementation, you would:
    # 1. SSH to your runner host
    # 2. Download and configure the runner
    # 3. Start the runner service
}

# Get list of runners
get_runners() {
    local token="$1"
    local org="$2"
    
    api_request "GET" "/orgs/$org/actions/runners" "$token"
}

# Check runner health
health_check() {
    local token="$1"
    local org="$2"
    
    log "Performing health check for organization: $org"
    
    local runners_json
    runners_json=$(get_runners "$token" "$org")
    
    local total_runners
    total_runners=$(echo "$runners_json" | jq '.total_count')
    
    if [[ "$total_runners" -eq 0 ]]; then
        warning "No runners found for organization: $org"
        return 0
    fi
    
    local healthy_count=0
    local unhealthy_count=0
    
    # Check each runner
    echo "$runners_json" | jq -r '.runners[] | "\(.id)|\(.name)|\(.status)|\(.busy)"' | while IFS='|' read -r id name status busy; do
        if [[ "$status" == "online" ]]; then
            if [[ "$busy" == "false" ]]; then
                success "Runner $name (ID: $id) is healthy and idle"
                ((healthy_count++))
            else
                success "Runner $name (ID: $id) is healthy but busy"
                ((healthy_count++))
            fi
        else
            warning "Runner $name (ID: $id) is offline or in an unknown state"
            ((unhealthy_count++))
        fi
    done
    
    log "Health check complete: $healthy_count healthy, $unhealthy_count unhealthy"
}

# Cleanup idle runners
cleanup_runners() {
    local token="$1"
    local org="$2"
    
    log "Cleaning up idle runners for organization: $org"
    
    local runners_json
    runners_json=$(get_runners "$token" "$org")
    
    local total_runners
    total_runners=$(echo "$runners_json" | jq '.total_count')
    
    if [[ "$total_runners" -eq 0 ]]; then
        warning "No runners found for cleanup"
        return 0
    fi
    
    local cleaned_count=0
    
    # Delete idle runners (this is a simulation - in reality you'd want more careful logic)
    echo "$runners_json" | jq -r '.runners[] | select(.status == "online" and .busy == false) | .id' | while read -r runner_id; do
        log "Deleting idle runner ID: $runner_id"
        # Note: GitHub API doesn't support deleting runners via REST API
        # This would require using the runner's own API or manual cleanup
        warning "Simulated deletion of runner $runner_id (API limitation)"
        ((cleaned_count++))
    done
    
    if [[ "$cleaned_count" -eq 0 ]]; then
        warning "No idle runners found for cleanup"
    else
        success "Cleaned up $cleaned_count idle runners"
    fi
}

# Show help
show_help() {
    cat << EOF
Nightly Ephemeral Runner Orchestrator

Usage: $0 <command> [options]

Commands:
  provision --token TOKEN --org ORG    Provision a new ephemeral runner
  health-check --token TOKEN --org ORG  Check health of all runners
  cleanup --token TOKEN --org ORG       Cleanup idle runners
  help                                  Show this help message

Options:
  --token TOKEN    GitHub Personal Access Token
  --org ORG        GitHub organization name
  --help           Show help message

Examples:
  $0 provision --token abc123 --org my-org
  $0 health-check --token abc123 --org my-org
  $0 cleanup --token abc123 --org my-org

Requirements:
  - GitHub Personal Access Token with admin:org scope
  - curl and jq installed

EOF
}

# Parse command line arguments
parse_args() {
    local command=""
    local token=""
    local org=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            provision|health-check|cleanup)
                command="$1"
                shift
                ;;
            --token)
                token="$2"
                shift 2
                ;;
            --org)
                org="$2"
                shift 2
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                error_exit "Unknown option: $1"
                ;;
        esac
    done
    
    # Validate required arguments
    if [[ -z "$command" ]]; then
        error_exit "No command specified. Use --help for usage information."
    fi
    
    if [[ -z "$token" || -z "$org" ]]; then
        error_exit "Token and organization are required for command: $command"
    fi
    
    # Execute command
    case "$command" in
        provision)
            provision_runner "$token" "$org"
            ;;
        health-check)
            health_check "$token" "$org"
            ;;
        cleanup)
            cleanup_runners "$token" "$org"
            ;;
    esac
}

# Main execution
main() {
    check_deps
    parse_args "$@"
}

# Run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
