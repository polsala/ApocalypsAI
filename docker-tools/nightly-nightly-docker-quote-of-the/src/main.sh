#!/usr/bin/env sh
# Read quotes from quotes.txt
QUOTES=$(cat quotes.txt | grep -v '^#' | grep -v '^$')
# Count lines
COUNT=$(echo "$QUOTES" | wc -l | tr -d ' ')
# Determine index
if [ -n "$QUOTE_INDEX" ]; then
  INDEX=$((QUOTE_INDEX % COUNT))
else
  INDEX=$((RANDOM % COUNT))
fi
# Get the quote
QUOTE=$(echo "$QUOTES" | sed -n "$((INDEX+1))p")
echo "$QUOTE"
