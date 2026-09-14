#!/bin/bash

PR_TITLE="$1"
PR_BODY="$2"
WHIMSY_KEYWORDS_STR="$3"
DOOM_KEYWORDS_STR="$4"
MIN_WHIMSY_COUNT="$5"
MIN_DOOM_COUNT="$6"

# Convert comma-separated strings to arrays
IFS=',' read -r -a WHIMSY_KEYWORDS <<< "$WHIMSY_KEYWORDS_STR"
IFS=',' read -r -a DOOM_KEYWORDS <<< "$DOOM_KEYWORDS_STR"

# Combine title and body for checking
CONTENT="${PR_TITLE} ${PR_BODY}"
CONTENT_LOWER=$(echo "$CONTENT" | tr '[:upper:]' '[:lower:]')

WHIMSY_FOUND_COUNT=0
for keyword in "${WHIMSY_KEYWORDS[@]}"; do
  # Ensure keyword is lowercased for comparison
  lower_keyword=$(echo "$keyword" | tr '[:upper:]' '[:lower:]')
  if [[ "$CONTENT_LOWER" =~ "$lower_keyword" ]]; then
    WHIMSY_FOUND_COUNT=$((WHIMSY_FOUND_COUNT + 1))
  fi
done

DOOM_FOUND_COUNT=0
for keyword in "${DOOM_KEYWORDS[@]}"; do
  # Ensure keyword is lowercased for comparison
  lower_keyword=$(echo "$keyword" | tr '[:upper:]' '[:lower:]')
  if [[ "$CONTENT_LOWER" =~ "$lower_keyword" ]]; then
    DOOM_FOUND_COUNT=$((DOOM_FOUND_COUNT + 1))
  fi
done

MESSAGE=""
STATUS="pass"

if (( WHIMSY_FOUND_COUNT < MIN_WHIMSY_COUNT )); then
  MESSAGE+="Lacks sufficient whimsy (found $WHIMSY_FOUND_COUNT, requires $MIN_WHIMSY_COUNT). "
  STATUS="fail"
fi

if (( DOOM_FOUND_COUNT < MIN_DOOM_COUNT )); then
  MESSAGE+="Lacks sufficient doom (found $DOOM_FOUND_COUNT, requires $MIN_DOOM_COUNT). "
  STATUS="fail"
fi

if [ "$STATUS" = "pass" ]; then
  MESSAGE="Tone check passed! Found $WHIMSY_FOUND_COUNT whimsical and $DOOM_FOUND_COUNT doom-related keywords."
fi

echo "status:$STATUS"
echo "message:$MESSAGE"

if [ "$STATUS" = "fail" ]; then
  exit 1
fi
