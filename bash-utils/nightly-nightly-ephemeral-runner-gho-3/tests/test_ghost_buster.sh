#!/bin/bash

# Test suite for ghost_buster.sh
# Mock rationale: These tests verify the script's logic without making actual cloud API calls

set -euo pipefail

# Source the script functions for testing (without executing main)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/../src/ghost_buster.sh"

# Mock functions to avoid actual cloud calls
mock_aws_cli() {
    echo "Mock AWS CLI available"
}

mock_az_cli() {
    echo "Mock Azure CLI available"
}

mock_gcloud() {
    echo "Mock GCP CLI available"
}

mock_jq() {
    echo "Mock jq available"
}

# Test age conversion
test_age_to_seconds() {
    log_info "Testing age_to_seconds function..."
    
    # Test hours
    local result
    result=$(age_to_seconds "1h")
    [[ $result -eq 3600 ]] && log_success "1h -> 3600 seconds" || { log_error "1h conversion failed"; return 1; }
    
    # Test minutes
    result=$(age_to_seconds "30m")
    [[ $result -eq 1800 ]] && log_success "30m -> 1800 seconds" || { log_error "30m conversion failed"; return 1; }
    
    # Test days
    result=$(age_to_seconds "1d")
    [[ $result -eq 86400 ]] && log_success "1d -> 86400 seconds" || { log_error "1d conversion failed"; return 1; }
    
    log_success "age_to_seconds tests passed"
}

# Test age validation
test_validate_age() {
    log_info "Testing age validation..."
    
    # Valid formats
    validate_age "1h" && log_success "Valid age format: 1h" || { log_error "1h validation failed"; return 1; }
    validate_age "30m" && log_success "Valid age format: 30m" || { log_error "30m validation failed"; return 1; }
    validate_age "2d" && log_success "Valid age format: 2d" || { log_error "2d validation failed"; return 1; }
    
    # Invalid formats
    if validate_age "invalid" 2>/dev/null; then
        log_error "Invalid age format was accepted"
        return 1
    else
        log_success "Invalid age format correctly rejected"
    fi
    
    log_success "age validation tests passed"
}

# Test instance expiration logic
test_is_instance_expired() {
    log_info "Testing instance expiration logic..."
    
    # Mock current time (for testing)
    local current_time=1000000
    local old_time=900000  # 100000 seconds old
    local recent_time=999000  # 1000 seconds old
    
    # Test with 1 hour threshold (3600 seconds)
    local age_seconds=3600
    
    # Old instance should be expired
    if is_instance_expired "$(date -d @$old_time -u +%Y-%m-%dT%H:%M:%SZ)" "$age_seconds"; then
        log_success "Old instance correctly identified as expired"
    else
        log_error "Old instance not identified as expired"
        return 1
    fi
    
    # Recent instance should not be expired
    if is_instance_expired "$(date -d @$recent_time -u +%Y-%m-%dT%H:%M:%SZ)" "$age_seconds"; then
        log_error "Recent instance incorrectly identified as expired"
        return 1
    else
        log_success "Recent instance correctly identified as not expired"
    fi
    
    log_success "instance expiration tests passed"
}

# Test argument parsing
test_parse_args() {
    log_info "Testing argument parsing..."
    
    # Reset globals
    DRY_RUN=false
    AGE_THRESHOLD="2h"
    PROVIDERS="aws,azure,gcp"
    
    # Test dry run
    parse_args --dry-run
    [[ "$DRY_RUN" == "true" ]] && log_success "Dry run flag parsed correctly" || { log_error "Dry run flag not set"; return 1; }
    
    # Reset and test age
    DRY_RUN=false
    parse_args --age 1h
    [[ "$AGE_THRESHOLD" == "1h" ]] && log_success "Age threshold parsed correctly" || { log_error "Age threshold not set"; return 1; }
    
    # Reset and test providers
    DRY_RUN=false
    AGE_THRESHOLD="2h"
    parse_args --providers aws,azure
    [[ "$PROVIDERS" == "aws,azure" ]] && log_success "Providers parsed correctly" || { log_error "Providers not set"; return 1; }
    
    log_success "argument parsing tests passed"
}

# Test help function
test_show_help() {
    log_info "Testing help function..."
    
    # Capture help output
    local help_output
    help_output=$(show_help 2>&1)
    
    if [[ -n "$help_output" ]] && grep -q "Usage:" <<< "$help_output"; then
        log_success "Help function works correctly"
    else
        log_error "Help function failed"
        return 1
    fi
}

# Test dependency checking with mocks
test_check_dependencies() {
    log_info "Testing dependency checking..."
    
    # Mock the command -v checks
    command() {
        case "$2" in
            aws) return 0 ;;
            az) return 0 ;;
            gcloud) return 0 ;;
            jq) return 0 ;;
            *) return 1 ;;
        esac
    }
    
    # This should succeed with our mocks
    if check_dependencies 2>/dev/null; then
        log_success "Dependency check passed with mocked tools"
    else
        log_error "Dependency check failed"
        return 1
    fi
}

# Run all tests
run_tests() {
    log_info "=== Running Ghost Buster Tests ==="
    
    # Source the script to get access to functions
    # We need to extract just the function definitions
    grep -E "^function |^age_to_seconds|^validate_age|^is_instance_expired|^parse_args|^show_help|^check_dependencies" "$SCRIPT_PATH" > /tmp/test_functions.sh
    source /tmp/test_functions.sh
    
    local test_count=0
    local pass_count=0
    
    # Run each test
    for test in test_age_to_seconds test_validate_age test_is_instance_expired test_parse_args test_show_help test_check_dependencies; do
        ((test_count++))
        log_info "Running $test..."
        if $test; then
            ((pass_count++))
        else
            log_error "$test failed!"
        fi
    done
    
    # Cleanup
    rm -f /tmp/test_functions.sh
    
    log_info "=== Test Results ==="
    log_info "Passed: $pass_count/$test_count"
    
    if [[ $pass_count -eq $test_count ]]; then
        log_success "All tests passed!"
        return 0
    else
        log_error "Some tests failed!"
        return 1
    fi
}

# Entry point for tests
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_tests
fi
