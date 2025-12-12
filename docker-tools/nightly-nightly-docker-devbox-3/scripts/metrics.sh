#!/bin/bash

# Nightly Docker DevBox - Metrics Script
# View health metrics

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_usage() {
    echo "Usage: $0 [container_name]"
    echo ""
    echo "View health metrics for a Nightly DevBox container."
    echo ""
    echo "If no container name is specified, the script will find the first"
    echo "running Nightly DevBox container."
}

find_container() {
    local container_name=$1
    
    if [[ -n "$container_name" ]]; then
        # Check if specific container exists and is running
        if docker ps --format "{{.Names}}" | grep -q "^${container_name}$"; then
            echo "$container_name"
            return 0
        else
            log_error "Container not found or not running: $container_name"
            return 1
        fi
    else
        # Find any running Nightly DevBox container
        local containers
        containers=$(docker ps --format "{{.Names}}" | grep "nightly-devbox" | head -1)
        
        if [[ -n "$containers" ]]; then
            echo "$containers"
            return 0
        else
            log_error "No running Nightly DevBox containers found"
            return 1
        fi
    fi
}

show_container_info() {
    local container_name=$1
    
    log_info "Container Information:"
    echo ""
    
    # Basic info
    echo "  Name: $container_name"
    echo "  Status: $(docker inspect --format='{{.State.Status}}' $container_name)"
    echo "  Health: $(docker inspect --format='{{.State.Health.Status}}' $container_name)"
    echo "  Image: $(docker inspect --format='{{.Config.Image}}' $container_name)"
    echo ""
    
    # Resource usage
    log_info "Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}" $container_name
    echo ""
    
    # Port mappings
    log_info "Port Mappings:"
    docker port $container_name || echo "  No port mappings"
    echo ""
    
    # Volumes
    log_info "Volume Mappings:"
    docker inspect --format='{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' $container_name || echo "  No volume mappings"
    echo ""
    
    # Recent logs
    log_info "Recent Logs:"
    docker logs --tail 20 $container_name || echo "  No logs available"
}

main() {
    local container_name=${1:-""}
    
    if [[ "$container_name" == "-h" || "$container_name" == "--help" ]]; then
        show_usage
        exit 0
    fi
    
    log_info "Finding container..."
    container_name=$(find_container "$container_name") || exit 1
    
    show_container_info "$container_name"
}

main "$@"
