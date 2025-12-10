#!/bin/bash

# Tests for Nightly Chaos Chaos Cha
# These tests use mocks to ensure determinism and offline execution

set -euo pipefail

# Mock functions to avoid actual system modifications
mock_sudo() {
  echo "Mock: sudo $*"
}

mock_tc() {
  echo "Mock: tc $*"
}

mock_yes() {
  echo "Mock: yes started"
}

mock_dd() {
  echo "Mock: dd started"
}

mock_pkill() {
  echo "Mock: pkill $*"
}

mock_rm() {
  echo "Mock: rm $*"
}

# Override commands with mocks
sudo() { mock_sudo "$@"; }
tc() { mock_tc "$@"; }
yes() { mock_yes; }
dd() { mock_dd "$@"; }
pkill() { mock_pkill "$@"; }
rm() { mock_rm "$@"; }

# Source the main script functions (excluding the main execution)
source <(grep -v '^run_chaos_scenario' src/main.sh)

# Test function to verify chaos scenario execution
test_chaos_scenario() {
  echo "Testing chaos-chaos-cha scenario..."
  
  # Capture output
  output=$(run_chaos_scenario "chaos-chaos-cha" 1)
  
  # Verify expected actions were taken
  if echo "$output" | grep -q "Introducing network latency" && 
     echo "$output" | grep -q "Introducing CPU load" && 
     echo "$output" | grep -q "Introducing memory pressure"; then
    echo "✓ Chaos scenario executed correctly"
  else
    echo "✗ Chaos scenario failed"
    echo "Output: $output"
    exit 1
  fi
}

# Test function to verify cleanup execution
test_cleanup_scenario() {
  echo "Testing cleanup after chaos scenario..."
  
  # Capture output
  output=$(run_chaos_scenario "chaos-chaos-cha" 1)
  
  # Verify cleanup was performed
  if echo "$output" | grep -q "Removing network latency" && 
     echo "$output" | grep -q "Removing CPU load" && 
     echo "$output" | grep -q "Removing memory pressure"; then
    echo "✓ Cleanup executed correctly"
  else
    echo "✗ Cleanup failed"
    echo "Output: $output"
    exit 1
  fi
}

# Test function to verify single-mode scenarios
test_single_mode_scenario() {
  echo "Testing network-only scenario..."
  
  output=$(run_chaos_scenario "network-only" 1)
  
  if echo "$output" | grep -q "Introducing network latency" && 
     echo "$output" | grep -q "Removing network latency"; then
    echo "✓ Network-only scenario executed correctly"
  else
    echo "✗ Network-only scenario failed"
    echo "Output: $output"
    exit 1
  fi
}

# Test function to verify invalid mode handling
test_invalid_mode() {
  echo "Testing invalid mode handling..."
  
  if run_chaos_scenario "invalid-mode" 1 2>&1 | grep -q "Unknown mode"; then
    echo "✓ Invalid mode handled correctly"
  else
    echo "✗ Invalid mode not handled properly"
    exit 1
  fi
}

# Run all tests
main() {
  echo "Running tests for Nightly Chaos Chaos Cha..."
  echo "========================================="
  
  test_chaos_scenario
  test_cleanup_scenario
  test_single_mode_scenario
  test_invalid_mode
  
  echo "========================================="
  echo "All tests passed!"
}

# Execute tests
main
