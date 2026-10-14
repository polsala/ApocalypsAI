#!/bin/bash

# Mock rationale: We need to simulate the GitHub Actions environment variables
# and external commands like `jq` and `gh` for deterministic and offline testing.

# --- Setup Mock Environment ---

# Create a temporary directory for test artifacts
TEST_DIR=$(mktemp -d)
export GITHUB_EVENT_PATH="$TEST_DIR/event.json"
export GITHUB_OUTPUT="$TEST_DIR/output.txt" # GitHub Actions writes outputs to this file

# Mock `jq` command
# Mock rationale: `jq` is an external dependency. For offline testing, we simulate its behavior.
jq() {
  case "$1" in
    -r)
      case "$2" in
        '.pull_request.title') echo "$MOCK_PR_TITLE" ;;
        '.pull_request.body // ""') echo "$MOCK_PR_BODY" ;;
        '.pull_request.number') echo "$MOCK_PR_NUMBER" ;;
        *) echo "Error: Unknown jq path $2" >&2; exit 1 ;;
      esac
      ;;
    *) echo "Error: Unknown jq command $1" >&2; exit 1 ;;
  esac
}
export -f jq # Export the function so it's available in subshells

# Mock `gh` command
# Mock rationale: `gh` CLI is an external dependency used for commenting.
# We capture its arguments to verify the comment content.
mock_gh_output="$TEST_DIR/gh_output.txt"
gh() {
  echo "gh $*" >> "$mock_gh_output"
}
export -f gh # Export the function

# --- Test Cases ---

run_action_logic() {
  # This function simulates the 'run' block of the action.yml
  # It takes inputs as arguments for easier testing.
  local github_token="$1"
  local whimsical_phrases="$2"

  # Clear previous outputs and mock gh output
  > "$GITHUB_OUTPUT"
  > "$mock_gh_output"

  # Set inputs as environment variables for the script
  export GH_TOKEN="$github_token"
  
  # Simulate the action's run block logic directly
  PR_TITLE=$(jq -r '.pull_request.title' "$GITHUB_EVENT_PATH")
  PR_BODY=$(jq -r '.pull_request.body // ""' "$GITHUB_EVENT_PATH")
  PR_NUMBER=$(jq -r '.pull_request.number' "$GITHUB_EVENT_PATH")

  PR_CONTENT="$PR_TITLE $PR_BODY"

  IFS=',' read -r -a PHRASE_ARRAY <<< "$whimsical_phrases"

  CHEER_NEEDED="true"
  for phrase in "${PHRASE_ARRAY[@]}"; do
    trimmed_phrase=$(echo "$phrase" | xargs)
    if [[ "$PR_CONTENT" == *"$trimmed_phrase"* ]]; then
      CHEER_NEEDED="false"
      break
    fi
  done

  if [ "$CHEER_NEEDED" == "true" ]; then
    RANDOM_INDEX=$(( RANDOM % ${#PHRASE_ARRAY[@]} ))
    SUGGESTED_PHRASE=$(echo "${PHRASE_ARRAY[$RANDOM_INDEX]}" | xargs)

    COMMENT_BODY="The ApocalypsAI Nightly Integrator observes your PR is technically sound, but could use a touch of cosmic sparkle! ✨\n\nConsider adding a whimsical emoji or phrase like \`$SUGGESTED_PHRASE\` to your title or description to brighten the digital wasteland. Every bit of cheer helps! 😊"
    
    # Simulate gh command execution
    gh pr comment "$PR_NUMBER" --body "$COMMENT_BODY"

    echo "cheered_up=true" >> "$GITHUB_OUTPUT"
  else
    echo "cheered_up=false" >> "$GITHUB_OUTPUT"
  fi
}

assert_output() {
  local expected_key="$1"
  local expected_value="$2"
  local actual_output=$(grep "^$expected_key=" "$GITHUB_OUTPUT" | cut -d'=' -f2)
  if [ "$actual_output" != "$expected_value" ]; then
    echo "FAIL: Expected $expected_key=$expected_value, got $expected_key=$actual_output"
    exit 1
  fi
  echo "PASS: $expected_key=$expected_value"
}

assert_gh_comment_contains() {
  local expected_text="$1"
  if ! grep -q "$expected_text" "$mock_gh_output"; then
    echo "FAIL: Expected gh comment to contain '$expected_text', but it did not."
    cat "$mock_gh_output"
    exit 1
  fi
  echo "PASS: gh comment contains '$expected_text'"
}

# Test Case 1: PR needs cheer-up
echo "--- Running Test Case 1: PR needs cheer-up ---"
MOCK_PR_TITLE="feat: add new widget"
MOCK_PR_BODY="This PR introduces a new widget for displaying data."
MOCK_PR_NUMBER="123"
run_action_logic "mock_token" "✨, 🌟, 😄"
assert_output "cheered_up" "true"
assert_gh_comment_contains "The ApocalypsAI Nightly Integrator observes your PR is technically sound, but could use a touch of cosmic sparkle! ✨"
assert_gh_comment_contains "Consider adding a whimsical emoji or phrase like"

# Test Case 2: PR already has cheer-up (emoji in title)
echo "--- Running Test Case 2: PR already has cheer-up (emoji in title) ---"
MOCK_PR_TITLE="feat: add new widget ✨"
MOCK_PR_BODY="This PR introduces a new widget for displaying data."
MOCK_PR_NUMBER="124"
run_action_logic "mock_token" "✨, 🌟, 😄"
assert_output "cheered_up" "false"
if [ -s "$mock_gh_output" ]; then
  echo "FAIL: Expected no gh comment, but found one."
  cat "$mock_gh_output"
  exit 1
fi
echo "PASS: No gh comment made."

# Test Case 3: PR already has cheer-up (phrase in body)
echo "--- Running Test Case 3: PR already has cheer-up (phrase in body) ---"
MOCK_PR_TITLE="fix: resolve critical bug"
MOCK_PR_BODY="This PR resolves a critical bug. Feeling joyful about this fix! 😄"
MOCK_PR_NUMBER="125"
run_action_logic "mock_token" "✨, 🌟, 😄"
assert_output "cheered_up" "false"
if [ -s "$mock_gh_output" ]; then
  echo "FAIL: Expected no gh comment, but found one."
  cat "$mock_gh_output"
  exit 1
fi
echo "PASS: No gh comment made."

# Test Case 4: Custom whimsical phrases
echo "--- Running Test Case 4: Custom whimsical phrases ---"
MOCK_PR_TITLE="docs: update README"
MOCK_PR_BODY="Updated documentation for new features."
MOCK_PR_NUMBER="126"
run_action_logic "mock_token" "🚀, 🌌, 👽"
assert_output "cheered_up" "true"
assert_gh_comment_contains "Consider adding a whimsical emoji or phrase like"
assert_gh_comment_contains "gh pr comment 126 --body"

# --- Cleanup ---
rm -rf "$TEST_DIR"
echo "All tests passed!"
