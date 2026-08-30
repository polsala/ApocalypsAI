#!/bin/bash

MAX_STASIS_DAYS=$1
FAIL_ON_STASIS=$2

echo "Nightly Commit Chronometer: Initiating temporal stasis scan..."

# Get the last commit date in ISO 8601 format
LAST_COMMIT_DATE_STR=$(git log -1 --format=%cd --date=iso-strict HEAD)
if [ -z "$LAST_COMMIT_DATE_STR" ]; then
  echo "::error::Could not retrieve last commit date. Is this a valid git repository?"
  exit 1
fi

# Convert to Unix timestamp
LAST_COMMIT_TIMESTAMP=$(date -d "$LAST_COMMIT_DATE_STR" +%s)
CURRENT_TIMESTAMP=$(date +%s)

# Calculate difference in seconds, then convert to days
TIME_DIFF_SECONDS=$((CURRENT_TIMESTAMP - LAST_COMMIT_TIMESTAMP))
COMMIT_AGE_DAYS=$((TIME_DIFF_SECONDS / 86400)) # 86400 seconds in a day

echo "Last commit detected: $LAST_COMMIT_DATE_STR"
echo "Current temporal flux: $COMMIT_AGE_DAYS days since last commit."
echo "Temporal stasis threshold: $MAX_STASIS_DAYS days."

STASIS_DETECTED="false"
if (( COMMIT_AGE_DAYS > MAX_STASIS_DAYS )); then
  STASIS_DETECTED="true"
  MESSAGE="Temporal stasis detected! This branch's last commit is $COMMIT_AGE_DAYS days old, exceeding the threshold of $MAX_STASIS_DAYS days."
  if [ "$FAIL_ON_STASIS" = "true" ]; then
    echo "::error::$MESSAGE"
    exit 1
  else
    echo "::warning::$MESSAGE"
  fi
else
  echo "Temporal flow is healthy. No stasis detected."
fi

echo "stasis-detected=$STASIS_DETECTED" >> "$GITHUB_OUTPUT"
echo "commit-age-days=$COMMIT_AGE_DAYS" >> "$GITHUB_OUTPUT"

exit 0
