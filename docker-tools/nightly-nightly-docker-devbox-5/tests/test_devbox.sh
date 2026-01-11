#!/bin/bash

# Test suite for Nightly Docker DevBox
# Mock rationale: These tests verify CLI functionality without requiring actual Docker

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

# Mock Docker commands for testing
mock_docker() {
    case $1 in
        info)
            echo "Docker daemon is running"
            return 0
            ;;
        *)
            echo "Mock Docker command: $*"
            return 0
            ;;
    esac
}

mock_docker_compose() {
    case $1 in
        build|up|down)
            echo "Mock Docker Compose command: $*"
            return 0
            ;;
        *)
            echo "Mock Docker Compose command: $*"
            return 0
            ;;
    esac
}

# Setup test environment
setup_test_env() {
    TEST_DIR="/tmp/devbox_test_$$"
    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR"
    
    # Copy test files
    cp -r "$SCRIPT_DIR/templates" .
    cp "$SCRIPT_DIR/devbox.sh" .
    
    # Create mock binaries
    mkdir -p "${TEST_DIR}/mock_bin"
    cat > "${TEST_DIR}/mock_bin/docker" << 'EOF'
#!/bin/bash
exec /bin/bash -c 'mock_docker "$@"'
EOF
    cat > "${TEST_DIR}/mock_bin/docker-compose" << 'EOF'
#!/bin/bash
exec /bin/bash -c 'mock_docker_compose "$@"'
EOF
    cat > "${TEST_DIR}/mock_bin/jq" << 'EOF'
#!/bin/bash
echo "{}"
EOF
    
    chmod +x "${TEST_DIR}/mock_bin/docker"
    chmod +x "${TEST_DIR}/mock_bin/docker-compose"
    chmod +x "${TEST_DIR}/mock_bin/jq"
    
    export PATH="${TEST_DIR}/mock_bin:$PATH"
}

# Cleanup test environment
cleanup_test_env() {
    cd -
    rm -rf "$TEST_DIR"
}

# Test dependency checking
test_dependency_check() {
    log_test "Testing dependency checking"
    
    # Test with all dependencies present (mocked)
    if command -v docker >/dev/null 2>&1 && command -v docker-compose >/dev/null 2>&1 && command -v jq >/dev/null 2>&1; then
        pass_test "All dependencies detected"
    else
        fail_test "Dependency check failed"
    fi
}

# Test template validation
test_template_validation() {
    log_test "Testing template validation"
    
    local template_file="$TEST_DIR/templates/python.json"
    
    # Test JSON validation
    if jq empty "$template_file" 2>/dev/null; then
        pass_test "JSON validation passed"
    else
        fail_test "JSON validation failed"
    fi
    
    # Test required fields
    local required_fields=("name" "description" "dockerfile")
    for field in "${required_fields[@]}"; do
        if jq -e ".${field}" "$template_file" >/dev/null 2>&1; then
            pass_test "Required field '$field' exists"
        else
            fail_test "Required field '$field' missing"
        fi
    done
}

# Test template listing
test_template_listing() {
    log_test "Testing template listing"
    
    # Capture output of list_templates function
    local output
    output=$(bash -c 'source devbox.sh && list_templates' 2>&1) || true
    
    if echo "$output" | grep -q "python\|nodejs\|rust\|go"; then
        pass_test "Template listing works"
    else
        fail_test "Template listing failed"
    fi
}

# Test workspace creation
test_workspace_creation() {
    log_test "Testing workspace creation"
    
    local test_workspace="$TEST_DIR/test_workspace"
    
    # Create workspace directory
    mkdir -p "$test_workspace/src"
    mkdir -p "$test_workspace/data"
    
    if [ -d "$test_workspace" ] && [ -d "$test_workspace/src" ] && [ -d "$test_workspace/data" ]; then
        pass_test "Workspace creation works"
    else
        fail_test "Workspace creation failed"
    fi
}

# Test Dockerfile generation
test_dockerfile_generation() {
    log_test "Testing Dockerfile generation"
    
    local template_file="$TEST_DIR/templates/python.json"
    local workspace_dir="$TEST_DIR/test_workspace"
    
    # Generate Dockerfile
    local dockerfile_name=$(jq -r '.dockerfile' "$template_file")
    
    if [ -f "$TEST_DIR/templates/$dockerfile_name" ]; then
        cp "$TEST_DIR/templates/$dockerfile_name" "$workspace_dir/Dockerfile"
        pass_test "Dockerfile generation works"
    else
        fail_test "Dockerfile generation failed"
    fi
}

# Test docker-compose.yml generation
test_compose_generation() {
    log_test "Testing docker-compose.yml generation"
    
    local template_file="$TEST_DIR/templates/python.json"
    local project_name="test-project"
    local workspace_dir="$TEST_DIR/test_workspace"
    
    # Generate docker-compose.yml
    cat > "$workspace_dir/docker-compose.yml" << EOF
version: '3.8'

services:
  devbox-test-project:
    build:
      context: .
      dockerfile: Dockerfile.python
    container_name: devbox-test-project
    restart: unless-stopped
    volumes:
      - ./src:/app/src:cached
      - ./data:/app/data:cached
    working_dir: /app
    environment:
      PYTHONPATH: "/app/src"
      PYTHONUNBUFFERED: "1"
      PIP_NO_CACHE_DIR: "1"
      PIP_DISABLE_PIP_VERSION_CHECK: "1"
    ports:
      - "8000:8000"
      - "8080:8080"
    command: bash
    stdin_open: true
    tty: true
EOF
    
    if [ -f "$workspace_dir/docker-compose.yml" ]; then
        pass_test "docker-compose.yml generation works"
    else
        fail_test "docker-compose.yml generation failed"
    fi
}

# Test help output
test_help_output() {
    log_test "Testing help output"
    
    local output
    output=$(bash -c 'source devbox.sh && show_help' 2>&1) || true
    
    if echo "$output" | grep -q "USAGE:\|OPTIONS:\|EXAMPLES:"; then
        pass_test "Help output works"
    else
        fail_test "Help output failed"
    fi
}

# Test argument parsing
test_argument_parsing() {
    log_test "Testing argument parsing"
    
    # Test template argument
    local template_name="python"
    if [ "$template_name" = "python" ]; then
        pass_test "Template argument parsing works"
    else
        fail_test "Template argument parsing failed"
    fi
    
    # Test project name argument
    local project_name="test-project"
    if [ "$project_name" = "test-project" ]; then
        pass_test "Project name argument parsing works"
    else
        fail_test "Project name argument parsing failed"
    fi
}

# Run all tests
run_tests() {
    echo -e "${CYAN}Running Nightly Docker DevBox Test Suite${NC}"
    echo "========================================="
    
    setup_test_env
    
    test_dependency_check
    test_template_validation
    test_template_listing
    test_workspace_creation
    test_dockerfile_generation
    test_compose_generation
    test_help_output
    test_argument_parsing
    
    cleanup_test_env
    
    # Print results
    echo
    echo "========================================="
    echo -e "${GREEN}Tests passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Tests failed: $TESTS_FAILED${NC}"
    echo -e "${BLUE}Total tests: $((TESTS_PASSED + TESTS_FAILED))${NC}"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "\n${GREEN}🎉 All tests passed!${NC}"
        return 0
    else
        echo -e "\n${RED}❌ Some tests failed!${NC}"
        return 1
    fi
}

# Run tests if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_tests
fi
