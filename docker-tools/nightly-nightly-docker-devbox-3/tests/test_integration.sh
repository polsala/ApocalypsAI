#!/bin/bash

# Nightly Docker DevBox - Integration Tests
# Test with actual Docker containers

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

test_docker_available() {
    if command -v docker &> /dev/null && docker info &> /dev/null; then
        log_success "Docker is available"
        return 0
    else
        log_error "Docker is not available"
        return 1
    fi
}

test_build_image() {
    local language=$1
    local image_name="test-nightly-devbox-$language"
    
    log_info "Testing $language image build..."
    
    if docker build -f "$ROOT_DIR/dockerfiles/Dockerfile.$language" -t "$image_name" "$ROOT_DIR" 2>/dev/null; then
        log_success "$language image built successfully"
        docker rmi "$image_name" 2>/dev/null || true
        return 0
    else
        log_error "$language image build failed"
        return 1
    fi
}

test_container_health() {
    local language=$1
    local image_name="test-nightly-devbox-$language"
    
    log_info "Testing $language container health..."
    
    # Build image
    docker build -f "$ROOT_DIR/dockerfiles/Dockerfile.$language" -t "$image_name" "$ROOT_DIR" 2>/dev/null || {
        log_error "Failed to build $language image for health test"
        return 1
    }
    
    # Run container in background
    local container_name="test-health-$language-$(date +%s)"
    docker run -d --name "$container_name" --health-interval=5s --health-retries=2 --health-timeout=3s "$image_name" sleep 30
    
    # Wait for health check
    sleep 10
    
    # Check health status
    local health_status=$(docker inspect --format='{{.State.Health.Status}}' "$container_name")
    
    docker stop "$container_name" 2>/dev/null || true
    docker rm "$container_name" 2>/dev/null || true
    docker rmi "$image_name" 2>/dev/null || true
    
    if [[ "$health_status" == "healthy" ]]; then
        log_success "$language container health check passed"
        return 0
    else
        log_error "$language container health check failed: $health_status"
        return 1
    fi
}

test_script_functionality() {
    local script=$1
    local test_args=$2
    
    log_info "Testing script: $(basename $script) with args: $test_args"
    
    if timeout 30s bash -c "$script $test_args" &> /dev/null; then
        log_success "Script works: $(basename $script)"
        return 0
    else
        log_error "Script failed: $(basename $script)"
        return 1
    fi
}

main() {
    log_info "Running integration tests..."
    
    local failed_tests=0
    
    # Check Docker availability
    if ! test_docker_available; then
        exit 1
    fi
    
    # Test building all images
    local languages=("python" "node" "rust" "go")
    
    for language in "${languages[@]}"; do
        if ! test_build_image "$language"; then
            ((failed_tests++))
        fi
    done
    
    # Test container health for each language
    for language in "${languages[@]}"; do
        if ! test_container_health "$language"; then
            ((failed_tests++))
        fi
    done
    
    # Test script functionality
    local scripts=(
        "$ROOT_DIR/scripts/console.sh"
        "$ROOT_DIR/scripts/metrics.sh"
        "$ROOT_DIR/scripts/cleanup.sh"
    )
    
    for script in "${scripts[@]}"; do
        if ! test_script_functionality "$script" "--help"; then
            ((failed_tests++))
        fi
    done
    
    if [[ $failed_tests -eq 0 ]]; then
        log_success "All integration tests passed"
        exit 0
    else
        log_error "$failed_tests integration tests failed"
        exit 1
    fi
}

main "$@"
