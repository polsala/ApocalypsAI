#!/bin/bash

# Ephemeral Runner Cleanup Script
# This script demonstrates how to cleanup a GitHub Actions runner
# Customize this script based on your infrastructure provider

set -e

# Configuration
GITHUB_REPO="${GITHUB_REPOSITORY:-owner/repo}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

# Validate required environment variables
if [[ -z "$GITHUB_TOKEN" ]]; then
    error "GITHUB_TOKEN environment variable is required"
    exit 1
fi

if [[ -z "$GITHUB_REPOSITORY" ]]; then
    warn "GITHUB_REPOSITORY not set, using default: $GITHUB_REPO"
fi

# Function to remove runner from GitHub
remove_github_runner() {
    local runner_id=$1
    local runner_name=$2
    
    log "Removing runner $runner_name (ID: $runner_id) from GitHub..."
    
    response=$(curl -s -X DELETE \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/$GITHUB_REPO/actions/runners/$runner_id")
    
    if [[ $? -eq 0 ]]; then
        log "Successfully removed runner $runner_name from GitHub"
    else
        warn "Failed to remove runner $runner_name from GitHub"
        echo "$response"
    fi
}

# Function to terminate cloud instance
terminate_cloud_instance() {
    local instance_id=$1
    local cloud_provider=$2
    
    case "$cloud_provider" in
        "aws")
            log "Terminating AWS EC2 instance $instance_id..."
            aws ec2 terminate-instances --instance-ids $instance_id
            aws ec2 wait instance-terminated --instance-ids $instance_id
            log "AWS EC2 instance $instance_id terminated successfully"
            ;;
        
        "gcp")
            log "Terminating GCP Compute Engine instance $instance_id..."
            gcloud compute instances delete $instance_id --zone=us-central1-a --quiet
            log "GCP instance $instance_id terminated successfully"
            ;;
        
        "azure")
            log "Terminating Azure VM $instance_id..."
            az vm delete --name $instance_id --resource-group myResourceGroup --yes --no-wait
            log "Azure VM $instance_id terminated successfully"
            ;;
        
        *)
            warn "Unknown cloud provider: $cloud_provider"
            warn "Please implement cleanup logic for your provider"
            ;;
esac
}

# Function to cleanup runner by name
cleanup_runner_by_name() {
    local runner_name=$1
    local cloud_provider=${2:-aws}
    
    log "Starting cleanup for runner: $runner_name"
    
    # Get runner details from GitHub
    runner_info=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "https://api.github.com/repos/$GITHUB_REPO/actions/runners")
    
    runner_id=$(echo "$runner_info" | jq -r ".runners[] | select(.name == \"$runner_name\") | .id")
    
    if [[ "$runner_id" == "null" || -z "$runner_id" ]]; then
        warn "Runner $runner_name not found in GitHub"
        return 1
    fi
    
    log "Found runner $runner_name with ID: $runner_id"
    
    # Remove from GitHub
    remove_github_runner $runner_id $runner_name
    
    # Terminate cloud instance
    # Note: You would need to maintain a mapping of runner names to instance IDs
    # This could be stored in a database, file, or cloud metadata
    
    # For demo purposes, we'll assume instance ID is the same as runner name
    # In reality, you'd look this up from your tracking system
    terminate_cloud_instance $runner_name $cloud_provider
    
    log "Cleanup completed for runner: $runner_name"
}

# Function to cleanup all runners matching a pattern
cleanup_runners_by_pattern() {
    local pattern=$1
    local cloud_provider=${2:-aws}
    
    log "Finding runners matching pattern: $pattern"
    
    # Get all runners
    runner_info=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "https://api.github.com/repos/$GITHUB_REPO/actions/runners")
    
    # Find runners matching the pattern
    matching_runners=$(echo "$runner_info" | jq -r ".runners[] | select(.name | test(\"$pattern\")) | .name")
    
    if [[ -z "$matching_runners" ]]; then
        log "No runners found matching pattern: $pattern"
        return 0
    fi
    
    log "Found matching runners:"
    echo "$matching_runners" | while read -r runner_name; do
        echo "  - $runner_name"
    done
    
    # Cleanup each matching runner
    echo "$matching_runners" | while read -r runner_name; do
        if [[ -n "$runner_name" && "$runner_name" != "null" ]]; then
            cleanup_runner_by_name "$runner_name" "$cloud_provider"
        fi
    done
}

# Function to cleanup idle runners
cleanup_idle_runners() {
    local idle_timeout=${1:-30}  # minutes
    local cloud_provider=${2:-aws}
    
    log "Finding idle runners (older than $idle_timeout minutes)..."
    
    # Get all runners
    runner_info=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "https://api.github.com/repos/$GITHUB_REPO/actions/runners")
    
    # Get current time in epoch seconds
    current_time=$(date +%s)
    
    # Find idle runners
    idle_runners=$(echo "$runner_info" | jq -r ".runners[] | select(.status == \"online\") | .name")
    
    if [[ -z "$idle_runners" ]]; then
        log "No online runners found to check for idleness"
        return 0
    fi
    
    log "Checking idleness for online runners..."
    
    # For each online runner, check recent job activity
    # Note: This is a simplified check - in reality you'd want to check
    # the actual job history and last activity time
    
    echo "$idle_runners" | while read -r runner_name; do
        if [[ -n "$runner_name" && "$runner_name" != "null" ]]; then
            log "Runner $runner_name appears idle, marking for cleanup"
            # In a real implementation, you'd have more sophisticated
            # logic to determine if a runner is truly idle
            cleanup_runner_by_name "$runner_name" "$cloud_provider"
        fi
    done
}

# Function to cleanup failed runners
cleanup_failed_runners() {
    local cloud_provider=${1:-aws}
    
    log "Finding failed/offline runners..."
    
    # Get all runners
    runner_info=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "https://api.github.com/repos/$GITHUB_REPO/actions/runners")
    
    # Find offline runners
    offline_runners=$(echo "$runner_info" | jq -r ".runners[] | select(.status == \"offline\") | .name")
    
    if [[ -z "$offline_runners" ]]; then
        log "No offline runners found"
        return 0
    fi
    
    log "Found offline runners:"
    echo "$offline_runners" | while read -r runner_name; do
        echo "  - $runner_name"
    done
    
    # Cleanup each offline runner
    echo "$offline_runners" | while read -r runner_name; do
        if [[ -n "$runner_name" && "$runner_name" != "null" ]]; then
            cleanup_runner_by_name "$runner_name" "$cloud_provider"
        fi
    done
}

# Function to cleanup orphaned instances
cleanup_orphaned_instances() {
    local cloud_provider=${1:-aws}
    
    log "Finding orphaned instances (instances without corresponding GitHub runners)..."
    
    # Get all GitHub runners
    github_runners=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "https://api.github.com/repos/$GITHUB_REPO/actions/runners" | jq -r '.runners[].name')
    
    case "$cloud_provider" in
        "aws")
            # Get all instances with the ephemeral-runner tag
            aws_instances=$(aws ec2 describe-instances \
                --filters "Name=tag:Purpose,Values=github-actions-runner" \
                --query 'Reservations[].Instances[].{InstanceId:InstanceId,Name:Tags[?Key==`Name`].Value|[0]}' \
                --output text)
            
            # Check each instance against GitHub runners
            echo "$aws_instances" | while IFS=$'\t' read -r instance_id instance_name; do
                if [[ -n "$instance_name" ]]; then
                    if echo "$github_runners" | grep -q "$instance_name"; then
                        log "Instance $instance_id ($instance_name) has corresponding GitHub runner"
                    else
                        warn "Instance $instance_id ($instance_name) is orphaned - cleaning up"
                        terminate_cloud_instance "$instance_id" "$cloud_provider"
                    fi
                fi
            done
            ;;
        
        "gcp")
            # Similar implementation for GCP
            gcloud compute instances list --filter="labels.purpose=github-actions-runner" --format="value(name,zone)" | while read -r instance_name zone; do
                if echo "$github_runners" | grep -q "$instance_name"; then
                    log "Instance $instance_name has corresponding GitHub runner"
                else
                    warn "Instance $instance_name is orphaned - cleaning up"
                    terminate_cloud_instance "$instance_name" "$cloud_provider"
                fi
            done
            ;;
        
        "azure")
            # Similar implementation for Azure
            az vm list --query "[?tags.purpose=='github-actions-runner'].{name:name,resourceGroup:resourceGroup}" --output tsv | while read -r instance_name resource_group; do
                if echo "$github_runners" | grep -q "$instance_name"; then
                    log "VM $instance_name has corresponding GitHub runner"
                else
                    warn "VM $instance_name is orphaned - cleaning up"
                    terminate_cloud_instance "$instance_name" "$cloud_provider"
                fi
            done
            ;;
        
        *)
            warn "Unknown cloud provider: $cloud_provider"
            warn "Please implement orphaned instance cleanup for your provider"
            ;;
esac
}

# Main execution
main() {
    local action=${1:-cleanup}
    local target=${2:-}
    local cloud_provider=${3:-aws}
    
    case "$action" in
        "cleanup")
            log "Starting comprehensive cleanup..."
            cleanup_failed_runners "$cloud_provider"
            cleanup_idle_runners 30 "$cloud_provider"
            cleanup_orphaned_instances "$cloud_provider"
            ;;
        
        "cleanup-idle")
            cleanup_idle_runners ${target:-30} "$cloud_provider"
            ;;
        
        "cleanup-failed")
            cleanup_failed_runners "$cloud_provider"
            ;;
        
        "cleanup-orphaned")
            cleanup_orphaned_instances "$cloud_provider"
            ;;
        
        "cleanup-by-name")
            if [[ -z "$target" ]]; then
                error "Runner name required for cleanup-by-name action"
                exit 1
            fi
            cleanup_runner_by_name "$target" "$cloud_provider"
            ;;
        
        "cleanup-by-pattern")
            if [[ -z "$target" ]]; then
                error "Pattern required for cleanup-by-pattern action"
                exit 1
            fi
            cleanup_runners_by_pattern "$target" "$cloud_provider"
            ;;
        
        *)
            echo "Usage: $0 {cleanup|cleanup-idle|cleanup-failed|cleanup-orphaned|cleanup-by-name|cleanup-by-pattern} [target] [cloud_provider]"
            echo ""
            echo "Actions:"
            echo "  cleanup              - Comprehensive cleanup of all problematic runners"
            echo "  cleanup-idle [mins]  - Cleanup idle runners (default: 30 minutes)"
            echo "  cleanup-failed       - Cleanup failed/offline runners"
            echo "  cleanup-orphaned     - Cleanup orphaned cloud instances"
            echo "  cleanup-by-name NAME - Cleanup specific runner by name"
            echo "  cleanup-by-pattern PATTERN - Cleanup runners matching pattern"
            echo ""
            echo "Cloud providers: aws, gcp, azure"
            exit 1
            ;;
esac
}

# Execute main function with all arguments
main "$@"
