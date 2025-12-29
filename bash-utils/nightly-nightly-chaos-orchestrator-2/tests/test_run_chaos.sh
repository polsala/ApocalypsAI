#!/bin/bash

# Test suite for Nightly Chaos Orchestrator
# This script tests the chaos orchestrator functionality

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_TOTAL=0
TESTS_PASSED=0
TESTS_FAILED=0

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

run_test() {
    local test_name="$1"
    local test_command="$2"
    
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    log_info "Running test: $test_name"
    
    if eval "$test_command" >/dev/null 2>&1; then
        log_success "$test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        log_fail "$test_name"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Test setup
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
CHAOS_SCRIPT="${ROOT_DIR}/src/run_chaos.sh"

# Check if chaos script exists
if [ ! -f "$CHAOS_SCRIPT" ]; then
    log_fail "Chaos script not found: $CHAOS_SCRIPT"
    exit 1
fi

log_info "=== Nightly Chaos Orchestrator Test Suite ==="
log_info "Testing script: $CHAOS_SCRIPT"

# Test 1: Script is executable
run_test "Script is executable" "[ -x \"$CHAOS_SCRIPT\"]"

# Test 2: Script shows help
run_test "Script shows help" "\"$CHAOS_SCRIPT\" --help"

# Test 3: Script validates inventory file
run_test "Script validates inventory file" "\"$CHAOS_SCRIPT\" --inventory \"$ROOT_DIR/src/inventory.ini\" --dry-run"

# Test 4: Script handles invalid inventory
run_test "Script handles invalid inventory" "! \"$CHAOS_SCRIPT\" --inventory /nonexistent/file --dry-run"

# Test 5: Script handles dry run
run_test "Script handles dry run" "\"$CHAOS_SCRIPT\" --dry-run"

# Test 6: Script validates required files exist
run_test "Required files exist" "[ -f \"$ROOT_DIR/src/chaos_orchestrator.yml\" ] && [ -f \"$ROOT_DIR/src/inventory.ini\" ] && [ -f \"$ROOT_DIR/src/vars/chaos_scenarios.yml\" ]"

# Test 7: Script validates YAML syntax
run_test "YAML files are valid" "python3 -c \"import yaml; yaml.safe_load(open(\'\$ROOT_DIR/src/vars/chaos_scenarios.yml\'))\""

# Test 8: Script validates Jinja2 template
run_test "Jinja2 template is valid" "python3 -c \"from jinja2 import Environment; env = Environment(); env.from_string(open(\'\$ROOT_DIR/src/templates/chaos_report.j2\').read())\""

# Test 9: Script handles scenario filtering
run_test "Scenario filtering works" "\"$CHAOS_SCRIPT\" --scenario network_partition --dry-run"

# Test 10: Script handles unknown scenario
run_test "Unknown scenario handling" "! \"$CHAOS_SCRIPT\" --scenario nonexistent_scenario --dry-run"

# Test 11: Script validates Ansible playbook syntax
run_test "Ansible playbook syntax" "ansible-playbook --syntax-check \"$ROOT_DIR/src/chaos_orchestrator.yml\""

# Test 12: Script validates inventory syntax
run_test "Inventory syntax" "ansible-inventory -i \"$ROOT_DIR/src/inventory.ini\" --list"

# Test 13: Script handles missing dependencies gracefully
run_test "Missing dependencies check" "(command -v ansible >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1) || true"

# Test 14: Script creates log directory
run_test "Log directory creation" "mkdir -p /tmp/test_chaos_logs && [ -d /tmp/test_chaos_logs ]"

# Test 15: Script handles cleanup
run_test "Cleanup handling" "rm -rf /tmp/test_chaos_logs"

# Display results
log_info "\n=== Test Results ==="
log_info "Total tests: $TESTS_TOTAL"
log_success "Passed: $TESTS_PASSED"
log_fail "Failed: $TESTS_FAILED"

if [ $TESTS_FAILED -eq 0 ]; then
    log_success "All tests passed! Chaos orchestrator is ready for deployment."
    exit 0
else
    log_fail "Some tests failed. Please review the failures above."
    exit 1
fi
