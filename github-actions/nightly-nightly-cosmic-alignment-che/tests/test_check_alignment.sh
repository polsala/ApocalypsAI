#!/bin/bash

# Source the script to test
SCRIPT_TO_TEST="../src/check_alignment.sh"

# Helper function to run test cases
run_test() {
    local test_name="$1"
    local expected_exit_code="$2"
    local expected_alignment_status="$3"
    local expected_reason_substring="$4"
    local setup_commands="$5"

    echo "--- Running Test: $test_name ---"

    # Reset environment variables for each test
    unset INPUT_REQUIRED_BRANCH_PATTERN
    unset INPUT_REQUIRED_COMMIT_PHRASE
    unset INPUT_FORBIDDEN_DAY_OF_WEEK
    unset INPUT_REQUIRED_ENV_VAR_NAME
    unset GITHUB_REF_NAME
    unset LATEST_COMMIT_MESSAGE # Updated to match script variable
    unset CURRENT_DAY_OF_WEEK   # Updated to match script variable
    unset COSMIC_ALIGNMENT_STATUS # For the env var test

    # Mock rationale: GITHUB_REF_NAME, LATEST_COMMIT_MESSAGE, CURRENT_DAY_OF_WEEK are dynamic.
    # We set them explicitly to control the test environment and ensure determinism.
    export GITHUB_REF_NAME="main"
    export LATEST_COMMIT_MESSAGE="Initial commit" # Default mock commit message
    export CURRENT_DAY_OF_WEEK="Monday" # Default mock day

    # Execute setup commands
    eval "$setup_commands"

    # Capture output and exit code
    OUTPUT=$(bash "$SCRIPT_TO_TEST" 2>&1)
    EXIT_CODE=$?

    # Extract outputs (mocking ::set-output parsing)
    ACTUAL_ALIGNMENT_STATUS=$(echo "$OUTPUT" | grep "::set-output name=alignment_status::" | sed -E 's/::set-output name=alignment_status::(.*)/\1/')
    ACTUAL_REASON=$(echo "$OUTPUT" | grep "::set-output name=reason::" | sed -E 's/::set-output name=reason::(.*)/\1/')

    if [[ "$EXIT_CODE" -eq "$expected_exit_code" && \
          "$ACTUAL_ALIGNMENT_STATUS" == "$expected_alignment_status" && \
          "$ACTUAL_REASON" == *"$expected_reason_substring"* ]]; then
        echo "PASS: $test_name"
    else
        echo "FAIL: $test_name"
        echo "  Expected Exit Code: $expected_exit_code, Got: $EXIT_CODE"
        echo "  Expected Alignment Status: $expected_alignment_status, Got: $ACTUAL_ALIGNMENT_STATUS"
        echo "  Expected Reason Substring: '$expected_reason_substring', Got: '$ACTUAL_REASON'"
        echo "  Full Output:"
        echo "$OUTPUT"
        exit 1
    fi
    echo ""
}

# Test Cases

# 1. All conditions pass (default mocks)
run_test "All conditions pass" 0 "aligned" "Cosmic alignment achieved" ""

# 2. Forbidden day of week (Friday)
run_test "Forbidden day of week (Friday)" 1 "misaligned" "Deployment forbidden on Friday" "export CURRENT_DAY_OF_WEEK='Friday'; export INPUT_FORBIDDEN_DAY_OF_WEEK='Friday'"

# 3. Branch pattern mismatch
run_test "Branch pattern mismatch" 1 "misaligned" "Branch 'feature/new' does not match required pattern '^main$'" "export GITHUB_REF_NAME='feature/new'; export INPUT_REQUIRED_BRANCH_PATTERN='^main$'"

# 4. Commit message missing phrase
run_test "Commit message missing phrase" 1 "misaligned" "Latest commit message does not contain required phrase 'Ready for launch!'" "export LATEST_COMMIT_MESSAGE='Fix bug'; export INPUT_REQUIRED_COMMIT_PHRASE='Ready for launch!'"

# 5. Commit message contains phrase
run_test "Commit message contains phrase" 0 "aligned" "Cosmic alignment achieved" "export LATEST_COMMIT_MESSAGE='Fix bug. Ready for launch!'; export INPUT_REQUIRED_COMMIT_PHRASE='Ready for launch!'"

# 6. Required environment variable missing
run_test "Required environment variable missing" 1 "misaligned" "Required environment variable 'COSMIC_ALIGNMENT_STATUS' is not set to 'true'." "export INPUT_REQUIRED_ENV_VAR_NAME='COSMIC_ALIGNMENT_STATUS'; unset COSMIC_ALIGNMENT_STATUS"

# 7. Required environment variable set to false
run_test "Required environment variable set to false" 1 "misaligned" "Required environment variable 'COSMIC_ALIGNMENT_STATUS' is not set to 'true'." "export INPUT_REQUIRED_ENV_VAR_NAME='COSMIC_ALIGNMENT_STATUS'; export COSMIC_ALIGNMENT_STATUS='false'"

# 8. Required environment variable set to true
run_test "Required environment variable set to true" 0 "aligned" "Cosmic alignment achieved" "export INPUT_REQUIRED_ENV_VAR_NAME='COSMIC_ALIGNMENT_STATUS'; export COSMIC_ALIGNMENT_STATUS='true'"

# 9. Multiple conditions fail (first one should be reported) - Forbidden day
run_test "Multiple conditions fail (Forbidden day first)" 1 "misaligned" "Deployment forbidden on Friday" "export CURRENT_DAY_OF_WEEK='Friday'; export INPUT_FORBIDDEN_DAY_OF_WEEK='Friday'; export GITHUB_REF_NAME='feature/new'; export INPUT_REQUIRED_BRANCH_PATTERN='^main$'"

# 10. Multiple conditions fail (Branch pattern first if day is fine)
run_test "Multiple conditions fail (Branch pattern first)" 1 "misaligned" "Branch 'feature/new' does not match required pattern '^main$'" "export GITHUB_REF_NAME='feature/new'; export INPUT_REQUIRED_BRANCH_PATTERN='^main$'; export INPUT_REQUIRED_COMMIT_PHRASE='Ready for launch!'"

echo "All tests completed."
