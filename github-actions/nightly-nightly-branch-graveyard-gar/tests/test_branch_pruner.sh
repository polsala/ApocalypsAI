#!/bin/bash

# Mock rationale: This test script directly invokes the branch_pruner.sh script
# in its "test mode" by providing a mock data file instead of relying on actual
# git commands. This ensures determinism and offline execution.

set -euo pipefail

# Create a temporary directory for test files
TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR"' EXIT

# Define the path to the script under test
SCRIPT_PATH="./src/branch_pruner.sh"

# Mock GITHUB_OUTPUT for testing
MOCK_GITHUB_OUTPUT="$TEST_DIR/mock_github_output.txt"
export GITHUB_OUTPUT="$MOCK_GITHUB_OUTPUT"

# --- Test Case 1: No stale branches --- 
echo "Running Test Case 1: No stale branches"
TEST_FILE_1="$TEST_DIR/branches_1.txt"
CURRENT_TIME=$(date +%s)
# All branches are recent
echo "feature-A|$CURRENT_TIME" > "$TEST_FILE_1"
echo "feature-B|$CURRENT_TIME" >> "$TEST_FILE_1"
echo "origin/main|$CURRENT_TIME" >> "$TEST_FILE_1" # Should be ignored by default

bash "$SCRIPT_PATH" 90 "main" "$TEST_FILE_1" > /dev/null # Redirect stdout to /dev/null to avoid clutter
OUTPUT_1=$(cat "$MOCK_GITHUB_OUTPUT")

if [[ "$OUTPUT_1" == *"stale-branches=[]"* && "$OUTPUT_1" == *"stale-branches-count=0"* ]]; then
    echo "Test Case 1 PASSED"
else
    echo "Test Case 1 FAILED"
    echo "Output: $OUTPUT_1"
    exit 1
fi
rm "$MOCK_GITHUB_OUTPUT" # Clear for next test

# --- Test Case 2: Some stale branches --- 
echo "Running Test Case 2: Some stale branches"
TEST_FILE_2="$TEST_DIR/branches_2.txt"
OLD_TIME=$((CURRENT_TIME - (100 * 24 * 60 * 60))) # 100 days ago
RECENT_TIME=$((CURRENT_TIME - (10 * 24 * 60 * 60))) # 10 days ago

echo "feature-stale-1|$OLD_TIME" > "$TEST_FILE_2"
echo "feature-recent-1|$RECENT_TIME" >> "$TEST_FILE_2"
echo "feature-stale-2|$OLD_TIME" >> "$TEST_FILE_2"
echo "origin/develop|$RECENT_TIME" >> "$TEST_FILE_2" # Should be ignored by explicit ignore
echo "release-1.0|$OLD_TIME" >> "$TEST_FILE_2" # Should be ignored by pattern

bash "$SCRIPT_PATH" 90 "develop,release-*" "$TEST_FILE_2" > /dev/null
OUTPUT_2=$(cat "$MOCK_GITHUB_OUTPUT")

# Expected stale branches: feature-stale-1, feature-stale-2
if [[ "$OUTPUT_2" == *"stale-branches=[\"feature-stale-1\",\"feature-stale-2\"]"* && "$OUTPUT_2" == *"stale-branches-count=2"* ]]; then
    echo "Test Case 2 PASSED"
else
    echo "Test Case 2 FAILED"
    echo "Output: $OUTPUT_2"
    exit 1
fi
rm "$MOCK_GITHUB_OUTPUT" # Clear for next test

# --- Test Case 3: All branches ignored --- 
echo "Running Test Case 3: All branches ignored"
TEST_FILE_3="$TEST_DIR/branches_3.txt"
echo "feature-ignored-1|$OLD_TIME" > "$TEST_FILE_3"
echo "feature-ignored-2|$OLD_TIME" >> "$TEST_FILE_3"

bash "$SCRIPT_PATH" 90 "feature-ignored-1,feature-ignored-2" "$TEST_FILE_3" > /dev/null
OUTPUT_3=$(cat "$MOCK_GITHUB_OUTPUT")

if [[ "$OUTPUT_3" == *"stale-branches=[]"* && "$OUTPUT_3" == *"stale-branches-count=0"* ]]; then
    echo "Test Case 3 PASSED"
else
    echo "Test Case 3 FAILED"
    echo "Output: $OUTPUT_3"
    exit 1
fi
rm "$MOCK_GITHUB_OUTPUT" # Clear for next test

echo "All tests passed!"
