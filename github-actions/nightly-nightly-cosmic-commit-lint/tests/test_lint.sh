#!/bin/bash

# Mock rationale: We are testing the core logic of lint.sh in isolation.
# We mock the GitHub Actions environment by directly passing the commit message
# and cosmic level as arguments. The script's output (status and suggestion)
# is captured from stdout, allowing for deterministic assertions without
# needing a real GitHub Actions runner or Git repository.
# Error/warning messages sent to stderr are suppressed in tests for cleaner output.

SCRIPT_PATH="$(dirname "$0")"/../src/lint.sh

# Function to run the lint script and capture outputs
run_lint_test() {
  local commit_msg="$1"
  local cosmic_level="$2"
  local expected_status="$3"
  local expected_suggestion_present="$4" # true/false if suggestion is expected
  local test_name="$5"

  echo "--- Running test: $test_name ---"

  # Run the script, redirecting stdout to a temporary file for parsing outputs
  # and stderr to /dev/null to suppress ::warning/::notice messages in test output
  TEMP_STDOUT_FILE=$(mktemp)
  /bin/bash "$SCRIPT_PATH" "$commit_msg" "$cosmic_level" > "$TEMP_STDOUT_FILE" 2>/dev/null
  ACTUAL_EXIT_CODE=$? # The script itself should always exit 0 unless there's a bash error

  ACTUAL_STATUS=$(grep "status=" "$TEMP_STDOUT_FILE" | cut -d'=' -f2)
  ACTUAL_SUGGESTION=$(grep "suggestion=" "$TEMP_STDOUT_FILE" | cut -d'=' -f2)

  echo "  Commit Message: '$commit_msg'"
  echo "  Cosmic Level: '$cosmic_level'"
  echo "  Expected Status: '$expected_status', Actual Status: '$ACTUAL_STATUS'"
  echo "  Actual Suggestion: '$ACTUAL_SUGGESTION'"

  local test_passed=true

  if [ "$ACTUAL_STATUS" != "$expected_status" ]; then
    echo "  ❌ Status Mismatch: Expected '$expected_status', got '$ACTUAL_STATUS'"
    test_passed=false
  fi

  if [ "$expected_suggestion_present" = "true" ] && [ -z "$ACTUAL_SUGGESTION" ]; then
    echo "  ❌ Suggestion Missing: Expected a suggestion, but none found."
    test_passed=false
  elif [ "$expected_suggestion_present" = "false" ] && [ -n "$ACTUAL_SUGGESTION" ]; then
    echo "  ❌ Unexpected Suggestion: Did not expect a suggestion, but got '$ACTUAL_SUGGESTION'."
    test_passed=false
  fi

  if $test_passed; then
    echo "  ✅ PASS: $test_name"
    rm "$TEMP_STDOUT_FILE"
    return 0
  else
    echo "  ❌ FAIL: $test_name"
    echo "  Captured Script Output:"
    cat "$TEMP_STDOUT_FILE"
    rm "$TEMP_STDOUT_FILE"
    return 1
  fi
}

ALL_TESTS_PASSED=true

# Test Cases

# 1. Valid conventional commit, not bland (should be success, no suggestion)
run_lint_test "feat: add new cosmic ray detector with advanced sensors" "stardust" "success" "false" "Valid conventional commit, no blandness" || ALL_TESTS_PASSED=false

# 2. Bland message, stardust level (should be success, with suggestion)
run_lint_test "fix: update dependencies" "stardust" "success" "true" "Bland, stardust level" || ALL_TESTS_PASSED=false

# 3. Bland message, nebula level (should be warning, with suggestion)
run_lint_test "chore: small changes" "nebula" "warning" "true" "Bland, nebula level" || ALL_TESTS_PASSED=false

# 4. Bland message, blackhole level (should be failure, with suggestion)
run_lint_test "docs: initial commit" "blackhole" "failure" "true" "Bland, blackhole level" || ALL_TESTS_PASSED=false

# 5. No conventional prefix, not bland, stardust level (should be warning, no suggestion)
run_lint_test "Added a new feature with great cosmic power" "stardust" "warning" "false" "No conventional prefix, not bland" || ALL_TESTS_PASSED=false

# 6. No conventional prefix, not bland, blackhole level (should be failure, no suggestion)
run_lint_test "Fixed a critical bug in the warp core drive" "blackhole" "failure" "false" "No conventional prefix, not bland, blackhole" || ALL_TESTS_PASSED=false

# 7. Very short message, stardust level (should be success, with suggestion)
run_lint_test "feat: x" "stardust" "success" "true" "Very short, stardust" || ALL_TESTS_PASSED=false

# 8. Very short message, blackhole level (should be failure, with suggestion)
run_lint_test "fix: y" "blackhole" "failure" "true" "Very short, blackhole" || ALL_TESTS_PASSED=false

# 9. Valid conventional commit, but short and bland, nebula level (should be warning, with suggestion)
run_lint_test "chore: update" "nebula" "warning" "true" "Valid but bland, nebula" || ALL_TESTS_PASSED=false

# 10. Valid conventional commit, not bland, blackhole level (should be success, no suggestion)
run_lint_test "feat: implement new interstellar communication protocol" "blackhole" "success" "false" "Valid, not bland, blackhole" || ALL_TESTS_PASSED=false

# 11. No conventional prefix, but bland, stardust level (should be warning, with suggestion)
run_lint_test "wip" "stardust" "warning" "true" "No conventional prefix, bland, stardust" || ALL_TESTS_PASSED=false

# Final result
if $ALL_TESTS_PASSED; then
  echo "All tests passed! ✨"
  exit 0
else
  echo "Some tests failed! 💀"
  exit 1
fi
