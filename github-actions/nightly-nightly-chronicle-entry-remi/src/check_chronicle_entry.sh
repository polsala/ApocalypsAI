#!/bin/bash

# This script checks a PR body for a required phrase and, if not found,
# indicates that a comment should be posted to the PR.

PR_BODY_FILE="$1"
PR_NUMBER="$2"
REPO_FULL_NAME="$3"
GITHUB_TOKEN="$4"
REQUIRED_PHRASE="$5"
COMMENT_MESSAGE="$6"

# Validate all required arguments are provided
if [ -z "$PR_BODY_FILE" ] || [ -z "$PR_NUMBER" ] || [ -z "$REPO_FULL_NAME" ] || [ -z "$GITHUB_TOKEN" ] || [ -z "$REQUIRED_PHRASE" ] || [ -z "$COMMENT_MESSAGE" ]; then
  echo "Error: Missing required arguments for check_chronicle_entry.sh"
  exit 1
fi

# Read the PR body from the provided file
PR_BODY=$(cat "$PR_BODY_FILE")

# Check if the PR body contains the required phrase using regex
if echo "$PR_BODY" | grep -qE "$REQUIRED_PHRASE"; then
  echo "Chronicle Entry found. All clear!"
  echo "chronicle_entry_found=true" >> "$GITHUB_OUTPUT"
  exit 0
else
  echo "Chronicle Entry not found. Reminding contributor..."
  echo "chronicle_entry_found=false" >> "$GITHUB_OUTPUT"

  # Mock rationale: In a real GitHub Action run, this 'gh api' command would post a comment
  # to the Pull Request. For offline, deterministic testing, we print the command
  # that *would* be executed. The test script will verify this output.
  echo "Would post comment: gh api --method POST -H \"Accept: application/vnd.github.v3+json\" /repos/$REPO_FULL_NAME/issues/$PR_NUMBER/comments -f body=\"$COMMENT_MESSAGE\""
  
  # In a live GitHub Actions environment, the actual command would be:
  # gh api --method POST -H "Accept: application/vnd.github.v3+json" \
  #   /repos/"$REPO_FULL_NAME"/issues/"$PR_NUMBER"/comments \
  #   -f body="$COMMENT_MESSAGE"
  
  exit 1 # Indicate failure for the action status
fi
