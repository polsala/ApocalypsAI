#!/usr/bin/env bash

# nightly-env-var-diff
# Compare two .env files and report added, removed, and modified variables.
# Usage: ./src/diff_env.sh <old.env> <new.env>

set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <old.env> <new.env>" >&2
  exit 1
fi

old_file="$1"
new_file="$2"

declare -A old_vars
declare -A new_vars

load_file() {
  local file="$1"
  declare -n map_ref="$2"
  while IFS='=' read -r key value; do
    # Trim whitespace
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)
    # Skip empty lines and comments
    [[ -z "$key" ]] && continue
    [[ "$key" =~ ^# ]] && continue
    map_ref["$key"]="$value"
  done < "$file"
}

load_file "$old_file" old_vars
load_file "$new_file" new_vars

added=()
removed=()
modified=()

# Detect added and modified
for key in "${!new_vars[@]}"; do
  if [[ -v old_vars["$key"] ]]; then
    if [[ "${old_vars["$key"]}" != "${new_vars["$key"]}" ]]; then
      modified+=("$key: ${old_vars["$key"]} -> ${new_vars["$key"]}")
    fi
  else
    added+=("$key=${new_vars["$key"]}")
  fi
done

# Detect removed
for key in "${!old_vars[@]}"; do
  if [[ ! -v new_vars["$key"] ]]; then
    removed+=("$key")
  fi
done

output_section() {
  local title="$1"
  shift
  local items=("$@")
  if [[ ${#items[@]} -gt 0 ]]; then
    echo "$title:"
    for item in "${items[@]}"; do
      echo "$item"
    done
    echo ""
  fi
}

output_section "Added" "${added[@]}"
output_section "Removed" "${removed[@]}"
output_section "Modified" "${modified[@]}"
