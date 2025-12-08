#!/bin/bash

# Test suite for Nightly Bash Backup Buddy

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

# Test functions
log_info() {
  echo -e "${BLUE}[TEST]${NC} $1"
}

log_pass() {
  echo -e "${GREEN}[PASS]${NC} $1"
  ((TESTS_PASSED++))
}

log_fail() {
  echo -e "${RED}[FAIL]${NC} $1"
  ((TESTS_FAILED++))
}

# Setup test environment
setup_test_env() {
  TEST_DIR="/tmp/backup_buddy_test_$$"
  TEST_SOURCE_DIR="$TEST_DIR/source"
  TEST_BACKUP_DIR="$TEST_DIR/backups"
  TEST_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  TEST_SCRIPT="$TEST_SCRIPT_DIR/src/main.sh"
  
  mkdir -p "$TEST_SOURCE_DIR"
  mkdir -p "$TEST_BACKUP_DIR"
  
  # Create test files
  echo "Test content 1" > "$TEST_SOURCE_DIR/file1.txt"
  echo "Test content 2" > "$TEST_SOURCE_DIR/file2.txt"
  mkdir -p "$TEST_SOURCE_DIR/subdir"
  echo "Test content 3" > "$TEST_SOURCE_DIR/subdir/file3.txt"
  
  log_info "Test environment created at: $TEST_DIR"
}

# Cleanup test environment
cleanup_test_env() {
  if [[ -d "$TEST_DIR" ]]; then
    rm -rf "$TEST_DIR"
    log_info "Test environment cleaned up"
  fi
}

# Run test with trap for cleanup
run_test() {
  local test_name="$1"
  local test_func="$2"
  
  ((TESTS_TOTAL++))
  log_info "Running: $test_name"
  
  # Setup trap to cleanup on exit
  trap cleanup_test_env EXIT
  
  if $test_func; then
    log_pass "$test_name"
  else
    log_fail "$test_name"
  fi
}

# Test help output
test_help() {
  if $TEST_SCRIPT --help > /dev/null 2>&1; then
    return 0
  else
    return 1
  fi
}

# Test dry run
test_dry_run() {
  local output
  output=$(mktemp)
  
  if $TEST_SCRIPT --dry-run "$TEST_SOURCE_DIR" "$TEST_BACKUP_DIR" > "$output" 2>&1; then
    # Check if dry run message is present
    if grep -q "DRY RUN" "$output"; then
      rm -f "$output"
      return 0
    fi
  fi
  
  rm -f "$output"
  return 1
}

# Test valid compression levels
test_valid_compress_levels() {
  local level
  for level in 1 3 6 9; do
    if ! $TEST_SCRIPT --compress $level --dry-run "$TEST_SOURCE_DIR" "$TEST_BACKUP_DIR" > /dev/null 2>&1; then
      return 1
    fi
  done
  return 0
}

# Test invalid compression levels
test_invalid_compress_levels() {
  local level
  for level in 0 10 abc -5; do
    if $TEST_SCRIPT --compress $level --dry-run "$TEST_SOURCE_DIR" "$TEST_BACKUP_DIR" > /dev/null 2>&1; then
      # Should have failed
      return 1
    fi
  done
  return 0
}

# Test missing arguments
test_missing_arguments() {
  # No arguments
  if $TEST_SCRIPT > /dev/null 2>&1; then
    return 1
  fi
  
  # Only source
  if $TEST_SCRIPT "$TEST_SOURCE_DIR" > /dev/null 2>&1; then
    return 1
  fi
  
  return 0
}

# Test non-existent source directory
test_nonexistent_source() {
  local nonexistent_dir="$TEST_DIR/nonexistent"
  
  if [[ -d "$nonexistent_dir" ]]; then
    return 1
  fi
  
  if $TEST_SCRIPT "$nonexistent_dir" "$TEST_BACKUP_DIR" > /dev/null 2>&1; then
    return 1
  fi
  
  return 0
}

# Test backup creation and validation
test_backup_creation() {
  local archive_count
  
  # Count archives before
  archive_count=$(find "$TEST_BACKUP_DIR" -name "*.tar.gz" | wc -l)
  
  if ! $TEST_SCRIPT "$TEST_SOURCE_DIR" "$TEST_BACKUP_DIR" > /dev/null 2>&1; then
    return 1
  fi
  
  # Count archives after
  local new_archive_count=$(find "$TEST_BACKUP_DIR" -name "*.tar.gz" | wc -l)
  
  if [[ $new_archive_count -le $archive_count ]]; then
    return 1
  fi
  
  # Find the newest archive
  local newest_archive=$(find "$TEST_BACKUP_DIR" -name "*.tar.gz" -type f | head -1)
  
  if [[ -z "$newest_archive" ]]; then
    return 1
  fi
  
  # Verify archive contents
  if ! tar -tzf "$newest_archive" > /dev/null 2>&1; then
    return 1
  fi
  
  # Verify checksum file exists
  local checksum_file="$newest_archive.sha256"
  if [[ ! -f "$checksum_file" ]]; then
    return 1
  fi
  
  return 0
}

# Test multiple backups
test_multiple_backups() {
  local i
  
  for i in 1 2 3; do
    if ! $TEST_SCRIPT "$TEST_SOURCE_DIR" "$TEST_BACKUP_DIR" > /dev/null 2>&1; then
      return 1
    fi
  done
  
  # Should have 3 archives
  local archive_count=$(find "$TEST_BACKUP_DIR" -name "*.tar.gz" | wc -l)
  
  if [[ $archive_count -ne 3 ]]; then
    return 1
  fi
  
  return 0
}

# Test script execution permissions
test_script_permissions() {
  if [[ -x "$TEST_SCRIPT" ]]; then
    return 0
  else
    return 1
  fi
}

# Test required dependencies
test_dependencies() {
  local deps=("tar" "gzip" "sha256sum")
  local dep
  
  for dep in "${deps[@]}"; do
    if ! command -v "$dep" > /dev/null 2>&1; then
      log_fail "Missing dependency: $dep"
      return 1
    fi
  done
  
  return 0
}

# Mock functions for isolated testing
mock_tar_fail() {
  # Mock tar to always fail
  alias tar='echo "tar failed" >&2; false'
}

mock_sha256sum_fail() {
  # Mock sha256sum to always fail
  alias sha256sum='echo "sha256sum failed" >&2; false'
}

# Test error handling
test_error_handling() {
  # Mock tar to fail
  mock_tar_fail
  
  if $TEST_SCRIPT "$TEST_SOURCE_DIR" "$TEST_BACKUP_DIR" > /dev/null 2>&1; then
    # Should have failed
    unalias tar
    return 1
  fi
  
  unalias tar
  return 0
}

# Main test runner
main() {
  echo "======================================="
  echo "Nightly Bash Backup Buddy - Test Suite"
  echo "=======================================\n"
  
  # Check dependencies first
  if ! test_dependencies; then
    echo -e "${RED}Missing required dependencies. Cannot run tests.${NC}"
    exit 1
  fi
  
  # Setup test environment
  setup_test_env
  
  # Run tests
  run_test "Help output" test_help
  run_test "Dry run mode" test_dry_run
  run_test "Valid compression levels" test_valid_compress_levels
  run_test "Invalid compression levels" test_invalid_compress_levels
  run_test "Missing arguments" test_missing_arguments
  run_test "Non-existent source directory" test_nonexistent_source
  run_test "Backup creation and validation" test_backup_creation
  run_test "Multiple backups" test_multiple_backups
  run_test "Script permissions" test_script_permissions
  run_test "Error handling" test_error_handling
  
  # Cleanup
  cleanup_test_env
  
  # Print results
  echo
  echo "======================================="
  echo "Test Results"
  echo "======================================="
  echo "Total tests: $TESTS_TOTAL"
  echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
  echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
  
  if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "\n${GREEN}All tests passed! 🎉${NC}"
    exit 0
  else
    echo -e "\n${RED}Some tests failed! 😞${NC}"
    exit 1
  fi
}

# Run tests if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
