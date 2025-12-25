#!/bin/bash

# Nightly Ephemeral Runner Harvester
# A whimsical-yet-useful Bash utility for harvesting and reusing GitHub runners

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/../.runner-config"
LOG_FILE="${SCRIPT_DIR}/../harvest.log"
BACKUP_DIR="${SCRIPT_DIR}/../backups"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    log "ERROR" "$1"
    exit 1
}

# Success logging
success() {
    log "SUCCESS" "$1"
    echo -e "${GREEN}✓ $1${NC}"
}

# Warning logging
warning() {
    log "WARNING" "$1"
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Info logging
info() {
    log "INFO" "$1"
    echo -e "${BLUE}ℹ $1${NC}"
}

# Debug logging (only if verbose)
debug() {
    if [[ "$VERBOSE" == "true" ]]; then
        log "DEBUG" "$1"
        echo -e "${BLUE}🐛 $1${NC}"
    fi
}

# Check dependencies
check_dependencies() {
    local missing=()
    
    command -v gh >/dev/null 2>&1 || missing+=("GitHub CLI (gh)")
    command -v jq >/dev/null 2>&1 || missing+=("jq")
    command -v curl >/dev/null 2>&1 || missing+=("curl")
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        error_exit "Missing dependencies: ${missing[*]}\nPlease install them before running this script."
    fi
}

# Load configuration
load_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        error_exit "Configuration file not found: $CONFIG_FILE\nPlease create a .runner-config file with your repository settings."
    fi
    
    # Parse YAML config using Python (more reliable than bash parsing)
    python3 << 'EOF' > /tmp/config.json
import yaml
import json
import sys

try:
    with open(sys.argv[1], 'r') as f:
        config = yaml.safe_load(f)
    json.dump(config, sys.stdout, indent=2)
except Exception as e:
    print(f"Error parsing config: {e}", file=sys.stderr)
    sys.exit(1)
EOF "$CONFIG_FILE"

    if [[ $? -ne 0 ]]; then
        error_exit "Failed to parse configuration file."
    fi
}

# Get repositories from config
get_repositories() {
    jq -r '.repositories[]' /tmp/config.json
}

# Get runner labels from config
get_runner_labels() {
    jq -r '.runner_labels[]' /tmp/config.json
}

# Get max runners per repo
get_max_runners() {
    jq -r '.max_runners_per_repo // 5' /tmp/config.json
}

# Get harvest interval
get_harvest_interval() {
    jq -r '.harvest_interval // 300' /tmp/config.json
}

# Check GitHub authentication
check_auth() {
    if ! gh auth status >/dev/null 2>&1; then
        error_exit "GitHub CLI is not authenticated. Please run 'gh auth login' first."
    fi
}

# Get runner token for a repository
get_runner_token() {
    local repo="$1"
    debug "Getting runner token for $repo"
    
    local token=""
    token=$(gh api "/repos/$repo/actions/runners/registration-token" -q '.token' 2>/dev/null) || {
        warning "Failed to get runner token for $repo"
        echo ""
        return 1
    }
    
    echo "$token"
}

# List existing runners for a repository
list_runners() {
    local repo="$1"
    debug "Listing runners for $repo"
    
    gh api "/repos/$repo/actions/runners" -q '.runners[] | {id, name, status, busy, labels}' 2>/dev/null || {
        warning "Failed to list runners for $repo"
        echo "[]"
    }
}

# Register a new runner
register_runner() {
    local repo="$1"
    local token="$2"
    local labels="$3"
    
    debug "Registering runner for $repo with labels: $labels"
    
    # Create runner registration payload
    local payload="{\"name\": \"ephemeral-runner-$(date +%s)-$(openssl rand -hex 4)\", \"labels\": [$(echo "$labels" | sed 's/ /","/g' | sed 's/^/"/' | sed 's/$/"/')]}"
    
    local response=""
    response=$(gh api "/repos/$repo/actions/runners" \
        -X POST \
        -H "Content-Type: application/json" \
        -d "$payload" \
        2>/dev/null) || {
        warning "Failed to register runner for $repo"
        return 1
    }
    
    echo "$response"
}

# Harvest runners from all repositories
harvest_runners() {
    info "Starting runner harvest process..."
    
    local repos=($(get_repositories))
    local max_runners=$(get_max_runners)
    local labels=($(get_runner_labels))
    local labels_str="$(IFS=,; echo "${labels[*]}")"
    
    local total_harvested=0
    local total_failed=0
    
    for repo in "${repos[@]}"; do
        info "Harvesting runners for repository: $repo"
        
        # Get existing runners count
        local existing_count=0
        existing_count=$(list_runners "$repo" | jq 'length' 2>/dev/null || echo 0)
        
        if [[ $existing_count -ge $max_runners ]]; then
            warning "Repository $repo already has maximum runners ($existing_count). Skipping."
            continue
        fi
        
        # Get runner token
        local token=""
        token=$(get_runner_token "$repo")
        
        if [[ -z "$token" ]]; then
            total_failed=$((total_failed + 1))
            continue
        fi
        
        # Register new runner
        local response=""
        response=$(register_runner "$repo" "$token" "$labels_str")
        
        if [[ -n "$response" ]]; then
            local runner_name=""
            runner_name=$(echo "$response" | jq -r '.name' 2>/dev/null || echo "unknown")
            success "Successfully registered runner: $runner_name for $repo"
            total_harvested=$((total_harvested + 1))
        else
            total_failed=$((total_failed + 1))
        fi
        
        # Rate limiting
        sleep 1
    done
    
    info "Harvest complete. Harvested: $total_harvested, Failed: $total_failed"
}

# Reuse existing runners across repositories
reuse_runners() {
    info "Starting runner reuse process..."
    
    local repos=($(get_repositories))
    local reused_count=0
    
    # Get all runners from all repositories
    local all_runners=()
    for repo in "${repos[@]}"; do
        debug "Getting runners from $repo"
        local runners=""
        runners=$(list_runners "$repo")
        all_runners+=("$runners")
    done
    
    # Analyze runner usage patterns
    local idle_runners=0
    local busy_runners=0
    
    for runners_json in "${all_runners[@]}"; do
        idle_runners=$((idle_runners + $(echo "$runners_json" | jq '[.[] | select(.busy == false)] | length' 2>/dev/null || echo 0)))
        busy_runners=$((busy_runners + $(echo "$runners_json" | jq '[.[] | select(.busy == true)] | length' 2>/dev/null || echo 0)))
    done
    
    info "Runner analysis: Idle: $idle_runners, Busy: $busy_runners"
    
    if [[ $idle_runners -gt 0 ]]; then
        success "Found $idle_runners idle runners that can be reused"
        reused_count=$idle_runners
    else
        info "No idle runners found for reuse"
    fi
    
    info "Reuse analysis complete. Potentially reusable: $reused_count runners"
}

# Generate cost analysis report
analyze_costs() {
    info "Generating cost analysis report..."
    
    local repos=($(get_repositories))
    local total_runners=0
    local total_busy=0
    local total_idle=0
    
    # Collect runner statistics
    for repo in "${repos[@]}"; do
        debug "Analyzing costs for $repo"
        local runners=""
        runners=$(list_runners "$repo")
        
        local repo_total=0
        local repo_busy=0
        local repo_idle=0
        
        repo_total=$(echo "$runners" | jq 'length' 2>/dev/null || echo 0)
        repo_busy=$(echo "$runners" | jq '[.[] | select(.busy == true)] | length' 2>/dev/null || echo 0)
        repo_idle=$(echo "$runners" | jq '[.[] | select(.busy == false)] | length' 2>/dev/null || echo 0)
        
        total_runners=$((total_runners + repo_total))
        total_busy=$((total_busy + repo_busy))
        total_idle=$((total_idle + repo_idle))
    done
    
    # Calculate utilization rate
    local utilization_rate=0
    if [[ $total_runners -gt 0 ]]; then
        utilization_rate=$(echo "scale=2; $total_busy * 100 / $total_runners" | bc -l)
    fi
    
    # Generate cost report
    local cost_report="${SCRIPT_DIR}/../cost_analysis_report.txt"
    cat > "$cost_report" << EOF
# Ephemeral Runner Cost Analysis Report
Generated: $(date)

## Summary
Total Runners: $total_runners
Busy Runners: $total_busy
Idle Runners: $total_idle
Utilization Rate: ${utilization_rate}%

## Cost Optimization Recommendations
EOF
    
    if [[ $(echo "$utilization_rate < 50" | bc -l) -eq 1 ]]; then
        cat >> "$cost_report" << EOF

⚠️  **LOW UTILIZATION DETECTED**
- Current utilization rate is below 50%
- Consider reducing the number of registered runners
- Implement more aggressive runner cleanup policies
- Review job scheduling to better utilize existing runners

## Estimated Savings
- Reduce runner count by 20-30% to improve utilization
- Implement auto-scaling based on job queue length
- Use spot instances for cost savings (if applicable)
EOF
    else
        cat >> "$cost_report" << EOF

✅ **GOOD UTILIZATION**
- Current utilization rate is healthy
- Continue monitoring for optimization opportunities

## Optimization Opportunities
- Consider implementing predictive scaling
- Review runner labels for better job routing
- Implement job prioritization for critical workloads
EOF
    fi
    
    cat >> "$cost_report" << EOF

## Repository Breakdown
EOF
    
    for repo in "${repos[@]}"; do
        local runners=""
        runners=$(list_runners "$repo")
        local repo_total=0
        local repo_busy=0
        local repo_idle=0
        
        repo_total=$(echo "$runners" | jq 'length' 2>/dev/null || echo 0)
        repo_busy=$(echo "$runners" | jq '[.[] | select(.busy == true)] | length' 2>/dev/null || echo 0)
        repo_idle=$(echo "$runners" | jq '[.[] | select(.busy == false)] | length' 2>/dev/null || echo 0)
        
        echo "- $repo: Total: $repo_total, Busy: $repo_busy, Idle: $repo_idle" >> "$cost_report"
    done
    
    success "Cost analysis report generated: $cost_report"
}

# Create backup of current state
create_backup() {
    info "Creating backup of current runner state..."
    
    mkdir -p "$BACKUP_DIR"
    local backup_file="$BACKUP_DIR/runner_state_$(date +%Y%m%d_%H%M%S).json"
    
    local repos=($(get_repositories))
    local backup_data="{\"timestamp\": \"$(date -Iseconds)\", \"repositories\": {}}"
    
    for repo in "${repos[@]}"; do
        local runners=""
        runners=$(list_runners "$repo")
        backup_data=$(echo "$backup_data" | jq ".repositories.\"$repo\" = $runners")
    done
    
    echo "$backup_data" > "$backup_file"
    success "Backup created: $backup_file"
}

# Display help
show_help() {
    cat << EOF
Nightly Ephemeral Runner Harvester

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --harvest              Discover and register new runners
    --reuse                Reuse existing runners across repositories
    --cost-analysis        Generate cost optimization report
    --full                 Run complete workflow (harvest + reuse + analysis)
    --config <file>        Specify configuration file path
    --verbose              Enable verbose logging
    --help                 Show this help message

EXAMPLES:
    $0 --harvest
    $0 --reuse --verbose
    $0 --cost-analysis
    $0 --full
    $0 --config custom-config.yaml

CONFIGURATION:
    Create a .runner-config file with your repository settings:
    
    repositories:
      - owner/repo1
      - owner/repo2
    runner_labels:
      - "ephemeral"
      - "cost-optimized"
    max_runners_per_repo: 5
    harvest_interval: 300

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --harvest)
                ACTION="harvest"
                shift
                ;;
            --reuse)
                ACTION="reuse"
                shift
                ;;
            --cost-analysis)
                ACTION="cost-analysis"
                shift
                ;;
            --full)
                ACTION="full"
                shift
                ;;
            --config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE="true"
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                error_exit "Unknown option: $1\nUse --help for usage information."
                ;;
esac
done
}

# Main execution
main() {
    # Initialize logging
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "Starting Ephemeral Runner Harvester at $(date)" > "$LOG_FILE"
    
    # Parse arguments
    ACTION=""
    VERBOSE="false"
    parse_args "$@"
    
    if [[ -z "$ACTION" ]]; then
        error_exit "No action specified.\nUse --help for usage information."
    fi
    
    # Check dependencies
    check_dependencies
    
    # Load configuration
    load_config
    
    # Check authentication
    check_auth
    
    # Create backup
    create_backup
    
    # Execute requested action
    case "$ACTION" in
        harvest)
            harvest_runners
            ;;
        reuse)
            reuse_runners
            ;;
        cost-analysis)
            analyze_costs
            ;;
        full)
            harvest_runners
            reuse_runners
            analyze_costs
            ;;
        *)
            error_exit "Invalid action: $ACTION"
            ;;
esac
    
    success "Runner harvester completed successfully"
}

# Run main function with all arguments
main "$@"
