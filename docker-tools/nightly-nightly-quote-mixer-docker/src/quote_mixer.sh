#!/usr/bin/env bash
set -euo pipefail

# Default line number
LINE=${1:-1}

# Files
MOTIVATIONAL="/app/src/motivational.txt"
APOCALYPTIC="/app/src/apocalyptic.txt"

# Get total lines
MOT_LINES=$(wc -l < "$MOTIVATIONAL")
APO_LINES=$(wc -l < "$APOCALYPTIC")

# Wrap line number
MOT_LINE=$(( (LINE - 1) % MOT_LINES + 1 ))
APO_LINE=$(( (LINE - 1) % APO_LINES + 1 ))

# Extract lines
MOT_QUOTE=$(sed -n "${MOT_LINE}p" "$MOTIVATIONAL")
APO_QUOTE=$(sed -n "${APO_LINE}p" "$APOCALYPTIC")

# Output combined quote
echo "\"$MOT_QUOTE\" — $APO_QUOTE"
