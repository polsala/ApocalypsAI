#!/bin/bash

# Nightly Docker DevBox Cleanup Script
# Removes a development environment container and its volumes

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed and running
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        log_error "Docker is not running. Please start Docker daemon."
        exit 1
    fi
}

# Check if container exists
check_container() {
    local name="$1"
    
    if ! docker ps -a --format "table {{.Names}}" | grep -q "^${name}$"; then
        log_error "Container '$name' does not exist."
        exit 1
    fi
}

# Cleanup development environment (container + volumes)
cleanup_devbox() {
    local name="$1"
    
    log_info "Cleaning up development environment '$name' (container + volumes)"
    
    # Stop container if running
    if docker ps --format "table {{.Names}}" | grep -q "^${name}$"; then
        docker stop "$name" 2>/dev/null || true
    fi
    
    # Remove container
    docker rm "$name" 2>/dev/null || true
    
    # Remove volume
    docker volume rm "${name}_workspace" 2>/dev/null || true
    
    log_info "Successfully cleaned up development environment '$name'"
    log_info "Container and volume removed"
}

# Show usage information
show_usage() {
    echo "Usage: $0 <environment_name>"
    echo ""
    echo "Example:"
    echo "  $0 my-python-project"
}

# Main execution
main() {
    if [ $# -ne 1 ]; then
        log_error "Invalid number of arguments"
        show_usage
        exit 1
    fi
    
    local name="$1"
    
    log_info "Starting Nightly Docker DevBox cleanup process"
    
    check_docker
    check_container "$name"
    cleanup_devbox "$name"
}

# Run main function
main "$@"
