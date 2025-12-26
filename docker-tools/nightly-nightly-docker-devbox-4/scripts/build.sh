#!/bin/bash

# Nightly Docker DevBox Build Script
# Builds the multi-stage Docker image with all language stacks

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

# Build the Docker image
build_image() {
    log_info "Building Nightly Docker DevBox image..."
    
    cd "$ROOT_DIR"
    
    # Build the final stage
    docker build -t nightly-devbox:latest -f Dockerfile .
    
    if [ $? -eq 0 ]; then
        log_info "Successfully built nightly-devbox:latest"
    else
        log_error "Failed to build Docker image"
        exit 1
    fi
}

# Main execution
main() {
    log_info "Starting Nightly Docker DevBox build process"
    
    check_docker
    build_image
    
    log_info "Build completed successfully!"
    log_info "You can now create development environments using the scripts in ./scripts/"
}

# Run main function
main
