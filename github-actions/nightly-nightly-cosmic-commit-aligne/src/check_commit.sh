#!/bin/bash

# This script checks a commit message against cosmic alignment principles.
# It takes the commit message, positive keywords, negative keywords, min/max length as arguments.
# Outputs 'aligned: true/false' and 'reason: <message>'

COMMIT_MESSAGE="$1"
POSITIVE_KEYWORDS_STR="$2"
NEGATIVE_KEYWORDS_STR="$3"
MIN_LENGTH="$4"
MAX_LENGTH="$5"

# Convert comma-separated strings to arrays
IFS=',' read -r -a POSITIVE_KEYWORDS <<< "$POSITIVE_KEYWORDS_STR"
IFS=',' read -r -a NEGATIVE_KEYWORDS <<< "$NEGATIVE_KEYWORDS_STR"

ALIGNED="true"
REASON=""

# --- Length Resonance Check ---
MESSAGE_LENGTH=${#COMMIT_MESSAGE}
if (( MESSAGE_LENGTH < MIN_LENGTH )); then
  ALIGNED="false"
  REASON="Commit message is too short ($MESSAGE_LENGTH chars). Minimum is $MIN_LENGTH chars."
elif (( MESSAGE_LENGTH > MAX_LENGTH )); then
  ALIGNED="false"
  REASON="Commit message is too long ($MESSAGE_LENGTH chars). Maximum is $MAX_LENGTH chars."
fi

# --- Positive Vibe Check (only if not already failed by length) ---
# Only perform this check if there are positive keywords defined
if [ "$ALIGNED" = "true" ] && [ ${#POSITIVE_KEYWORDS[@]} -gt 0 ]; then
  FOUND_POSITIVE="false"
  for keyword in "${POSITIVE_KEYWORDS[@]}"; do
    LOWER_MESSAGE=$(echo "$COMMIT_MESSAGE" | tr '[:upper:]' '[:lower:]')
    LOWER_KEYWORD=$(echo "$keyword" | tr '[:upper:]' '[:lower:]')
    # Check for whole word match, case-insensitive
    if [[ "$LOWER_MESSAGE" =~ (^|[[:space:]])$LOWER_KEYWORD($|[[:space:]]) ]]; then
      FOUND_POSITIVE="true"
      break
    fi
  done

  if [ "$FOUND_POSITIVE" = "false" ]; then
    ALIGNED="false"
    REASON="Commit message lacks positive cosmic energy. Consider using keywords like: ${POSITIVE_KEYWORDS_STR}."
  fi
fi

# --- Negative Energy Shield (only if not already failed) ---
# Only perform this check if there are negative keywords defined
if [ "$ALIGNED" = "true" ] && [ ${#NEGATIVE_KEYWORDS[@]} -gt 0 ]; then
  for keyword in "${NEGATIVE_KEYWORDS[@]}"; do
    LOWER_MESSAGE=$(echo "$COMMIT_MESSAGE" | tr '[:upper:]' '[:lower:]')
    LOWER_KEYWORD=$(echo "$keyword" | tr '[:upper:]' '[:lower:]')
    # Check for whole word match, case-insensitive
    if [[ "$LOWER_MESSAGE" =~ (^|[[:space:]])$LOWER_KEYWORD($|[[:space:]]) ]]; then
      ALIGNED="false"
      REASON="Commit message contains negative cosmic energy: '$keyword'. Please rephrase for celestial harmony."
      break
    fi
  done
fi

echo "aligned: $ALIGNED"
echo "reason: $REASON"

if [ "$ALIGNED" = "false" ]; then
  exit 1
fi
