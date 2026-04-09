#!/bin/sh

# List of whimsical apocalypse survival tips
TIPS=(
  "Always keep a spare can of beans."
  "Never trust a talking cactus."
  "Water is more valuable than gold."
  "Map your routes before the sky falls."
  "Carry a multi‑tool, even if you don't need it."
)

COUNT=${#TIPS[@]}

if [ -n "$1" ]; then
  SEED=$1
  INDEX=$((SEED % COUNT))
else
  # $RANDOM is available in ash (Alpine's /bin/sh)
  INDEX=$((RANDOM % COUNT))
fi

echo "${TIPS[$INDEX]}"
