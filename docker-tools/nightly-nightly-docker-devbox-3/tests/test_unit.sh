#!/bin/bash

# Nightly Docker DevBox - Unit Tests
# Test the scripts without Docker

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

test_script_executable() {
    local script=$1
    
    if [[ -x "$script" ]]; then
        log_success "Script is executable: $(basename $script)"
        return 0
    else
        log_error "Script is not executable: $(basename $script)"
        return 1
    fi
}

test_dockerfile_exists() {
    local dockerfile=$1
    
    if [[ -f "$dockerfile" ]]; then
        log_success "Dockerfile exists: $(basename $dockerfile)"
        return 0
    else
        log_error "Dockerfile missing: $(basename $dockerfile)"
        return 1
    fi
}

test_welcome_art_exists() {
    if [[ -f "$ROOT_DIR/assets/welcome.txt" ]]; then
        log_success "Welcome art exists"
        return 0
    else
        log_error "Welcome art missing"
        return 1
    fi
}

test_help_commands() {
    local script=$1
    
    log_info "Testing help command for: $(basename $script)"
    
    # Test help flag
    if timeout 10s bash -c "$script --help" &> /dev/null; then
        log_success "Help command works: $(basename $script)"
        return 0
    else
        log_error "Help command failed: $(basename $script)"
        return 1
    fi
}

main() {
    log_info "Running unit tests..."
    
    local failed_tests=0
    
    # Test that all scripts are executable
    local scripts=(
        "$ROOT_DIR/scripts/build.sh"
        "$ROOT_DIR/scripts/run.sh"
        "$ROOT_DIR/scripts/console.sh"
        "$ROOT_DIR/scripts/metrics.sh"
        "$ROOT_DIR/scripts/cleanup.sh"
        "$ROOT_DIR/scripts/test.sh"
    )
    
    for script in "${scripts[@]}"; do
        if ! test_script_executable "$script"; then
            ((failed_tests++))
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
        if ! test_dockerfile_exists "$dockerfile"; then
            ((failed_tests++))
        fi
    done
    
    # Test that welcome art exists
    if ! test_welcome_art_exists; then
        ((failed_tests++))
    fi
    
    # Test help commands
    for script in "${scripts[@]}"; do
        if ! test_help_commands "$script"; then
            ((failed_tests++))
        fi
    done
    
    if [[ $failed_tests -eq 0 ]]; then
        log_success "All unit tests passed"
        exit 0
    else
        log_error "$failed_tests unit tests failed"
        exit 1
    fi
}

main "$@"
