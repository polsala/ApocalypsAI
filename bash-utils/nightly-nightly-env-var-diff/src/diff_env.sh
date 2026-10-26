#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <old.env> <new.env>"
  exit 1
fi

old_file=$1
new_file=$2

# Function to parse env file into key=value lines ignoring comments and empty lines
parse() {
  grep -v '^#' "$1" | grep -v '^$' | sort
}

old=$(parse "$old_file")
new=$(parse "$new_file")

# Get keys
old_keys=$(echo "$old" | cut -d= -f1)
new_keys=$(echo "$new" | cut -d= -f1)

# Added: in new not in old
added=$(comm -13 <(echo "$old_keys") <(echo "$new_keys"))
# Removed: in old not in new
removed=$(comm -23 <(echo "$old_keys") <(echo "$new_keys"))
# Potentially changed: intersection
common=$(comm -12 <(echo "$old_keys") <(echo "$new_keys"))

changed=""
while IFS= read -r key; do
  old_val=$(echo "$old" | grep "^${key}=" | cut -d= -f2-)
  new_val=$(echo "$new" | grep "^${key}=" | cut -d= -f2-)
  if [[ "$old_val" != "$new_val" ]]; then
    changed+="${key}: ${old_val} => ${new_val}"$'\n'
  fi
done <<< "$common"

if [[ -n "$added" ]]; then
  echo "Added variables:"
  echo "$added"
  echo
fi

if [[ -n "$removed" ]]; then
  echo "Removed variables:"
  echo "$removed"
  echo
fi

if [[ -n "$changed" ]]; then
  echo "Changed variables:"
  echo -n "$changed"
fi

exit 0
