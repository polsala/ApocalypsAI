#!/bin/bash

# Tests for Nightly Chaos Chaos Cha
# Run with: bash tests/test_main.sh

set -euo pipefail

# Colors for test output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Source the main script (but don't execute it)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAIN_SCRIPT="$SCRIPT_DIR/src/main.sh"

# Mock functions for testing
mock_get_random_message() {
  echo "Mock message"
}

mock_sleep() {
  # Don't actually sleep during tests
  return 0
}

mock_tput() {
  # Don't actually change terminal during tests
  return 0
}

mock_rm() {
  # Don't actually remove files during tests
  return 0
}

# Function to run a test
run_test() {
  local test_name="$1"
  local test_function="$2"
  
  TESTS_RUN=$((TESTS_RUN + 1))
  echo -e "${BLUE}[TEST]${NC} Running: $test_name"
  
  if $test_function; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo -e "${GREEN}[PASS]${NC} $test_name"
  else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "${RED}[FAIL]${NC} $test_name"
  fi
  echo
}

# Test 1: Script loads without errors
test_script_loads() {
  # Mock external dependencies
  export -f mock_get_random_message
  export -f mock_sleep
  export -f mock_tput
  export -f mock_rm
  
  # Try to source the script
  if source "$MAIN_SCRIPT" 2>/dev/null; then
    return 0
  else
    return 1
  fi
}

# Test 2: Help option works
test_help_option() {
  local output
  output=$(bash "$MAIN_SCRIPT" --help 2>&1)
  
  if echo "$output" | grep -q "Usage:"; then
    return 0
  else
    echo "Help output: $output"
    return 1
  fi
}

# Test 3: Invalid chaos level is rejected
test_invalid_chaos_level() {
  # Test too high
  if bash "$MAIN_SCRIPT" --chaos-level 11 2>&1 | grep -q "Error"; then
    # Test too low
    if bash "$MAIN_SCRIPT" --chaos-level 0 2>&1 | grep -q "Error"; then
      # Test non-numeric
      if bash "$MAIN_SCRIPT" --chaos-level abc 2>&1 | grep -q "Error"; then
        return 0
      fi
    fi
  fi
  return 1
}

# Test 4: Valid chaos levels are accepted
test_valid_chaos_levels() {
  # Test boundary values
  for level in 1 5 10; do
    # Run with timeout to avoid actual chaos taking too long
    if timeout 5 bash "$MAIN_SCRIPT" --chaos-level $level --quiet 2>&1; then
      continue
    else
      return 1
    fi
  done
  return 0
}

# Test 5: Quiet mode reduces output
test_quiet_mode() {
  local normal_output quiet_output
  
  # Capture output with timeout
  normal_output=$(timeout 3 bash "$MAIN_SCRIPT" --chaos-level 3 2>&1)
  quiet_output=$(timeout 3 bash "$MAIN_SCRIPT" --chaos-level 3 --quiet 2>&1)
  
  # Quiet mode should have less or equal output
  if [[ ${#quiet_output} -le ${#normal_output} ]]; then
    return 0
  else
    echo "Normal output: $normal_output"
    echo "Quiet output: $quiet_output"
    return 1
  fi
}

# Test 6: Script exits with correct code on success
test_exit_code() {
  # Mock sleep to avoid waiting
  if timeout 5 bash "$MAIN_SCRIPT" --chaos-level 2 --quiet 2>&1; then
    return 0
  else
    return 1
  fi
}

# Test 7: Unknown option is rejected
test_unknown_option() {
  if bash "$MAIN_SCRIPT" --unknown-option 2>&1 | grep -q "Unknown option"; then
    return 0
  else
    return 1
  fi
}

# Test 8: Chaos level requires a value
test_chaos_level_requires_value() {
  if bash "$MAIN_SCRIPT" --chaos-level 2>&1 | grep -q "Error"; then
    return 0
  else
    return 1
  fi
}

# Test 9: Script handles missing value gracefully
test_missing_chaos_value() {
  if bash "$MAIN_SCRIPT" -c 2>&1 | grep -q "Error"; then
    return 0
  else
    return 1
  fi
}

# Test 10: Script runs without arguments
test_no_arguments() {
  # Mock sleep to avoid waiting
  if timeout 5 bash "$MAIN_SCRIPT" 2>&1; then
    return 0
  else
    return 1
  fi
}

# Function to print test summary
print_summary() {
  echo -e "${BLUE}================================${NC}"
  echo -e "${BLUE}Test Summary${NC}"
  echo -e "${BLUE}================================${NC}"
  echo -e "Total tests: $TESTS_RUN"
  echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
  echo -e "${RED}Failed: $TESTS_FAILED${NC}"
  
  if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}[SUCCESS] All tests passed!${NC}"
    return 0
  else
    echo -e "${RED}[FAILURE] Some tests failed!${NC}"
    return 1
  fi
}

# Main test execution
main() {
  echo -e "${BLUE}================================${NC}"
  echo -e "${BLUE}Running Chaos Chaos Cha Tests${NC}"
  echo -e "${BLUE}================================${NC}"
  echo
  
  # Run all tests
  run_test "Script loads without errors" test_script_loads
  run_test "Help option works" test_help_option
  run_test "Invalid chaos level is rejected" test_invalid_chaos_level
  run_test "Valid chaos levels are accepted" test_valid_chaos_levels
  run_test "Quiet mode reduces output" test_quiet_mode
  run_test "Script exits with correct code on success" test_exit_code
  run_test "Unknown option is rejected" test_unknown_option
  run_test "Chaos level requires a value" test_chaos_level_requires_value
  run_test "Script handles missing value gracefully" test_missing_chaos_value
  run_test "Script runs without arguments" test_no_arguments
  
  # Print summary
  print_summary
  exit $?
}

# Run tests if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
