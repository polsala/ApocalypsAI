#!/bin/bash

# Template validation tests for Nightly Docker DevBox
# Mock rationale: These tests validate template JSON structure without external dependencies

set -euo pipefail

# Colors for test output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TOTAL_TESTS=0

# Test functions
log_test() {
    echo -e "${BLUE}[TEST] $1${NC}"
}

pass_test() {
    echo -e "${GREEN}✓ PASS: $1${NC}"
    ((TESTS_PASSED++))
}

fail_test() {
    echo -e "${RED}✗ FAIL: $1${NC}"
    ((TESTS_FAILED++))
}

# Setup test environment
setup_test_env() {
    TEST_DIR="/tmp/devbox_templates_test_$$"
    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR"
    
    # Copy template files
    cp -r "$SCRIPT_DIR/templates" .
}

# Cleanup test environment
cleanup_test_env() {
    cd -
    rm -rf "$TEST_DIR"
}

# Test template JSON structure
test_template_structure() {
    local template_name="$1"
    local template_file="$TEST_DIR/templates/${template_name}.json"
    
    log_test "Testing template structure for $template_name"
    
    if [ ! -f "$template_file" ]; then
        fail_test "Template file not found: $template_file"
        return 1
    fi
    
    # Test JSON validity
    if ! jq empty "$template_file" 2>/dev/null; then
        fail_test "Invalid JSON in template: $template_file"
        return 1
    fi
    pass_test "JSON syntax is valid"
    
    # Test required fields
    local required_fields=("name" "description" "dockerfile" "base_image")
    for field in "${required_fields[@]}"; do
        if jq -e ".${field}" "$template_file" >/dev/null 2>&1; then
            pass_test "Required field '$field' exists"
        else
            fail_test "Required field '$field' missing"
            return 1
        fi
    done
    
    # Test optional fields
    local optional_fields=("ports" "environment" "startup_command" "dependencies")
    for field in "${optional_fields[@]}"; do
        if jq -e ".${field}" "$template_file" >/dev/null 2>&1; then
            pass_test "Optional field '$field' exists"
        else
            pass_test "Optional field '$field' not present (ok)"
        fi
    done
}

# Test Dockerfile references
test_dockerfile_references() {
    log_test "Testing Dockerfile references"
    
    for template_file in "$TEST_DIR/templates"/*.json; do
        if [ -f "$template_file" ]; then
            local template_name=$(basename "$template_file" .json)
            local dockerfile_name=$(jq -r '.dockerfile' "$template_file")
            local dockerfile_path="$TEST_DIR/templates/$dockerfile_name"
            
            if [ -f "$dockerfile_path" ]; then
                pass_test "Dockerfile reference valid for $template_name"
            else
                fail_test "Dockerfile reference invalid for $template_name: $dockerfile_name"
            fi
        fi
    done
}

# Test environment variable structure
test_environment_variables() {
    log_test "Testing environment variable structure"
    
    for template_file in "$TEST_DIR/templates"/*.json; do
        if [ -f "$template_file" ]; then
            local template_name=$(basename "$template_file" .json)
            
            # Check if environment field exists and is an object
            if jq -e '.environment' "$template_file" >/dev/null 2>&1; then
                if jq -e '.environment | type == "object"' "$template_file" >/dev/null 2>&1; then
                    pass_test "Environment variables structure valid for $template_name"
                else
                    fail_test "Environment variables not an object for $template_name"
                fi
            else
                pass_test "No environment variables for $template_name (ok)"
            fi
        fi
    done
}

# Test port configuration
test_port_configuration() {
    log_test "Testing port configuration"
    
    for template_file in "$TEST_DIR/templates"/*.json; do
        if [ -f "$template_file" ]; then
            local template_name=$(basename "$template_file" .json)
            
            # Check if ports field exists and is an array
            if jq -e '.ports' "$template_file" >/dev/null 2>&1; then
                if jq -e '.ports | type == "array"' "$template_file" >/dev/null 2>&1; then
                    local port_count=$(jq '.ports | length' "$template_file")
                    if [ "$port_count" -gt 0 ]; then
                        pass_test "Port configuration valid for $template_name ($port_count ports)"
                    else
                        fail_test "Port array is empty for $template_name"
                    fi
                else
                    fail_test "Ports not an array for $template_name"
                fi
            else
                pass_test "No ports configured for $template_name (ok)"
            fi
        fi
    done
}

# Test dependencies field
test_dependencies_field() {
    log_test "Testing dependencies field"
    
    for template_file in "$TEST_DIR/templates"/*.json; do
        if [ -f "$template_file" ]; then
            local template_name=$(basename "$template_file" .json)
            
            # Check if dependencies field exists and is an array
            if jq -e '.dependencies' "$template_file" >/dev/null 2>&1; then
                if jq -e '.dependencies | type == "array"' "$template_file" >/dev/null 2>&1; then
                    local dep_count=$(jq '.dependencies | length' "$template_file")
                    if [ "$dep_count" -gt 0 ]; then
                        pass_test "Dependencies field valid for $template_name ($dep_count dependencies)"
                    else
                        fail_test "Dependencies array is empty for $template_name"
                    fi
                else
                    fail_test "Dependencies not an array for $template_name"
                fi
            else
                pass_test "No dependencies field for $template_name (ok)"
            fi
        fi
    done
}

# Run all tests
run_tests() {
    echo -e "${CYAN}Running Template Validation Test Suite${NC}"
    echo "======================================="
    
    setup_test_env
    
    # Test each template
    test_template_structure "python"
    test_template_structure "nodejs"
    test_template_structure "rust"
    test_template_structure "go"
    
    test_dockerfile_references
    test_environment_variables
    test_port_configuration
    test_dependencies_field
    
    cleanup_test_env
    
    # Print results
    echo
    echo "========================================="
    echo -e "${GREEN}Tests passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Tests failed: $TESTS_FAILED${NC}"
    echo -e "${BLUE}Total tests: $((TESTS_PASSED + TESTS_FAILED))${NC}"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "\n${GREEN}🎉 All template tests passed!${NC}"
        return 0
    else
        echo -e "\n${RED}❌ Some template tests failed!${NC}"
        return 1
    fi
}

# Run tests if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_tests
fi
