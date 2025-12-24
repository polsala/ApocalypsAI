#!/usr/bin/env bash

# List of fortunes
fortunes=(
    "You will find unexpected treasure today."
    "A friendly face will bring you good news."
    "Beware of the silent shadows."
    "Your courage will be rewarded soon."
    "A sudden storm will clear the path."
)

# If an index is provided (for testing), use it; otherwise pick random
if [[ -n "$1" ]]; then
    idx=$1
else
    idx=$((RANDOM % ${#fortunes[@]}))
fi

echo "${fortunes[$idx]}"
