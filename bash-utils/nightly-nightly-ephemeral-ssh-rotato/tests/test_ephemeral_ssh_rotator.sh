#!/bin/bash

# Test suite for Nightly Ephemeral SSH Rotator
# Run with: bash tests/test_ephemeral_ssh_rotator.sh

set -euo pipefail

# Test configuration
TEST_DIR="/tmp/ephemeral_ssh_test_$$"
TEST_KEY_DIR="$TEST_DIR/.ephemeral_ssh"
TEST_LOG_FILE="$TEST_KEY_DIR/audit.log"
SCRIPT_PATH="$(cd "$(dirname "$0")/.." && pwd)/src/ephemeral_ssh_rotator.sh"

# Mock rationale: We mock ssh-keygen to avoid dependency on actual OpenSSH during testing
MOCK_SSH_KEYGEN="$TEST_DIR/mock_ssh_keygen"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test functions
print_test() {
    local color="$1"
    local message="$2"
    echo -e "${color}[TEST] $message${NC}"
}

pass() {
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
    print_test "$GREEN" "PASS: $1"
}

fail() {
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    print_test "$RED" "FAIL: $1"
}

# Setup test environment
setup() {
    print_test "$BLUE" "Setting up test environment..."
    
    # Create test directory
    mkdir -p "$TEST_DIR"
    mkdir -p "$TEST_KEY_DIR"
    
    # Create mock ssh-keygen
    cat > "$MOCK_SSH_KEYGEN" << 'EOF'
#!/bin/bash
# Mock ssh-keygen for testing
if [[ "$1" == "-t" && "$3" == "-b" && "$5" == "-f" ]]; then
    local output_file="$6"
    local pub_file="${output_file}.pub"
    
    # Create dummy private key file
    echo "-----BEGIN OPENSSH PRIVATE KEY-----" > "$output_file"
    echo "dummy_private_key_content" >> "$output_file"
    echo "-----END OPENSSH PRIVATE KEY-----" >> "$output_file"
    
    # Create dummy public key file
    echo "ssh-rsa AAAAB3NzaC1yc2E dummy_public_key" > "$pub_file"
    
    # Mock fingerprint output when -lf is used
    if [[ "$2" == "-lf" ]]; then
        echo "2048 SHA256:dummy_fingerprint $output_file (RSA)"
        exit 0
    fi
    
    exit 0
fi

echo "Mock ssh-keygen called with: $@" >&2
exit 1
EOF
    chmod +x "$MOCK_SSH_KEYGEN"
    
    # Set environment variables for testing
    export KEY_DIR="$TEST_KEY_DIR"
    export LOG_FILE="$TEST_LOG_FILE"
    export SSH_KEYGEN="$MOCK_SSH_KEYGEN"
    export KEY_TTL_HOURS=1  # Short TTL for testing
    
    print_test "$GREEN" "Test environment ready"
}

# Cleanup test environment
cleanup() {
    print_test "$BLUE" "Cleaning up test environment..."
    if [[ -d "$TEST_DIR" ]]; then
        rm -rf "$TEST_DIR"
    fi
    print_test "$GREEN" "Cleanup complete"
}

# Test help command
test_help() {
    print_test "$BLUE" "Testing help command..."
    
    if output=$(bash "$SCRIPT_PATH" help 2>&1); then
        if echo "$output" | grep -q "USAGE:" && echo "$output" | grep -q "generate"; then
            pass "Help command displays correctly"
        else
            fail "Help command output missing expected content"
        fi
    else
        fail "Help command failed to execute"
    fi
}

test_generate_key() {
    print_test "$BLUE" "Testing key generation..."
    
    # Count keys before
    local keys_before=$(find "$TEST_KEY_DIR" -name "ephemeral_key_*" 2>/dev/null | wc -l)
    
    if bash "$SCRIPT_PATH" generate >/dev/null 2>&1; then
        # Count keys after
        local keys_after=$(find "$TEST_KEY_DIR" -name "ephemeral_key_*" 2>/dev/null | wc -l)
        
        if [[ $keys_after -gt $keys_before ]]; then
            pass "Key generation creates new key files"
        else
            fail "Key generation did not create new files"
        fi
        
        # Check if log file was created
        if [[ -f "$TEST_LOG_FILE" ]] && grep -q "GENERATED" "$TEST_LOG_FILE"; then
            pass "Key generation logs to audit file"
        else
            fail "Key generation did not log to audit file"
        fi
    else
        fail "Key generation command failed"
    fi
}

test_list_keys() {
    print_test "$BLUE" "Testing list command..."
    
    # Generate a test key first
    bash "$SCRIPT_PATH" generate >/dev/null 2>&1
    
    if output=$(bash "$SCRIPT_PATH" list 2>&1); then
        if echo "$output" | grep -q "Ephemeral SSH keys"; then
            pass "List command displays key information"
        else
            fail "List command output missing expected content"
        fi
    else
        fail "List command failed"
    fi
}

test_cleanup_expired() {
    print_test "$BLUE" "Testing cleanup of expired keys..."
    
    # Create an old key file (simulate expiration)
    local old_key="$TEST_KEY_DIR/ephemeral_key_old"
    touch "$old_key"
    # Make it appear old by modifying timestamp
    touch -t $(date -d '2 days ago' '+%Y%m%d%H%M') "$old_key" 2>/dev/null || true
    
    local keys_before=$(find "$TEST_KEY_DIR" -name "ephemeral_key_*" 2>/dev/null | wc -l)
    
    if bash "$SCRIPT_PATH" cleanup >/dev/null 2>&1; then
        local keys_after=$(find "$TEST_KEY_DIR" -name "ephemeral_key_*" 2>/dev/null | wc -l)
        
        if [[ $keys_after -lt $keys_before ]]; then
            pass "Cleanup removes expired keys"
        else
            fail "Cleanup did not remove expired keys"
        fi
    else
        fail "Cleanup command failed"
    fi
}

test_rotate_keys() {
    print_test "$BLUE" "Testing key rotation..."
    
    local keys_before=$(find "$TEST_KEY_DIR" -name "ephemeral_key_*" 2>/dev/null | wc -l)
    
    if bash "$SCRIPT_PATH" rotate >/dev/null 2>&1; then
        local keys_after=$(find "$TEST_KEY_DIR" -name "ephemeral_key_*" 2>/dev/null | wc -l)
        
        # Should have at least one key (newly generated)
        if [[ $keys_after -ge 1 ]]; then
            pass "Rotate command generates new keys"
        else
            fail "Rotate command did not generate new keys"
        fi
    else
        fail "Rotate command failed"
    fi
}

test_log_display() {
    print_test "$BLUE" "Testing log display..."
    
    # Generate a key to create log entries
    bash "$SCRIPT_PATH" generate >/dev/null 2>&1
    
    if output=$(bash "$SCRIPT_PATH" log 2>&1); then
        if echo "$output" | grep -q "Audit log"; then
            pass "Log command displays audit log"
        else
            fail "Log command output missing expected content"
        fi
    else
        fail "Log command failed"
    fi
}

test_clear_log() {
    print_test "$BLUE" "Testing log clearing..."
    
    # Add some content to log
    echo "test entry" >> "$TEST_LOG_FILE"
    
    if bash "$SCRIPT_PATH" clear-log >/dev/null 2>&1; then
        if [[ ! -s "$TEST_LOG_FILE" ]]; then
            pass "Clear log command empties log file"
        else
            fail "Clear log command did not empty log file"
        fi
    else
        fail "Clear log command failed"
    fi
}

test_environment_variables() {
    print_test "$BLUE" "Testing environment variable usage..."
    
    # Test with custom KEY_TTL_HOURS
    local original_ttl="$KEY_TTL_HOURS"
    export KEY_TTL_HOURS=48
    
    if bash "$SCRIPT_PATH" help 2>&1 | grep -q "48"; then
        pass "Environment variables are respected"
    else
        fail "Environment variables not being used"
    fi
    
    # Restore original value
    export KEY_TTL_HOURS="$original_ttl"
}

test_error_handling() {
    print_test "$BLUE" "Testing error handling..."
    
    # Test unknown command
    if ! bash "$SCRIPT_PATH" unknown_command 2>&1 | grep -q "Unknown command"; then
        fail "Error handling for unknown command failed"
    else
        pass "Error handling for unknown command works"
    fi
}

# Run all tests
run_tests() {
    print_test "$BLUE" "Running test suite..."
    echo
    
    test_help
    test_generate_key
    test_list_keys
    test_cleanup_expired
    test_rotate_keys
    test_log_display
    test_clear_log
    test_environment_variables
    test_error_handling
    
    echo
    print_test "$BLUE" "Test Results:"
    print_test "$GREEN" "  Passed: $TESTS_PASSED"
    print_test "$RED" "  Failed: $TESTS_FAILED"
    print_test "$BLUE" "  Total:  $TESTS_RUN"
    
    if [[ $TESTS_FAILED -eq 0 ]]; then
        print_test "$GREEN" "All tests passed! ✓"
        return 0
    else
        print_test "$RED" "Some tests failed! ✗"
        return 1
    fi
}

# Main execution
main() {
    setup
    run_tests
    local exit_code=$?
    cleanup
    exit $exit_code
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
