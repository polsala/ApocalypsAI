#!/bin/bash

set -euo pipefail

# Mock git for deterministic testing
# Mock rationale: We replace the actual 'git' command with a shell function
# that returns predefined outputs. This allows us to simulate different
# repository states (e.g., branches with various commit dates) without
# needing a real Git repository or network access, making tests fast and reliable.
mock_git() {
    case "$@" in
        "for-each-ref --sort=-committerdate refs/remotes/origin/ --format=%(refname:short) %(committerdate:unix)")
            # Simulate branches with different commit dates
            # Current timestamp for reference: 1678886400 (March 15, 2023, 12:00:00 PM UTC)
            # Stale threshold for 90 days (1678886400 - 90*24*60*60 = 1671024000) (Dec 15, 2022)
            # Stale threshold for 30 days (1678886400 - 30*24*60*60 = 1676294400) (Feb 13, 2023)
            echo "origin/main 1678886400" # Current, not stale
            echo "origin/feature-new 1678800000" # ~1 day old, not stale
            echo "origin/feature-old 1671000000" # ~91 days old, stale for 90 days
            echo "origin/bugfix-ancient 1660000000" # Very old, stale
            echo "origin/dev 1678886400" # Current, not stale
            echo "origin/feature-just-stale 1671024000" # Exactly 90 days old, stale
            echo "origin/feature-not-stale-yet 1671024001" # 89 days, 23h, 59m, 59s old, not stale for 90 days
            echo "origin/HEAD 1678886400" # Should be skipped
            echo "origin/master 1678886400" # Should be skipped
            ;;
        *)
            echo "Error: Unexpected git command: $@" >&2
            exit 1
            ;;
    esac
}

# Override the git command with our mock function
export -f git
alias git=mock_git

# Set a fixed current timestamp for deterministic tests
# Mock rationale: Fixing the current timestamp ensures that the 'stale' calculation
# is consistent across test runs, regardless of when the test is executed.
# This prevents time-dependent test failures.
date() {
    if [[ "$@" == "+%s" ]]; then
        echo "1678886400" # March 15, 2023, 12:00:00 PM UTC
    else
        command date "$@"
    fi
}
export -f date

# Create a temporary output file for GITHUB_OUTPUT
TEMP_GITHUB_OUTPUT=$(mktemp)
export GITHUB_OUTPUT=$TEMP_GITHUB_OUTPUT

# Test Case 1: Default 90 days stale threshold
echo "--- Test Case 1: Default 90 days stale threshold ---"
bash ../src/prune_branches.sh 90

OUTPUT=$(cat "$TEMP_GITHUB_OUTPUT")
EXPECTED_OUTPUT="stale-branches=[\"feature-old\",\"bugfix-ancient\",\"feature-just-stale\"]"

if [[ "$OUTPUT" == "$EXPECTED_OUTPUT" ]]; then
    echo "Test Case 1 PASSED"
else
    echo "Test Case 1 FAILED"
    echo "Expected: $EXPECTED_OUTPUT"
    echo "Got: $OUTPUT"
    exit 1
fi

# Clean up for next test case
echo "" > "$TEMP_GITHUB_OUTPUT"

# Test Case 2: 30 days stale threshold
echo "--- Test Case 2: 30 days stale threshold ---"
bash ../src/prune_branches.sh 30

OUTPUT=$(cat "$TEMP_GITHUB_OUTPUT")
# Stale threshold for 30 days: 1676294400 (February 13, 2023, 12:00:00 PM UTC)
# Branches older than this:
# feature-old (1671000000) < 1676294400 -> stale
# bugfix-ancient (1660000000) < 1676294400 -> stale
# feature-just-stale (1671024000) < 1676294400 -> stale
# feature-not-stale-yet (1671024001) < 1676294400 -> stale
EXPECTED_OUTPUT="stale-branches=[\"feature-old\",\"bugfix-ancient\",\"feature-just-stale\",\"feature-not-stale-yet\"]"

if [[ "$OUTPUT" == "$EXPECTED_OUTPUT" ]]; then
    echo "Test Case 2 PASSED"
else
    echo "Test Case 2 FAILED"
    echo "Expected: $EXPECTED_OUTPUT"
    echo "Got: $OUTPUT"
    exit 1
fi

# Clean up
rm "$TEMP_GITHUB_OUTPUT"

echo "All tests completed."
