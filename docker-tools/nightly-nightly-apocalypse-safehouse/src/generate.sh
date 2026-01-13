#!/usr/bin/env bash

# nightly‑apocalypse‑safehouse‑generator
# Generates a simple ASCII safe‑house layout.

# Default parameters
rooms=5
seed=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --rooms)
      rooms=$2
      shift 2
      ;;
    --seed)
      seed=$2
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
 done

# Validate rooms
if ! [[ $rooms =~ ^[0-9]+$ ]] || (( rooms < 1 )); then
  echo "--rooms must be a positive integer" >&2
  exit 1
fi

# Set deterministic seed if provided
if [[ -n $seed ]]; then
  RANDOM=$seed
fi

# Helper to generate a random room name
function random_room_name() {
  adjectives=(\"Dusty\" \"Silent\" \"Echoing\" \"Gloomy\" \"Radiant\" \"Shattered\" \"Hidden\" \"Forgotten\")
  nouns=(\"Vault\" \"Bunker\" \"Haven\" \"Sanctum\" \"Lair\" \"Den\" \"Refuge\" \"Outpost\")
  echo "${adjectives[$RANDOM % ${#adjectives[@]}]} ${nouns[$RANDOM % ${#nouns[@]}]}"
}

# Build layout lines
lines=()
for (( i=1; i<=rooms; i++ )); do
  name=$(random_room_name)
  lines+=("| Room $i: $name |")
done

# Determine max width for box drawing
max_len=0
for line in "${lines[@]}"; do
  len=${#line}
  if (( len > max_len )); then
    max_len=$len
  fi
done

# Top border
printf "+%0.s-" $(seq 1 $((max_len-2)))
printf "+
"

# Body
for line in "${lines[@]}"; do
  printf "| %-${max_len-4}s |
" "${line:2:-2}"
 done

# Bottom border
printf "+%0.s-" $(seq 1 $((max_len-2)))
printf "+
"
