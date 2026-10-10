#!/usr/bin/env bash
set -euo pipefail

# Default values
NUM=5
MAP_FILE=""
REPO="."

# Parse options
while getopts "n:m:d:" opt; do
  case $opt in
    n) NUM=$OPTARG ;;
    m) MAP_FILE=$OPTARG ;;
    d) REPO=$OPTARG ;;
    *)
      echo "Usage: $0 [-n NUM] [-m MAP_FILE] [-d REPO]" >&2
      exit 1
      ;;
  esac
done

# Build keyword‑to‑emoji map
declare -A map
if [[ -n $MAP_FILE ]]; then
  while IFS='=' read -r key val; do
    # Skip empty lines or comments
    [[ -z $key ]] && continue
    [[ $key == \#* ]] && continue
    map["$key"]=$val
  done < "$MAP_FILE"
else
  # Built‑in defaults
  map["fix"]="🔧"
  map["bug"]="🐞"
  map["feature"]="✨"
fi

# Retrieve commit messages
pushd "$REPO" > /dev/null
COMMIT_MSGS=$(git log -n "$NUM" --pretty=%B)
popd > /dev/null

# Process each line of the commit messages
while IFS= read -r line; do
  out="$line"
  for k in "${!map[@]}"; do
    v="${map[$k]}"
    # Use word boundaries to avoid partial replacements
    out=$(echo "$out" | sed -E "s/\\b${k}\\b/${v}/g")
  done
  echo "$out"
done <<< "$COMMIT_MSGS"
