#!/bin/bash

# Test suite for Nightly Chaos Config Validator
# Mock rationale: Tests validate functionality without external dependencies

set -euo pipefail

# Colors for test output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'
BOLD='\033[1m'

# Test directory
TEST_DIR=$(mktemp -d)
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
VALIDATOR="$SCRIPT_DIR/src/main.sh"

# Cleanup function
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Test helpers
log_test() {
    echo -e "${BLUE}[TEST]${NC} $*"
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $*"
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $*"
}

# Create test files
create_test_files() {
    log_test "Creating test files..."
    
    # Test JSON - Good configuration
    cat > "$TEST_DIR/good-config.json" << 'EOF'
{
  "services": {
    "database": [
      {"host": "db1.example.com", "port": 5432},
      {"host": "db2.example.com", "port": 5432},
      {"host": "db3.example.com", "port": 5432}
    ],
    "api": [
      {"host": "api1.example.com", "port": 8080},
      {"host": "api2.example.com", "port": 8080}
    ],
    "web": {
      "circuit_breaker": true,
      "timeout": 5000,
      "retries": 3,
      "health_check": "/health",
      "load_balancer": true
    }
  }
}
EOF
    
    # Test JSON - Bad configuration
    cat > "$TEST_DIR/bad-config.json" << 'EOF'
{
  "services": {
    "database": {
      "host": "single-db.example.com",
      "port": 5432
    },
    "web": {
      "timeout": 100
    }
  }
}
EOF
    
    # Test YAML - Good configuration
    cat > "$TEST_DIR/good-config.yaml" << 'EOF'
---
services:
  database:
    - host: db1.example.com
      port: 5432
    - host: db2.example.com
      port: 5432
    - host: db3.example.com
      port: 5432
  api:
    - host: api1.example.com
      port: 8080
    - host: api2.example.com
      port: 8080
  web:
    circuit_breaker: true
    timeout: 5000
    retries: 3
    health_check: /health
    load_balancer: true
EOF
    
    # Test YAML - Bad configuration
    cat > "$TEST_DIR/bad-config.yaml" << 'EOF'
---
services:
  database:
    host: single-db.example.com
    port: 5432
  web:
    timeout: 100
EOF
    
    # Test INI - Good configuration
    cat > "$TEST_DIR/good-config.ini" << 'EOF'
[database]
host1=db1.example.com
host2=db2.example.com
host3=db3.example.com
port=5432

[api]
host1=api1.example.com
host2=api2.example.com
port=8080

[web]
circuit_breaker=true
timeout=5000
retries=3
health_check=/health
load_balancer=true
EOF
    
    # Test INI - Bad configuration
    cat > "$TEST_DIR/bad-config.ini" << 'EOF'
[database]
host=single-db.example.com
port=5432

[web]
timeout=100
EOF
    
    # Test invalid JSON
    cat > "$TEST_DIR/invalid.json" << 'EOF'
{
  "invalid": json content
}
EOF
    
    # Test invalid YAML
    cat > "$TEST_DIR/invalid.yaml" << 'EOF'
---
invalid: yaml content:
  - broken
    syntax
EOF
}

# Test functions
test_help() {
    log_test "Testing help option..."
    
    if $VALIDATOR --help > /dev/null 2>&1; then
        log_pass "Help option works"
    else
        log_fail "Help option failed"
        return 1
    fi
}

test_verbose() {
    log_test "Testing verbose option..."
    
    if $VALIDATOR --verbose "$TEST_DIR/good-config.json" > /dev/null 2>&1; then
        log_pass "Verbose option works"
    else
        log_fail "Verbose option failed"
        return 1
    fi
}

test_json_good() {
    log_test "Testing good JSON configuration..."
    
    local output
    output=$($VALIDATOR "$TEST_DIR/good-config.json" 2>&1)
    local score
    score=$(echo "$output" | grep "Resilience Score:" | sed 's/.*: \([0-9]*\)\/100/\1/')
    
    if [[ $score -ge 80 ]]; then
        log_pass "Good JSON config scored $score/100"
    else
        log_fail "Good JSON config scored only $score/100"
        echo "$output"
        return 1
    fi
}

test_json_bad() {
    log_test "Testing bad JSON configuration..."
    
    local output
    output=$($VALIDATOR "$TEST_DIR/bad-config.json" 2>&1)
    local score
    score=$(echo "$output" | grep "Resilience Score:" | sed 's/.*: \([0-9]*\)\/100/\1/')
    
    if [[ $score -lt 60 ]]; then
        log_pass "Bad JSON config scored $score/100 (as expected)"
    else
        log_fail "Bad JSON config scored $score/100 (should be lower)"
        echo "$output"
        return 1
    fi
}

test_yaml_good() {
    log_test "Testing good YAML configuration..."
    
    local output
    output=$($VALIDATOR "$TEST_DIR/good-config.yaml" 2>&1)
    local score
    score=$(echo "$output" | grep "Resilience Score:" | sed 's/.*: \([0-9]*\)\/100/\1/')
    
    if [[ $score -ge 80 ]]; then
        log_pass "Good YAML config scored $score/100"
    else
        log_fail "Good YAML config scored only $score/100"
        echo "$output"
        return 1
    fi
}

test_yaml_bad() {
    log_test "Testing bad YAML configuration..."
    
    local output
    output=$($VALIDATOR "$TEST_DIR/bad-config.yaml" 2>&1)
    local score
    score=$(echo "$output" | grep "Resilience Score:" | sed 's/.*: \([0-9]*\)\/100/\1/')
    
    if [[ $score -lt 60 ]]; then
        log_pass "Bad YAML config scored $score/100 (as expected)"
    else
        log_fail "Bad YAML config scored $score/100 (should be lower)"
        echo "$output"
        return 1
    fi
}

test_ini_good() {
    log_test "Testing good INI configuration..."
    
    local output
    output=$($VALIDATOR "$TEST_DIR/good-config.ini" 2>&1)
    local score
    score=$(echo "$output" | grep "Resilience Score:" | sed 's/.*: \([0-9]*\)\/100/\1/')
    
    if [[ $score -ge 80 ]]; then
        log_pass "Good INI config scored $score/100"
    else
        log_fail "Good INI config scored only $score/100"
        echo "$output"
        return 1
    fi
}

test_ini_bad() {
    log_test "Testing bad INI configuration..."
    
    local output
    output=$($VALIDATOR "$TEST_DIR/bad-config.ini" 2>&1)
    local score
    score=$(echo "$output" | grep "Resilience Score:" | sed 's/.*: \([0-9]*\)\/100/\1/')
    
    if [[ $score -lt 60 ]]; then
        log_pass "Bad INI config scored $score/100 (as expected)"
    else
        log_fail "Bad INI config scored $score/100 (should be lower)"
        echo "$output"
        return 1
    fi
}

test_invalid_json() {
    log_test "Testing invalid JSON file..."
    
    if $VALIDATOR "$TEST_DIR/invalid.json" > /dev/null 2>&1; then
        log_fail "Invalid JSON should have failed validation"
        return 1
    else
        log_pass "Invalid JSON correctly rejected"
    fi
}

test_invalid_yaml() {
    log_test "Testing invalid YAML file..."
    
    if $VALIDATOR "$TEST_DIR/invalid.yaml" > /dev/null 2>&1; then
        log_fail "Invalid YAML should have failed validation"
        return 1
    else
        log_pass "Invalid YAML correctly rejected"
    fi
}

test_nonexistent_file() {
    log_test "Testing nonexistent file..."
    
    local nonexistent_file="$TEST_DIR/does-not-exist.json"
    
    if $VALIDATOR "$nonexistent_file" > /dev/null 2>&1; then
        log_fail "Nonexistent file should have failed validation"
        return 1
    else
        log_pass "Nonexistent file correctly rejected"
    fi
}

test_unsupported_format() {
    log_test "Testing unsupported file format..."
    
    # Create a text file
    echo "This is not a supported config format" > "$TEST_DIR/test.txt"
    
    if $VALIDATOR "$TEST_DIR/test.txt" > /dev/null 2>&1; then
        log_fail "Unsupported format should have failed validation"
        return 1
    else
        log_pass "Unsupported format correctly rejected"
    fi
}

test_multiple_files() {
    log_test "Testing multiple files..."
    
    local output
    output=$($VALIDATOR "$TEST_DIR/good-config.json" "$TEST_DIR/bad-config.json" 2>&1)
    
    if echo "$output" | grep -q "good-config.json" && echo "$output" | grep -q "bad-config.json"; then
        log_pass "Multiple files processed correctly"
    else
        log_fail "Multiple files not processed correctly"
        echo "$output"
        return 1
    fi
}

test_missing_dependencies() {
    log_test "Testing missing jq dependency..."
    
    # Temporarily rename jq if it exists
    local jq_path=""
    if command -v jq &> /dev/null; then
        jq_path=$(which jq)
        sudo mv "$jq_path" "$jq_path.backup"
        
        if ! $VALIDATOR "$TEST_DIR/good-config.json" > /dev/null 2>&1; then
            log_pass "Missing jq dependency correctly detected"
        else
            log_fail "Missing jq dependency not detected"
            return 1
        fi
        
        # Restore jq
        sudo mv "$jq_path.backup" "$jq_path"
    else
        log_test "jq not installed, skipping dependency test"
    fi
}

# Run all tests
run_tests() {
    log_test "Starting test suite..."
    echo
    
    local tests=(
        test_help
        test_verbose
        test_json_good
        test_json_bad
        test_yaml_good
        test_yaml_bad
        test_ini_good
        test_ini_bad
        test_invalid_json
        test_invalid_yaml
        test_nonexistent_file
        test_unsupported_format
        test_multiple_files
        test_missing_dependencies
    )
    
    local passed=0
    local failed=0
    
    for test in "${tests[@]}"; do
        if $test; then
            ((passed++))
        else
            ((failed++))
        fi
        echo
    done
    
    echo -e "${BOLD}Test Results:${NC}"
    echo -e "${GREEN}Passed: $passed${NC}"
    echo -e "${RED}Failed: $failed${NC}"
    
    if [[ $failed -eq 0 ]]; then
        echo -e "${GREEN}All tests passed! 🎉${NC}"
        return 0
    else
        echo -e "${RED}Some tests failed! 🚨${NC}"
        return 1
    fi
}

# Main execution
main() {
    # Check if validator script exists
    if [[ ! -f "$VALIDATOR" ]]; then
        echo -e "${RED}Validator script not found: $VALIDATOR${NC}"
        exit 1
    fi
    
    # Make script executable
    chmod +x "$VALIDATOR"
    
    # Create test files
    create_test_files
    
    # Run tests
    run_tests
}

# Run main function
main "$@"
