#!/bin/bash
# Mock rationale: This script ensures a clean slate after tests, removing all temporary files and directories created for testing.

TEST_DIR="/tmp/digital_dust_bunnies_test"
REPORT_PATH="/tmp/dust_bunny_sweeper_report_localhost.txt"

echo "Cleaning up mock files in $TEST_DIR..."
rm -rf "$TEST_DIR" "$REPORT_PATH"
echo "Cleanup complete."
