#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <old.env> <new.env>"
  exit 1
fi

old_file=$1
new_file=$2

# Parse an .env file: strip comments/blank lines and sort
parse_env() {
  grep -v '^#' "$1" | grep -v '^$' | sort
}

old_kv=$(parse_env "$old_file")
new_kv=$(parse_env "$new_file")

# Determine added, removed, and common lines
added=$(comm -13 <(echo "$old_kv") <(echo "$new_kv") || true)
removed=$(comm -23 <(echo "$old_kv") <(echo "$new_kv") || true)
common=$(comm -12 <(echo "$old_kv") <(echo "$new_kv") || true)

# Detect changed keys (present in both but with different values)
changed_keys=""
while IFS='=' read -r key _; do
  old_val=$(grep "^$key=" <<<"$old_kv" | cut -d'=' -f2-)
  new_val=$(grep "^$key=" <<<"$new_kv" | cut -d'=' -f2-)
  if [[ "$old_val" != "$new_val" ]]; then
    changed_keys+="$key\n"
  fi
done <<<"$common"

# Output report
if [[ -n "$added" ]]; then
  echo "🚀 Added variables:"
  while IFS= read -r line; do
    echo "  + $line"
  done <<<"$added"
fi

if [[ -n "$removed" ]]; then
  echo "🗑️ Removed variables:"
  while IFS= read -r line; do
    echo "  - $line"
  done <<<"$removed"
fi

if [[ -n "$changed_keys" ]]; then
  echo "🔄 Changed variables:"
  while IFS= read -r key; do
    old_val=$(grep "^$key=" <<<"$old_kv" | cut -d'=' -f2-)
    new_val=$(grep "^$key=" <<<"$new_kv" | cut -d'=' -f2-)
    echo "  * $key: \"$old_val\" → \"$new_val\""
  done <<<"$changed_keys"
fi

if [[ -z "$added" && -z "$removed" && -z "$changed_keys" ]]; then
  echo "✅ No differences detected. Your env is in perfect harmony."
fi
