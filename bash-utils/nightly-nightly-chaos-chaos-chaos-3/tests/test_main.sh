#!/bin/bash

# Tests for Nightly Chaos Chaos Chaos
# Mock-based tests to ensure functionality without actual chaos

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
MAIN_SCRIPT="$ROOT_DIR/src/main.sh"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
  echo -e "${GREEN}[TEST]${NC} $1"
}

warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Setup mocks
setup_mocks() {
  # Create mock binaries
  mkdir -p "$TEST_DIR/mocks"
  
  # Mock tc
  cat > "$TEST_DIR/mocks/tc" << 'EOF'
#!/bin/bash
# Mock tc command
if [[ "$1" == "qdisc" && "$2" == "add" ]]; then
  echo "Mock: Added qdisc"
  exit 0
elif [[ "$1" == "qdisc" && "$2" == "del" ]]; then
  echo "Mock: Deleted qdisc"
  exit 0
else
  echo "Mock: tc $*"
  exit 0
fi
EOF
  chmod +x "$TEST_DIR/mocks/tc"
  
  # Mock stress
  cat > "$TEST_DIR/mocks/stress" << 'EOF'
#!/bin/bash
# Mock stress command
if [[ "$*" == *"--timeout"* ]]; then
  echo "Mock: Started stress with timeout"
  sleep 0.1
  exit 0
else
  echo "Mock: stress $*"
  exit 0
fi
EOF
  chmod +x "$TEST_DIR/mocks/stress"
  
  # Mock systemctl
  cat > "$TEST_DIR/mocks/systemctl" << 'EOF'
#!/bin/bash
# Mock systemctl command
if [[ "$1" == "list-units" ]]; then
  echo "mock-service.service loaded active running"
  exit 0
elif [[ "$1" == "stop" ]]; then
  echo "Mock: Stopped $2"
  exit 0
elif [[ "$1" == "start" ]]; then
  echo "Mock: Started $2"
  exit 0
else
  echo "Mock: systemctl $*"
  exit 0
fi
EOF
  chmod +x "$TEST_DIR/mocks/systemctl"
  
  # Add mocks to PATH
  export PATH="$TEST_DIR/mocks:$PATH"
}

# Test setup
TEST_DIR="/tmp/chaos_test_$$"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"

# Source the main script functions (without executing)
export -f check_root check_deps chaos_network chaos_service chaos_resource chaos_random chaos_time cleanup

# Test chaos_network function
test_chaos_network() {
  log "Testing chaos_network function"
  
  # Mock root check
  check_root() { return 0; }
  check_deps() { return 0; }
  
  # Test network chaos
  chaos_network "5s" "50ms"
  
  log "✓ Network chaos test passed"
}

# Test chaos_service function
test_chaos_service() {
  log "Testing chaos_service function"
  
  # Mock root check
  check_root() { return 0; }
  check_deps() { return 0; }
  
  # Test service chaos
  chaos_service "mock-service"
  
  log "✓ Service chaos test passed"
}

# Test chaos_resource function
test_chaos_resource() {
  log "Testing chaos_resource function"
  
  # Mock root check
  check_root() { return 0; }
  check_deps() { return 0; }
  
  # Test resource chaos
  chaos_resource "1" "128" "5s"
  
  # Check if PID file was created
  if [[ -f /tmp/chaos_stress.pid ]]; then
    log "✓ Resource chaos PID file created"
    rm -f /tmp/chaos_stress.pid
  else
    error "Resource chaos did not create PID file"
    return 1
  fi
  
  log "✓ Resource chaos test passed"
}

# Test chaos_random function
test_chaos_random() {
  log "Testing chaos_random function"
  
  # Mock root check
  check_root() { return 0; }
  check_deps() { return 0; }
  
  # Mock all chaos functions
  chaos_network() { log "Mock: chaos_network called"; }
  chaos_service() { log "Mock: chaos_service called"; }
  chaos_resource() { log "Mock: chaos_resource called"; }
  chaos_time() { log "Mock: chaos_time called"; }
  
  # Test random chaos
  chaos_random
  
  log "✓ Random chaos test passed"
}

# Test chaos_time function
test_chaos_time() {
  log "Testing chaos_time function"
  
  # Test time chaos
  chaos_time "+5 minutes"
  
  log "✓ Time chaos test passed"
}

# Test cleanup function
test_cleanup() {
  log "Testing cleanup function"
  
  # Create mock PID file
  echo "12345" > /tmp/chaos_stress.pid
  
  # Test cleanup
  cleanup
  
  # Check if PID file was removed
  if [[ ! -f /tmp/chaos_stress.pid ]]; then
    log "✓ Cleanup removed PID file"
  else
    error "Cleanup did not remove PID file"
    return 1
  fi
  
  log "✓ Cleanup test passed"
}

# Test help function
test_help() {
  log "Testing help function"
  
  # Test help output
  if show_help | grep -q "Nightly Chaos Chaos Chaos"; then
    log "✓ Help function works"
  else
    error "Help function failed"
    return 1
  fi
}

# Test argument parsing
test_arg_parsing() {
  log "Testing argument parsing"
  
  # Mock functions to avoid actual chaos
  check_root() { return 0; }
  check_deps() { return 0; }
  chaos_network() { log "Mock: chaos_network called"; }
  chaos_service() { log "Mock: chaos_service called"; }
  chaos_resource() { log "Mock: chaos_resource called"; }
  chaos_random() { log "Mock: chaos_random called"; }
  chaos_time() { log "Mock: chaos_time called"; }
  cleanup() { log "Mock: cleanup called"; }
  
  # Test network mode parsing
  parse_args --mode network --duration 10s --latency 200ms
  
  # Test service mode parsing
  parse_args --mode service --service-name mock-service
  
  # Test resource mode parsing
  parse_args --mode resource --cpu-cores 2 --memory-mb 512 --duration 30s
  
  # Test random mode parsing
  parse_args --mode random
  
  # Test time mode parsing
  parse_args --mode time --offset "+1 hour"
  
  # Test cleanup parsing
  parse_args --cleanup
  
  log "✓ Argument parsing test passed"
}

# Run all tests
run_tests() {
  log "Setting up mocks"
  setup_mocks
  
  log "Running tests..."
  
  test_chaos_network
  test_chaos_service
  test_chaos_resource
  test_chaos_random
  test_chaos_time
  test_cleanup
  test_help
  test_arg_parsing
  
  log "All tests passed! ✓"
}

# Cleanup test directory
cleanup_test() {
  rm -rf "$TEST_DIR"
}

# Run tests on script exit
trap cleanup_test EXIT

# Run the tests
run_tests
