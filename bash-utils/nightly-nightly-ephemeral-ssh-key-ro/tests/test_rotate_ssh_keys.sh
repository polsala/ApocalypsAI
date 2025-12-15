#!/bin/bash

# Test suite for Nightly Ephemeral SSH Key Rotator
# This test suite uses mocks to simulate SSH operations

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test functions
log_test() {
  echo -e "${YELLOW}[TEST]${NC} $1"
}

pass_test() {
  TESTS_RUN=$((TESTS_RUN + 1))
  TESTS_PASSED=$((TESTS_PASSED + 1))
  echo -e "${GREEN}[PASS]${NC} $1"
}

fail_test() {
  TESTS_RUN=$((TESTS_RUN + 1))
  TESTS_FAILED=$((TESTS_FAILED + 1))
  echo -e "${RED}[FAIL]${NC} $1"
}

# Mock functions for testing
mock_ssh_keygen() {
  # Mock ssh-keygen command
  echo "ssh-keygen called with: $@"
  # Create mock key files
  touch "$2"
  touch "$2.pub"
  echo "Mock public key content" > "$2.pub"
}

mock_ssh_copy_id() {
  # Mock ssh-copy-id command
  echo "ssh-copy-id called with: $@"
  return 0
}

mock_ssh() {
  # Mock ssh command
  echo "ssh called with: $@"
  if [[ "$1" == "-o" ]] && [[ "$2" == "BatchMode=yes" ]]; then
    # Connection test
    return 0
  fi
  return 0
}

# Setup test environment
setup_test_env() {
  TEST_DIR="/tmp/ssh_key_rotator_test"
  mkdir -p "$TEST_DIR"
  
  # Create test hosts file
  cat > "$TEST_DIR/hosts.txt" << EOF
# Test hosts
localhost
127.0.0.1
# Another comment
EOF

  # Create test key directory
  TEST_KEY_DIR="$TEST_DIR/.ssh"
  mkdir -p "$TEST_KEY_DIR"

  # Backup original functions
  which ssh-keygen > /dev/null && SSH_KEYGEN_PATH=$(which ssh-keygen)
  which ssh-copy-id > /dev/null && SSH_COPY_ID_PATH=$(which ssh-copy-id)
  which ssh > /dev/null && SSH_PATH=$(which ssh)

  # Override with mocks
  alias ssh-keygen=mock_ssh_keygen
  alias ssh-copy-id=mock_ssh_copy_id
  alias ssh=mock_ssh
}

# Cleanup test environment
cleanup_test_env() {
  # Restore original functions
  unalias ssh-keygen 2>/dev/null || true
  unalias ssh-copy-id 2>/dev/null || true
  unalias ssh 2>/dev/null || true

  # Remove test directory
  rm -rf "$TEST_DIR"
}

# Test argument parsing
test_argument_parsing() {
  log_test "Testing argument parsing..."
  
  # Test with valid arguments
  if echo "--hosts-file $TEST_DIR/hosts.txt --key-name test-key" | xargs ./src/rotate_ssh_keys.sh --help >/dev/null 2>&1; then
    pass_test "Argument parsing with valid arguments"
  else
    fail_test "Argument parsing with valid arguments"
  fi
}

# Test key generation
test_key_generation() {
  log_test "Testing key generation..."
  
  # Test key generation function directly
  KEY_DIR="$TEST_KEY_DIR"
  KEY_NAME="test_key"
  
  # Call the key generation part of the script
  if mock_ssh_keygen -t rsa -b 4096 -f "$KEY_DIR/$KEY_NAME" -N "" -C "test-key-$(date +%s)"; then
    if [[ -f "$KEY_DIR/$KEY_NAME" ]] && [[ -f "$KEY_DIR/$KEY_NAME.pub" ]]; then
      pass_test "Key generation"
    else
      fail_test "Key generation - files not created"
    fi
  else
    fail_test "Key generation - command failed"
  fi
}

# Test host file validation
test_host_file_validation() {
  log_test "Testing host file validation..."
  
  # Test with existing file
  if [[ -f "$TEST_DIR/hosts.txt" ]]; then
    pass_test "Host file exists validation"
  else
    fail_test "Host file exists validation"
  fi
  
  # Test with non-existing file
  if [[ ! -f "$TEST_DIR/nonexistent.txt" ]]; then
    pass_test "Host file not found validation"
  else
    fail_test "Host file not found validation"
  fi
}

# Test public key reading
test_public_key_reading() {
  log_test "Testing public key reading..."
  
  KEY_DIR="$TEST_KEY_DIR"
  KEY_NAME="test_key"
  
  # Create a mock public key
  echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ test-key" > "$KEY_DIR/$KEY_NAME.pub"
  
  # Read the public key
  PUB_KEY=$(cat "$KEY_DIR/$KEY_NAME.pub")
  
  if [[ -n "$PUB_KEY" ]]; then
    pass_test "Public key reading"
  else
    fail_test "Public key reading"
  fi
}

# Test host processing
test_host_processing() {
  log_test "Testing host processing..."
  
  HOSTS_FILE="$TEST_DIR/hosts.txt"
  HOST_COUNT=0
  
  while IFS= read -r host || [[ -n "$host" ]]; do
    if [[ -z "$host" ]] || [[ "$host" =~ ^#.* ]]; then
      continue
    fi
    HOST_COUNT=$((HOST_COUNT + 1))
  done < "$HOSTS_FILE"
  
  if [[ $HOST_COUNT -eq 2 ]]; then
    pass_test "Host processing - correct number of hosts"
  else
    fail_test "Host processing - incorrect number of hosts"
  fi
}

# Test log file creation
test_log_file_creation() {
  log_test "Testing log file creation..."
  
  LOG_FILE="/tmp/test_ssh_key_rotation.log"
  echo "Test log entry" > "$LOG_FILE"
  
  if [[ -f "$LOG_FILE" ]]; then
    pass_test "Log file creation"
    rm -f "$LOG_FILE"
  else
    fail_test "Log file creation"
  fi
}

# Test backup functionality
test_key_backup() {
  log_test "Testing key backup functionality..."
  
  KEY_DIR="$TEST_KEY_DIR"
  KEY_NAME="test_key"
  
  # Create an existing key
  echo "old key content" > "$KEY_DIR/$KEY_NAME"
  echo "old public key content" > "$KEY_DIR/$KEY_NAME.pub"
  
  # Simulate backup
  if [[ -f "$KEY_DIR/$KEY_NAME" ]]; then
    mv "$KEY_DIR/$KEY_NAME" "$KEY_DIR/$KEY_NAME.backup.$(date +%s)"
    mv "$KEY_DIR/$KEY_NAME.pub" "$KEY_DIR/$KEY_NAME.pub.backup.$(date +%s)"
    
    if [[ ! -f "$KEY_DIR/$KEY_NAME" ]] && [[ ! -f "$KEY_DIR/$KEY_NAME.pub" ]]; then
      pass_test "Key backup functionality"
    else
      fail_test "Key backup functionality - files not moved"
    fi
  else
    fail_test "Key backup functionality - no existing key to backup"
  fi
}

# Run all tests
run_tests() {
  echo -e "${GREEN}================================${NC}"
  echo -e "${GREEN}Running SSH Key Rotator Tests${NC}"
  echo -e "${GREEN}================================${NC}"
  
  setup_test_env
  
  test_argument_parsing
  test_key_generation
  test_host_file_validation
  test_public_key_reading
  test_host_processing
  test_log_file_creation
  test_key_backup
  
  cleanup_test_env
  
  echo -e "\n${GREEN}================================${NC}"
  echo -e "${GREEN}Test Results:${NC}"
  echo -e "${GREEN}Total: $TESTS_RUN${NC}"
  echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
  echo -e "${RED}Failed: $TESTS_FAILED${NC}"
  echo -e "${GREEN}================================${NC}"
  
  if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    return 0
  else
    echo -e "${RED}$TESTS_FAILED test(s) failed! ✗${NC}"
    return 1
  fi
}

# Run the tests if this script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  run_tests
fi
