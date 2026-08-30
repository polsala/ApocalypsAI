#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Running tests for nightly-code-complimenter..."

# --- Mocking curl ---
# Mock rationale: `curl` is mocked to prevent actual network calls to GitHub,
# ensuring tests are deterministic and offline. It captures the arguments
# passed to it and simulates a successful API response.
MOCKED_CURL_ARGS=""
MOCKED_CURL_DATA=""
MOCKED_CURL_URL=""

curl() {
    MOCKED_CURL_ARGS="$@"
    MOCKED_CURL_DATA=""
    MOCKED_CURL_URL=""

    local next_arg_is_data=false
    for arg in "$@"; do
        if [ "$next_arg_is_data" = true ]; then
            MOCKED_CURL_DATA="$arg"
            next_arg_is_data=false
        fi

        if [ "$arg" = "-d" ]; then
            next_arg_is_data=true
        elif [[ ! "$arg" =~ ^- ]]; then # If it's not an option, it might be the URL
            MOCKED_CURL_URL="$arg"
        fi
    done

    # Remove quotes from data if present
    MOCKED_CURL_DATA=$(echo "$MOCKED_CURL_DATA" | sed 's/^"//;s/"$//')

    echo "Mocked curl called with: $*" >&2
    echo "Captured URL: $MOCKED_CURL_URL" >&2
    echo "Captured Data: $MOCKED_CURL_DATA" >&2
    echo '{"id": 12345, "body": "Mocked compliment", "url": "https://api.github.com/repos/test/repo/issues/1/comments/12345"}'
    return 0 # Simulate success
}
export -f curl # Make the mock function available to subshells

# --- Test Variables ---
TEST_GITHUB_TOKEN="ghp_test_token"
TEST_PR_NUMBER="123"
TEST_REPO_FULL_NAME="test-org/test-repo"
TEST_COMPLIMENT_TYPE="general"

# --- Run the script with test variables ---
echo "Executing src/complimenter.sh with mocked environment..."
GITHUB_TOKEN="${TEST_GITHUB_TOKEN}" \
PR_NUMBER="${TEST_PR_NUMBER}" \
REPO_FULL_NAME="${TEST_REPO_FULL_NAME}" \
COMPLIMENT_TYPE="${TEST_COMPLIMENT_TYPE}" \
bash src/complimenter.sh

# --- Assertions ---
echo "Verifying curl call..."

# 1. Check if curl was called
if [ -z "$MOCKED_CURL_ARGS" ]; then
    echo "Test Failed: curl was not called."
    exit 1
fi

# 2. Check HTTP method
if ! echo "$MOCKED_CURL_ARGS" | grep -q -- "-X POST"; then
    echo "Test Failed: curl was not called with -X POST."
    exit 1
fi

# 3. Check Authorization header
if ! echo "$MOCKED_CURL_ARGS" | grep -q -- "-H \"Authorization: token ${TEST_GITHUB_TOKEN}\""; then
    echo "Test Failed: Authorization header missing or incorrect."
    exit 1
fi

# 4. Check Accept header
if ! echo "$MOCKED_CURL_ARGS" | grep -q -- "-H \"Accept: application/vnd.github.v3+json\""; then
    echo "Test Failed: Accept header missing or incorrect."
    exit 1
fi

# 5. Check API URL
EXPECTED_API_URL="https://api.github.com/repos/${TEST_REPO_FULL_NAME}/issues/${TEST_PR_NUMBER}/comments"
if [ "$MOCKED_CURL_URL" != "$EXPECTED_API_URL" ]; then
    echo "Test Failed: Incorrect API URL. Expected '$EXPECTED_API_URL', got '$MOCKED_CURL_URL'."
    exit 1
fi

# 6. Check Payload content (body should contain a compliment)
if [ -z "$MOCKED_CURL_DATA" ]; then
    echo "Test Failed: No data payload (-d) found in curl call."
    exit 1
fi

# The payload is a JSON string. We need to parse it to check the 'body' field.
# Mock rationale: `jq` is used here to parse the captured JSON payload,
# which is part of the test's internal logic, not an external dependency for the action itself.
# It's used to verify the structure and content of the data sent to the mocked API.
COMMENT_BODY=$(echo "$MOCKED_CURL_DATA" | jq -r '.body')

if [ -z "$COMMENT_BODY" ]; then
    echo "Test Failed: Comment body is empty in the payload."
    exit 1
fi

# Check if the comment body is one of the predefined compliments
# Source the script to get the COMPLIMENTS array for validation
. src/complimenter.sh

IS_VALID_COMPLIMENT=false
for C in "${COMPLIMENTS[@]}"; do
    if [ "$COMMENT_BODY" == "$C" ]; then
        IS_VALID_COMPLIMENT=true
        break
    fi
done

if [ "$IS_VALID_COMPLIMENT" = false ]; then
    echo "Test Failed: Posted comment body is not one of the expected compliments."
    echo "Posted: '$COMMENT_BODY'"
    exit 1
fi

echo "All tests passed for nightly-code-complimenter!"
exit 0
