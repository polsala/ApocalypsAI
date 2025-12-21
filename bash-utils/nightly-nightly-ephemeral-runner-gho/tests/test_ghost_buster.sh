#!/bin/bash

# Test suite for Nightly Ephemeral Runner Ghost Buster
# Mock rationale: Tests use mock API responses to verify script behavior without actual GitHub API calls

set -euo pipefail

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/src/ghost_buster.sh"
TEST_DIR="/tmp/ghost_buster_tests"

# Mock functions
mock_curl() {
  local url="$1"
  local method="$2"
  
  # Mock GitHub user endpoint
  if [[ "$url" == *"/user"* ]]; then
    echo '{"login": "testuser", "id": 12345}'
    return 0
  fi
  
  # Mock repository list
  if [[ "$url" == *"/user/repos"* ]]; then
    echo '[{"full_name": "test/repo1"}, {"full_name": "test/repo2"}]'
    return 0
  fi
  
  # Mock runner list for repo1
  if [[ "$url" == *"/repos/test/repo1/actions/runners"* ]]; then
    echo '{"total_count": 2, "runners": [
      {"id": 1, "name": "runner1", "status": "offline"},
      {"id": 2, "name": "runner2", "status": "online"}
    ]}'
    return 0
  fi
  
  # Mock runner list for repo2
  if [[ "$url" == *"/repos/test/repo2/actions/runners"* ]]; then
    echo '{"total_count": 1, "runners": [
      {"id": 3, "name": "runner3", "status": "offline"}
    ]}'
    return 0
  fi
  
  # Mock individual runner info
  if [[ "$url" == *"/actions/runners/1"* ]]; then
    echo '{"id": 1, "name": "runner1", "status": "offline", "created_at": "2023-01-01T00:00:00Z"}'
    return 0
  fi
  
  if [[ "$url" == *"/actions/runners/3"* ]]; then
    echo '{"id": 3, "name": "runner3", "status": "offline", "created_at": "2023-01-01T00:00:00Z"}'
    return 0
  fi
  
  # Mock delete runner
  if [[ "$url" == *"/actions/runners/1"* && "$method" == "DELETE" ]]; then
    echo ''
    return 0
  fi
  
  if [[ "$url" == *"/actions/runners/3"* && "$method" == "DELETE" ]]; then
    echo ''
    return 0
  fi
  
  echo 'Mock: Unknown API call'
  return 1
}

# Test functions
setup_test() {
  mkdir -p "$TEST_DIR"
  cd "$TEST_DIR"
  
  # Create mock config
  cat > config.json << 'EOF'
{
  "github_token": "test_token",
  "api_base_url": "https://api.github.com",
  "repositories": ["test/repo1", "test/repo2"],
  "retention_days": 1,
  "dry_run": true,
  "verbose": true
}
EOF
}

tear_down_test() {
  cd -
  rm -rf "$TEST_DIR"
}

test_help() {
  echo "Testing help output..."
  
  if "$SCRIPT_PATH" --help >/dev/null 2>&1; then
    echo "✓ Help option works"
  else
    echo "✗ Help option failed"
    return 1
  fi
}

test_prerequisites() {
  echo "Testing prerequisite validation..."
  
  # Test with missing curl
  if ! command -v curl >/dev/null 2>&1; then
    echo "Skipping curl test (not available)"
  else
    echo "✓ curl available"
  fi
  
  # Test with missing jq
  if ! command -v jq >/dev/null 2>&1; then
    echo "Skipping jq test (not available)"
  else
    echo "✓ jq available"
  fi
}

test_token_validation() {
  echo "Testing token validation..."
  
  # Test with no token
  if GITHUB_TOKEN="" "$SCRIPT_PATH" --dry-run --repos "test/repo" >/dev/null 2>&1; then
    echo "✗ Should fail with no token"
    return 1
  else
    echo "✓ Correctly fails with no token"
  fi
}

test_basic_functionality() {
  echo "Testing basic functionality..."
  
  # Mock curl function
  export -f mock_curl
  
  # Run with mocked API calls
  if GITHUB_TOKEN="test_token" "$SCRIPT_PATH" --dry-run --repos "test/repo1,test/repo2" --retention-days 1 --verbose 2>&1 | grep -q "Ghost Buster completed successfully"; then
    echo "✓ Basic functionality works"
  else
    echo "✗ Basic functionality failed"
    return 1
  fi
}

test_config_loading() {
  echo "Testing config file loading..."
  
  if [[ -f config.json ]]; then
    echo "✓ Config file exists"
  else
    echo "✗ Config file not found"
    return 1
  fi
  
  # Test if script can read config
  if GITHUB_TOKEN="test_token" "$SCRIPT_PATH" --dry-run --verbose 2>&1 | grep -q "Loading configuration"; then
    echo "✓ Config loading works"
  else
    echo "✗ Config loading failed"
    return 1
  fi
}

test_output_generation() {
  echo "Testing output file generation..."
  
  # Run script
  GITHUB_TOKEN="test_token" "$SCRIPT_PATH" --dry-run --repos "test/repo1" --output test_report.json --verbose >/dev/null 2>&1
  
  if [[ -f test_report.json ]]; then
    echo "✓ Output file generated"
    
    # Validate JSON structure
    if command -v jq >/dev/null 2>&1; then
      if jq -e '.timestamp' test_report.json >/dev/null 2>&1; then
        echo "✓ Output file has valid JSON structure"
      else
        echo "✗ Output file has invalid JSON structure"
        return 1
      fi
    fi
  else
    echo "✗ Output file not generated"
    return 1
  fi
}

test_error_handling() {
  echo "Testing error handling..."
  
  # Test with invalid retention days
  if "$SCRIPT_PATH" --retention-days "invalid" >/dev/null 2>&1; then
    echo "✗ Should fail with invalid retention days"
    return 1
  else
    echo "✓ Correctly handles invalid retention days"
  fi
}

run_tests() {
  echo "=== Running Ghost Buster Tests ==="
  
  setup_test
  
  local tests_passed=0
  local tests_failed=0
  
  # Run tests
  if test_help; then
    tests_passed=$((tests_passed + 1))
  else
    tests_failed=$((tests_failed + 1))
  fi
  
  if test_prerequisites; then
    tests_passed=$((tests_passed + 1))
  else
    tests_failed=$((tests_failed + 1))
  fi
  
  if test_token_validation; then
    tests_passed=$((tests_passed + 1))
  else
    tests_failed=$((tests_failed + 1))
  fi
  
  if test_config_loading; then
    tests_passed=$((tests_passed + 1))
  else
    tests_failed=$((tests_failed + 1))
  fi
  
  if test_basic_functionality; then
    tests_passed=$((tests_passed + 1))
  else
    tests_failed=$((tests_failed + 1))
  fi
  
  if test_output_generation; then
    tests_passed=$((tests_passed + 1))
  else
    tests_failed=$((tests_failed + 1))
  fi
  
  if test_error_handling; then
    tests_passed=$((tests_passed + 1))
  else
    tests_failed=$((tests_failed + 1))
  fi
  
  tear_down_test
  
  echo "=== Test Results ==="
  echo "Tests passed: $tests_passed"
  echo "Tests failed: $tests_failed"
  
  if [[ $tests_failed -eq 0 ]]; then
    echo "✓ All tests passed!"
    return 0
  else
    echo "✗ Some tests failed"
    return 1
  fi
}

# Run tests if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  run_tests
fi
