#!/usr/bin/env bash
set -euo pipefail

# Predefined motivational phrases
PHRASES=(
    "Keep calm and carry on."
    "The only limit is your mind."
    "Every day is a new adventure."
    "Believe you can and you're halfway there."
    "Stay curious, stay humble."
)

# If the user supplied a custom phrase, use it; otherwise pick randomly
if [[ -n "${ECHO_ECHO_PHRASE:-}" ]]; then
    PHRASE="${ECHO_ECHO_PHRASE}"
else
    INDEX=$((RANDOM % ${#PHRASES[@]}))
    PHRASE="${PHRASES[$INDEX]}"
fi

# Current UTC timestamp in ISO 8601
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Output
printf "%s %s\n" "[$TIMESTAMP]" "$PHRASE"
