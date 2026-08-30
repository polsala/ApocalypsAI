#!/usr/bin/env bash
# Read CSV from stdin or file argument

declare -A items
while IFS=',' read -r name qty; do
  name=$(echo "$name" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
  items["$name"]=$qty
done

# Simple recipe database
declare -A recipes
recipes["rice,beans"]="Rice and Beans Bowl"
recipes["rice,tomato"]="Tomato Rice Soup"
recipes["beans,tomato"]="Bean and Tomato Stew"

suggested=()
for key in "${!recipes[@]}"; do
  IFS=',' read -r a b <<< "$key"
  if [[ -n "${items[$a]}" && -n "${items[$b]}" ]]; then
    suggested+=("${recipes[$key]}")
  fi
done

if [[ ${#suggested[@]} -eq 0 ]]; then
  echo "No recipes found."
else
  echo "Suggested recipes:"
  for r in "${suggested[@]}"; do
    echo "- $r"
  done
fi
