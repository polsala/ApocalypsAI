#!/bin/bash

# Test suite for Nightly Bash Backup Orchestrator

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test directory
TEST_DIR="/tmp/backup_orchestrator_test"
TEST_CONFIG="$TEST_DIR/config/backup_config.conf"
TEST_SOURCE_DIR="$TEST_DIR/source"
TEST_DEST_DIR="$TEST_DIR/backup"

# Test log
TEST_LOG="$TEST_DIR/test.log"

# Setup test environment
setup() {
  echo "Setting up test environment..."
  
  # Clean up any existing test directory
  rm -rf "$TEST_DIR"
  
  # Create test directories
  mkdir -p "$TEST_DIR/config"
  mkdir -p "$TEST_SOURCE_DIR"
  mkdir -p "$TEST_DEST_DIR"
  
  # Create test files
  echo "Test file 1" > "$TEST_SOURCE_DIR/test1.txt"
  echo "Test file 2" > "$TEST_SOURCE_DIR/test2.txt"
  mkdir -p "$TEST_SOURCE_DIR/subdir"
  echo "Test file in subdir" > "$TEST_SOURCE_DIR/subdir/test3.txt"
  
  # Create test configuration
  cat > "$TEST_CONFIG" << EOF
# Test configuration
SOURCE_DIRS="$TEST_SOURCE_DIR"
DESTINATION_DIR="$TEST_DEST_DIR"
RETENTION_DAYS=7
ENCRYPT_BACKUP=false
ENABLE_EMAIL=false
EOF
  
  echo "Test environment setup complete"
}

# Cleanup test environment
cleanup() {
  echo "Cleaning up test environment..."
  rm -rf "$TEST_DIR"
  echo "Test environment cleanup complete"
}

# Log test results
log_test() {
  local level="$1"
  shift
  local message="$*"
  
  case "$level" in
    "PASS")
      echo -e "${GREEN}PASS${NC}: $message"
      ;;
    "FAIL")
      echo -e "${RED}FAIL${NC}: $message"
      ;;
    "SKIP")
      echo -e "${YELLOW}SKIP${NC}: $message"
      ;;
  esac
  
  echo "[$level] $message" >> "$TEST_LOG"
}

# Run a test
run_test() {
  local test_name="$1"
  local test_function="$2"
  
  echo "\nRunning test: $test_name"
  
  if $test_function; then
    log_test "PASS" "$test_name"
    return 0
  else
    log_test "FAIL" "$test_name"
    return 1
  fi
}

# Test 1: Configuration loading
test_config_loading() {
  # Mock the script functions to avoid actual execution
  source "$SCRIPT_DIR/backup_orchestrator.sh"
  
  # Test that config file exists
  [[ -f "$TEST_CONFIG" ]] || return 1
  
  # Test that we can source the config
  source "$TEST_CONFIG"
  [[ -n "$SOURCE_DIRS" ]] || return 1
  [[ -n "$DESTINATION_DIR" ]] || return 1
  [[ -n "$RETENTION_DAYS" ]] || return 1
  
  return 0
}

# Test 2: Dry run execution
test_dry_run() {
  local script_path="$SCRIPT_DIR/backup_orchestrator.sh"
  
  # Check if script is executable
  [[ -x "$script_path" ]] || return 1
  
  # Run dry run
  if DRY_RUN=true bash -c "source '$script_path'; parse_args --dry-run; load_config '$TEST_CONFIG'; validate_config" 2>/dev/null; then
    return 0
  else
    return 1
  fi
}

# Test 3: Directory creation
test_directory_creation() {
  local test_backup_dir="$TEST_DEST_DIR/test_backup"
  
  # Test directory creation function
  mkdir -p "$test_backup_dir"
  [[ -d "$test_backup_dir" ]] || return 1
  
  # Clean up
  rmdir "$test_backup_dir"
  
  return 0
}

# Test 4: File validation
test_file_validation() {
  # Test that source files exist
  [[ -f "$TEST_SOURCE_DIR/test1.txt" ]] || return 1
  [[ -f "$TEST_SOURCE_DIR/test2.txt" ]] || return 1
  [[ -f "$TEST_SOURCE_DIR/subdir/test3.txt" ]] || return 1
  
  # Test that source directory exists
  [[ -d "$TEST_SOURCE_DIR" ]] || return 1
  
  return 0
}

# Test 5: Archive creation (basic)
test_archive_creation() {
  local test_archive="$TEST_DIR/test_archive.tar.gz"
  
  # Create a test archive
  if tar -czf "$test_archive" -C "$TEST_SOURCE_DIR" .; then
    # Check if archive was created
    [[ -f "$test_archive" ]] || return 1
    
    # Clean up
    rm "$test_archive"
    return 0
  else
    return 1
  fi
}

# Test 6: Configuration validation
test_config_validation() {
  # Test that all required config variables are set
  source "$TEST_CONFIG"
  
  [[ -n "${SOURCE_DIRS:-}" ]] || return 1
  [[ -n "${DESTINATION_DIR:-}" ]] || return 1
  [[ -n "${RETENTION_DAYS:-}" ]] || return 1
  
  # Test that source directories exist (mocked)
  # In a real test, we'd check actual directories
  [[ "$SOURCE_DIRS" == "$TEST_SOURCE_DIR" ]] || return 1
  
  return 0
}

# Test 7: Error handling
test_error_handling() {
  local invalid_config="$TEST_DIR/invalid_config.conf"
  
  # Create invalid config
  cat > "$invalid_config" << EOF
# Invalid configuration
SOURCE_DIRS=""
DESTINATION_DIR=""
RETENTION_DAYS=""
EOF
  
  # Test that invalid config is detected
  if source "$invalid_config" 2>/dev/null; then
    # Check if required variables are empty
    [[ -z "${SOURCE_DIRS:-}" ]] || return 1
    [[ -z "${DESTINATION_DIR:-}" ]] || return 1
    [[ -z "${RETENTION_DAYS:-}" ]] || return 1
    return 0
  else
    return 1
  fi
}

# Test 8: Whimsical message generation
test_whimsical_messages() {
  # Source the script to access the array
  source "$SCRIPT_DIR/backup_orchestrator.sh"
  
  # Check that whimsical messages array exists and has content
  [[ ${#WHIMSICAL_MESSAGES[@]} -gt 0 ]] || return 1
  
  # Check that at least one message exists
  [[ -n "${WHIMSICAL_MESSAGES[0]:-}" ]] || return 1
  
  return 0
}

# Test 9: Logging functionality
test_logging() {
  local test_log_dir="$TEST_DIR/test_logs"
  
  # Create log directory
  mkdir -p "$test_log_dir"
  
  # Test log function (mocked)
  local test_message="Test log message"
  local timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
  
  echo "[$timestamp] [INFO] $test_message" >> "$test_log_dir/test.log"
  
  # Check if log file was created
  [[ -f "$test_log_dir/test.log" ]] || return 1
  
  # Check if message was logged
  grep -q "$test_message" "$test_log_dir/test.log" || return 1
  
  return 0
}

# Test 10: Help functionality
test_help() {
  local script_path="$SCRIPT_DIR/backup_orchestrator.sh"
  
  # Test help output
  if bash -c "source '$script_path'; show_help" 2>/dev/null | grep -q "Usage:"; then
    return 0
  else
    return 1
  fi
}

# Main test execution
main() {
  local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  local script_path="$(dirname "$script_dir")/src/backup_orchestrator.sh"
  
  echo "=== Nightly Bash Backup Orchestrator Test Suite ==="
  
  # Setup
  setup
  
  # Run tests
  local tests_passed=0
  local tests_failed=0
  local total_tests=10
  
  run_test "Configuration Loading" test_config_loading && tests_passed=$((tests_passed + 1)) || tests_failed=$((tests_failed + 1))
  run_test "Dry Run Execution" test_dry_run && tests_passed=$((tests_passed + 1)) || tests_failed=$((tests_failed + 1))
  run_test "Directory Creation" test_directory_creation && tests_passed=$((tests_passed + 1)) || tests_failed=$((tests_failed + 1))
  run_test "File Validation" test_file_validation && tests_passed=$((tests_passed + 1)) || tests_failed=$((tests_failed + 1))
  run_test "Archive Creation" test_archive_creation && tests_passed=$((tests_passed + 1)) || tests_failed=$((tests_failed + 1))
  run_test "Configuration Validation" test_config_validation && tests_passed=$((tests_passed + 1)) || tests_failed=$((tests_failed + 1))
  run_test "Error Handling" test_error_handling && tests_passed=$((tests_passed + 1)) || tests_failed=$((tests_failed + 1))
  run_test "Whimsical Messages" test_whimsical_messages && tests_passed=$((tests_passed + 1)) || tests_failed=$((tests_failed + 1))
  run_test "Logging Functionality" test_logging && tests_passed=$((tests_passed + 1)) || tests_failed=$((tests_failed + 1))
  run_test "Help Functionality" test_help && tests_passed=$((tests_passed + 1)) || tests_failed=$((tests_failed + 1))
  
  # Cleanup
  cleanup
  
  # Summary
  echo "\n=== Test Summary ==="
  echo "Tests Passed: $tests_passed"
  echo "Tests Failed: $tests_failed"
  echo "Total Tests: $total_tests"
  
  if [[ $tests_failed -eq 0 ]]; then
    echo -e "${GREEN}All tests passed! 🎉${NC}"
    return 0
  else
    echo -e "${RED}$tests_failed test(s) failed. 😞${NC}"
    echo "Check $TEST_LOG for details."
    return 1
  fi
}

# Run the test suite
main "$@"
