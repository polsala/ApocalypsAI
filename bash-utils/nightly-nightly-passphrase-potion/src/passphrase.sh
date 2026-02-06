#!/usr/bin/env bash

# nightly-passphrase-potion – whimsical passphrase generator
# ----------------------------------------------------------
# Usage: ./passphrase.sh [--list <wordfile>] [--seed <int>]
#   --list : path to a word list (one word per line). Defaults to /usr/share/dict/words.
#   --seed : integer seed for deterministic output (useful for tests).
#
# The script selects four words, capitalises the first letter of each,
# and joins them with four symbols drawn from a predefined set.

set -euo pipefail

# Default configuration
WORD_FILE="/usr/share/dict/words"
SEED=""
SYMBOLS=('!' '@' '#' '$' '%' '&' '*' '?')
WORD_COUNT=4

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --list)
      WORD_FILE="$2"
      shift 2
      ;;
    --seed)
      SEED="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

# Load words into an array, ignoring empty lines and comments
if [[ ! -f "$WORD_FILE" ]]; then
  echo "Word list not found: $WORD_FILE" >&2
  exit 1
fi
mapfile -t WORDS < <(grep -vE '^#|^$' "$WORD_FILE")
TOTAL=${#WORDS[@]}
if (( TOTAL == 0 )); then
  echo "Word list is empty: $WORD_FILE" >&2
  exit 1
fi

# Helper to get deterministic index
get_index() {
  local offset=$1
  if [[ -n "$SEED" ]]; then
    echo $(( (SEED + offset) % TOTAL ))
  else
    echo $(( RANDOM % TOTAL ))
  fi
}

# Helper to get deterministic symbol index
get_sym_index() {
  local offset=$1
  local sym_total=${#SYMBOLS[@]}
  if [[ -n "$SEED" ]]; then
    echo $(( (SEED + offset) % sym_total ))
  else
    echo $(( RANDOM % sym_total ))
  fi
}

PASS=""
for i in $(seq 0 $((WORD_COUNT-1))); do
  idx=$(get_index $i)
  word="${WORDS[$idx]}"
  # Capitalise first letter
  word_capitalized="${word^}"
  PASS+="$word_capitalized"
  if (( i < WORD_COUNT-1 )); then
    sym_idx=$(get_sym_index $i)
    PASS+="${SYMBOLS[$sym_idx]}"
  fi
done

echo "$PASS"
