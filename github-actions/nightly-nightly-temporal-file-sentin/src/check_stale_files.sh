#!/bin/bash

AGE_THRESHOLD_DAYS=$1
CURRENT_TIMESTAMP=$(date +%s)
THRESHOLD_SECONDS=$((AGE_THRESHOLD_DAYS * 24 * 60 * 60))
STALE_FILES=""

# Use git ls-files to get all tracked files
git ls-files | while read -r file; do
    # Get the last commit timestamp for the file
    # %at is author date, UNIX timestamp
    LAST_MOD_TIMESTAMP=$(git log -1 --format="%at" -- "$file" 2>/dev/null)

    if [ -z "$LAST_MOD_TIMESTAMP" ]; then
        # File might be new and not yet committed, or untracked.
        # For this utility, we focus on tracked files with a commit history.
        continue
    fi

    AGE_SECONDS=$((CURRENT_TIMESTAMP - LAST_MOD_TIMESTAMP))

    if [ "$AGE_SECONDS" -gt "$THRESHOLD_SECONDS" ]; then
        STALE_FILES+="$file\n"
    fi
done

# Remove trailing newline if any and print
echo -e "$STALE_FILES" | sed '/^$/d'
