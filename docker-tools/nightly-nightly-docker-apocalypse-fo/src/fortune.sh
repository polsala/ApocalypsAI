#!/bin/sh
set -e
FILE="fortunes.txt"
if [ ! -f "$FILE" ]; then
  echo "Fortunes file missing"
  exit 1
fi
if [ -n "$FORTUNE_INDEX" ]; then
  INDEX=$FORTUNE_INDEX
else
  TOTAL=$(wc -l < "$FILE")
  INDEX=$(( (RANDOM % TOTAL) + 1 ))
fi
sed -n "${INDEX}p" "$FILE"
