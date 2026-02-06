#!/usr/bin/env sh\n# Select a random tip from tips.txt and print it.\nif [ -f tips.txt ]; then\n  tip=$(shuf -n 1 tips.txt)\n  echo "$tip"\nelse\n  echo "No tips available."\n  exit 1\nfi
