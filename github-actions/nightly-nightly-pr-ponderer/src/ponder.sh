#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Extract PR number from GITHUB_REF
# GITHUB_REF format: refs/pull/<PR_NUMBER>/merge
PR_NUMBER=$(echo "$GITHUB_REF" | awk -F'/' '{print $3}')

if [ -z "$PR_NUMBER" ]; then
  echo "Could not determine PR number from GITHUB_REF: $GITHUB_REF. Skipping comment."
  exit 0
fi

# Use provided questions file or a default one
QUESTIONS_FILE_PATH="${QUESTIONS_FILE:-.github/pr_ponderer_questions.txt}"

# Default questions if the file doesn't exist or is empty
DEFAULT_QUESTIONS=(
  "What if the universe is just a giant simulation, and this PR is a critical patch?"
  "Have you considered the existential implications of this code's future maintenance?"
  "If a tree falls in the forest and no one reviews its PR, does it still merge?"
  "Does this PR spark joy, or merely fix a bug?"
  "In the grand tapestry of existence, how does this change weave its thread?"
  "Is this code truly 'done', or merely 'released'?"
  "What wisdom would a future archaeologist glean from this commit?"
  "If this PR were a philosophical treatise, what would its central argument be?"
  "Beyond the immediate fix, what deeper truth does this code reveal?"
  "Does this solution simplify complexity, or merely shift it elsewhere?"
)

QUESTIONS=()
if [ -f "$QUESTIONS_FILE_PATH" ] && [ -s "$QUESTIONS_FILE_PATH" ]; then
  # Read questions from file, one per line
  mapfile -t QUESTIONS < "$QUESTIONS_FILE_PATH"
else
  echo "Questions file '$QUESTIONS_FILE_PATH' not found or is empty. Using default questions."
  QUESTIONS=("${DEFAULT_QUESTIONS[@]}")
fi

NUM_QUESTIONS=${#QUESTIONS[@]}

if [ "$NUM_QUESTIONS" -eq 0 ]; then
  echo "No questions available to ponder. Skipping comment."
  exit 0
fi

# Pick a random question
RANDOM_INDEX=$(( RANDOM % NUM_QUESTIONS ))
PONDER_QUESTION="${QUESTIONS[$RANDOM_INDEX]}"

# Construct the comment body
COMMENT_BODY="### 🤔 A Moment to Ponder...\n\n${PONDER_QUESTION}\n\n---\n_This message was brought to you by the ApocalypsAI Nightly Integrator._"

# Post the comment using GitHub CLI
# Mock rationale: In a real run, this would post to GitHub. For tests, 'gh' is mocked.
gh api \
  --method POST \
  -H "Accept: application/vnd.github.v3+json" \
  "/repos/$GITHUB_REPOSITORY/issues/$PR_NUMBER/comments" \
  -f body="$COMMENT_BODY"

echo "Pondering question added to PR #$PR_NUMBER."
