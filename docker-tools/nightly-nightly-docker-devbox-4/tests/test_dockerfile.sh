#!/bin/bash

# Test script for Dockerfile functionality
# Tests that all language stacks are properly installed

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

# Test Python installation
test_python() {
    log_info "Testing Python installation..."
    
    if docker run --rm nightly-devbox:latest python3 --version; then
        log_info "✓ Python is available"
        
        # Test Python packages
        if docker run --rm nightly-devbox:latest python3 -c "import pytest, black, flake8, jupyter"; then
            log_info "✓ Python development packages are available"
            return 0
        else
            log_error "✗ Python development packages are missing"
            return 1
        fi
    else
        log_error "✗ Python is not available"
        return 1
    fi
}

# Test Rust installation
test_rust() {
    log_info "Testing Rust installation..."
    
    if docker run --rm nightly-devbox:latest rustc --version; then
        log_info "✓ Rust compiler is available"
        
        if docker run --rm nightly-devbox:latest cargo --version; then
            log_info "✓ Cargo is available"
            
            # Test Rust tools
            if docker run --rm nightly-devbox:latest rustfmt --version; then
                log_info "✓ rustfmt is available"
            else
                log_warn "✗ rustfmt is not available"
            fi
            
            if docker run --rm nightly-devbox:latest clippy --version; then
                log_info "✓ clippy is available"
            else
                log_warn "✗ clippy is not available"
            fi
            
            return 0
        else
            log_error "✗ Cargo is not available"
            return 1
        fi
    else
        log_error "✗ Rust compiler is not available"
        return 1
    fi
}

# Test Go installation
test_go() {
    log_info "Testing Go installation..."
    
    if docker run --rm nightly-devbox:latest go version; then
        log_info "✓ Go is available"
        
        # Test Go tools
        if docker run --rm nightly-devbox:latest gofmt --version; then
            log_info "✓ gofmt is available"
        else
            log_warn "✗ gofmt is not available"
        fi
        
        if docker run --rm nightly-devbox:latest go vet; then
            log_info "✓ go vet is available"
        else
            log_warn "✗ go vet is not available"
        fi
        
        return 0
    else
        log_error "✗ Go is not available"
        return 1
    fi
}

# Test Node.js installation
test_nodejs() {
    log_info "Testing Node.js installation..."
    
    if docker run --rm nightly-devbox:latest node --version; then
        log_info "✓ Node.js is available"
        
        if docker run --rm nightly-devbox:latest npm --version; then
            log_info "✓ npm is available"
            
            # Test Node.js tools
            if docker run --rm nightly-devbox:latest eslint --version; then
                log_info "✓ ESLint is available"
            else
                log_warn "✗ ESLint is not available"
            fi
            
            if docker run --rm nightly-devbox:latest prettier --version; then
                log_info "✓ Prettier is available"
            else
                log_warn "✗ Prettier is not available"
            fi
            
            return 0
        else
            log_error "✗ npm is not available"
            return 1
        fi
    else
        log_error "✗ Node.js is not available"
        return 1
    fi
}

# Test Java installation
test_java() {
    log_info "Testing Java installation..."
    
    if docker run --rm nightly-devbox:latest java -version; then
        log_info "✓ Java is available"
        
        if docker run --rm nightly-devbox:latest javac -version; then
            log_info "✓ Java compiler is available"
            
            # Test Java tools
            if docker run --rm nightly-devbox:latest mvn --version; then
                log_info "✓ Maven is available"
            else
                log_warn "✗ Maven is not available"
            fi
            
            if docker run --rm nightly-devbox:latest gradle --version; then
                log_info "✓ Gradle is available"
            else
                log_warn "✗ Gradle is not available"
            fi
            
            return 0
        else
            log_error "✗ Java compiler is not available"
            return 1
        fi
    else
        log_error "✗ Java is not available"
        return 1
    fi
}

# Test C++ installation
test_cpp() {
    log_info "Testing C++ installation..."
    
    if docker run --rm nightly-devbox:latest gcc --version; then
        log_info "✓ GCC is available"
        
        if docker run --rm nightly-devbox:latest g++ --version; then
            log_info "✓ G++ is available"
            
            # Test C++ tools
            if docker run --rm nightly-devbox:latest gdb --version; then
                log_info "✓ GDB is available"
            else
                log_warn "✗ GDB is not available"
            fi
            
            if docker run --rm nightly-devbox:latest clang --version; then
                log_info "✓ Clang is available"
            else
                log_warn "✗ Clang is not available"
            fi
            
            return 0
        else
            log_error "✗ G++ is not available"
            return 1
        fi
    else
        log_error "✗ GCC is not available"
        return 1
    fi
}

# Run all tests
run_tests() {
    log_info "Starting Dockerfile functionality tests"
    
    local tests_passed=0
    local tests_failed=0
    
    # Test 1: Python
    if test_python; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    
    # Test 2: Rust
    if test_rust; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    
    # Test 3: Go
    if test_go; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    
    # Test 4: Node.js
    if test_nodejs; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    
    # Test 5: Java
    if test_java; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    
    # Test 6: C++
    if test_cpp; then
        ((tests_passed++))
    else
        ((tests_failed++))
    fi
    
    # Summary
    log_info "\nTest Summary:"
    log_info "Tests passed: $tests_passed"
    log_info "Tests failed: $tests_failed"
    
    if [ $tests_failed -eq 0 ]; then
        log_info "🎉 All Dockerfile tests passed!"
        return 0
    else
        log_error "❌ Some Dockerfile tests failed!"
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
