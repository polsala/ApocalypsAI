#!/bin/bash

# Nightly Docker Ephemeral Runner
# Self-destructing GitHub Actions runner

set -e

# Configuration
GITHUB_TOKEN=${GITHUB_TOKEN:-""}
GITHUB_REPO=${GITHUB_REPO:-""}
RUNNER_NAME=${RUNNER_NAME:-"ephemeral-runner-$(date +%s)"}
MAX_JOBS=${MAX_JOBS:-1}
HEALTH_CHECK_INTERVAL=${HEALTH_CHECK_INTERVAL:-30}
JOB_TIMEOUT=${JOB_TIMEOUT:-3600}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Validate required environment variables
validate_config() {
    log "Validating configuration..."
    
    if [ -z "$GITHUB_TOKEN" ]; then
        error "GITHUB_TOKEN is required"
        exit 1
    fi
    
    if [ -z "$GITHUB_REPO" ]; then
        error "GITHUB_REPO is required"
        exit 1
    fi
    
    if [[ ! "$GITHUB_REPO" =~ ^[^/]+/[^/]+$ ]]; then
        error "GITHUB_REPO must be in format 'owner/repo'"
        exit 1
    fi
    
    success "Configuration validated"
}

# Register runner with GitHub
register_runner() {
    log "Registering runner with GitHub..."
    
    # Extract owner and repo from GITHUB_REPO
    OWNER=$(echo "$GITHUB_REPO" | cut -d'/' -f1)
    REPO=$(echo "$GITHUB_REPO" | cut -d'/' -f2)
    
    # Configure runner
    ./config.sh \
        --url "https://github.com/$GITHUB_REPO" \
        --token "$GITHUB_TOKEN" \
        --name "$RUNNER_NAME" \
        --unattended \
        --replace \
        --ephemeral
    
    if [ $? -eq 0 ]; then
        success "Runner registered successfully"
    else
        error "Failed to register runner"
        exit 1
    fi
}

# Start health check loop
start_health_check() {
    log "Starting health check loop..."
    
    while true; do
        if [ -f "/tmp/runner_stopped" ]; then
            log "Health check detected runner stop, exiting..."
            break
        fi
        
        # Check if runner process is still running
        if ! pgrep -f "Runner.Listener" > /dev/null; then
            warning "Runner process not found, triggering self-destruction"
            touch /tmp/runner_stopped
            break
        fi
        
        sleep "$HEALTH_CHECK_INTERVAL"
    done
}

# Monitor job execution
monitor_jobs() {
    log "Starting job monitoring..."
    
    local job_count=0
    
    while [ $job_count -lt $MAX_JOBS ]; do
        # Check if runner is still registered and online
        if ! ./bin/Runner.Listener --help > /dev/null 2>&1; then
            warning "Runner listener not available, stopping"
            break
        fi
        
        # Wait for job
        log "Waiting for job assignment (job $((job_count + 1))/$MAX_JOBS)..."
        
        # Check every 10 seconds for job status
        for i in {1..60}; do
            if [ -f "/tmp/runner_stopped" ]; then
                break 2
            fi
            sleep 10
        done
        
        # If we're here, a job might have completed or timed out
        job_count=$((job_count + 1))
        log "Job $job_count completed"
    done
    
    success "Reached job limit ($MAX_JOBS jobs), triggering self-destruction"
}

# Cleanup and self-destruct
self_destruct() {
    log "Initiating self-destruction sequence..."
    
    # Stop runner
    if [ -f ".runner" ]; then
        log "Stopping runner..."
        ./run.sh --stop
    fi
    
    # Unregister runner
    log "Unregistering runner from GitHub..."
    ./config.sh remove --token "$GITHUB_TOKEN" --unattended || true
    
    # Clean up files
    log "Cleaning up temporary files..."
    rm -f /tmp/runner_stopped
    
    success "Self-destruction complete"
    
    # Exit with code that triggers container restart
    exit 0
}

# Signal handlers
trap 'log "Received SIGTERM, initiating graceful shutdown"; touch /tmp/runner_stopped; self_destruct' SIGTERM
trap 'log "Received SIGINT, initiating graceful shutdown"; touch /tmp/runner_stopped; self_destruct' SIGINT

# Main execution
main() {
    log "Starting Nightly Docker Ephemeral Runner"
    log "Runner Name: $RUNNER_NAME"
    log "Repository: $GITHUB_REPO"
    log "Max Jobs: $MAX_JOBS"
    log "Health Check Interval: ${HEALTH_CHECK_INTERVAL}s"
    log "Job Timeout: ${JOB_TIMEOUT}s"
    
    # Validate configuration
    validate_config
    
    # Register with GitHub
    register_runner
    
    # Start health check in background
    start_health_check &
    HEALTH_CHECK_PID=$!
    
    # Monitor jobs
    monitor_jobs
    
    # Cleanup
    self_destruct
    
    # Wait for health check to finish
    wait $HEALTH_CHECK_PID
}

# Run main function
main
