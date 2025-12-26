#!/bin/bash

# Test script for Nightly Docker DevBox
# Tests the creation, starting, and cleanup of development environments

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
        log_error "Docker is not installed. Skipping tests."
        return 1
    fi

    if ! docker info &> /dev/null; then
        log_error "Docker is not running. Skipping tests."
        return 1
    fi
    return 0
}

# Test Docker image build
test_image_build() {
    log_info "Testing Docker image build..."
    
    cd "$ROOT_DIR"
    
    # Build the image
    if docker build -t nightly-devbox:test -f Dockerfile .; then
        log_info "✓ Docker image build successful"
        return 0
    else
        log_error "✗ Docker image build failed"
        return 1
    fi
}

# Test development environment creation
test_devbox_creation() {
    local name="test-devbox-$$"
    
    log_info "Testing development environment creation..."
    
    # Create a test devbox
    if "$ROOT_DIR/scripts/create_devbox.sh" python "$name"; then
        log_info "✓ Development environment creation successful"
        
        # Check if container was created
        if docker ps -a --format "table {{.Names}}" | grep -q "^${name}$"; then
            log_info "✓ Container exists"
        else
            log_error "✗ Container was not created"
            return 1
        fi
        
        # Check if volume was created
        if docker volume ls --format "table {{.Name}}" | grep -q "${name}_workspace"; then
            log_info "✓ Volume exists"
        else
            log_error "✗ Volume was not created"
            return 1
        fi
        
        # Clean up
        "$ROOT_DIR/scripts/cleanup_devbox.sh" "$name" 2>/dev/null || true
        
        return 0
    else
        log_error "✗ Development environment creation failed"
        return 1
    fi
}

# Test development environment start/stop
test_devbox_lifecycle() {
    local name="test-lifecycle-$$"
    
    log_info "Testing development environment lifecycle..."
    
    # Create devbox
    "$ROOT_DIR/scripts/create_devbox.sh" python "$name" 2>/dev/null || return 1
    
    # Start devbox
    if "$ROOT_DIR/scripts/start_devbox.sh" "$name"; then
        log_info "✓ Development environment start successful"
        
        # Check if container is running
        if docker ps --format "table {{.Names}}" | grep -q "^${name}$"; then
            log_info "✓ Container is running"
        else
            log_error "✗ Container is not running"
            return 1
        fi
        
        # Stop devbox
        if "$ROOT_DIR/scripts/stop_devbox.sh" "$name"; then
            log_info "✓ Development environment stop successful"
        else
            log_error "✗ Development environment stop failed"
            return 1
        fi
        
        # Clean up
        "$ROOT_DIR/scripts/cleanup_devbox.sh" "$name" 2>/dev/null || true
        
        return 0
    else
        log_error "✗ Development environment start failed"
        return 1
    fi
}

# Test language stack validation
test_language_validation() {
    log_info "Testing language stack validation..."
    
    # Test valid stacks
    local valid_stacks=("python" "rust" "go" "nodejs" "java" "cpp")
    for stack in "${valid_stacks[@]}"; do
        if "$ROOT_DIR/scripts/create_devbox.sh" "$stack" "test-validation-$$" 2>/dev/null; then
            log_info "✓ Valid stack '$stack' accepted"
            "$ROOT_DIR/scripts/cleanup_devbox.sh" "test-validation-$$" 2>/dev/null || true
        else
            log_error "✗ Valid stack '$stack' rejected"
            return 1
        fi
    done
    
    # Test invalid stack
    if ! "$ROOT_DIR/scripts/create_devbox.sh" "invalid" "test-invalid-$$" 2>/dev/null; then
        log_info "✓ Invalid stack 'invalid' rejected"
        return 0
    else
        log_error "✗ Invalid stack 'invalid' accepted"
        return 1
    fi
}

# Run all tests
run_tests() {
    log_info "Starting Nightly Docker DevBox tests"
    
    local tests_passed=0
    local tests_failed=0
    
    # Test 1: Docker image build
    if test_image_build; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    
    # Test 2: Development environment creation
    if test_devbox_creation; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    
    # Test 3: Development environment lifecycle
    if test_devbox_lifecycle; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    
    # Test 4: Language stack validation
    if test_language_validation; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    
    # Summary
    log_info "\nTest Summary:"
    log_info "Tests passed: $tests_passed"
    log_info "Tests failed: $tests_failed"
    
    if [ $tests_failed -eq 0 ]; then
        log_info "🎉 All tests passed!"
        return 0
    else
        log_error "❌ Some tests failed!"
        return 1
    fi
}

# Main execution
main() {
    if ! check_docker; then
        log_warn "Docker not available, skipping tests"
        exit 0
    fi
    
    run_tests
}

# Run main function
main
