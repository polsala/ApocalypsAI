#!/bin/bash

# Test suite for Nightly Bash Chaos Chaos Chaos 2

set -euo pipefail

# Mock rationale: We mock external commands to test logic without actual chaos
mock_chaos() {
  # Mock tc command
  tc() {
    echo "Mock tc: $*"
  }
  export -f tc
  
  # Mock dd command
  dd() {
    echo "Mock dd: $*"
  }
  export -f dd
  
  # Mock timeout command
  timeout() {
    echo "Mock timeout: $*"
  }
  export -f timeout
}

# Run tests
run_tests() {
  echo "Running chaos generator tests..."
  
  # Test 1: Basic execution
  echo "Test 1: Basic execution"
  mock_chaos
  ./src/main.sh --level 1 > /tmp/test_output.log 2>&1
  if grep -q "Starting chaos level 1" /tmp/test_output.log; then
    echo "✓ Test 1 passed"
  else
    echo "✗ Test 1 failed"
    cat /tmp/test_output.log
    exit 1
  fi
  
  # Test 2: Multiple chaos events
  echo "Test 2: Multiple chaos events"
  ./src/main.sh --level 3 > /tmp/test_output2.log 2>&1
  if grep -q "CHAOS: Executing chaos event 3" /tmp/test_output2.log; then
    echo "✓ Test 2 passed"
  else
    echo "✗ Test 2 failed"
    cat /tmp/test_output2.log
    exit 1
  fi
  
  # Test 3: Log file creation
  echo "Test 3: Log file creation"
  ./src/main.sh --level 1 > /tmp/test_output3.log 2>&1
  LOG_FILE=$(grep "Report saved to" /tmp/test_output3.log | sed 's/.*Report saved to //')
  if [[ -f "$LOG_FILE" ]]; then
    echo "✓ Test 3 passed"
  else
    echo "✗ Test 3 failed"
    exit 1
  fi
  
  echo "All tests passed!"
}

# Execute tests
run_tests
