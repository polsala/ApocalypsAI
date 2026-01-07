#!/bin/bash

# Test suite for quickstart-generator.sh
# Mock rationale: Tests verify template generation, argument parsing, and error handling

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Function to print colored output
print_info() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

print_failure() {
    echo -e "${RED}[FAIL]${NC} $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Setup test environment
setup() {
    TEST_DIR="/tmp/quickstart_test_$$"
    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR"
    
    # Copy script to test directory
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    cp "$SCRIPT_DIR/src/quickstart-generator.sh" .
    chmod +x quickstart-generator.sh
    
    print_info "Test directory: $TEST_DIR"
}

# Cleanup test environment
cleanup() {
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
    fi
}

# Run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    print_info "Running: $test_name"
    
    if eval "$test_command" >/dev/null 2>&1; then
        print_success "$test_name"
    else
        print_failure "$test_name"
        return 1
    fi
}

# Test 1: Help message
test_help() {
    ./quickstart-generator.sh --help
}

# Test 2: List templates
test_list_templates() {
    ./quickstart-generator.sh --list-templates
}

# Test 3: Generate web project
test_generate_web() {
    ./quickstart-generator.sh --type web --project "Test Web Project" --output test_web.md
    [[ -f "test_web.md" ]] && grep -q "Test Web Project" test_web.md
}

# Test 4: Generate CLI project
test_generate_cli() {
    ./quickstart-generator.sh --type cli --project "Test CLI Project" --output test_cli.md
    [[ -f "test_cli.md" ]] && grep -q "Test CLI Project" test_cli.md
}

# Test 5: Generate library project
test_generate_library() {
    ./quickstart-generator.sh --type library --project "Test Library Project" --output test_library.md
    [[ -f "test_library.md" ]] && grep -q "Test Library Project" test_library.md
}

# Test 6: Generate API project
test_generate_api() {
    ./quickstart-generator.sh --type api --project "Test API Project" --output test_api.md
    [[ -f "test_api.md" ]] && grep -q "Test API Project" test_api.md
}

# Test 7: Generate mobile project
test_generate_mobile() {
    ./quickstart-generator.sh --type mobile --project "Test Mobile Project" --output test_mobile.md
    [[ -f "test_mobile.md" ]] && grep -q "Test Mobile Project" test_mobile.md
}

# Test 8: Custom template
test_custom_template() {
    # Create a custom template
    cat > custom.tpl << 'EOF'
# Custom Template

This is a custom template for {{PROJECT_NAME}}.
Author: {{AUTHOR}}
License: {{LICENSE}}
EOF
    
    ./quickstart-generator.sh --template custom.tpl --project "Custom Project" --output test_custom.md
    [[ -f "test_custom.md" ]] && grep -q "Custom Project" test_custom.md
}

# Test 9: Environment variables
test_environment_variables() {
    QUICKSTART_AUTHOR="Test Author" \
    QUICKSTART_EMAIL="test@example.com" \
    QUICKSTART_LICENSE="Apache 2.0" \
    QUICKSTART_VERSION="2.0.0" \
    ./quickstart-generator.sh --type web --project "Env Test Project" --output test_env.md
    
    [[ -f "test_env.md" ]] && \
    grep -q "Test Author" test_env.md && \
    grep -q "test@example.com" test_env.md && \
    grep -q "Apache 2.0" test_env.md
}

# Test 10: Verbose output
test_verbose() {
    ./quickstart-generator.sh --verbose --type web --project "Verbose Test" --output test_verbose.md
    [[ -f "test_verbose.md" ]] && grep -q "Verbose Test" test_verbose.md
}

# Test 11: Missing project name
test_missing_project_name() {
    ! ./quickstart-generator.sh --type web 2>/dev/null
}

# Test 12: Invalid project type
test_invalid_type() {
    ! ./quickstart-generator.sh --type invalid --project "Test" 2>/dev/null
}

# Test 13: Non-existent custom template
test_nonexistent_template() {
    ! ./quickstart-generator.sh --template nonexistent.tpl --project "Test" 2>/dev/null
}

# Test 14: Template content verification
test_template_content() {
    ./quickstart-generator.sh --type web --project "Content Test" --output test_content.md
    
    # Check that all placeholders are replaced
    ! grep -q "{{PROJECT_NAME}}" test_content.md && \
    ! grep -q "{{AUTHOR}}" test_content.md && \
    ! grep -q "{{EMAIL}}" test_content.md && \
    ! grep -q "{{LICENSE}}" test_content.md
}

# Test 15: Multiple runs don't conflict
test_multiple_runs() {
    ./quickstart-generator.sh --type web --project "First Project" --output first.md
    ./quickstart-generator.sh --type cli --project "Second Project" --output second.md
    
    [[ -f "first.md" ]] && [[ -f "second.md" ]] && \
    grep -q "First Project" first.md && \
    grep -q "Second Project" second.md
}

# Main test execution
main() {
    print_info "Starting quickstart-generator.sh test suite"
    print_info "========================================="
    
    # Setup
    setup
    
    # Trap cleanup on exit
    trap cleanup EXIT
    
    # Run tests
    run_test "Help message" "test_help"
    run_test "List templates" "test_list_templates"
    run_test "Generate web project" "test_generate_web"
    run_test "Generate CLI project" "test_generate_cli"
    run_test "Generate library project" "test_generate_library"
    run_test "Generate API project" "test_generate_api"
    run_test "Generate mobile project" "test_generate_mobile"
    run_test "Custom template" "test_custom_template"
    run_test "Environment variables" "test_environment_variables"
    run_test "Verbose output" "test_verbose"
    run_test "Missing project name" "test_missing_project_name"
    run_test "Invalid project type" "test_invalid_type"
    run_test "Non-existent custom template" "test_nonexistent_template"
    run_test "Template content verification" "test_template_content"
    run_test "Multiple runs don't conflict" "test_multiple_runs"
    
    # Print results
    echo
    print_info "========================================="
    print_info "Test Results:"
    print_info "Passed: $TESTS_PASSED"
    print_info "Failed: $TESTS_FAILED"
    print_info "Total:  $((TESTS_PASSED + TESTS_FAILED))"
    
    if [[ $TESTS_FAILED -eq 0 ]]; then
        print_success "All tests passed! 🎉"
        exit 0
    else
        print_failure "Some tests failed! 😞"
        exit 1
    fi
}

# Run the test suite
main
