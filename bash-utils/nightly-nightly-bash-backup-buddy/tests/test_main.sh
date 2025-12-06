#!/bin/bash

# Test suite for Nightly Bash Backup Buddy
# Run with: bash tests/test_main.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test configuration
TEST_DIR="/tmp/backup_buddy_test"
TEST_SOURCE="$TEST_DIR/source"
TEST_BACKUP="$TEST_DIR/backups"
SCRIPT_PATH="$(cd "$(dirname \"$0\")/.." && pwd)/src/main.sh"

# Mock functions for testing
mock_tar() {
  # Mock tar command for testing
  if [[ $1 == "-czf" ]]; then
    # Create an empty file to simulate tar.gz
    touch "$2"
    return 0
  fi
  return 1
}

# Print colored output
print_test() {
  echo -e "${BLUE}[TEST]${NC} $*"
}

print_pass() {
  echo -e "${GREEN}[PASS]${NC} $*"
}

print_fail() {
  echo -e "${RED}[FAIL]${NC} $*"
}

# Setup test environment
setup() {
  print_test "Setting up test environment..."
  
  # Clean up any existing test directory
  if [[ -d "$TEST_DIR" ]]; then
    rm -rf "$TEST_DIR"
  fi
  
  # Create test directories
  mkdir -p "$TEST_SOURCE/subdir"
  mkdir -p "$TEST_BACKUP"
  
  # Create test files
  echo "Test file content" > "$TEST_SOURCE/test_file.txt"
  echo "Subdirectory file" > "$TEST_SOURCE/subdir/nested_file.txt"
  echo "Important data" > "$TEST_SOURCE/critical.txt"
  
  print_test "Test environment ready"
}

# Cleanup test environment
cleanup() {
  print_test "Cleaning up test environment..."
  if [[ -d "$TEST_DIR" ]]; then
    rm -rf "$TEST_DIR"
  fi
}

# Test 1: Basic directory backup
test_basic_backup() {
  print_test "Test 1: Basic directory backup"
  
  local result=0
  if bash "$SCRIPT_PATH" "$TEST_SOURCE" "$TEST_BACKUP"; then
    # Check if backup directory was created
    local backup_dirs
    backup_dirs=$(find "$TEST_BACKUP" -name "backup_*" -type d | wc -l)
    
    if [[ $backup_dirs -eq 1 ]]; then
      print_pass "Basic backup created successfully"
    else
      print_fail "Expected 1 backup directory, found $backup_dirs"
      result=1
    fi
  else
    print_fail "Basic backup failed"
    result=1
  fi
  
  return $result
}

# Test 2: Compressed backup
test_compressed_backup() {
  print_test "Test 2: Compressed backup"
  
  local result=0
  if bash "$SCRIPT_PATH" --compress "$TEST_SOURCE" "$TEST_BACKUP"; then
    # Check if compressed backup was created
    local backup_files
    backup_files=$(find "$TEST_BACKUP" -name "backup_*.tar.gz" | wc -l)
    
    if [[ $backup_files -eq 1 ]]; then
      print_pass "Compressed backup created successfully"
    else
      print_fail "Expected 1 compressed backup file, found $backup_files"
      result=1
    fi
  else
    print_fail "Compressed backup failed"
    result=1
  fi
  
  return $result
}

# Test 3: Dry run mode
test_dry_run() {
  print_test "Test 3: Dry run mode"
  
  local result=0
  
  # Count backups before dry run
  local backups_before
  backups_before=$(find "$TEST_BACKUP" -name "backup_*" | wc -l)
  
  if bash "$SCRIPT_PATH" --dry-run "$TEST_SOURCE" "$TEST_BACKUP"; then
    # Count backups after dry run
    local backups_after
    backups_after=$(find "$TEST_BACKUP" -name "backup_*" | wc -l)
    
    if [[ $backups_before -eq $backups_after ]]; then
      print_pass "Dry run mode works correctly (no backups created)"
    else
      print_fail "Dry run created backups when it shouldn't"
      result=1
    fi
  else
    print_fail "Dry run failed"
    result=1
  fi
  
  return $result
}

# Test 4: Retention policy
test_retention_policy() {
  print_test "Test 4: Retention policy"
  
  local result=0
  
  # Create multiple backups to test retention
  for i in {1..7}; do
    bash "$SCRIPT_PATH" --retention 5 "$TEST_SOURCE" "$TEST_BACKUP" > /dev/null 2>&1 || true
    sleep 1 # Ensure different timestamps
  done
  
  # Count final backups
  local backup_count
  backup_count=$(find "$TEST_BACKUP" -name "backup_*" -type d | wc -l)
  
  if [[ $backup_count -le 5 ]]; then
    print_pass "Retention policy works (kept $backup_count backups, max 5)"
  else
    print_fail "Retention policy failed (kept $backup_count backups, expected ≤5)"
    result=1
  fi
  
  return $result
}

# Test 5: Invalid arguments
test_invalid_arguments() {
  print_test "Test 5: Invalid arguments"
  
  local result=0
  
  # Test with no arguments
  if bash "$SCRIPT_PATH" 2>&1 | grep -q "Usage:"; then
    print_pass "Correctly rejects missing arguments"
  else
    print_fail "Should reject missing arguments"
    result=1
  fi
  
  # Test with invalid retention
  if bash "$SCRIPT_PATH" --retention abc "$TEST_SOURCE" "$TEST_BACKUP" 2>&1 | grep -q "positive integer"; then
    print_pass "Correctly rejects invalid retention value"
  else
    print_fail "Should reject invalid retention value"
    result=1
  fi
  
  return $result
}

# Test 6: Non-existent source directory
test_nonexistent_source() {
  print_test "Test 6: Non-existent source directory"
  
  local result=0
  
  if ! bash "$SCRIPT_PATH" "/nonexistent/path" "$TEST_BACKUP" 2>&1 | grep -q "does not exist"; then
    print_fail "Should detect non-existent source directory"
    result=1
  else
    print_pass "Correctly detects non-existent source directory"
  fi
  
  return $result
}

# Test 7: Help option
test_help() {
  print_test "Test 7: Help option"
  
  local result=0
  
  if bash "$SCRIPT_PATH" --help 2>&1 | grep -q "USAGE:\|DESCRIPTION:\|OPTIONS:"; then
    print_pass "Help option displays correctly"
  else
    print_fail "Help option not working"
    result=1
  fi
  
  return $result
}

# Run all tests
run_tests() {
  print_test "Running Nightly Bash Backup Buddy test suite..."
  echo
  
  local passed=0
  local failed=0
  
  # Test 1
  if test_basic_backup; then
    ((passed++))
  else
    ((failed++))
  fi
  
  # Test 2
  if test_compressed_backup; then
    ((passed++))
  else
    ((failed++))
  fi
  
  # Test 3
  if test_dry_run; then
    ((passed++))
  else
    ((failed++))
  fi
  
  # Test 4
  if test_retention_policy; then
    ((passed++))
  else
    ((failed++))
  fi
  
  # Test 5
  if test_invalid_arguments; then
    ((passed++))
  else
    ((failed++))
  fi
  
  # Test 6
  if test_nonexistent_source; then
    ((passed++))
  else
    ((failed++))
  fi
  
  # Test 7
  if test_help; then
    ((passed++))
  else
    ((failed++))
  fi
  
  echo
  print_test "Test Results:"
  print_test "  Passed: $passed"
  print_test "  Failed: $failed"
  print_test "  Total:  $((passed + failed))"
  
  if [[ $failed -eq 0 ]]; then
    print_pass "All tests passed! 🎉"
    return 0
  else
    print_fail "$failed test(s) failed"
    return 1
  fi
}

# Main execution
main() {
  # Trap cleanup on exit
  trap cleanup EXIT
  
  # Setup and run tests
  setup
  run_tests
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
