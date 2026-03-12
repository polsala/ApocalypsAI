#!/bin/bash

PR_TITLE="$1"
PR_DESCRIPTION="$2"
TITLE_REGEX="$3"
DESCRIPTION_REGEX="$4"
FAIL_ON_MISMATCH="$5"

echo "--- Cosmic PR Alignment Check ---"
echo "PR Title: ${PR_TITLE}"
echo "PR Description (first 100 chars): ${PR_DESCRIPTION:0:100}..."
echo "Title Regex: ${TITLE_REGEX}"
echo "Description Regex: ${DESCRIPTION_REGEX}"
echo "Fail on Mismatch: ${FAIL_ON_MISMATCH}"
echo "---------------------------------"

TITLE_MATCH=false
# Bash regex matching for title
if [[ "${PR_TITLE}" =~ ${TITLE_REGEX} ]]; then
  echo "✅ PR Title is cosmically aligned!"
  TITLE_MATCH=true
else
  echo "❌ PR Title is NOT cosmically aligned. Expected pattern: '${TITLE_REGEX}'"
fi

DESCRIPTION_MATCH=false
# Bash regex matching for description
if [[ "${PR_DESCRIPTION}" =~ ${DESCRIPTION_REGEX} ]]; then
  echo "✅ PR Description is cosmically aligned!"
  DESCRIPTION_MATCH=true
else
  echo "❌ PR Description is NOT cosmically aligned. Expected pattern: '${DESCRIPTION_REGEX}'"
fi

if [ "$FAIL_ON_MISMATCH" = "true" ]; then
  if [ "$TITLE_MATCH" = "false" ] || [ "$DESCRIPTION_MATCH" = "false" ]; then
    echo "🚨 Cosmic alignment failed! Exiting with error."
    exit 1
  fi
fi

echo "✨ Cosmic alignment check completed."
