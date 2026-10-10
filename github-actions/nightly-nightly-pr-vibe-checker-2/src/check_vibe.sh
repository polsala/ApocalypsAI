#!/bin/bash

set -euo pipefail

PR_TITLE=$(jq -r .pull_request.title "$GITHUB_EVENT_PATH")
PR_TITLE_LOWER=$(echo "$PR_TITLE" | tr '[:upper:]' '[:lower:]')

REQUIRED_KEYWORDS_STR="${INPUT_REQUIRED_KEYWORDS}"
FORBIDDEN_KEYWORDS_STR="${INPUT_FORBIDDEN_KEYWORDS}"
FAIL_ON_NO_MATCH_REQUIRED="${INPUT_FAIL_ON_NO_MATCH_REQUIRED}"
FAIL_ON_MATCH_FORBIDDEN="${INPUT_FAIL_ON_MATCH_FORBIDDEN}"

VIBE_STATUS="pass"

echo "--- PR Vibe Check ---"
echo "PR Title: '$PR_TITLE'"

# Check for required keywords
if [ -n "$REQUIRED_KEYWORDS_STR" ]; then
    REQUIRED_FOUND=false
    IFS=',' read -ra REQUIRED_ARRAY <<< "$REQUIRED_KEYWORDS_STR"
    for keyword in "${REQUIRED_ARRAY[@]}"; do
        keyword_lower=$(echo "$keyword" | tr '[:upper:]' '[:lower:]')
        if [[ "$PR_TITLE_LOWER" == *"$keyword_lower"* ]]; then
            echo "✅ Required keyword found: '$keyword'"
            REQUIRED_FOUND=true
            break
        fi
    done

    if [ "$REQUIRED_FOUND" = false ]; then
        echo "❌ No required keywords found in PR title. Required: '$REQUIRED_KEYWORDS_STR'"
        VIBE_STATUS="fail"
        if [ "$FAIL_ON_NO_MATCH_REQUIRED" = "true" ]; then
            echo "::error ::PR title does not contain any required keywords." >&2
            exit 1
        fi
    fi
fi

# Check for forbidden keywords
if [ -n "$FORBIDDEN_KEYWORDS_STR" ]; then
    FORBIDDEN_FOUND=false
    IFS=',' read -ra FORBIDDEN_ARRAY <<< "$FORBIDDEN_KEYWORDS_STR"
    for keyword in "${FORBIDDEN_ARRAY[@]}"; do
        keyword_lower=$(echo "$keyword" | tr '[:upper:]' '[:lower:]')
        if [[ "$PR_TITLE_LOWER" == *"$keyword_lower"* ]]; then
            echo "❌ Forbidden keyword found: '$keyword'"
            FORBIDDEN_FOUND=true
            break
        fi
    done

    if [ "$FORBIDDEN_FOUND" = true ]; then
        VIBE_STATUS="fail"
        if [ "$FAIL_ON_MATCH_FORBIDDEN" = "true" ]; then
            echo "::error ::PR title contains forbidden keywords." >&2
            exit 1
        fi
    fi
fi

echo "Vibe Status: $VIBE_STATUS"
echo "vibe-status=$VIBE_STATUS" >> "$GITHUB_OUTPUT"
