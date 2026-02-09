#!/bin/bash
# Mock rationale: This script mocks the GitHub CLI ('gh') to prevent actual API calls during tests.
# It captures the arguments passed to 'gh' and writes them to a predefined file,
# allowing tests to verify that the action would have invoked 'gh' correctly.

# Ensure the output file is defined, default if not
MOCK_OUTPUT_FILE="${MOCK_OUTPUT_FILE:-/tmp/mock_gh_output.txt}"

# Append all arguments to the mock output file
echo "$@" >> "$MOCK_OUTPUT_FILE"

# Simulate a successful exit
exit 0
