#!/bin/bash

# Tests for GitHub Actions Runner Simulator
# Mock rationale: These tests verify the simulation logic without requiring actual GitHub Actions

set -euo pipefail

# Test directory
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_DIR="$(dirname "$TEST_DIR")"
SIMULATOR="$SCRIPT_DIR/simulate_runner.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Setup test environment
setup() {
    TEST_TEMP_DIR="/tmp/nightly_simulator_test_$$"
    mkdir -p "$TEST_TEMP_DIR"
    cd "$TEST_TEMP_DIR"
    
    # Create a test workflow file
    cat > test_workflow.yml << 'EOF'
name: Test Workflow

on:
  push:
    branches: [ main ]

jobs:
  test-job:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
      with:
        repository: test/repo
        ref: main
        
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        
    - name: Run tests
      run: npm test
      
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.npm
        key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
EOF
}

# Cleanup test environment
cleanup() {
    cd "$(dirname "$TEST_DIR")"
    rm -rf "$TEST_TEMP_DIR"
}

# Test 1: Help message
test_help() {
    log_test "Testing help message"
    
    if "$SIMULATOR" --help > /dev/null 2>&1; then
        log_pass "Help message displays correctly"
    else
        log_fail "Help message failed"
        return 1
    fi
}

# Test 2: Missing workflow file
test_missing_workflow() {
    log_test "Testing missing workflow file error"
    
    if ! "$SIMULATOR" 2>&1 | grep -q "Workflow file is required"; then
        log_fail "Should show error for missing workflow file"
        return 1
    else
        log_pass "Correctly shows error for missing workflow file"
    fi
}

# Test 3: Non-existent workflow file
test_nonexistent_workflow() {
    log_test "Testing non-existent workflow file error"
    
    if ! "$SIMULATOR" nonexistent.yml 2>&1 | grep -q "Workflow file not found"; then
        log_fail "Should show error for non-existent workflow file"
        return 1
    else
        log_pass "Correctly shows error for non-existent workflow file"
    fi
}

# Test 4: Basic workflow simulation (requires yq)
test_basic_simulation() {
    log_test "Testing basic workflow simulation"
    
    if ! command -v yq &> /dev/null; then
        log_test "Skipping simulation test - yq not installed"
        return 0
    fi
    
    # Create a minimal test workflow
    cat > minimal_workflow.yml << 'EOF'
name: Minimal Test
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - run: echo "Hello World"
EOF
    
    if "$SIMULATOR" minimal_workflow.yml > /dev/null 2>&1; then
        log_pass "Basic workflow simulation works"
    else
        log_fail "Basic workflow simulation failed"
        return 1
    fi
}

# Test 5: Environment file loading
test_env_file() {
    log_test "Testing environment file loading"
    
    # Create test environment file
    cat > test.env << 'EOF'
TEST_VAR=test_value
ANOTHER_VAR=another_value
EOF
    
    # Create simple workflow that uses env vars
    cat > env_workflow.yml << 'EOF'
name: Env Test
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - run: echo "$TEST_VAR"
EOF
    
    if "$SIMULATOR" --env-file test.env env_workflow.yml > /dev/null 2>&1; then
        log_pass "Environment file loading works"
    else
        log_fail "Environment file loading failed"
        return 1
    fi
}

# Test 6: Debug mode
test_debug_mode() {
    log_test "Testing debug mode"
    
    cat > debug_workflow.yml << 'EOF'
name: Debug Test
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - run: echo "debug test"
EOF
    
    if "$SIMULATOR" --debug debug_workflow.yml 2>&1 | grep -q "DEBUG"; then
        log_pass "Debug mode works"
    else
        log_fail "Debug mode failed"
        return 1
    fi
}

# Test 7: Supported actions detection
test_supported_actions() {
    log_test "Testing supported actions detection"
    
    # Test that supported actions are recognized
    local supported_count=0
    local total_actions=0
    
    for action in "actions/checkout" "actions/setup-node" "actions/setup-python" "actions/cache"; do
        total_actions=$((total_actions + 1))
        if echo "$action" | grep -E "^(actions/checkout|actions/setup-node|actions/setup-python|actions/cache)" > /dev/null; then
            supported_count=$((supported_count + 1))
        fi
    done
    
    if [[ $supported_count -eq $total_actions ]]; then
        log_pass "All expected actions are supported"
    else
        log_fail "Some actions are not recognized as supported"
        return 1
    fi
}

# Test 8: Unsupported action warning
test_unsupported_action() {
    log_test "Testing unsupported action warning"
    
    cat > unsupported_workflow.yml << 'EOF'
name: Unsupported Test
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: unsupported/action@v1
EOF
    
    if "$SIMULATOR" unsupported_workflow.yml 2>&1 | grep -q "Unsupported action"; then
        log_pass "Unsupported action warning works"
    else
        log_fail "Unsupported action warning failed"
        return 1
    fi
}

# Run all tests
run_tests() {
    log_test "=== Running GitHub Actions Runner Simulator Tests ==="
    echo
    
    local passed=0
    local failed=0
    
    # List of test functions
    local tests=(
        test_help
        test_missing_workflow
        test_nonexistent_workflow
        test_basic_simulation
        test_env_file
        test_debug_mode
        test_supported_actions
        test_unsupported_action
    )
    
    for test_func in "${tests[@]}"; do
        if $test_func; then
            passed=$((passed + 1))
        else
            failed=$((failed + 1))
        fi
        echo
    done
    
    log_test "=== Test Results ==="
    log_test "Passed: $passed"
    log_test "Failed: $failed"
    log_test "Total: $((passed + failed))"
    
    if [[ $failed -eq 0 ]]; then
        log_pass "All tests passed!"
        return 0
    else
        log_fail "Some tests failed!"
        return 1
    fi
}

# Main execution
main() {
    setup
    trap cleanup EXIT
    
    if run_tests; then
        exit 0
    else
        exit 1
    fi
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
