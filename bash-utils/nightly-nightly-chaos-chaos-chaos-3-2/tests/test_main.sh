#!/bin/bash

# Tests for Nightly Chaos Chaos Chaos 3

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
  echo -e "${GREEN}[TEST]${NC} $1"
}

warn() {
  echo -e "${YELLOW}[TEST] WARNING:${NC} $1"
}

error() {
  echo -e "${RED}[TEST] ERROR:${NC} $1"
}

# Mock functions for testing
mock_stress() {
  echo "stress command mocked"
}

mock_tc() {
  echo "tc command mocked"
}

mock_systemctl() {
  echo "systemctl command mocked"
}

# Test that script is executable
test_script_executable() {
  log "Testing script is executable..."
  if [[ -x "../src/main.sh" ]]; then
    log "✓ Script is executable"
  else
    error "✗ Script is not executable"
    exit 1
  fi
}

# Test that script has proper shebang
test_shebang() {
  log "Testing shebang..."
  if head -n 1 "../src/main.sh" | grep -q "#!/bin/bash"; then
    log "✓ Shebang is correct"
  else
    error "✗ Shebang is incorrect"
    exit 1
  fi
}

# Test that script contains required functions
test_required_functions() {
  log "Testing required functions exist..."
  
  local functions=("log" "warn" "error" "init_report" "add_to_report" "command_exists" "chaos_network" "chaos_resources" "chaos_services" "chaos_files" "execute_chaos" "show_report" "cleanup" "main")
  
  for func in "${functions[@]}"; do
    if grep -q "^$func()" "../src/main.sh"; then
      log "✓ Function $func exists"
    else
      error "✗ Function $func missing"
      exit 1
    fi
  done
}

# Test that script uses set -euo pipefail
test_strict_mode() {
  log "Testing strict mode..."
  if grep -q "set -euo pipefail" "../src/main.sh"; then
    log "✓ Strict mode is enabled"
  else
    error "✗ Strict mode not enabled"
    exit 1
  fi
}

# Test that script has trap for cleanup
test_cleanup_trap() {
  log "Testing cleanup trap..."
  if grep -q "trap cleanup EXIT" "../src/main.sh"; then
    log "✓ Cleanup trap is set"
  else
    error "✗ Cleanup trap not found"
    exit 1
  fi
}

# Test that script initializes report
test_report_initialization() {
  log "Testing report initialization..."
  if grep -q "init_report" "../src/main.sh"; then
    log "✓ Report initialization found"
  else
    error "✗ Report initialization not found"
    exit 1
  fi
}

# Test that script has proper error handling
test_error_handling() {
  log "Testing error handling..."
  if grep -q "set -e" "../src/main.sh"; then
    log "✓ Error handling is enabled"
  else
    error "✗ Error handling not enabled"
    exit 1
  fi
}

# Test that script has comments and documentation
test_documentation() {
  log "Testing documentation..."
  if grep -q "#.*chaos" "../src/main.sh"; then
    log "✓ Documentation comments found"
  else
    error "✗ Documentation comments not found"
    exit 1
  fi
}

# Run all tests
run_tests() {
  log "Running tests for Nightly Chaos Chaos Chaos 3..."
  echo ""
  
  test_script_executable
  test_shebang
  test_strict_mode
  test_cleanup_trap
  test_error_handling
  test_required_functions
  test_report_initialization
  test_documentation
  
  echo ""
  log "All tests passed! ✓"
}

# Run tests
run_tests
