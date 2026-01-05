#!/bin/bash

# Test suite for Nightly Bash Quickstart Generator
# Uses mock fixtures and deterministic testing

set -euo pipefail

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
GENERATOR_SCRIPT="$ROOT_DIR/src/quickstart-generator.sh"

# Test directory
TEST_DIR="/tmp/quickstart-test-$$"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test logging functions
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
  mkdir -p "$TEST_DIR/templates"
  mkdir -p "$TEST_DIR/output"
  mkdir -p "$TEST_DIR/batch-templates"
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
# {{PROJECT_NAME}} Quickstart Guide

Welcome to {{PROJECT_NAME}}! This guide will help you get started quickly.

## Project Information

- **Version**: {{VERSION}}
- **Author**: {{AUTHOR}}
- **Description**: {{DESCRIPTION}}

## Prerequisites

- {{PREREQUISITE_1}}
- {{PREREQUISITE_2}}

## Installation

```bash
{{INSTALL_COMMAND}}
```

## Usage

```bash
{{USAGE_EXAMPLE}}
```

## Support

For support, contact {{SUPPORT_EMAIL}}.
EOF
}

# Create test configuration
create_test_config() {
  local config_file="$1"
  cat > "$config_file" << 'EOF'
{
  "PROJECT_NAME": "Test Project",
  "VERSION": "1.0.0",
  "AUTHOR": "Test Author",
  "DESCRIPTION": "A test project for quickstart generation",
  "INSTALL_COMMAND": "npm install",
  "USAGE_EXAMPLE": "npm start",
  "PREREQUISITE_1": "Node.js 16+",
  "PREREQUISITE_2": "npm 8+",
  "SUPPORT_EMAIL": "test@example.com"
}
EOF
}

# Run test with expected output
run_test() {
  local test_name="$1"
  local expected_output="$2"
  
  log_info "Running test: $test_name"
  
  # Run the generator
  if "$GENERATOR_SCRIPT" "$@"; then
    # Check if output file was created
    if [[ -f "$expected_output" ]]; then
      log_success "Output file created: $expected_output"
      return 0
    else
      log_error "Output file not created: $expected_output"
      return 1
    fi
  else
    log_error "Generator failed"
    return 1
  fi
}

# Test placeholder replacement
test_placeholder_replacement() {
  log_info "Testing placeholder replacement..."
  
  local template_file="$TEST_DIR/templates/test-template.md"
  local output_file="$TEST_DIR/output/test-output.md"
  local config_file="$TEST_DIR/config.json"
  
  # Create test files
  create_test_template "$template_file"
  create_test_config "$config_file"
  
  # Run generator
  if run_test "placeholder_replacement" "$output_file" \
    --template "$template_file" \
    --output "$output_file" \
    --config "$config_file"; then
    
    # Verify content
    if grep -q "Test Project" "$output_file" && \
       grep -q "1.0.0" "$output_file" && \
       grep -q "Test Author" "$output_file" && \
       grep -q "npm install" "$output_file"; then
      log_success "Placeholder replacement test passed"
      return 0
    else
      log_error "Placeholder replacement test failed - content verification failed"
      cat "$output_file"
      return 1
    fi
  else
    log_error "Placeholder replacement test failed - generator failed"
    return 1
  fi
}

# Test command line values override config
test_command_line_override() {
  log_info "Testing command line value override..."
  
  local template_file="$TEST_DIR/templates/override-template.md"
  local output_file="$TEST_DIR/output/override-output.md"
  local config_file="$TEST_DIR/config.json"
  
  # Create test files
  create_test_template "$template_file"
  create_test_config "$config_file"
  
  # Run generator with command line override
  if run_test "command_line_override" "$output_file" \
    --template "$template_file" \
    --output "$output_file" \
    --config "$config_file" \
    --values "PROJECT_NAME=Override Project" \
    "VERSION=2.0.0"; then
    
    # Verify override values
    if grep -q "Override Project" "$output_file" && \
       grep -q "2.0.0" "$output_file" && \
       ! grep -q "Test Project" "$output_file"; then
      log_success "Command line override test passed"
      return 0
    else
      log_error "Command line override test failed - override verification failed"
      cat "$output_file"
      return 1
    fi
  else
    log_error "Command line override test failed - generator failed"
    return 1
  fi
}

# Test batch processing
test_batch_processing() {
  log_info "Testing batch processing..."
  
  local batch_template1="$TEST_DIR/batch-templates/template1.md"
  local batch_template2="$TEST_DIR/batch-templates/template2.md"
  local config_file="$TEST_DIR/config.json"
  
  # Create batch templates
  create_test_template "$batch_template1"
  create_test_template "$batch_template2"
  create_test_config "$config_file"
  
  # Run batch generator
  if run_test "batch_processing" "$TEST_DIR/output" \
    --batch \
    --templates-dir "$TEST_DIR/batch-templates" \
    --output-dir "$TEST_DIR/output" \
    --config "$config_file"; then
    
    # Check if both output files were created
    local output1="$TEST_DIR/output/template1-quickstart.md"
    local output2="$TEST_DIR/output/template2-quickstart.md"
    
    if [[ -f "$output1" ]] && [[ -f "$output2" ]]; then
      log_success "Batch processing test passed"
      return 0
    else
      log_error "Batch processing test failed - output files not created"
      return 1
    fi
  else
    log_error "Batch processing test failed - generator failed"
    return 1
  fi
}

# Test missing template file
test_missing_template() {
  log_info "Testing missing template file..."
  
  local output_file="$TEST_DIR/output/missing-output.md"
  
  # Run generator with non-existent template
  if "$GENERATOR_SCRIPT" \
    --template "/nonexistent/template.md" \
    --output "$output_file" \
    2>/dev/null; then
    log_error "Missing template test failed - generator should have failed"
    return 1
  else
    log_success "Missing template test passed - generator correctly failed"
    return 0
  fi
}

# Test help option
test_help_option() {
  log_info "Testing help option..."
  
  if "$GENERATOR_SCRIPT" --help >/dev/null 2>&1; then
    log_success "Help option test passed"
    return 0
  else
    log_error "Help option test failed"
    return 1
  fi
}

# Test environment variables
test_environment_variables() {
  log_info "Testing environment variables..."
  
  local template_file="$TEST_DIR/templates/env-template.md"
  local output_file="$TEST_DIR/output/env-output.md"
  local config_file="$TEST_DIR/config.json"
  
  # Create test files
  create_test_template "$template_file"
  create_test_config "$config_file"
  
  # Set environment variables
  export QUICKSTART_PROJECT_NAME="Env Project"
  export QUICKSTART_VERSION="3.0.0"
  
  # Run generator
  if run_test "environment_variables" "$output_file" \
    --template "$template_file" \
    --output "$output_file" \
    --config "$config_file"; then
    
    # Verify environment variable values
    if grep -q "Env Project" "$output_file" && \
       grep -q "3.0.0" "$output_file"; then
      log_success "Environment variables test passed"
      return 0
    else
      log_error "Environment variables test failed - env var verification failed"
      cat "$output_file"
      return 1
    fi
  else
    log_error "Environment variables test failed - generator failed"
    return 1
  fi
}

# Test special characters in values
test_special_characters() {
  log_info "Testing special characters in values..."
  
  local template_file="$TEST_DIR/templates/special-template.md"
  local output_file="$TEST_DIR/output/special-output.md"
  local config_file="$TEST_DIR/config.json"
  
  # Create template with special characters
  cat > "$template_file" << 'EOF'
# {{PROJECT_NAME}}

Description: {{DESCRIPTION}}

Install: {{INSTALL_COMMAND}}
EOF
  
  # Create config with special characters
  cat > "$config_file" << 'EOF'
{
  "PROJECT_NAME": "My Project & Co.",
  "DESCRIPTION": "A project with / special \ characters",
  "INSTALL_COMMAND": "npm install && yarn build"
}
EOF
  
  # Run generator
  if run_test "special_characters" "$output_file" \
    --template "$template_file" \
    --output "$output_file" \
    --config "$config_file"; then
    
    # Verify special characters are preserved
    if grep -q "My Project & Co." "$output_file" && \
       grep -q "special \\ characters" "$output_file" && \
       grep -q "npm install && yarn build" "$output_file"; then
      log_success "Special characters test passed"
      return 0
    else
      log_error "Special characters test failed - special char verification failed"
      cat "$output_file"
      return 1
    fi
  else
    log_error "Special characters test failed - generator failed"
    return 1
  fi
}

# Run all tests
run_all_tests() {
  log_info "Running all tests..."
  
  local tests=(
    "test_placeholder_replacement"
    "test_command_line_override"
    "test_batch_processing"
    "test_missing_template"
    "test_help_option"
    "test_environment_variables"
    "test_special_characters"
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
  
  log_info "Test Results: $passed passed, $failed failed"
  
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
  log_info "Nightly Bash Quickstart Generator Test Suite"
  log_info "============================================"
  
  # Check if generator script exists
  if [[ ! -f "$GENERATOR_SCRIPT" ]]; then
    log_error "Generator script not found: $GENERATOR_SCRIPT"
    exit 1
  fi
  
  # Setup
  setup
  
  # Run tests
  local exit_code=0
  if ! run_all_tests; then
    exit_code=1
  fi
  
  # Cleanup
  cleanup
  
  exit $exit_code
}

# Run main function
main
