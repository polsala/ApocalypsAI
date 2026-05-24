#!/bin/bash

# Arguments:
# $1: PR_UPDATED_AT (ISO 8601 format, e.g., 2023-10-26T10:00:00Z)
# $2: INACTIVITY_DAYS (integer)
# $3: COMMENT_PREFIX (string)
# $4: CURRENT_DATE (ISO 8601 format, e.g., 2023-10-27T10:00:00Z) - for testability

PR_UPDATED_AT=$1
INACTIVITY_DAYS=$2
COMMENT_PREFIX=$3
CURRENT_DATE=$4

# Convert dates to Unix timestamps
# Using GNU date for -d option, common on GitHub Actions runners (Ubuntu)
PR_TIMESTAMP=$(date -d "$PR_UPDATED_AT" +%s)
CURRENT_TIMESTAMP=$(date -d "$CURRENT_DATE" +%s)

# Calculate difference in seconds
DIFF_SECONDS=$((CURRENT_TIMESTAMP - PR_TIMESTAMP))
DIFF_DAYS=$((DIFF_SECONDS / 86400)) # 60 * 60 * 24

SHOULD_COMMENT="false"
COMMENT_BODY=""

if (( DIFF_DAYS >= INACTIVITY_DAYS )); then
  SHOULD_COMMENT="true"
  MESSAGES=(
    "The void whispers, 'Your PR awaits its destiny! A gentle nudge from the cosmic winds.'"
    "Even in the apocalypse, progress is a beacon. This PR is a beacon. Shine on!"
    "A moment of reflection: Is this PR ready to join the annals of merged history? Let's find out!"
    "The stars align for this PR! Perhaps a fresh pair of eyes, or a final commit, is all it needs?"
    "Don't let this PR become a relic of a forgotten era! A little love goes a long way."
    "The ApocalypsAI Integrator senses great potential in this PR. Awaiting your next move!"
    "Time, like a river, flows ever onward. Let's get this PR flowing too!""
    "Is this PR merely resting, or has it entered a state of temporal stasis? A gentle awakening is in order."
  )
  RANDOM_INDEX=$(( RANDOM % ${#MESSAGES[@]} ))
  COMMENT_BODY="${COMMENT_PREFIX} ${MESSAGES[$RANDOM_INDEX]}"
fi

echo "should_comment=$SHOULD_COMMENT"
echo "comment_body=$COMMENT_BODY"
