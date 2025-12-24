#!/bin/bash

# Tests for Nightly Ephemeral Runner Orchestrator
# Mock-based tests to ensure functionality without actual API calls

set -euo pipefail

# Mock functions
mock_curl() {
    # Mock GitHub API responses
    case "$2" in
        */registration-token)
            echo '{"token":"mock_token_123","expires_at":"2024-01-01T00:00:00Z"}'
            echo '201'  # HTTP status
            ;;
        */actions/runners)
            if [[ "$1" == "GET" ]]; then
                echo '{"total_count":2,"runners":[{"id":1,"name":"runner-1","status":"online","busy":false},{"id":2,"name":"runner-2","status":"online","busy":true}]}'
                echo '200'
            else
                echo '{}'
                echo '204'
            fi
            ;;
        *)
            echo '{}'
            echo '404'
            ;;
    esac
}

# Mock jq
mock_jq() {
    local filter="$1"
    local input="$2"
    
    case "$filter" in
        '.token')
            echo 'mock_token_123'
            ;;
        '.total_count')
            echo '2'
            ;;
        '.runners[]')
            echo '{"id":1,"name":"runner-1","status":"online","busy":false}'
            echo '{"id":2,"name":"runner-2","status":"online","busy":true}'
            ;;
        '.runners[] | "\(.id)|\(.name)|\(.status)|\(.busy)"')
            echo '1|runner-1|online|false'
            echo '2|runner-2|online|true'
            ;;
        '.runners[] | select(.status == "online" and .busy == false) | .id')
            echo '1'
            ;;
        *)
            echo '{}'
            ;;
    esac
}

# Test setup
setup() {
    # Backup original commands
    command -v curl >/dev/null && alias curl_backup=curl
    command -v jq >/dev/null && alias jq_backup=jq
    
    # Create mocks
    alias curl='mock_curl'
    alias jq='mock_jq'
    
    # Create test log file
    TEST_LOG="/tmp/test_runner_orchestrator.log"
    > "$TEST_LOG"
}

# Test teardown
teardown() {
    # Restore original commands
    unalias curl 2>/dev/null || true
    unalias jq 2>/dev/null || true
    [[ -n "${curl_backup+x}" ]] && alias curl=curl_backup
    [[ -n "${jq_backup+x}" ]] && alias jq=jq_backup
    
    # Clean up test files
    rm -f "$TEST_LOG"
}

# Test helper to check if log contains text
log_contains() {
    local text="$1"
    if grep -q "$text" "$TEST_LOG" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Test provision runner
test_provision_runner() {
    echo "Testing provision_runner..."
    
    # Source the main script functions
    source "$(dirname "$0")/../src/main.sh"
    
    # Call provision_runner
    provision_runner "test_token" "test_org"
    
    # Check if log contains expected messages
    if log_contains "Provisioning runner:" && log_contains "provisioned successfully"; then
        echo "✓ provision_runner test passed"
    else
        echo "✗ provision_runner test failed"
        cat "$TEST_LOG"
        return 1
    fi
}

# Test health check
test_health_check() {
    echo "Testing health_check..."
    
    # Source the main script functions
    source "$(dirname "$0")/../src/main.sh"
    
    # Call health_check
    health_check "test_token" "test_org"
    
    # Check if log contains expected messages
    if log_contains "Performing health check" && log_contains "healthy"; then
        echo "✓ health_check test passed"
    else
        echo "✗ health_check test failed"
        cat "$TEST_LOG"
        return 1
    fi
}

# Test cleanup runners
test_cleanup_runners() {
    echo "Testing cleanup_runners..."
    
    # Source the main script functions
    source "$(dirname "$0")/../src/main.sh"
    
    # Call cleanup_runners
    cleanup_runners "test_token" "test_org"
    
    # Check if log contains expected messages
    if log_contains "Cleaning up idle runners"; then
        echo "✓ cleanup_runners test passed"
    else
        echo "✗ cleanup_runners test failed"
        cat "$TEST_LOG"
        return 1
    fi
}

# Test argument parsing
test_parse_args() {
    echo "Testing argument parsing..."
    
    # Test valid arguments
    if parse_args "provision" "--token" "test_token" "--org" "test_org" >/dev/null 2>&1; then
        echo "✓ Valid arguments test passed"
    else
        echo "✗ Valid arguments test failed"
        return 1
    fi
    
    # Test missing token
    if ! parse_args "provision" "--org" "test_org" >/dev/null 2>&1; then
        echo "✓ Missing token test passed"
    else
        echo "✗ Missing token test failed"
        return 1
    fi
    
    # Test missing org
    if ! parse_args "provision" "--token" "test_token" >/dev/null 2>&1; then
        echo "✓ Missing org test passed"
    else
        echo "✗ Missing org test failed"
        return 1
    fi
}

# Test dependency checking
test_check_deps() {
    echo "Testing dependency checking..."
    
    # Mock missing curl
    unalias curl 2>/dev/null || true
    if ! check_deps >/dev/null 2>&1; then
        echo "✓ Missing curl test passed"
    else
        echo "✗ Missing curl test failed"
        return 1
    fi
    
    # Restore curl
    alias curl='mock_curl'
    
    # Mock missing jq
    unalias jq 2>/dev/null || true
    if ! check_deps >/dev/null 2>&1; then
        echo "✓ Missing jq test passed"
    else
        echo "✗ Missing jq test failed"
        return 1
    fi
    
    # Restore jq
    alias jq='mock_jq'
    
    # Test with all deps
    if check_deps >/dev/null 2>&1; then
        echo "✓ All dependencies test passed"
    else
        echo "✗ All dependencies test failed"
        return 1
    fi
}

# Run all tests
run_tests() {
    echo "Running tests for Nightly Ephemeral Runner Orchestrator..."
    echo
    
    setup
    
    local tests=(
        test_check_deps
        test_parse_args
        test_provision_runner
        test_health_check
        test_cleanup_runners
    )
    
    local failed=0
    
    for test in "${tests[@]}"; do
        if $test; then
            echo
        else
            echo
            failed=1
        fi
    done
    
    teardown
    
    if [[ $failed -eq 0 ]]; then
        echo "All tests passed! ✓"
        return 0
    else
        echo "Some tests failed! ✗"
        return 1
    fi
}

# Run tests if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_tests
fi
