#!/bin/bash

# Test suite for chaos-monkey.sh
# Mock rationale: We mock system commands to avoid actual chaos during testing

set -euo pipefail

# Test directory setup
TEST_DIR=$(mktemp -d)
LOG_FILE="$TEST_DIR/chaos.log"
CHAOS_SCRIPT="./src/chaos-monkey.sh"

# Cleanup function
cleanup() {
  rm -rf "$TEST_DIR"
  unset -f ip systemctl stress-ng timeout
}

trap cleanup EXIT

# Mock system commands
ip() { echo "Mocked ip $*"; }
systemctl() { echo "Mocked systemctl $*"; }
stress-ng() { echo "Mocked stress-ng $*"; }
timeout() { echo "Mocked timeout $*"; }

# Test 1: Script runs without errors in dry-run mode
test_dry_run() {
  echo "Testing dry run mode..."
  DRY_RUN=1 LOG_FILE="$LOG_FILE" bash "$CHAOS_SCRIPT"
  
  if [[ -f "$LOG_FILE" ]] && grep -q "Chaos Monkey started" "$LOG_FILE"; then
    echo "PASS: Dry run executed successfully"
  else
    echo "FAIL: Dry run failed"
    return 1
  fi
}

# Test 2: Script respects probability setting
test_probability() {
  echo "Testing probability setting..."
  DRY_RUN=1 CHAOS_PROBABILITY=0 LOG_FILE="$LOG_FILE" bash "$CHAOS_SCRIPT"
  
  if grep -q "No chaos today" "$LOG_FILE"; then
    echo "PASS: Respects zero probability"
  else
    echo "FAIL: Did not respect zero probability"
    return 1
  fi
}

# Test 3: All chaos functions execute without errors
test_chaos_functions() {
  echo "Testing chaos functions..."
  
  # Source the script to test functions directly
  source "$CHAOS_SCRIPT"
  
  # Override log function for testing
  log() { echo "TEST: $1"; }
  
  # Test each chaos function
  cause_cpu_stress
  cause_network_chaos
  cause_service_chaos
  cause_memory_stress
  cause_disk_stress
  
  echo "PASS: All chaos functions executed"
}

# Run tests
run_tests() {
  test_dry_run
  test_probability
  test_chaos_functions
  echo "All tests passed!"
}

# Execute tests
run_tests
