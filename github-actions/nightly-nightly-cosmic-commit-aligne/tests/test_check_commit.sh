#!/bin/bash

# Mock rationale: These tests directly invoke the check_commit.sh script with predefined
# commit messages and parameters, simulating different scenarios without needing
# actual Git history or GitHub API calls. This ensures determinism and offline execution.

SCRIPT_PATH="./src/check_commit.sh"

# Default parameters for testing
DEFAULT_POSITIVE="feat,fix,chore,docs,refactor,style,test,build,ci,perf,revert,improve,add,update"
DEFAULT_NEGATIVE="broken,fail,buggy,mess,oops,ugh,bad,error"
DEFAULT_MIN_LEN="10"
DEFAULT_MAX_LEN="100"

run_test() {
  local test_name="$1"
  local commit_msg="$2"
  local expected_aligned="$3"
  local expected_reason_part="$4" # Part of the reason string to check for
  local positive_kws="${5:-$DEFAULT_POSITIVE}"
  local negative_kws="${6:-$DEFAULT_NEGATIVE}"
  local min_len="${7:-$DEFAULT_MIN_LEN}"
  local max_len="${8:-$DEFAULT_MAX_LEN}"

  echo "--- Running Test: $test_name ---"
  OUTPUT=$("$SCRIPT_PATH" "$commit_msg" "$positive_kws" "$negative_kws" "$min_len" "$max_len")
  EXIT_CODE=$?

  ACTUAL_ALIGNED=$(echo "$OUTPUT" | grep "aligned:" | cut -d':' -f2 | xargs)
  ACTUAL_REASON=$(echo "$OUTPUT" | grep "reason:" | cut -d':' -f2- | xargs)

  if [ "$ACTUAL_ALIGNED" = "$expected_aligned" ] && [[ "$ACTUAL_REASON" == *"$expected_reason_part"* ]]; then
    echo "PASS: $test_name"
  else
    echo "FAIL: $test_name"
    echo "  Commit Message: '$commit_msg'"
    echo "  Expected Aligned: $expected_aligned, Got: $ACTUAL_ALIGNED"
    echo "  Expected Reason Part: '$expected_reason_part', Got: '$ACTUAL_REASON'"
    echo "  Full Output:"
    echo "$OUTPUT"
    exit 1
  fi
  echo ""
}

# Test Cases

# 1. Good commit message
run_test "Good Commit - Feat" "feat: Add new cosmic alignment sensor" "true" ""

# 2. Good commit message with different positive keyword
run_test "Good Commit - Fix" "fix: Resolve minor temporal distortion" "true" ""

# 3. Good commit message - case insensitive positive keyword
run_test "Good Commit - Chore (case insensitive)" "CHORE: Update celestial navigation charts" "true" ""

# 4. Commit message too short
run_test "Bad Commit - Too Short" "fix" "false" "too short"

# 5. Commit message too long
run_test "Bad Commit - Too Long" "feat: This is an extremely long commit message that goes way beyond the cosmic limits of what is considered a harmonious and concise summary of changes. It just keeps going and going and going, much like a rogue asteroid." "false" "too long"

# 6. Commit message with negative keyword
run_test "Bad Commit - Negative Keyword" "fix: Ugh, this was broken" "false" "negative cosmic energy: 'ugh'"

# 7. Commit message with negative keyword (case insensitive)
run_test "Bad Commit - Negative Keyword (case insensitive)" "feat: Remove BAD code" "false" "negative cosmic energy: 'bad'"

# 8. Commit message missing positive keyword
run_test "Bad Commit - Missing Positive Keyword" "Updated some files" "false" "lacks positive cosmic energy"

# 9. Custom positive keywords - success
run_test "Custom Positive - Success" "refactor: Streamline warp core" "true" "" "refactor,optimize" "" "5" "50"

# 10. Custom positive keywords - failure
run_test "Custom Positive - Failure" "Adjusted settings" "false" "lacks positive cosmic energy" "refactor,optimize" "" "5" "50"

# 11. Custom negative keywords - success
run_test "Custom Negative - Success" "feat: Add new feature" "true" "" "" "deprecated,remove_me" "5" "50"

# 12. Custom negative keywords - failure
run_test "Custom Negative - Failure" "feat: Remove deprecated function" "false" "negative cosmic energy: 'deprecated'" "" "deprecated,remove_me" "5" "50"

# 13. Edge case: message exactly min length
run_test "Edge Case - Min Length" "feat: abcdef" "true" "" "" "" "10" "100"

# 14. Edge case: message exactly max length
run_test "Edge Case - Max Length" "feat: This is a very long message that should be exactly one hundred characters long for testing purposes." "true" "" "" "" "10" "100"

# 15. No positive keywords configured (should pass as check is skipped)
run_test "No Positive Keywords Required" "Just a message" "true" "" "" "" "5" "50"

# 16. No negative keywords configured (should pass as check is skipped)
run_test "No Negative Keywords Required" "This is a broken message" "true" "" "feat" "" "5" "50"
