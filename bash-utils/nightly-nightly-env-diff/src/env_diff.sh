#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <old.env> <new.env>"
  exit 1
fi

old_file=$1
new_file=$2

declare -A old new

# Load old env file
while IFS='=' read -r key value; do
  [[ -z $key || $key == \#* ]] && continue
  old["$key"]="$value"
done < "$old_file"

# Load new env file
while IFS='=' read -r key value; do
  [[ -z $key || $key == \#* ]] && continue
  new["$key"]="$value"
done < "$new_file"

added=()
removed=()
changed=()

# Detect added and changed variables
for k in "${!new[@]}"; do
  if [[ -z ${old[$k]+_} ]]; then
    added+=("$k")
  elif [[ "${old[$k]}" != "${new[$k]}" ]]; then
    changed+=("$k")
  fi
done

# Detect removed variables
for k in "${!old[@]}"; do
  if [[ -z ${new[$k]+_} ]]; then
    removed+=("$k")
  fi
done

if [[ ${#added[@]} -gt 0 ]]; then
  echo "Added: ${added[*]}"
fi
if [[ ${#removed[@]} -gt 0 ]]; then
  echo "Removed: ${removed[*]}"
fi
if [[ ${#changed[@]} -gt 0 ]]; then
  echo -n "Changed:"
  for k in "${changed[@]}"; do
    echo -n " $k (${old[$k]}->${new[$k]})"
  done
  echo
fi
