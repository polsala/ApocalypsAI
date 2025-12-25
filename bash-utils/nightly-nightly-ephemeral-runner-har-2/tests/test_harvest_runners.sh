#!/usr/bin/env bash

# Test suite for Nightly Ephemeral Runner Harvester
# Uses mock data and functions to test without real API calls

set -euo pipefail

# Source the script to test (mock the functions)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UTIL_DIR="$(dirname "$SCRIPT_DIR")"
SCRIPT_PATH="$UTIL_DIR/src/harvest_runners.sh"

# Mock functions for testing
mock_api_request() {
  local method="$1"
  local url="$2"
  local data="${3:-}"

  # Mock responses based on URL patterns
  case "$url" in
    *"/user/repos"*)
      echo '[{"full_name":"test/repo1"},{"full_name":"test/repo2"}]'
      ;;
    *"/repos/test/repo1/actions/runners"*)
      echo '{"runners":[{"id":1,"status":"online"},{"id":2,"status":"offline"}]}'
      ;;
    *"/repos/test/repo1/actions/runs"*)
      echo '{"workflow_runs":[{"id":100,"status":"completed","runner_id":1},{"id":101,"status":"in_progress","runner_id":2}]}'
      ;;
    *"/repos/test/repo2/actions/runners"*)
      echo '{"runners":[{"id":3,"status":"online"}]}'
      ;;
    *"/repos/test/repo2/actions/runs"*)
      echo '{"workflow_runs":[{"id":200,"status":"completed","runner_id":3}]}'
      ;;
    *)
      echo '{}'
      ;;
  esac
}

mock_log() {
  echo "$1" >> "$TEST_LOG"
}

mock_error_exit() {
  echo "ERROR: $1" >&2
  exit 1
}

mock_success() {
  echo "SUCCESS: $1"
}

mock_warning() {
  echo "WARNING: $1"
}

# Setup test environment
setup() {
  TEST_DIR="$(mktemp -d)"
  TEST_LOG="$TEST_DIR/test.log"
  export GITHUB_TOKEN="test_token"
  export GITHUB_ORG=""

  # Create a copy of the script with mocked functions
  sed 's/api_request()/mock_api_request/g' "$SCRIPT_PATH" > "$TEST_DIR/harvest_runners_test.sh"
  sed -i 's/log(/mock_log(/g' "$TEST_DIR/harvest_runners_test.sh"
  sed -i 's/error_exit(/mock_error_exit(/g' "$TEST_DIR/harvest_runners_test.sh"
  sed -i 's/success(/mock_success(/g' "$TEST_DIR/harvest_runners_test.sh"
  sed -i 's/warning(/mock_warning(/g' "$TEST_DIR/harvest_runners_test.sh"

  chmod +x "$TEST_DIR/harvest_runners_test.sh"
}

# Cleanup test environment
cleanup() {
  rm -rf "$TEST_DIR"
}

# Test 1: Dry run mode
test_dry_run() {
  echo "Running test: Dry run mode"

  # Run the script in dry run mode
  "$TEST_DIR/harvest_runners_test.sh" --dry-run

  # Check if the log contains expected messages
  if grep -q "Starting runner harvesting process" "$TEST_LOG"; then
    echo "✓ Dry run started successfully"
  else
    echo "✗ Dry run failed to start"
    return 1
  fi

  if grep -q "[DRY RUN] Would harvest" "$TEST_LOG"; then
    echo "✓ Dry run mode working correctly"
  else
    echo "✗ Dry run mode not working"
    return 1
  fi
}

# Test 2: Token validation
test_token_validation() {
  echo "Running test: Token validation"

  # Test with missing token
  unset GITHUB_TOKEN
  if "$TEST_DIR/harvest_runners_test.sh" 2>&1 | grep -q "GitHub token is required"; then
    echo "✓ Token validation working"
  else
    echo "✗ Token validation failed"
    return 1
  fi

  # Restore token
  export GITHUB_TOKEN="test_token"
}

# Test 3: Help option
test_help_option() {
  echo "Running test: Help option"

  if "$TEST_DIR/harvest_runners_test.sh" --help | grep -q "Usage:"; then
    echo "✓ Help option working"
  else
    echo "✗ Help option failed"
    return 1
  fi
}

# Test 4: Organization scope
test_org_scope() {
  echo "Running test: Organization scope"

  # Mock org API response
  mock_api_request() {
    case "$2" in
      *"/orgs/testorg/repos"*)
        echo '[{"full_name":"testorg/repo1"}]'
        ;;
      *"/repos/testorg/repo1/actions/runners"*)
        echo '{"runners":[{"id":1,"status":"online"}]}'
        ;;
      *"/repos/testorg/repo1/actions/runs"*)
        echo '{"workflow_runs":[{"id":100,"status":"completed","runner_id":1}]}'
        ;;
      *)
        echo '{}'
        ;;
    esac
  }

  export GITHUB_ORG="testorg"
  "$TEST_DIR/harvest_runners_test.sh"

  if grep -q "Organization scope: testorg" "$TEST_LOG"; then
    echo "✓ Organization scope working"
  else
    echo "✗ Organization scope failed"
    return 1
  fi
}

# Test 5: JSON parsing and runner detection
test_runner_detection() {
  echo "Running test: Runner detection"

  # This test verifies that the script can parse JSON responses
  # and identify idle runners correctly
  "$TEST_DIR/harvest_runners_test.sh" --dry-run

  # Check if idle runners were detected
  if grep -q "Found idle runner" "$TEST_LOG"; then
    echo "✓ Runner detection working"
  else
    echo "✗ Runner detection failed"
    return 1
  fi
}

# Run all tests
run_tests() {
  echo "=== Running Nightly Ephemeral Runner Harvester Tests ==="
  echo

  setup

  local tests_passed=0
  local tests_failed=0

  # Run each test
  if test_dry_run; then
    tests_passed=$((tests_passed + 1))
  else
    tests_failed=$((tests_failed + 1))
  fi

  setup # Reset for next test
  if test_token_validation; then
    tests_passed=$((tests_passed + 1))
  else
    tests_failed=$((tests_failed + 1))
  fi

  setup # Reset for next test
  if test_help_option; then
    tests_passed=$((tests_passed + 1))
  else
    tests_failed=$((tests_failed + 1))
  fi

  setup # Reset for next test
  if test_org_scope; then
    tests_passed=$((tests_passed + 1))
  else
    tests_failed=$((tests_failed + 1))
  fi

  setup # Reset for next test
  if test_runner_detection; then
    tests_passed=$((tests_passed + 1))
  else
    tests_failed=$((tests_failed + 1))
  fi

  cleanup

  echo
  echo "=== Test Results ==="
  echo "Tests passed: $tests_passed"
  echo "Tests failed: $tests_failed"

  if [[ $tests_failed -eq 0 ]]; then
    echo "✓ All tests passed!"
    return 0
  else
    echo "✗ Some tests failed!"
    return 1
  fi
}

# Run the test suite if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  run_tests
fi
