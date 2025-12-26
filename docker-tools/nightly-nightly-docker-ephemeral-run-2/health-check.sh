#!/bin/bash

# Health check script for the ephemeral runner
# Monitors runner status and triggers cleanup if needed

set -e

# Configuration
HEALTH_CHECK_INTERVAL=${HEALTH_CHECK_INTERVAL:-30}
MAX_RETRIES=3
RETRY_COUNT=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if runner is healthy
check_runner_health() {
    # Check if runner process is running
    if ! pgrep -f "Runner.Listener" > /dev/null; then
        error "Runner process not found"
        return 1
    fi
    
    # Check if runner configuration exists
    if [ ! -f ".runner" ]; then
        error "Runner configuration not found"
        return 1
    fi
    
    # Check if runner can communicate with GitHub (basic connectivity)
    if ! curl -s --connect-timeout 5 https://github.com > /dev/null; then
        warning "Cannot reach GitHub, network issue detected"
        return 1
    fi
    
    return 0
}

# Main health check loop
main() {
    log "Starting health check service"
    
    while true; do
        if [ -f "/tmp/runner_stopped" ]; then
            log "Health check stopping due to shutdown signal"
            break
        fi
        
        if check_runner_health; then
            log "Runner health check passed"
            RETRY_COUNT=0
        else
            RETRY_COUNT=$((RETRY_COUNT + 1))
            warning "Runner health check failed (attempt $RETRY_COUNT/$MAX_RETRIES)"
            
            if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
                error "Runner health check failed $MAX_RETRIES times, triggering cleanup"
                touch /tmp/runner_stopped
                break
            fi
        fi
        
        sleep "$HEALTH_CHECK_INTERVAL"
    done
    
    log "Health check service stopped"
}

# Handle signals
trap 'log "Health check received shutdown signal"; exit 0' SIGTERM SIGINT

# Run main function
main
