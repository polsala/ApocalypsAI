#!/bin/bash

# This script runs the unit tests for the nightly-syslog-filter-cli utility.
# It requires bashunit to be installed.

# --- Configuration ---

# Path to the bashunit executable
# If bashunit is in your PATH, you can just use 'bashunit'
BASHUNIT_CMD="bashunit"

# Directory containing the test files
TEST_DIR="$(dirname "$0")"

# Source directory for the utility script
SRC_DIR="$TEST_DIR/../src"

# --- Pre-requisites Check ---

if ! command -v "$BASHUNIT_CMD" &> /dev/null; then
    echo "Error: bashunit command not found." >&2
    echo "Please install bashunit: bash -c \"$(curl -fsSL https://raw.githubusercontent.com/bashunit/bashunit/main/install.sh)\"" >&2
    exit 1
fi

# --- Test Execution ---

echo "Running tests for nightly-syslog-filter-cli..."

# Source the utility script to make its functions available for mocking
source "$SRC_DIR/main.sh"

# Run all test files in the current directory
# bashunit will automatically discover files named test_*.sh
# We need to pass the path to the utility script and its functions to the test environment
# This is achieved by sourcing the script before running bashunit.

# The tests will mock the external commands and the syslog file reading.

# Execute tests
# We need to ensure the test environment has access to the functions from main.sh
# The easiest way is to run bashunit in a subshell that has sourced the script.

( 
    source "$SRC_DIR/main.sh"
    cd "$TEST_DIR"
    "$BASHUNIT_CMD" "test_*.sh"
)

exit $?
