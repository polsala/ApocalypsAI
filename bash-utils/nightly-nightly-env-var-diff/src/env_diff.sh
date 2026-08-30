#!/usr/bin/env bash

# nightly-env-var-diff – compare two .env files
# -------------------------------------------------
# Prints added, removed, and modified variables.
# -------------------------------------------------

set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <old.env> <new.env>" >&2
  exit 1
fi

old_file="$1"
new_file="$2"

# Ensure files exist
if [[ ! -f "$old_file" ]]; then
  echo "Error: '$old_file' does not exist" >&2
  exit 1
fi
if [[ ! -f "$new_file" ]]; then
  echo "Error: '$new_file' does not exist" >&2
  exit 1
fi

declare -A old_vars new_vars

parse_file() {
  local file="$1"
  local -n assoc=$2
  while IFS= read -r line || [[ -n "$line" ]]; do
    # Skip empty lines and comments
    [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
    # Trim surrounding whitespace
    line=$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    # Split on first '='
    key="${line%%=*}"
    value="${line#*=}"
    assoc["$key"]="$value"
  done < "$file"
}

parse_file "$old_file" old_vars
parse_file "$new_file" new_vars

added=()
removed=()
modified=()

# Detect added and modified
for key in "${!new_vars[@]}"; do
  if [[ -v "old_vars[$key]" ]]; then
    if [[ "${old_vars[$key]}" != "${new_vars[$key]}" ]]; then
      modified+=("$key=${old_vars[$key]} -> ${new_vars[$key]}")
    fi
  else
    added+=("$key=${new_vars[$key]}")
  fi
done

# Detect removed
for key in "${!old_vars[@]}"; do
  if [[ ! -v "new_vars[$key]" ]]; then
    removed+=("$key=${old_vars[$key]}")
  fi
done

output_section() {
  local title="$1"
  shift
  local items=("$@")
  if [[ ${#items[@]} -gt 0 ]]; then
    echo "$title:"
    for i in "${items[@]}"; do
      echo "  $i"
    done
  fi
}

output_section "Added" "${added[@]}"
output_section "Removed" "${removed[@]}"
output_section "Modified" "${modified[@]}"
