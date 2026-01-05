#!/bin/bash

# Test suite for quickstart-generator.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test directory
TEST_DIR="/tmp/quickstart-test"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GENERATOR_SCRIPT="$SCRIPT_DIR/src/quickstart-generator.sh"

# Logging functions
log_info() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Setup test environment
setup() {
    log_info "Setting up test environment..."
    rm -rf "$TEST_DIR"
    mkdir -p "$TEST_DIR/templates"
    mkdir -p "$TEST_DIR/expected"
    mkdir -p "$TEST_DIR/output"
}

# Cleanup test environment
cleanup() {
    log_info "Cleaning up test environment..."
    rm -rf "$TEST_DIR"
}

# Create test template
create_test_template() {
    local template_file="$1"
    cat > "$template_file" << 'EOF'
# {{PROJECT_NAME}} Quickstart

Welcome to {{PROJECT_NAME}}!

## Installation

{{INSTALL_COMMAND}}

## Usage

{{START_COMMAND}}

## Configuration

Set these environment variables:

- API_KEY={{API_KEY}}
- DEBUG={{DEBUG_MODE}}
EOF
}

# Create test values JSON
create_test_values() {
    local values_file="$1"
    cat > "$values_file" << 'EOF'
{
  "PROJECT_NAME": "Test Project",
  "INSTALL_COMMAND": "npm install",
  "START_COMMAND": "npm start",
  "API_KEY": "test-123",
  "DEBUG_MODE": "true"
}
EOF
}

# Run test and check output
run_test() {
    local test_name="$1"
    local template_file="$2"
    local output_file="$3"
    local expected_file="$4"
    local additional_args="$5"

    log_info "Running test: $test_name"

    # Run generator
    if $GENERATOR_SCRIPT --template "$template_file" --output "$output_file" $additional_args; then
        log_success "Generator executed successfully"
    else
        log_error "Generator failed to execute"
        return 1
    fi

    # Check if output file exists
    if [[ ! -f "$output_file" ]]; then
        log_error "Output file not created: $output_file"
        return 1
    fi

    # Check if expected file exists
    if [[ ! -f "$expected_file" ]]; then
        log_error "Expected file not found: $expected_file"
        return 1
    fi

    # Compare files
    if diff -q "$output_file" "$expected_file" >/dev/null 2>&1; then
        log_success "Output matches expected result"
        return 0
    else
        log_error "Output does not match expected result"
        log_info "Differences:"
        diff "$output_file" "$expected_file" || true
        return 1
    fi
}

# Test 1: Basic template processing
test_basic_template() {
    log_info "=== Test 1: Basic Template Processing ==="

    local template="$TEST_DIR/templates/basic.md"
    local output="$TEST_DIR/output/basic_output.md"
    local expected="$TEST_DIR/expected/basic_expected.md"
    local values="$TEST_DIR/values.json"

    # Create test files
    create_test_template "$template"
    create_test_values "$values"

    # Create expected output
    cat > "$expected" << 'EOF'
# Test Project Quickstart

Welcome to Test Project!

## Installation

npm install

## Usage

npm start

## Configuration

Set these environment variables:

- API_KEY=test-123
- DEBUG=true
EOF

    # Run test
    run_test "Basic template processing" "$template" "$output" "$expected" "--values $values"
}

# Test 2: Template with missing values
test_missing_values() {
    log_info "=== Test 2: Template with Missing Values ==="

    local template="$TEST_DIR/templates/missing.md"
    local output="$TEST_DIR/output/missing_output.md"
    local expected="$TEST_DIR/expected/missing_expected.md"

    # Create test template with extra placeholders
    cat > "$template" << 'EOF'
# {{PROJECT_NAME}} Quickstart

{{MISSING_PLACEHOLDER}}

{{ANOTHER_MISSING}}
EOF

    # Create expected output (placeholders should remain)
    cat > "$expected" << 'EOF'
# {{PROJECT_NAME}} Quickstart

{{MISSING_PLACEHOLDER}}

{{ANOTHER_MISSING}}
EOF

    # Run test
    run_test "Missing values handling" "$template" "$output" "$expected" ""
}

# Test 3: Batch processing
test_batch_processing() {
    log_info "=== Test 3: Batch Processing ==="

    local batch_dir="$TEST_DIR/templates"
    local output_dir="$TEST_DIR/output/batch"

    # Create multiple test templates
    create_test_template "$TEST_DIR/templates/template1.md"
    create_test_template "$TEST_DIR/templates/template2.txt"
    create_test_template "$TEST_DIR/templates/template3.template"

    # Create values file
    create_test_values "$TEST_DIR/values.json"

    # Run batch processing
    log_info "Running batch processing..."
    if $GENERATOR_SCRIPT --batch "$batch_dir" --output-dir "$output_dir" --values "$TEST_DIR/values.json"; then
        log_success "Batch processing completed successfully"
    else
        log_error "Batch processing failed"
        return 1
    fi

    # Check if output files were created
    local count=0
    for file in "$output_dir"/*.md; do
        if [[ -f "$file" ]]; then
            count=$((count + 1))
            log_success "Created batch output: $(basename "$file")"
        fi
    done

    if [[ $count -eq 3 ]]; then
        log_success "All batch files processed correctly"
        return 0
    else
        log_error "Expected 3 output files, got $count"
        return 1
    fi
}

# Test 4: Help functionality
test_help() {
    log_info "=== Test 4: Help Functionality ==="

    log_info "Testing help output..."
    if $GENERATOR_SCRIPT --help >/dev/null 2>&1; then
        log_success "Help command executed successfully"
    else
        log_error "Help command failed"
        return 1
    fi
}

# Test 5: Error handling
test_error_handling() {
    log_info "=== Test 5: Error Handling ==="

    # Test with non-existent template
    log_info "Testing with non-existent template..."
    if $GENERATOR_SCRIPT --template "/non/existent/file.md" --output "/tmp/test.md" 2>/dev/null; then
        log_error "Should have failed with non-existent template"
        return 1
    else
        log_success "Correctly failed with non-existent template"
    fi

    # Test with missing jq dependency (simulate by temporarily renaming jq)
    if command -v jq >/dev/null 2>&1; then
        local jq_path=$(which jq)
        sudo mv "$jq_path" "$jq_path.bak" 2>/dev/null || true
        if ! $GENERATOR_SCRIPT --template "/tmp/test.md" --output "/tmp/test.md" 2>/dev/null; then
            log_success "Correctly failed when jq is missing"
        else
            log_error "Should have failed when jq is missing"
            return 1
        fi
        sudo mv "$jq_path.bak" "$jq_path" 2>/dev/null || true
    else
        log_warning "jq not installed, skipping jq dependency test"
    fi
}

# Run all tests
run_all_tests() {
    local passed=0
    local failed=0

    log_info "Starting test suite..."

    # Test 1
    if test_basic_template; then
        passed=$((passed + 1))
    else
        failed=$((failed + 1))
    fi

    # Test 2
    if test_missing_values; then
        passed=$((passed + 1))
    else
        failed=$((failed + 1))
    fi

    # Test 3
    if test_batch_processing; then
        passed=$((passed + 1))
    else
        failed=$((failed + 1))
    fi

    # Test 4
    if test_help; then
        passed=$((passed + 1))
    else
        failed=$((failed + 1))
    fi

    # Test 5
    if test_error_handling; then
        passed=$((passed + 1))
    else
        failed=$((failed + 1))
    fi

    log_info "\n=== Test Results ==="
    log_info "Passed: $passed"
    log_info "Failed: $failed"

    if [[ $failed -eq 0 ]]; then
        log_success "All tests passed!"
        return 0
    else
        log_error "Some tests failed!"
        return 1
    fi
}

# Main execution
main() {
    # Check if generator script exists
    if [[ ! -f "$GENERATOR_SCRIPT" ]]; then
        log_error "Generator script not found: $GENERATOR_SCRIPT"
        exit 1
    fi

    # Setup
    setup

    # Run tests
    local result=0
    if ! run_all_tests; then
        result=1
    fi

    # Cleanup
    cleanup

    exit $result
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
