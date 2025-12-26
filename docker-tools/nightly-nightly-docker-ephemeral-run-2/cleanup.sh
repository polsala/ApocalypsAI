#!/bin/bash

# Cleanup script for ephemeral runner
# Ensures proper cleanup on container exit

set -e

# Configuration
GITHUB_TOKEN=${GITHUB_TOKEN:-""}

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

# Cleanup runner registration
cleanup_runner() {
    log "Cleaning up runner registration..."
    
    if [ -f ".runner" ]; then
        log "Stopping runner..."
        ./run.sh --stop || true
        
        if [ -n "$GITHUB_TOKEN" ]; then
            log "Unregistering runner from GitHub..."
            ./config.sh remove --token "$GITHUB_TOKEN" --unattended || true
        fi
        
        log "Removing runner configuration..."
        rm -f .runner
    fi
}

# Cleanup temporary files
cleanup_temp_files() {
    log "Cleaning up temporary files..."
    
    # Remove health check stop signal
    rm -f /tmp/runner_stopped
    
    # Remove work directory
    if [ -d "_work" ]; then
        log "Removing work directory..."
        rm -rf _work
    fi
    
    # Remove any other temporary files
    find . -name "*.tmp" -delete 2>/dev/null || true
    find . -name "*.log" -delete 2>/dev/null || true
}

# Main cleanup function
main() {
    log "Starting cleanup process..."
    
    cleanup_runner
    cleanup_temp_files
    
    success "Cleanup completed successfully"
}

# Handle signals
trap 'log "Cleanup received shutdown signal"; main; exit 0' SIGTERM SIGINT

# Run cleanup if script is called directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main
fi
