#!/bin/sh
# tip.sh - prints a random survival tip
TIP_FILE="tips.txt"
if [ ! -f "$TIP_FILE" ]; then
  echo "No tips found."
  exit 1
fi
# Use shuf if available, else fallback to awk random
if command -v shuf >/dev/null 2>&1; then
  tip=$(shuf -n 1 "$TIP_FILE")
else
  tip=$(awk 'BEGIN{srand()}{print rand() "\t" $0}' "$TIP_FILE" | sort -k1,1n | cut -f2- | head -n1)
fi
echo "$tip"
