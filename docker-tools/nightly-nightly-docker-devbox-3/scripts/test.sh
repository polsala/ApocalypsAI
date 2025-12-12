#!/bin/bash

# Nightly Docker DevBox - Test Script
# Run tests for the development environment

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
    echo "Usage: $0 [test_type]"
    echo ""
    echo "Run tests for Nightly DevBox."
    echo ""
    echo "Test types:"
    echo "  unit        - Unit tests for scripts (default)"
    echo "  integration - Integration tests with Docker"
    echo "  all         - Run all tests"
    echo "  help        - Show this help"
}

test_unit() {
    log_info "Running unit tests..."
    
    # Test that all scripts are executable
    local scripts=(
        "$ROOT_DIR/scripts/build.sh"
        "$ROOT_DIR/scripts/run.sh"
        "$ROOT_DIR/scripts/console.sh"
        "$ROOT_DIR/scripts/metrics.sh"
        "$ROOT_DIR/scripts/cleanup.sh"
    )
    
    for script in "${scripts[@]}"; do
        if [[ -x "$script" ]]; then
            log_success "Script is executable: $(basename $script)"
        else
            log_error "Script is not executable: $(basename $script)"
            return 1
        fi
    done
    
    # Test that Dockerfiles exist
    local dockerfiles=(
        "$ROOT_DIR/dockerfiles/Dockerfile.python"
        "$ROOT_DIR/dockerfiles/Dockerfile.node"
        "$ROOT_DIR/dockerfiles/Dockerfile.rust"
        "$ROOT_DIR/dockerfiles/Dockerfile.go"
    )
    
    for dockerfile in "${dockerfiles[@]}"; do
        if [[ -f "$dockerfile" ]]; then
            log_success "Dockerfile exists: $(basename $dockerfile)"
        else
            log_error "Dockerfile missing: $(basename $dockerfile)"
            return 1
        fi
    done
    
    # Test that welcome art exists
    if [[ -f "$ROOT_DIR/assets/welcome.txt" ]]; then
        log_success "Welcome art exists"
    else
        log_error "Welcome art missing"
        return 1
    fi
    
    log_success "Unit tests passed"
}

test_integration() {
    log_info "Running integration tests..."
    
    # Check if Docker is available
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        return 1
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        return 1
    fi
    
    # Test building Python image
    log_info "Testing Python image build..."
    if docker build -f "$ROOT_DIR/dockerfiles/Dockerfile.python" -t "test-nightly-devbox-python" "$ROOT_DIR" 2>/dev/null; then
        log_success "Python image built successfully"
        docker rmi "test-nightly-devbox-python" 2>/dev/null || true
    else
        log_error "Python image build failed"
        return 1
    fi
    
    # Test building Node.js image
    log_info "Testing Node.js image build..."
    if docker build -f "$ROOT_DIR/dockerfiles/Dockerfile.node" -t "test-nightly-devbox-node" "$ROOT_DIR" 2>/dev/null; then
        log_success "Node.js image built successfully"
        docker rmi "test-nightly-devbox-node" 2>/dev/null || true
    else
        log_error "Node.js image build failed"
        return 1
    fi
    
    # Test building Rust image
    log_info "Testing Rust image build..."
    if docker build -f "$ROOT_DIR/dockerfiles/Dockerfile.rust" -t "test-nightly-devbox-rust" "$ROOT_DIR" 2>/dev/null; then
        log_success "Rust image built successfully"
        docker rmi "test-nightly-devbox-rust" 2>/dev/null || true
    else
        log_error "Rust image build failed"
        return 1
    fi
    
    # Test building Go image
    log_info "Testing Go image build..."
    if docker build -f "$ROOT_DIR/dockerfiles/Dockerfile.go" -t "test-nightly-devbox-go" "$ROOT_DIR" 2>/dev/null; then
        log_success "Go image built successfully"
        docker rmi "test-nightly-devbox-go" 2>/dev/null || true
    else
        log_error "Go image build failed"
        return 1
    fi
    
    log_success "Integration tests passed"
}

main() {
    local test_type=${1:-"unit"}
    
    case $test_type in
        unit)
            test_unit
            ;;
        integration)
            test_integration
            ;;
        all)
            test_unit
            test_integration
            ;;
        help)
            show_usage
            exit 0
            ;;
        *)
            log_error "Unknown test type: $test_type"
            show_usage
            exit 1
            ;;
    esac
}

main "$@"
