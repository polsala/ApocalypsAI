#!/bin/bash
# Mock rationale: This script creates a controlled environment for testing the playbook's file discovery and deletion logic.
# It uses 'touch -d' to set specific modification times, allowing deterministic testing of the 'age' parameter.

TEST_DIR="/tmp/digital_dust_bunnies_test"
REPORT_PATH="/tmp/dust_bunny_sweeper_report_localhost.txt"

echo "Setting up mock files in $TEST_DIR..."
rm -rf "$TEST_DIR" "$REPORT_PATH"
mkdir -p "$TEST_DIR"

# Create files older than 7 days
touch -d "8 days ago" "$TEST_DIR/old_file_1.txt"
touch -d "10 days ago" "$TEST_DIR/old_file_2.log"
mkdir -p "$TEST_DIR/old_dir"
touch -d "9 days ago" "$TEST_DIR/old_dir/old_file_in_dir.tmp"

# Create a file younger than 7 days
touch -d "1 day ago" "$TEST_DIR/recent_file.txt"

# Create a file exactly 7 days old (should NOT be picked up by 'age: 7d' which means > 7 days)
touch -d "7 days ago" "$TEST_DIR/seven_day_old_file.txt"

echo "Mock files created."
ls -l "$TEST_DIR"
