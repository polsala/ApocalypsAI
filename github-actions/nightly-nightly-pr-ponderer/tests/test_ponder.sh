#!/bin/bash

# Mock rationale: We need to prevent actual GitHub API calls during testing
# and instead capture the arguments passed to the 'gh' command to verify them.
# This mock simulates the 'gh' CLI tool's behavior for creating comments.

# --- Setup Mock gh ---
MOCK_GH_DIR=$(mktemp -d)
MOCK_GH_OUTPUT="${MOCK_GH_DIR}/gh_output.json"
MOCK_GH_PATH="${MOCK_GH_DIR}/gh"

cat <<EOF > "$MOCK_GH_PATH"
#!/bin/bash
echo "\$@" > "$MOCK_GH_OUTPUT"
echo '{"id": 123, "body": "Mock comment"}' # Simulate gh output
EOF
chmod +x "$MOCK_GH_PATH"

export PATH="$MOCK_GH_DIR:$PATH"
# --- End Setup Mock gh ---

# --- Setup Test Environment ---
TEST_QUESTIONS_FILE=$(mktemp)
cat <<EOF > "$TEST_QUESTIONS_FILE"
What if the universe is just a giant simulation, and this PR is a critical patch?
Have you considered the existential implications of this code's future maintenance?
If a tree falls in the forest and no one reviews its PR, does it still merge?
EOF

export GITHUB_TOKEN="mock-token" # Mock rationale: Prevent actual auth, just needs to be present
export GITHUB_REPOSITORY="polsala/ApocalypsAI"
export GITHUB_REF="refs/pull/42/merge" # Mock rationale: Simulate a PR context
export QUESTIONS_FILE="$TEST_QUESTIONS_FILE"

# --- Run the script ---
# Assuming src/ponder.sh is in the same directory as this test script for simplicity
# In a real action, github.action_path would point to the action's root.
# For this test, we'll simulate that by directly calling the script.
SCRIPT_PATH="$(dirname "$0")"/../src/ponder.sh
chmod +x "$SCRIPT_PATH"
"$SCRIPT_PATH"

# --- Assertions ---
if [ ! -f "$MOCK_GH_OUTPUT" ]; then
    echo "Test failed: Mock gh was not called."
    exit 1
fi

GH_CALL_ARGS=$(cat "$MOCK_GH_OUTPUT")

# Check if 'gh api' was called
if ! echo "$GH_CALL_ARGS" | grep -q "api"; then
    echo "Test failed: 'gh api' not found in call arguments."
    echo "Args: $GH_CALL_ARGS"
    exit 1
fi

# Check if the correct endpoint was targeted
if ! echo "$GH_CALL_ARGS" | grep -q "repos/polsala/ApocalypsAI/issues/42/comments"; then
    echo "Test failed: Incorrect API endpoint."
    echo "Args: $GH_CALL_ARGS"
    exit 1
fi

# Check if the comment body contains one of the questions
# The comment body will be escaped in the gh api call, so we need to match the escaped version
COMMENT_BODY_PATTERN="### 🤔 A Moment to Ponder...\\n\\n"

if ! echo "$GH_CALL_ARGS" | grep -q "${COMMENT_BODY_PATTERN}What if the universe is just a giant simulation, and this PR is a critical patch?\\n\\n---\\n_This message was brought to you by the ApocalypsAI Nightly Integrator._" && \
   ! echo "$GH_CALL_ARGS" | grep -q "${COMMENT_BODY_PATTERN}Have you considered the existential implications of this code's future maintenance?\\n\\n---\\n_This message was brought to you by the ApocalypsAI Nightly Integrator._" && \
   ! echo "$GH_CALL_ARGS" | grep -q "${COMMENT_BODY_PATTERN}If a tree falls in the forest and no one reviews its PR, does it still merge?\\n\\n---\\n_This message was brought to you by the ApocalypsAI Nightly Integrator._"; then
    echo "Test failed: Comment body does not contain an expected question."
    echo "GH Call Args: $GH_CALL_ARGS"
    exit 1
fi

echo "All tests passed!"

# --- Cleanup ---
rm -rf "$MOCK_GH_DIR"
rm "$TEST_QUESTIONS_FILE"
