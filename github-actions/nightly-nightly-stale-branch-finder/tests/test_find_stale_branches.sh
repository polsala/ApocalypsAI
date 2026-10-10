#!/bin/bash

set -euo pipefail

# Mock rationale: Override date command to ensure deterministic timestamps for testing.
# This allows consistent age calculations regardless of when the test is run.
mock_date() {
    case "$@" in
        "+%s") echo "1678886400" ;; # March 15, 2023 00:00:00 UTC
        "-d 2023-03-10T10:00:00Z" "+%s") echo "1678442400" ;; # March 10, 2023
        "-d 2023-01-01T00:00:00Z" "+%s") echo "1672531200" ;; # January 1, 2023
        "-d 2023-03-14T12:00:00Z" "+%s") echo "1678795200" ;; # March 14, 2023
        "-d 2023-03-15T00:00:00Z" "+%s") echo "1678886400" ;; # March 15, 2023 (current date for mock)
        "-d 2022-12-01T00:00:00Z" "+%s") echo "1669852800" ;; # December 1, 2022
        *) /bin/date "$@" ;; # Fallback for other date calls if any
    esac
}
alias date=mock_date # Mock rationale: Replace the real date command with our mock.

# Mock rationale: Override curl command to return predefined JSON responses for specific API endpoints.
# This prevents actual network calls and ensures tests are fast, deterministic, and offline.
mock_curl() {
    local url="$5" # The URL is the 5th argument to curl -s -H ... -H ... URL
    case "$url" in
        *branches?per_page=100)
            echo '[{"name":"main","commit":{"sha":"sha-main"}},{"name":"feature-new","commit":{"sha":"sha-new"}},{"name":"bugfix-old","commit":{"sha":"sha-old"}},{"name":"release/v1.0","commit":{"sha":"sha-release"}},{"name":"ignored-branch","commit":{"sha":"sha-ignored"}}]'
            ;;
        *branches/main)
            echo '{"name":"main","commit":{"sha":"sha-main"}}'
            ;;
        *commits/sha-main)
            echo '{"commit":{"committer":{"date":"2023-03-14T12:00:00Z"}}}' # Not stale (1 day old relative to mock_date)
            ;;
        *branches/feature-new)
            echo '{"name":"feature-new","commit":{"sha":"sha-new"}}'
            ;;
        *commits/sha-new)
            echo '{"commit":{"committer":{"date":"2023-03-10T10:00:00Z"}}}' # Stale (5 days old relative to mock_date)
            ;;
        *branches/bugfix-old)
            echo '{"name":"bugfix-old","commit":{"sha":"sha-old"}}'
            ;;
        *commits/sha-old)
            echo '{"commit":{"committer":{"date":"2023-01-01T00:00:00Z"}}}' # Very stale (73 days old relative to mock_date)
            ;;
        *branches/release/v1.0)
            echo '{"name":"release/v1.0","commit":{"sha":"sha-release"}}'
            ;;
        *commits/sha-release)
            echo '{"commit":{"committer":{"date":"2023-03-14T12:00:00Z"}}}' # Not stale
            ;;
        *branches/ignored-branch)
            echo '{"name":"ignored-branch","commit":{"sha":"sha-ignored"}}'
            ;;
        *commits/sha-ignored)
            echo '{"commit":{"committer":{"date":"2022-12-01T00:00:00Z"}}}' # Stale (104 days old relative to mock_date)
            ;;
        *)
            echo "Error: Unexpected curl call to $url" >&2
            exit 1
            ;;
    esac
}
alias curl=mock_curl # Mock rationale: Replace the real curl command with our mock.

# Source the script to be tested
SCRIPT_TO_TEST="../src/find_stale_branches.sh"

# Test function
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "$expected" == "$actual" ]]; then
        echo "✅ Test passed: $message"
    else
        echo "❌ Test failed: $message"
        echo "   Expected: '$expected'"
        echo "   Actual:   '$actual'"
        exit 1
    fi
}

echo "Running tests for find_stale_branches.sh"

# Test Case 1: Default threshold (90 days), no ignored branches
echo "--- Test Case 1: Default threshold, no ignored branches ---"
# Current mock date: March 15, 2023.
# sha-main: March 14, 2023 (1 day old) -> NOT STALE (<90 days)
# sha-new: March 10, 2023 (5 days old) -> NOT STALE (<90 days)
# sha-old: January 1, 2023 (73 days old) -> NOT STALE (<90 days)
# sha-release: March 14, 2023 (1 day old) -> NOT STALE (<90 days)
# sha-ignored: December 1, 2022 (104 days old) -> STALE (>90 days)
export GITHUB_REPOSITORY="test/repo" # Mock rationale: Set GITHUB_REPOSITORY for the script
RESULT=$(bash "$SCRIPT_TO_TEST" "mock_token" "90" "")
assert_equals '["ignored-branch"]' "$RESULT" "Identifies 'ignored-branch' as stale with 90-day threshold"

# Test Case 2: Custom threshold (3 days), no ignored branches
echo "--- Test Case 2: Custom threshold (3 days), no ignored branches ---"
# Current mock date: March 15, 2023.
# sha-main: March 14, 2023 (1 day old) -> NOT STALE (<3 days)
# sha-new: March 10, 2023 (5 days old) -> STALE (>3 days)
# sha-old: January 1, 2023 (73 days old) -> STALE (>3 days)
# sha-release: March 14, 2023 (1 day old) -> NOT STALE (<3 days)
# sha-ignored: December 1, 2022 (104 days old) -> STALE (>3 days)
RESULT=$(bash "$SCRIPT_TO_TEST" "mock_token" "3" "")
assert_equals '["feature-new","bugfix-old","ignored-branch"]' "$RESULT" "Identifies multiple stale branches with 3-day threshold"

# Test Case 3: Custom threshold (3 days), ignore 'main' and 'feature-new'
echo "--- Test Case 3: Custom threshold (3 days), ignore 'main,feature-new' ---"
# Current mock date: March 15, 2023.
# sha-main: IGNORED (exact match)
# sha-new: IGNORED (exact match)
# sha-old: January 1, 2023 (73 days old) -> STALE (>3 days)
# sha-release: March 14, 2023 (1 day old) -> NOT STALE (<3 days)
# sha-ignored: December 1, 2022 (104 days old) -> STALE (>3 days)
RESULT=$(bash "$SCRIPT_TO_TEST" "mock_token" "3" "main,feature-new")
assert_equals '["bugfix-old","ignored-branch"]' "$RESULT" "Ignores specified branches"

# Test Case 4: Custom threshold (3 days), ignore 'main' and 'release/.*'
echo "--- Test Case 4: Custom threshold (3 days), ignore 'main,release/.*' ---"
# Current mock date: March 15, 2023.
# sha-main: IGNORED (exact match)
# sha-new: March 10, 2023 (5 days old) -> STALE (>3 days)
# sha-old: January 1, 2023 (73 days old) -> STALE (>3 days)
# sha-release: IGNORED (regex match)
# sha-ignored: December 1, 2022 (104 days old) -> STALE (>3 days)
RESULT=$(bash "$SCRIPT_TO_TEST" "mock_token" "3" "main,release/.*")
assert_equals '["feature-new","bugfix-old","ignored-branch"]' "$RESULT" "Ignores branches matching regex pattern"

# Test Case 5: No stale branches (high threshold)
echo "--- Test Case 5: No stale branches (high threshold) ---"
# Current mock date: March 15, 2023.
# All branches are less than 200 days old.
RESULT=$(bash "$SCRIPT_TO_TEST" "mock_token" "200" "")
assert_equals '[]' "$RESULT" "Returns empty array when no branches are stale"

# Test Case 6: Empty branch list from API
echo "--- Test Case 6: Empty branch list from API ---"
# Mock rationale: Temporarily override mock_curl to simulate an empty branch list.
mock_curl_empty_branches() {
    local url="$5"
    if [[ "$url" == *branches?per_page=100 ]]; then
        echo '[]'
    else
        mock_curl "$@" # Fallback to original mock_curl for other calls if any
    fi
}
alias curl=mock_curl_empty_branches # Mock rationale: Replace curl with a mock that returns empty branches.
RESULT=$(bash "$SCRIPT_TO_TEST" "mock_token" "3" "")
assert_equals '[]' "$RESULT" "Handles empty branch list gracefully"
alias curl=mock_curl # Restore original mock_curl

echo "All tests completed."
