#!/bin/bash

# Nightly Ephemeral Runner Ghostbuster
# Detects and cleans up orphaned GitHub Actions self-hosted runners
# Supports AWS EC2, Azure VMs, and GCP Compute Engine

set -euo pipefail

# Script metadata
SCRIPT_VERSION="1.0.0"
SCRIPT_NAME="$(basename "$0")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default configuration
DEFAULT_AGE_THRESHOLD=7200  # 2 hours in seconds
DEFAULT_PROVIDERS="aws,azure,gcp"
DEFAULT_GITHUB_ORG=""
DEFAULT_GITHUB_REPO=""
DEFAULT_DRY_RUN=false
DEFAULT_CLEANUP=false
DEFAULT_VERBOSE=false
DEFAULT_YES=false
DEFAULT_REPORT_FILE=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1" >> "$DEBUG_LOG"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARN: $1" >> "$DEBUG_LOG"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >> "$DEBUG_LOG"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS: $1" >> "$DEBUG_LOG"
}

log_debug() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $1"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] DEBUG: $1" >> "$DEBUG_LOG"
    fi
}

# Utility functions
print_usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

Detects and cleans up orphaned GitHub Actions self-hosted runners across cloud providers.

OPTIONS:
    --dry-run               Show what would be deleted without actually deleting (default)
    --cleanup               Perform actual cleanup (requires confirmation unless --yes is used)
    --provider <provider>   Limit to specific cloud provider (aws|azure|gcp)
    --age-threshold <sec>   Only consider runners older than this threshold (default: $DEFAULT_AGE_THRESHOLD)
    --report <file>         Save detailed report to file
    --yes                   Skip confirmation prompts
    --verbose               Enable verbose logging
    --help                  Show this help message

ENVIRONMENT VARIABLES:
    GITHUB_ORG              GitHub organization name (required)
    GITHUB_REPO             GitHub repository name (optional, for repo runners)
    AGE_THRESHOLD           Age threshold in seconds (default: $DEFAULT_AGE_THRESHOLD)
    CLOUD_PROVIDERS         Comma-separated list of cloud providers (default: $DEFAULT_PROVIDERS)

EXAMPLES:
    $SCRIPT_NAME --dry-run
    $SCRIPT_NAME --cleanup --yes
    $SCRIPT_NAME --provider aws --cleanup --report cleanup_report.txt
    $SCRIPT_NAME --age-threshold 3600 --verbose

EOF
}

check_dependencies() {
    local missing_deps=()
    
    # Check for required CLI tools based on enabled providers
    if [[ ",${PROVIDERS[@]}," =~ ",aws," ]]; then
        if ! command -v aws &> /dev/null; then
            missing_deps+=("AWS CLI")
        fi
    fi
    
    if [[ ",${PROVIDERS[@]}," =~ ",azure," ]]; then
        if ! command -v az &> /dev/null; then
            missing_deps+=("Azure CLI")
        fi
    fi
    
    if [[ ",${PROVIDERS[@]}," =~ ",gcp," ]]; then
        if ! command -v gcloud &> /dev/null; then
            missing_deps+=("gcloud CLI")
        fi
    fi
    
    if ! command -v gh &> /dev/null; then
        missing_deps+=("GitHub CLI (gh)")
    fi
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_error "Please install the missing tools and try again."
        exit 1
    fi
}

check_github_auth() {
    log_info "Checking GitHub authentication..."
    
    if ! gh auth status &> /dev/null; then
        log_error "GitHub CLI is not authenticated. Please run 'gh auth login' first."
        exit 1
    fi
    
    log_success "GitHub authentication verified"
}

check_cloud_auth() {
    local provider=$1
    
    case "$provider" in
        "aws")
            log_info "Checking AWS authentication..."
            if ! aws sts get-caller-identity &> /dev/null; then
                log_error "AWS CLI is not authenticated. Please run 'aws configure' or set AWS credentials."
                return 1
            fi
            log_success "AWS authentication verified"
            ;;
        "azure")
            log_info "Checking Azure authentication..."
            if ! az account show &> /dev/null; then
                log_error "Azure CLI is not authenticated. Please run 'az login' first."
                return 1
            fi
            log_success "Azure authentication verified"
            ;;
        "gcp")
            log_info "Checking GCP authentication..."
            if ! gcloud auth list --filter=status:ACTIVE --format='value(account)' | head -n1 &> /dev/null; then
                log_error "GCP CLI is not authenticated. Please run 'gcloud auth login' first."
                return 1
            fi
            log_success "GCP authentication verified"
            ;;
    esac
}

get_github_runners() {
    log_info "Fetching registered GitHub runners..."
    
    local runners=()
    local api_url=""
    
    if [[ -n "$GITHUB_REPO" ]]; then
        # Check repo runners
        api_url="/repos/$GITHUB_ORG/$GITHUB_REPO/actions/runners"
    else
        # Check org runners
        api_url="/orgs/$GITHUB_ORG/actions/runners"
    fi
    
    # Use gh to get runners with pagination
    local page=1
    local per_page=100
    local has_more=true
    
    while [[ "$has_more" == "true" ]]; do
        log_debug "Fetching page $page of runners from GitHub API"
        
        local response
        if ! response=$(gh api "$api_url" --paginate --per-page "$per_page" --page "$page" 2>/dev/null); then
            log_error "Failed to fetch runners from GitHub API"
            return 1
        fi
        
        # Extract runner names using jq
        local page_runners
        if ! page_runners=$(echo "$response" | jq -r '.runners[].name // empty' 2>/dev/null); then
            log_warn "Failed to parse runners from API response, continuing..."
            break
        fi
        
        # Add to our list
        while IFS= read -r runner; do
            if [[ -n "$runner" && "$runner" != "null" ]]; then
                runners+=("$runner")
            fi
        done <<< "$page_runners"
        
        # Check if there are more pages
        if [[ $(echo "$response" | jq '.runners | length') -lt $per_page ]]; then
            has_more=false
        else
            ((page++))
        fi
        
        # Rate limiting
        sleep 0.5
    done
    
    log_info "Found ${#runners[@]} registered runners"
    printf '%s\n' "${runners[@]}"
}

get_aws_instances() {
    log_info "Fetching AWS EC2 instances..."
    
    # Filter for instances that might be runners
    # Look for instances with names containing 'runner' or tags indicating they're runners
    local filters=""
    
    # Build filters for different naming patterns
    local name_filters=(
        "Name=tag:Name,Values=*runner*"
        "Name=tag:Name,Values=*github*"
        "Name=tag:Name,Values=*ci*"
        "Name=tag:Name,Values=*ephemeral*"
        "Name=tag:Name,Values=*temp*"
    )
    
    # Also include instances without names but with runner-related tags
    local tag_filters=(
        "Name=tag:RunnerType,Values=*
        "Name=tag:GitHubRunner,Values=*
        "Name=tag:SelfHosted,Values=*
    )
    
    # Build the filter string
    local filter_string=""
    for filter in "${name_filters[@]}"; do
        if [[ -n "$filter_string" ]]; then
            filter_string="$filter_string,"
        fi
        filter_string="$filter_string$filter"
    done
    
    # Query AWS for instances
    local instances_json
    if ! instances_json=$(aws ec2 describe-instances \
        --filters "$filter_string" \
        --query 'Reservations[].Instances[?State.Name==`running`]' \
        --output json 2>/dev/null); then
        log_error "Failed to fetch AWS instances"
        return 1
    fi
    
    # Parse instances
    local instance_count
    instance_count=$(echo "$instances_json" | jq 'length')
    log_info "Found $instance_count AWS instances matching runner patterns"
    
    # Extract instance details
    echo "$instances_json" | jq -r '.[] | "aws|\(.InstanceId)|\(.Tags[] | select(.Key=="Name") | .Value // "unknown")|\(.LaunchTime)"' 2>/dev/null
}

get_azure_vms() {
    log_info "Fetching Azure VMs..."
    
    # Query Azure for VMs that might be runners
    local vms_json
    if ! vms_json=$(az vm list \
        --query '[?contains(name, `runner`) || contains(name, `github`) || contains(name, `ci`) || contains(name, `ephemeral`) || contains(name, `temp`)]' \
        --output json 2>/dev/null); then
        log_error "Failed to fetch Azure VMs"
        return 1
    fi
    
    local vm_count
    vm_count=$(echo "$vms_json" | jq 'length')
    log_info "Found $vm_count Azure VMs matching runner patterns"
    
    # Extract VM details
    echo "$vms_json" | jq -r '.[] | "azure|\(.vmId)|\(.name)|\(.timeCreated)"' 2>/dev/null
}

get_gcp_instances() {
    log_info "Fetching GCP Compute Engine instances..."
    
    # Get list of zones
    local zones
    if ! zones=$(gcloud compute zones list --format='value(name)' 2>/dev/null); then
        log_error "Failed to fetch GCP zones"
        return 1
    fi
    
    local all_instances=""
    
    # Query each zone for instances
    while IFS= read -r zone; do
        if [[ -n "$zone" ]]; then
            log_debug "Querying zone: $zone"
            
            local instances_json
            if ! instances_json=$(gcloud compute instances list \
                --zone="$zone" \
                --filter='name ~ "runner|github|ci|ephemeral|temp"' \
                --format='json(name, id, creationTimestamp)' 2>/dev/null); then
                log_warn "Failed to fetch instances from zone $zone"
                continue
            fi
            
            # Extract instance details and add zone info
            local zone_instances
            zone_instances=$(echo "$instances_json" | jq -r --arg zone "$zone" '.[] | "gcp|\(.id)|\(.name)|\(.creationTimestamp)|\($zone)"' 2>/dev/null)
            
            if [[ -n "$zone_instances" ]]; then
                all_instances="$all_instances\n$zone_instances"
            fi
        fi
    done <<< "$zones"
    
    # Count instances
    local instance_count
    instance_count=$(echo "$all_instances" | grep -c '^gcp|' || echo 0)
    log_info "Found $instance_count GCP instances matching runner patterns"
    
    echo "$all_instances" | grep '^gcp|'
}

get_all_instances() {
    local all_instances=()
    
    for provider in "${PROVIDERS[@]}"; do
        log_info "Checking $provider for potential runner instances..."
        
        if ! check_cloud_auth "$provider"; then
            log_warn "Skipping $provider due to authentication issues"
            continue
        fi
        
        local provider_instances=()
        
        case "$provider" in
            "aws")
                if ! mapfile -t provider_instances < <(get_aws_instances); then
                    log_warn "Failed to get AWS instances"
                    continue
                fi
                ;;
            "azure")
                if ! mapfile -t provider_instances < <(get_azure_vms); then
                    log_warn "Failed to get Azure VMs"
                    continue
                fi
                ;;
            "gcp")
                if ! mapfile -t provider_instances < <(get_gcp_instances); then
                    log_warn "Failed to get GCP instances"
                    continue
                fi
                ;;
        esac
        
        # Add to our master list
        for instance in "${provider_instances[@]}"; do
            if [[ -n "$instance" ]]; then
                all_instances+=("$instance")
            fi
        done
    done
    
    printf '%s\n' "${all_instances[@]}"
}

is_instance_orphaned() {
    local instance_name="$1"
    local registered_runners="$2"
    
    # Check if instance name matches any registered runner
    if echo "$registered_runners" | grep -q "^${instance_name}$"; then
        return 1  # Not orphaned
    fi
    
    return 0  # Orphaned
}

get_instance_age_seconds() {
    local launch_time="$1"
    
    # Convert launch time to seconds since epoch
    local launch_epoch
    if command -v gdate &> /dev/null; then
        # macOS with GNU date installed
        launch_epoch=$(gdate -d "$launch_time" +%s 2>/dev/null || echo 0)
    else
        # Linux or macOS with standard date
        launch_epoch=$(date -d "$launch_time" +%s 2>/dev/null || echo 0)
    fi
    
    if [[ $launch_epoch -eq 0 ]]; then
        # Try alternative formats
        launch_epoch=$(date -jf "%Y-%m-%dT%H:%M:%S%z" "$launch_time" +%s 2>/dev/null || echo 0)
    fi
    
    if [[ $launch_epoch -eq 0 ]]; then
        # Try parsing as ISO 8601 without timezone
        launch_epoch=$(date -jf "%Y-%m-%dT%H:%M:%S" "$launch_time" +%s 2>/dev/null || echo 0)
    fi
    
    if [[ $launch_epoch -eq 0 ]]; then
        log_warn "Failed to parse launch time: $launch_time"
        return 0
    fi
    
    local current_epoch
    current_epoch=$(date +%s)
    
    echo $((current_epoch - launch_epoch))
}

terminate_aws_instance() {
    local instance_id="$1"
    local instance_name="$2"
    
    log_info "Terminating AWS instance $instance_id ($instance_name)"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would terminate AWS instance: $instance_id"
        return 0
    fi
    
    if ! aws ec2 terminate-instances --instance-ids "$instance_id" &> /dev/null; then
        log_error "Failed to terminate AWS instance: $instance_id"
        return 1
    fi
    
    log_success "Terminated AWS instance: $instance_id"
}

terminate_azure_vm() {
    local vm_id="$1"
    local vm_name="$2"
    
    log_info "Terminating Azure VM $vm_id ($vm_name)"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would terminate Azure VM: $vm_id"
        return 0
    fi
    
    # Extract resource group from vm_id or use a different approach
    # For now, we'll need the resource group name
    log_warn "Azure VM termination requires resource group. Skipping: $vm_id"
    return 1
}

terminate_gcp_instance() {
    local instance_id="$1"
    local instance_name="$2"
    local zone="$3"
    
    log_info "Terminating GCP instance $instance_id ($instance_name) in zone $zone"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would terminate GCP instance: $instance_id"
        return 0
    fi
    
    if ! gcloud compute instances delete "$instance_name" --zone="$zone" --quiet &> /dev/null; then
        log_error "Failed to terminate GCP instance: $instance_id"
        return 1
    fi
    
    log_success "Terminated GCP instance: $instance_id"
}

terminate_instance() {
    local provider="$1"
    local instance_id="$2"
    local instance_name="$3"
    local zone="$4"  # Optional, for GCP
    
    case "$provider" in
        "aws")
            terminate_aws_instance "$instance_id" "$instance_name"
            ;;
        "azure")
            terminate_azure_vm "$instance_id" "$instance_name"
            ;;
        "gcp")
            terminate_gcp_instance "$instance_id" "$instance_name" "$zone"
            ;;
        *)
            log_error "Unknown provider: $provider"
            return 1
            ;;
    esac
}

confirm_cleanup() {
    if [[ "$YES" == "true" ]]; then
        return 0
    fi
    
    echo
    echo "⚠️  WARNING: This will terminate the orphaned instances listed above."
    echo "This action cannot be undone."
    echo
    read -p "Do you want to proceed? (yes/no): " -r
    
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        log_info "Cleanup cancelled by user"
        return 1
    fi
    
    return 0
}

format_duration() {
    local seconds=$1
    local days=$((seconds / 86400))
    local hours=$(((seconds % 86400) / 3600))
    local minutes=$(((seconds % 3600) / 60))
    local secs=$((seconds % 60))
    
    if [[ $days -gt 0 ]]; then
        echo "${days}d ${hours}h ${minutes}m"
    elif [[ $hours -gt 0 ]]; then
        echo "${hours}h ${minutes}m ${secs}s"
    elif [[ $minutes -gt 0 ]]; then
        echo "${minutes}m ${secs}s"
    else
        echo "${secs}s"
    fi
}

print_summary() {
    local total_instances=$1
    local registered_count=$2
    local orphaned_count=$3
    local terminated_count=$4
    
    echo
    echo "=== Ephemeral Runner Ghostbuster Summary ==="
    echo
    echo "Total instances found: $total_instances"
    echo "Registered runners: $registered_count"
    echo "Orphaned instances: $orphaned_count"
    echo "Terminated instances: $terminated_count"
    echo
    if [[ $orphaned_count -eq 0 ]]; then
        echo "🎉 No orphaned runners found! Your environment is clean."
    elif [[ $terminated_count -eq $orphaned_count ]]; then
        echo "✅ All orphaned runners have been successfully terminated."
    else
        echo "⚠️  Some orphaned runners could not be terminated. Check the logs for details."
    fi
    
    if [[ -n "$REPORT_FILE" ]]; then
        echo "📄 Detailed report saved to: $REPORT_FILE"
    fi
}

save_report() {
    local report_content="$1"
    
    if [[ -z "$REPORT_FILE" ]]; then
        return 0
    fi
    
    echo "$report_content" > "$REPORT_FILE"
    log_success "Report saved to: $REPORT_FILE"
}

# Main execution
main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --cleanup)
                CLEANUP=true
                shift
                ;;
            --provider)
                PROVIDER_SPECIFIC="$2"
                shift 2
                ;;
            --age-threshold)
                AGE_THRESHOLD_OVERRIDE="$2"
                shift 2
                ;;
            --report)
                REPORT_FILE="$2"
                shift 2
                ;;
            --yes)
                YES=true
                shift
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
    
    # Set up logging
    local timestamp
    timestamp=$(date '+%Y%m%d_%H%M%S')
    DEBUG_LOG="ghostbuster_debug_$timestamp.log"
    
    # Initialize configuration from environment and defaults
    PROVIDERS=(${PROVIDER_SPECIFIC:-$DEFAULT_PROVIDERS})
    GITHUB_ORG=${GITHUB_ORG:-$DEFAULT_GITHUB_ORG}
    GITHUB_REPO=${GITHUB_REPO:-$DEFAULT_GITHUB_REPO}
    AGE_THRESHOLD=${AGE_THRESHOLD_OVERRIDE:-$DEFAULT_AGE_THRESHOLD}
    DRY_RUN=${DRY_RUN:-$DEFAULT_DRY_RUN}
    CLEANUP=${CLEANUP:-$DEFAULT_CLEANUP}
    VERBOSE=${VERBOSE:-$DEFAULT_VERBOSE}
    YES=${YES:-$DEFAULT_YES}
    REPORT_FILE=${REPORT_FILE:-$DEFAULT_REPORT_FILE}
    
    # Generate timestamped report file if not specified
    if [[ -z "$REPORT_FILE" && "$CLEANUP" == "true" ]]; then
        REPORT_FILE="ghostbuster_report_$timestamp.txt"
    fi
    
    # Validate configuration
    if [[ -z "$GITHUB_ORG" ]]; then
        log_error "GitHub organization is required. Set GITHUB_ORG environment variable or use --help for usage."
        exit 1
    fi
    
    if [[ "$CLEANUP" == "true" && "$DRY_RUN" == "true" ]]; then
        log_error "Cannot specify both --cleanup and --dry-run"
        exit 1
    fi
    
    # Print header
    echo "=== Ephemeral Runner Ghostbuster v$SCRIPT_VERSION ==="
    echo "Organization: $GITHUB_ORG"
    if [[ -n "$GITHUB_REPO" ]]; then
        echo "Repository: $GITHUB_REPO"
    fi
    echo "Providers: ${PROVIDERS[*]}"
    echo "Age threshold: $(format_duration $AGE_THRESHOLD)"
    echo "Mode: $([ "$DRY_RUN" == "true" ] && echo "DRY RUN" || echo "CLEANUP")"
    echo "Timestamp: $(date)"
    echo
    
    # Check dependencies
    check_dependencies
    
    # Check authentication
    check_github_auth
    
    # Fetch registered runners
    local registered_runners
    if ! registered_runners=$(get_github_runners); then
        log_error "Failed to fetch registered runners from GitHub"
        exit 1
    fi
    
    # Fetch all instances
    local all_instances
    if ! all_instances=$(get_all_instances); then
        log_error "Failed to fetch instances from cloud providers"
        exit 1
    fi
    
    # Analyze instances
    local total_instances=0
    local registered_count=0
    local orphaned_count=0
    local terminated_count=0
    
    local orphaned_instances=()
    local report_content=""
    
    report_content="=== Ephemeral Runner Ghostbuster Report ===\n\n"
    report_content="$report_contentOrganization: $GITHUB_ORG\n"
    if [[ -n "$GITHUB_REPO" ]]; then
        report_content="$report_contentRepository: $GITHUB_REPO\n"
    fi
    report_content="$report_contentProviders: ${PROVIDERS[*]}\n"
    report_content="$report_contentAge threshold: $(format_duration $AGE_THRESHOLD)\n"
    report_content="$report_contentScan timestamp: $(date)\n\n"
    
    # Process each instance
    while IFS='|' read -r provider instance_id instance_name launch_time zone; do
        if [[ -z "$instance_id" || -z "$instance_name" ]]; then
            continue
        fi
        
        ((total_instances++))
        
        # Check if this instance is a registered runner
        if is_instance_orphaned "$instance_name" "$registered_runners"; then
            # Check age
            local age_seconds
            age_seconds=$(get_instance_age_seconds "$launch_time")
            
            if [[ $age_seconds -ge $AGE_THRESHOLD ]]; then
                orphaned_instances+=("$provider|$instance_id|$instance_name|$launch_time|$zone|$age_seconds")
                ((orphaned_count++))
                
                log_warn "Found orphaned instance: $provider $instance_id ($instance_name) - Age: $(format_duration $age_seconds)"
            else
                log_info "Instance $instance_name is orphaned but too young ($(format_duration $age_seconds)), skipping"
            fi
        else
            ((registered_count++))
            log_debug "Instance $instance_name is a registered runner"
        fi
    done <<< "$all_instances"
    
    # Report findings
    echo
    echo "=== Analysis Results ==="
    echo "Total instances found: $total_instances"
    echo "Registered runners: $registered_count"
    echo "Orphaned instances: $orphaned_count"
    echo
    
    if [[ $orphaned_count -eq 0 ]]; then
        echo "🎉 No orphaned runners found! Your environment is clean."
        save_report "$report_content\nNo orphaned runners found. Environment is clean.\n"
        print_summary $total_instances $registered_count $orphaned_count $terminated_count
        exit 0
    fi
    
    # Display orphaned instances
    echo "Orphaned instances found:"
    report_content="$report_contentOrphaned instances:\n"
    
    for orphan in "${orphaned_instances[@]}"; do
        IFS='|' read -r provider instance_id instance_name launch_time zone age_seconds <<< "$orphan"
        local age_formatted
        age_formatted=$(format_duration $age_seconds)
        
        echo "  - $provider: $instance_id ($instance_name) - Age: $age_formatted"
        report_content="$report_content  - $provider: $instance_id ($instance_name) - Age: $age_formatted\n"
    done
    
    # Perform cleanup if requested
    if [[ "$CLEANUP" == "true" ]]; then
        echo
        if ! confirm_cleanup; then
            save_report "$report_content\nCleanup cancelled by user.\n"
            print_summary $total_instances $registered_count $orphaned_count $terminated_count
            exit 0
        fi
        
        echo
        echo "=== Performing Cleanup ==="
        report_content="$report_content\nCleanup actions taken:\n"
        
        for orphan in "${orphaned_instances[@]}"; do
            IFS='|' read -r provider instance_id instance_name launch_time zone age_seconds <<< "$orphan"
            
            if terminate_instance "$provider" "$instance_id" "$instance_name" "$zone"; then
                ((terminated_count++))
                report_content="$report_content  - TERMINATED: $provider $instance_id ($instance_name)\n"
            else
                report_content="$report_content  - FAILED: $provider $instance_id ($instance_name)\n"
            fi
        done
        
        report_content="$report_content\nTotal terminated: $terminated_count\n"
    else
        echo
        echo "💡 Run with --cleanup to remove these orphaned instances"
        report_content="$report_content\nTo remove these instances, run with --cleanup flag.\n"
    fi
    
    # Save report
    save_report "$report_content"
    
    # Print final summary
    print_summary $total_instances $registered_count $orphaned_count $terminated_count
    
    # Exit with appropriate code
    if [[ $terminated_count -eq $orphaned_count ]]; then
        exit 0  # Success
    else
        exit 1  # Some failures
    fi
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
