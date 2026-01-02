#!/bin/bash

# Tests for language stacks
# Mock rationale: These tests verify stack-specific functionality

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
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/src"
STACKS_DIR="$SCRIPT_DIR/stacks"

setup() {
    log_info "Setting up stack tests"
}

test_python_stack() {
    log_info "Testing Python stack"
    
    if [[ ! -d "$STACKS_DIR/python" ]]; then
        log_error "Python stack directory not found"
        return 1
    fi
    
    if [[ ! -f "$STACKS_DIR/python/Dockerfile" ]]; then
        log_error "Python Dockerfile not found"
        return 1
    fi
    
    if [[ ! -f "$STACKS_DIR/python/setup.sh" ]]; then
        log_error "Python setup script not found"
        return 1
    fi
    
    # Test Dockerfile content
    if grep -q "python:3.11-slim" "$STACKS_DIR/python/Dockerfile"; then
        log_success "Python Dockerfile has correct base image"
    else
        log_error "Python Dockerfile missing correct base image"
        return 1
    fi
    
    # Test setup script
    if grep -q "#!/bin/bash" "$STACKS_DIR/python/setup.sh"; then
        log_success "Python setup script is executable"
    else
        log_error "Python setup script missing shebang"
        return 1
    fi
    
    log_success "Python stack tests passed"
}

test_rust_stack() {
    log_info "Testing Rust stack"
    
    if [[ ! -d "$STACKS_DIR/rust" ]]; then
        log_error "Rust stack directory not found"
        return 1
    fi
    
    if [[ ! -f "$STACKS_DIR/rust/Dockerfile" ]]; then
        log_error "Rust Dockerfile not found"
        return 1
    fi
    
    if [[ ! -f "$STACKS_DIR/rust/setup.sh" ]]; then
        log_error "Rust setup script not found"
        return 1
    fi
    
    # Test Dockerfile content
    if grep -q "rust:1.75-slim" "$STACKS_DIR/rust/Dockerfile"; then
        log_success "Rust Dockerfile has correct base image"
    else
        log_error "Rust Dockerfile missing correct base image"
        return 1
    fi
    
    # Test setup script
    if grep -q "#!/bin/bash" "$STACKS_DIR/rust/setup.sh"; then
        log_success "Rust setup script is executable"
    else
        log_error "Rust setup script missing shebang"
        return 1
    fi
    
    log_success "Rust stack tests passed"
}

test_stack_files() {
    log_info "Testing stack file structure"
    
    for stack in python rust; do
        if [[ -d "$STACKS_DIR/$stack" ]]; then
            log_info "Checking $stack stack structure"
            
            # Check for required files
            if [[ -f "$STACKS_DIR/$stack/Dockerfile" ]] && [[ -f "$STACKS_DIR/$stack/setup.sh" ]]; then
                log_success "$stack stack has required files"
            else
                log_error "$stack stack missing required files"
                return 1
            fi
            
            # Check Dockerfile syntax (basic check)
            if head -1 "$STACKS_DIR/$stack/Dockerfile" | grep -q "^FROM "; then
                log_success "$stack Dockerfile has valid FROM instruction"
            else
                log_error "$stack Dockerfile missing FROM instruction"
                return 1
            fi
        else
            log_warning "Stack $stack not found, skipping"
        fi
    done
}

# Run tests
main() {
    log_info "Starting stack tests"
    
    setup
    test_python_stack
    test_rust_stack
    test_stack_files
    
    log_success "All stack tests passed!"
}

# Run if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
