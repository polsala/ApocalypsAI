#!/bin/bash

set -e

# Create a temporary directory for mocks and outputs
TEST_DIR=$(mktemp -d)
PROVERBS_FILE="$TEST_DIR/proverbs.txt"
MOCK_GH_OUTPUT="$TEST_DIR/mock_gh_output.txt"
MOCK_GITHUB_EVENT_PATH="$TEST_DIR/event.json"

# Mock rationale: We create a dummy proverbs file for deterministic testing.
# With only one proverb, we ensure that specific proverb is picked.
echo "The best defense against a rogue AI is a well-tested regex." > "$PROVERBS_FILE"

# Mock rationale: Simulate the GITHUB_EVENT_PATH payload for a pull request.
echo '{"pull_request": {"number": 123}}' > "$MOCK_GITHUB_EVENT_PATH"

# Mock rationale: Create a mock 'gh' executable.
# This mock 'gh' will simply echo its arguments to a file,
# allowing us to verify what commands were "executed".
cat << 'EOF' > "$TEST_DIR/gh"
#!/bin/bash
echo "MOCK GH CALLED: $@" >> "$MOCK_GH_OUTPUT"
# Simulate reading from stdin for --body-file -
if [[ "$@" == *"--body-file -"* ]]; then
  cat >> "$MOCK_GH_OUTPUT"
fi
EOF
chmod +x "$TEST_DIR/gh"

# Set environment variables for the script
export PATH="$TEST_DIR:$PATH" # Add mock gh to PATH
export GITHUB_TOKEN="mock_token"
export GITHUB_EVENT_PATH="$MOCK_GITHUB_EVENT_PATH"
export GITHUB_REPOSITORY="polsala/ApocalypsAI" # Mock repository
export PROVERBS_FILE="$PROVERBS_FILE" # Pass the mock proverbs file path

# Run the entrypoint script
bash ../src/entrypoint.sh

# Assertions
# Check if the mock gh was called with the correct command and PR number
if ! grep -q "MOCK GH CALLED: pr comment 123 --body-file - --repo polsala/ApocalypsAI" "$MOCK_GH_OUTPUT"; then
  echo "Test Failed: Mock gh was not called correctly for PR comment."
  cat "$MOCK_GH_OUTPUT"
  exit 1
fi

# Check if the specific proverb from the mock file was passed as the body
if ! grep -q "The best defense against a rogue AI is a well-tested regex." "$MOCK_GH_OUTPUT"; then
  echo "Test Failed: Expected proverb not found in mock gh output."
  cat "$MOCK_GH_OUTPUT"
  exit 1
fi

echo "All tests passed!"

# Clean up
rm -rf "$TEST_DIR"
