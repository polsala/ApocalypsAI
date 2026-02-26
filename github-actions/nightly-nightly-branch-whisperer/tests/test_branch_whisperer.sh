#!/bin/bash

set -euo pipefail

# Mock the `date` command for deterministic current timestamp
# Mock rationale: Ensures that the "current time" for staleness calculation is fixed,
# making tests deterministic regardless of when they are run.
mock_date() {
    echo "1678886400" # March 15, 2023 00:00:00 UTC
}
export -f date # Export the function so subshells can use it

# Mock the `git` command for deterministic branch data
# Mock rationale: Prevents actual Git operations and provides controlled branch data,
# making tests offline and deterministic.
mock_git() {
    if [[ "$@" == "for-each-ref --sort=-committerdate refs/remotes/origin/ --format=%(refname:short)|%(committerdate:raw)" ]]; then
        cat tests/mock_branch_data.txt
    else
        echo "Error: Unexpected git command: $@" >&2
        exit 1
    fi
}
export -f git # Export the function so subshells can use it

# Test 1: No stale branches
echo "--- Running Test 1: No stale branches ---"
# Set mock current timestamp to be very recent, so no branches are stale
export MOCK_CURRENT_TIMESTAMP="1678886400" # March 15, 2023 00:00:00 UTC
export INPUT_STALE_DAYS="90" # Branches older than 90 days are stale
export INPUT_EXCLUDE_BRANCHES="main,master"
export GITHUB_REPOSITORY="test/repo" # Required by gh api, but we're mocking git
export PATH="$(pwd):$PATH" # Add current dir to PATH to pick up mock_git

# Simulate GitHub Actions environment variables for inputs
INPUT_STALE_DAYS="90"
INPUT_REPO_TOKEN="mock_token" # Not used by mocked git, but good practice

# Run the script with mocked git
OUTPUT=$(bash src/branch_whisperer.sh)

# Check outputs
STALE_COUNT=$(echo "$OUTPUT" | grep "::set-output name=stale-branches-count::" | sed -E 's/::set-output name=stale-branches-count::([0-9]+)/\1/')
STALE_REPORT=$(echo "$OUTPUT" | grep "::set-output name=stale-branches-report::" | sed -E 's/::set-output name=stale-branches-report::(.*)/\1/')

if [[ "$STALE_COUNT" -eq 0 ]]; then
    echo "✅ Test 1 Passed: Stale count is 0."
else
    echo "❌ Test 1 Failed: Expected 0 stale branches, got $STALE_COUNT."
    echo "Output: $OUTPUT"
    exit 1
fi

if [[ "$STALE_REPORT" == *"No stale branches found. All branches are vibrant and active! ✨"* ]]; then
    echo "✅ Test 1 Passed: Report indicates no stale branches."
else
    echo "❌ Test 1 Failed: Report does not indicate no stale branches."
    echo "Report: $STALE_REPORT"
    exit 1
fi

# Test 2: Some stale branches
echo "--- Running Test 2: Some stale branches ---"
# Set mock current timestamp to make some branches stale
export MOCK_CURRENT_TIMESTAMP="1689379200" # July 15, 2023 00:00:00 UTC (more than 90 days after March 15)
export INPUT_STALE_DAYS="90"
export INPUT_EXCLUDE_BRANCHES="main,master"

OUTPUT=$(bash src/branch_whisperer.sh)

STALE_COUNT=$(echo "$OUTPUT" | grep "::set-output name=stale-branches-count::" | sed -E 's/::set-output name=stale-branches-count::([0-9]+)/\1/')
STALE_REPORT=$(echo "$OUTPUT" | grep "::set-output name=stale-branches-report::" | sed -E 's/::set-output name=stale-branches-report::(.*)/\1/')

if [[ "$STALE_COUNT" -eq 2 ]]; then # feature/old-feature and bugfix/ancient-bug
    echo "✅ Test 2 Passed: Stale count is 2."
else
    echo "❌ Test 2 Failed: Expected 2 stale branches, got $STALE_COUNT."
    echo "Output: $OUTPUT"
    exit 1
fi

if [[ "$STALE_REPORT" == *"| \`feature/old-feature\` | 2022-12-01 |"* ]] && \
   [[ "$STALE_REPORT" == *"| \`bugfix/ancient-bug\` | 2022-11-15 |"* ]]; then
    echo "✅ Test 2 Passed: Report correctly lists stale branches."
else
    echo "❌ Test 2 Failed: Report does not list expected stale branches."
    echo "Report: $STALE_REPORT"
    exit 1
fi

# Test 3: Excluded branches are ignored
echo "--- Running Test 3: Excluded branches are ignored ---"
export MOCK_CURRENT_TIMESTAMP="1689379200" # July 15, 2023 00:00:00 UTC
export INPUT_STALE_DAYS="90"
export INPUT_EXCLUDE_BRANCHES="main,master,feature/old-feature" # Exclude one of the stale branches

OUTPUT=$(bash src/branch_whisperer.sh)

STALE_COUNT=$(echo "$OUTPUT" | grep "::set-output name=stale-branches-count::" | sed -E 's/::set-output name=stale-branches-count::([0-9]+)/\1/')
STALE_REPORT=$(echo "$OUTPUT" | grep "::set-output name=stale-branches-report::" | sed -E 's/::set-output name=stale-branches-report::(.*)/\1/')

if [[ "$STALE_COUNT" -eq 1 ]]; then # Only bugfix/ancient-bug should be stale
    echo "✅ Test 3 Passed: Stale count is 1."
else
    echo "❌ Test 3 Failed: Expected 1 stale branch, got $STALE_COUNT."
    echo "Output: $OUTPUT"
    exit 1
fi

if [[ "$STALE_REPORT" == *"| \`bugfix/ancient-bug\` | 2022-11-15 |"* ]] && \
   [[ "$STALE_REPORT" != *"| \`feature/old-feature\` |"* ]]; then
    echo "✅ Test 3 Passed: Report correctly excludes branches."
else
    echo "❌ Test 3 Failed: Report does not correctly exclude branches."
    echo "Report: $STALE_REPORT"
    exit 1
fi

echo "All tests completed."
