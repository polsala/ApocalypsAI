#!/bin/sh
set -e

TIPS=(
"Always keep a spare can of beans in your bunker."
"When the sky glows green, stay indoors and listen to the radio."
"A well‑sharpened machete is worth more than gold."
"Never trust a stranger bearing fresh coffee."
"Map the stars at night; they guide the lost."
)

# Get seed from env, default 0
SEED=${SEED:-0}
# Ensure SEED is numeric; fallback to 0 otherwise
case $SEED in
  ''|*[!0-9]*) SEED=0 ;;
esac
COUNT=${#TIPS[@]}
INDEX=$(( SEED % COUNT ))

echo "${TIPS[$INDEX]}"
