#!/usr/bin/env bash
set -e
# Use INPUT_DATE if provided, otherwise current UTC date
if [ -n "${INPUT_DATE}" ]; then
  DATE="${INPUT_DATE}"
else
  DATE=$(date -u +"%Y-%m-%d")
fi
# Compute weekday name
WEEKDAY=$(date -d "$DATE" +"%A")
# Write to GITHUB_OUTPUT
echo "weekday=$WEEKDAY" >> "$GITHUB_OUTPUT"
