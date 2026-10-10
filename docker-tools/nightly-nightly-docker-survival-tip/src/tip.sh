#!/usr/bin/env bash
# nightly-docker-survival-tip script

tips=(
"Always carry a spare bottle of water."
"Never trust a smiling mutant."
"Keep your flashlight charged."
"Remember: sand is your friend."
"Stay low, stay quiet."
)

# If an index argument is provided, use it; otherwise pick random
if [[ -n "$1" ]]; then
  idx=$1
else
  idx=$((RANDOM % ${#tips[@]}))
fi

echo "${tips[$idx]}"
