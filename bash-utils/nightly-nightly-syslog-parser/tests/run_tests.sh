#!/bin/bash

# This script runs all the tests for the nightly-syslog-parser utility.

# Navigate to the directory containing the test script
cd "$(dirname "$0")"

# Execute the test script
if bash test_nightly-syslog-parser.sh; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "One or more tests failed."
    exit 1
fi
