#!/bin/bash

# Mock rsync command
# Mock rationale: This mock replaces the actual 'rsync' command to allow for deterministic, offline testing.
# It captures the arguments passed to rsync and stores them for assertion.
_mock_rsync() {
    echo "MOCK_RSYNC_CALLED: $@" >> /tmp/mock_rsync.log
    # Simulate success
    return 0
}

# Function to set up the test environment
setup() {
    echo "Setting up test environment..."
    # Create dummy source directory and files
    mkdir -p /tmp/source_configs/
    touch /tmp/source_configs/bashrc
    touch /tmp/source_configs/vimrc
    
    # Clear mock log
    > /tmp/mock_rsync.log
    
    # Replace actual rsync with mock
    alias rsync='_mock_rsync'
}

# Function to tear down the test environment
teardown() {
    echo "Tearing down test environment..."
    # Clean up dummy files and directories
    rm -rf /tmp/source_configs/
    rm -rf /tmp/mock_rsync.log
    
    # Remove the alias
    unalias rsync
}

# Test case: Basic sync to multiple hosts
test_basic_sync() {
    echo "Running test_basic_sync..."
    setup
    
    # Source the script to be tested
    # Mock rationale: Sourcing allows the script's variables and functions to be available in the test environment.
    source src/sync_configs.sh
    
    # Assertions
    if grep -q "MOCK_RSYNC_CALLED: -avz --delete /tmp/source_configs/ test_user@host1:/tmp/dest_configs/" /tmp/mock_rsync.log; then
        echo "PASS: rsync called correctly for host1."
    else
        echo "FAIL: rsync not called correctly for host1."
        return 1
    fi
    
    if grep -q "MOCK_RSYNC_CALLED: -avz --delete /tmp/source_configs/ test_user@host2:/tmp/dest_configs/" /tmp/mock_rsync.log; then
        echo "PASS: rsync called correctly for host2."
    else
        echo "FAIL: rsync not called correctly for host2."
        return 1
    fi
    
    if grep -q "MOCK_RSYNC_CALLED: -avz --delete /tmp/source_configs/ test_user@host3:/tmp/dest_configs/" /tmp/mock_rsync.log; then
        echo "PASS: rsync called correctly for host3."
    else
        echo "FAIL: rsync not called correctly for host3."
        return 1
    fi
    
    # Check for completion message
    if grep -q "Configuration synchronization complete." <<< "$(tail -n 10 /tmp/mock_rsync.log)"; then
        echo "PASS: Completion message found."
    else
        echo "FAIL: Completion message not found."
        return 1
    fi
    
    teardown
    return 0
}

# Test case: Source directory not found
test_source_dir_not_found() {
    echo "Running test_source_dir_not_found..."
    setup
    
    # Temporarily remove the source directory
    rm -rf /tmp/source_configs/
    
    # Source the script and capture output
    # Mock rationale: Redirecting stdout and stderr to capture script output for assertion.
    output=$(source src/sync_configs.sh 2>&1)
    
    # Assertions
    if echo "$output" | grep -q "Error: Source directory '/tmp/source_configs/' not found."; then
        echo "PASS: Correct error message for missing source directory."
    else
        echo "FAIL: Incorrect or missing error message for missing source directory."
        echo "Output: $output"
        return 1
    fi
    
    teardown
    return 0
}

# --- Test Runner ---

run_tests() {
    local passed=0
    local failed=0
    
    # Execute each test function
    for test_func in $(compgen -A function | grep '^test_'); do
        echo "--- Running $test_func ---"
        if "$test_func"; then
            echo "--- $test_func PASSED ---"
            passed=$((passed + 1))
        else
            echo "--- $test_func FAILED ---"
            failed=$((failed + 1))
        fi
        echo ""
    done
    
    echo "===================="
    echo "Test Summary: Passed=$passed, Failed=$failed"
    echo "===================="
    
    if [ $failed -gt 0 ]; then
        exit 1
    fi
    exit 0
}

run_tests
