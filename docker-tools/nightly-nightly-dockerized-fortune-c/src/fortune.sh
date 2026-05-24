#!/bin/sh

# List of whimsical fortunes (one per line)
FORTUNES="You will find a hidden stash of canned beans.
A friendly mutant will share a secret.
Your compass points to the nearest coffee shop.
A stray robot will become your companion.
The clouds whisper the password to the vault."

# Use SEED env var for deterministic selection; fall back to current timestamp
SEED="${SEED:-$(date +%s)}"

# Count the number of fortunes
COUNT=$(printf "%s" "$FORTUNES" | wc -l)

# Select a line deterministically: (SEED % COUNT) + 1
INDEX=$(( (SEED % COUNT) + 1 ))

# Extract the chosen fortune using awk
SELECTED=$(printf "%s\n" "$FORTUNES" | awk -v idx="$INDEX" 'NR==idx')

printf "%s\n" "$SELECTED"
