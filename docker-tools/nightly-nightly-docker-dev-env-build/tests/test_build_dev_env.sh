#!/bin/bash

# Tests for build-dev-env.sh
# Mock rationale: These tests verify the script's functionality without requiring Docker

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test functions
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

# Test setup
TEST_DIR="/tmp/test-dev-env"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/src"
BUILD_SCRIPT="$SCRIPT_DIR/build-dev-env.sh"

setup() {
    log_info "Setting up test environment"
    rm -rf "$TEST_DIR"
    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR"
}

test_help() {
    log_info "Testing help functionality"
    if $BUILD_SCRIPT --help > /dev/null 2>&1; then
        log_success "Help command works"
    else
        log_error "Help command failed"
        return 1
    fi
}

test_python_stack() {
    log_info "Testing Python stack creation"
    if $BUILD_SCRIPT --stack python --name test-python --port 8080 > /dev/null 2>&1; then
        if [[ -d "test-python" ]] && [[ -f "test-python/Dockerfile" ]] && [[ -f "test-python/docker-compose.yml" ]]; then
            log_success "Python stack created successfully"
        else
            log_error "Python stack creation failed - missing files"
            return 1
        fi
    else
        log_error "Python stack creation failed"
        return 1
    fi
}

test_rust_stack() {
    log_info "Testing Rust stack creation"
    if $BUILD_SCRIPT --stack rust --name test-rust --port 3000 > /dev/null 2>&1; then
        if [[ -d "test-rust" ]] && [[ -f "test-rust/Dockerfile" ]] && [[ -f "test-rust/Cargo.toml" ]]; then
            log_success "Rust stack created successfully"
        else
            log_error "Rust stack creation failed - missing files"
            return 1
        fi
    else
        log_error "Rust stack creation failed"
        return 1
    fi
}

test_invalid_stack() {
    log_info "Testing invalid stack handling"
    if ! $BUILD_SCRIPT --stack invalid-stack --name test-invalid > /dev/null 2>&1; then
        log_success "Invalid stack properly rejected"
    else
        log_error "Invalid stack was not rejected"
        return 1
    fi
}

test_missing_docker() {
    log_info "Testing Docker availability check"
    # Mock docker command to simulate it's not available
    export PATH="/tmp/nonexistent:$PATH"
    if ! $BUILD_SCRIPT --stack python --name test-no-docker > /dev/null 2>&1; then
        log_success "Docker availability check works"
    else
        log_error "Docker availability check failed"
        return 1
    fi
    # Restore PATH
    export PATH="$ORIGINAL_PATH"
}

test_file_contents() {
    log_info "Testing generated file contents"
    
    # Test Dockerfile content
    if grep -q "python:3.11-slim" test-python/Dockerfile; then
        log_success "Python Dockerfile contains correct base image"
    else
        log_error "Python Dockerfile missing correct base image"
        return 1
    fi
    
    # Test docker-compose.yml content
    if grep -q "services:" test-python/docker-compose.yml && grep -q "app:" test-python/docker-compose.yml; then
        log_success "docker-compose.yml has correct structure"
    else
        log_error "docker-compose.yml missing required structure"
        return 1
    fi
    
    # Test Rust Cargo.toml
    if grep -q "[package]" test-rust/Cargo.toml && grep -q "name =" test-rust/Cargo.toml; then
        log_success "Cargo.toml has correct structure"
    else
        log_error "Cargo.toml missing required structure"
        return 1
    fi
}

test_cleanup() {
    log_info "Cleaning up test environment"
    cd /tmp
    rm -rf "$TEST_DIR"
}

# Run tests
main() {
    log_info "Starting tests for build-dev-env.sh"
    
    ORIGINAL_PATH="$PATH"
    setup
    
    test_help
    test_python_stack
    test_rust_stack
    test_invalid_stack
    test_missing_docker
    test_file_contents
    
    test_cleanup
    
    log_success "All tests passed!"
}

# Run if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
