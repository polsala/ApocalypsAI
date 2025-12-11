#!/bin/bash

# Script to run all tests for the Apoc Log Scrubber utility.

TEST_DIR=$(dirname "$0")

# Ensure we are in the test directory
cd "$TEST_DIR" || exit 1

# Execute the test script
./test_scrub_log.sh

exit $?
