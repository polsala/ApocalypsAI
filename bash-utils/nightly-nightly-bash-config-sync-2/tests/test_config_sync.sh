#!/bin/bash

# Mock rsync function
_mock_rsync() {
  echo "Mock rsync called with: $@"
  # Simulate success
  return 0
}

# Replace the actual rsync command with our mock
_original_rsync="rsync"
rsync() {
  _mock_rsync "$@"
}

# --- Test Cases ---

# Test 1: Basic sync to multiple hosts
echo "--- Test Case 1: Basic Sync ---"

# Define mock configuration for this test
REMOTE_HOSTS=("mockuser@mockhost1" "mockuser@mockhost2")
SOURCE_DIR="/tmp/local_configs/"
DEST_DIR="~/.config/synced_configs/"

# Create dummy source directory and files for the mock to 'see'
mkdir -p "$SOURCE_DIR"
touch "$SOURCE_DIR/file1.conf"
touch "$SOURCE_DIR/file2.txt"

# Source the script to make its variables available
source src/config_sync.sh

# Clean up dummy files after test
rm -rf "$SOURCE_DIR"

# Expected output check (basic, can be made more robust)
if grep -q "Mock rsync called with: -avz --delete /tmp/local_configs/ mockuser@mockhost1:~/.config/synced_configs/" <<< "$(echo "$(./src/config_sync.sh 2>&1)")"; then
  echo "✅ Test Case 1 Passed: rsync called correctly for host 1."
else
  echo "❌ Test Case 1 Failed: rsync call incorrect for host 1."
  exit 1
fi

if grep -q "Mock rsync called with: -avz --delete /tmp/local_configs/ mockuser@mockhost2:~/.config/synced_configs/" <<< "$(echo "$(./src/config_sync.sh 2>&1)")"; then
  echo "✅ Test Case 1 Passed: rsync called correctly for host 2."
else
  echo "❌ Test Case 1 Failed: rsync call incorrect for host 2."
  exit 1
fi

# Test 2: Source directory does not exist
echo "
--- Test Case 2: Non-existent Source Directory ---"

# Temporarily unset SOURCE_DIR to simulate non-existence
_original_source_dir="$SOURCE_DIR"
SOURCE_DIR="/non/existent/path/"

source src/config_sync.sh

if grep -q "❌ Error: Source directory '/non/existent/path/' does not exist locally." <<< "$(echo "$(./src/config_sync.sh 2>&1)")"; then
  echo "✅ Test Case 2 Passed: Correct error message for non-existent source."
else
  echo "❌ Test Case 2 Failed: Incorrect error message or no error for non-existent source."
  exit 1
fi

# Restore original SOURCE_DIR
SOURCE_DIR="$_original_source_dir"

# Restore original rsync command
rsync() { $_original_rsync "$@"; }

echo "
🎉 All tests completed."
