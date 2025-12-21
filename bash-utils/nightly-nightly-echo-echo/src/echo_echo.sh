#!/usr/bin/env bash
set -euo pipefail

PHRASES=(
  "The sky is a canvas of possibility."
  "Every bug is a hidden treasure."
  "Keep calm and code on."
  "When in doubt, add a comment."
  "The terminal is your playground."
)

usage() {
  echo "Usage: $0 [--list]"
  exit 1
}

if [[ $# -gt 0 ]]; then
  case "$1" in
    --list)
      printf "%s\n" "${PHRASES[@]}"
      exit 0
      ;;
    *)
      usage
      ;;
  esac
fi

# pick random
index=$((RANDOM % ${#PHRASES[@]}))
echo "${PHRASES[$index]}"
