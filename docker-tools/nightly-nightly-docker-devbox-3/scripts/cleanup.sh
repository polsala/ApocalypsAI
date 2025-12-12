#!/bin/bash

# Nightly Docker DevBox - Cleanup Script
# Clean up containers and images

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
    echo "Usage: $0 [options]"
    echo ""
    echo "Clean up Nightly DevBox containers and images."
    echo ""
    echo "Options:"
    echo "  -c, --containers    - Remove all Nightly DevBox containers"
    echo "  -i, --images        - Remove all Nightly DevBox images"
    echo "  -a, --all           - Remove containers and images"
    echo "  -h, --help          - Show this help"
}

cleanup_containers() {
    log_info "Finding Nightly DevBox containers..."
    local containers
    containers=$(docker ps -a --format "{{.Names}}" | grep "nightly-devbox")
    
    if [[ -z "$containers" ]]; then
        log_info "No Nightly DevBox containers found"
        return 0
    fi
    
    log_info "Stopping and removing containers..."
    echo "$containers" | while read container; do
        if [[ -n "$container" ]]; then
            log_info "Removing container: $container"
            docker rm -f "$container" 2>/dev/null || true
        fi
    done
    
    log_success "Containers cleaned up"
}

cleanup_images() {
    log_info "Finding Nightly DevBox images..."
    local images
    images=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep "nightly-devbox")
    
    if [[ -z "$images" ]]; then
        log_info "No Nightly DevBox images found"
        return 0
    fi
    
    log_info "Removing images..."
    echo "$images" | while read image; do
        if [[ -n "$image" ]]; then
            log_info "Removing image: $image"
            docker rmi -f "$image" 2>/dev/null || true
        fi
    done
    
    log_success "Images cleaned up"
}

main() {
    local cleanup_containers=false
    local cleanup_images=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -c|--containers)
                cleanup_containers=true
                shift
                ;;
            -i|--images)
                cleanup_images=true
                shift
                ;;
            -a|--all)
                cleanup_containers=true
                cleanup_images=true
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Default to cleaning both if no options specified
    if [[ "$cleanup_containers" == "false" && "$cleanup_images" == "false" ]]; then
        cleanup_containers=true
        cleanup_images=true
    fi
    
    if [[ "$cleanup_containers" == "true" ]]; then
        cleanup_containers
    fi
    
    if [[ "$cleanup_images" == "true" ]]; then
        cleanup_images
    fi
    
    log_success "Cleanup completed"
}

main "$@"
