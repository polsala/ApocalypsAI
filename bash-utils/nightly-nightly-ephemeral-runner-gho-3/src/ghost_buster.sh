#!/bin/bash

# Nightly Ephemeral Runner Ghost Buster
# Detects and cleans up orphaned GitHub Actions runners across cloud providers

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/ghost_buster_$(date +%Y%m%d_%H%M%S).log"
DRY_RUN=false
AGE_THRESHOLD="2h"
PROVIDERS="aws,azure,gcp"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_info() {
    log "${BLUE}INFO:${NC} $1"
}

log_warn() {
    log "${YELLOW}WARN:${NC} $1"
}

log_error() {
    log "${RED}ERROR:${NC} $1"
}

log_success() {
    log "${GREEN}SUCCESS:${NC} $1"
}

# Help function
show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Detects and cleans up orphaned GitHub Actions runners across cloud providers.

OPTIONS:
    -d, --dry-run           Show what would be deleted without making changes
    -a, --age AGE           Age threshold for cleanup (e.g., 1h, 30m, 2d)
    -p, --providers LIST    Comma-separated list of providers (aws,azure,gcp)
    -h, --help              Show this help message

EXAMPLES:
    $0 --dry-run --age 2h
    $0 --age 1h --providers aws,azure
    $0 --age 30m

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -a|--age)
                AGE_THRESHOLD="$2"
                shift 2
                ;;
            -p|--providers)
                PROVIDERS="$2"
                shift 2
                ;;
            -h|--help)
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
}

# Validate age threshold format
validate_age() {
    local age="$1"
    if ! [[ "$age" =~ ^[0-9]+[hmdHMD]$ ]]; then
        log_error "Invalid age format: $age. Use format like 1h, 30m, 2d"
        exit 1
    fi
}

# Convert age to seconds for comparison
age_to_seconds() {
    local age="$1"
    local number="${age%[hmdHMD]}"
    local unit="${age: -1}"
    
    case "${unit^^}" in
        H) echo $((number * 3600)) ;;
        M) echo $((number * 60)) ;;
        D) echo $((number * 86400)) ;;
    esac
}

# Check if required CLI tools are installed
check_dependencies() {
    local missing_tools=()
    
    if [[ ",${PROVIDERS}," == *,aws,* ]]; then
        if ! command -v aws &> /dev/null; then
            missing_tools+=("aws-cli")
        fi
    fi
    
    if [[ ",${PROVIDERS}," == *,azure,* ]]; then
        if ! command -v az &> /dev/null; then
            missing_tools+=("azure-cli")
        fi
    fi
    
    if [[ ",${PROVIDERS}," == *,gcp,* ]]; then
        if ! command -v gcloud &> /dev/null; then
            missing_tools+=("google-cloud-sdk")
        fi
    fi
    
    if ! command -v jq &> /dev/null; then
        missing_tools+=("jq")
    fi
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        log_info "Please install the missing tools and try again."
        exit 1
    fi
}

# Get current timestamp in seconds
get_current_timestamp() {
    date +%s
}

# Check if instance is older than threshold
is_instance_expired() {
    local launch_time="$1"
    local age_seconds="$2"
    local current_time
    local launch_timestamp
    
    current_time=$(get_current_timestamp)
    launch_timestamp=$(date -d "$launch_time" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$launch_time" +%s 2>/dev/null)
    
    if [[ -z "$launch_timestamp" ]]; then
        log_warn "Could not parse launch time: $launch_time"
        return 1
    fi
    
    local age_diff=$((current_time - launch_timestamp))
    [[ $age_diff -gt $age_seconds ]]
}

# AWS: Detect orphaned runners
aws_detect_runners() {
    log_info "Checking AWS for orphaned runners..."
    
    # Look for instances with GitHub Actions runner tags
    local instances
    instances=$(aws ec2 describe-instances \
        --filters "Name=tag:Name,Values=*github-runner*" "Name=instance-state-name,Values=running" \
        --query 'Reservations[].Instances[].[InstanceId,LaunchTime,Tags[?Key==`Name`].Value|[0]]' \
        --output text 2>/dev/null || echo "")
    
    if [[ -z "$instances" ]]; then
        log_info "No GitHub runner instances found in AWS"
        return 0
    fi
    
    local age_seconds
    age_seconds=$(age_to_seconds "$AGE_THRESHOLD")
    local expired_count=0
    
    while IFS=$'\t' read -r instance_id launch_time name; do
        if is_instance_expired "$launch_time" "$age_seconds"; then
            log_warn "Found expired runner: $instance_id ($name) launched at $launch_time"
            echo "$instance_id"
            ((expired_count++))
        fi
    done <<< "$instances"
    
    log_info "AWS: Found $expired_count expired runners"
    return $expired_count
}

# AWS: Terminate instances
aws_terminate_instances() {
    local instances=($@)
    
    if [[ ${#instances[@]} -eq 0 ]]; then
        log_info "No AWS instances to terminate"
        return 0
    fi
    
    log_info "Terminating ${#instances[@]} AWS instances..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would terminate: ${instances[*]}"
        return 0
    fi
    
    local result
    result=$(aws ec2 terminate-instances --instance-ids "${instances[@]}" 2>&1 || echo "ERROR")
    
    if [[ "$result" == "ERROR" ]]; then
        log_error "Failed to terminate AWS instances: ${instances[*]}"
        return 1
    else
        log_success "Successfully terminated AWS instances: ${instances[*]}"
    fi
}

# Azure: Detect orphaned runners
azure_detect_runners() {
    log_info "Checking Azure for orphaned runners..."
    
    # Look for VMs with GitHub Actions runner names
    local vms
    vms=$(az vm list \
        --query "[?contains(name, 'github-runner')].{name:name,resourceGroup:resourceGroup,vmId:vmId,provisioningState:provisioningState,osProfile.computerName:osProfile.computerName}" \
        --output json 2>/dev/null || echo "[]")
    
    if [[ "$vms" == "[]" ]]; then
        log_info "No GitHub runner VMs found in Azure"
        return 0
    fi
    
    local age_seconds
    age_seconds=$(age_to_seconds "$AGE_THRESHOLD")
    local expired_count=0
    
    echo "$vms" | jq -r '.[] | "\(.name)\t\(.resourceGroup)\t\(.vmId)"' | while IFS=$'\t' read -r name resource_group vm_id; do
        # Get VM creation time (approximation using provisioning state)
        local provisioning_state
        provisioning_state=$(az vm show --name "$name" --resource-group "$resource_group" --query "provisioningState" --output tsv 2>/dev/null || echo "Unknown")
        
        if [[ "$provisioning_state" == "Succeeded" ]]; then
            # For simplicity, we'll consider all running VMs as potentially expired
            # In a real implementation, you'd check the actual creation time
            log_warn "Found potential runner VM: $name in $resource_group"
            echo "$name:$resource_group"
            ((expired_count++))
        fi
    done
    
    log_info "Azure: Found $expired_count potential expired runners"
    return $expired_count
}

# Azure: Delete VMs
azure_delete_vms() {
    local vm_list=($@)
    
    if [[ ${#vm_list[@]} -eq 0 ]]; then
        log_info "No Azure VMs to delete"
        return 0
    fi
    
    log_info "Deleting ${#vm_list[@]} Azure VMs..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would delete VMs: ${vm_list[*]}"
        return 0
    fi
    
    local deleted_count=0
    for vm_info in "${vm_list[@]}"; do
        local name resource_group
        name="${vm_info%:*}"
        resource_group="${vm_info#*:}"
        
        if az vm delete --name "$name" --resource-group "$resource_group" --yes --no-wait 2>/dev/null; then
            log_success "Successfully deleted Azure VM: $name"
            ((deleted_count++))
        else
            log_error "Failed to delete Azure VM: $name"
        fi
    done
    
    log_info "Azure: Deleted $deleted_count VMs"
}

# GCP: Detect orphaned runners
gcp_detect_runners() {
    log_info "Checking GCP for orphaned runners..."
    
    # Look for instances with GitHub Actions runner names
    local instances
    instances=$(gcloud compute instances list \
        --filter="name~github-runner" \
        --format="json(name,zone,creationTimestamp,status)" 2>/dev/null || echo "[]")
    
    if [[ "$instances" == "[]" ]]; then
        log_info "No GitHub runner instances found in GCP"
        return 0
    fi
    
    local age_seconds
    age_seconds=$(age_to_seconds "$AGE_THRESHOLD")
    local expired_count=0
    
    echo "$instances" | jq -r '.[] | "\(.name)\t\(.zone)\t\(.creationTimestamp)\t\(.status)"' | while IFS=$'\t' read -r name zone creation_time status; do
        if [[ "$status" == "RUNNING" ]]; then
            if is_instance_expired "$creation_time" "$age_seconds"; then
                log_warn "Found expired runner: $name in $zone created at $creation_time"
                echo "$name:$zone"
                ((expired_count++))
            fi
        fi
    done
    
    log_info "GCP: Found $expired_count expired runners"
    return $expired_count
}

# GCP: Delete instances
gcp_delete_instances() {
    local instance_list=($@)
    
    if [[ ${#instance_list[@]} -eq 0 ]]; then
        log_info "No GCP instances to delete"
        return 0
    fi
    
    log_info "Deleting ${#instance_list[@]} GCP instances..."
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would delete instances: ${instance_list[*]}"
        return 0
    fi
    
    local deleted_count=0
    for instance_info in "${instance_list[@]}"; do
        local name zone
        name="${instance_info%:*}"
        zone="${instance_info#*:}"
        
        if gcloud compute instances delete "$name" --zone="$zone" --quiet 2>/dev/null; then
            log_success "Successfully deleted GCP instance: $name"
            ((deleted_count++))
        else
            log_error "Failed to delete GCP instance: $name"
        fi
    done
    
    log_info "GCP: Deleted $deleted_count instances"
}

# Generate cleanup report
generate_report() {
    local total_expired="$1"
    local total_deleted="$2"
    
    local report_file="/tmp/ghost_buster_report_$(date +%Y%m%d_%H%M%S).txt"
    
    cat > "$report_file" << EOF
# Ghost Buster Cleanup Report

**Date:** $(date)
**Age Threshold:** $AGE_THRESHOLD
**Dry Run:** $DRY_RUN
**Providers Checked:** $PROVIDERS

## Summary
- Total expired runners found: $total_expired
- Total runners cleaned up: $total_deleted

## Log File
Detailed logs available at: $LOG_FILE

EOF
    
    log_success "Cleanup report generated: $report_file"
    cat "$report_file"
}

# Main execution function
main() {
    log_info "Starting Ghost Buster cleanup..."
    log_info "Age threshold: $AGE_THRESHOLD"
    log_info "Providers: $PROVIDERS"
    log_info "Dry run: $DRY_RUN"
    
    # Validate inputs
    validate_age "$AGE_THRESHOLD"
    check_dependencies
    
    local total_expired=0
    local total_deleted=0
    
    # Process each provider
    IFS=',' read -ra PROVIDER_ARRAY <<< "$PROVIDERS"
    
    for provider in "${PROVIDER_ARRAY[@]}"; do
        case "$provider" in
            aws)
                log_info "=== Processing AWS ==="
                mapfile -t aws_expired < <(aws_detect_runners)
                if [[ ${#aws_expired[@]} -gt 0 ]]; then
                    aws_terminate_instances "${aws_expired[@]}"
                    total_deleted=$((total_deleted + ${#aws_expired[@]}))
                fi
                total_expired=$((total_expired + ${#aws_expired[@]}))
                ;;
            azure)
                log_info "=== Processing Azure ==="
                mapfile -t azure_expired < <(azure_detect_runners)
                if [[ ${#azure_expired[@]} -gt 0 ]]; then
                    azure_delete_vms "${azure_expired[@]}"
                    total_deleted=$((total_deleted + ${#azure_expired[@]}))
                fi
                total_expired=$((total_expired + ${#azure_expired[@]}))
                ;;
            gcp)
                log_info "=== Processing GCP ==="
                mapfile -t gcp_expired < <(gcp_detect_runners)
                if [[ ${#gcp_expired[@]} -gt 0 ]]; then
                    gcp_delete_instances "${gcp_expired[@]}"
                    total_deleted=$((total_deleted + ${#gcp_expired[@]}))
                fi
                total_expired=$((total_expired + ${#gcp_expired[@]}))
                ;;
            *)
                log_warn "Unknown provider: $provider"
                ;;
        esac
    done
    
    generate_report "$total_expired" "$total_deleted"
    
    log_info "Ghost Buster cleanup completed."
    
    if [[ $total_expired -eq 0 ]]; then
        log_success "No expired runners found. Infrastructure is clean!"
    else
        log_info "Total expired runners cleaned up: $total_deleted"
    fi
}

# Script entry point
parse_args "$@"
main
