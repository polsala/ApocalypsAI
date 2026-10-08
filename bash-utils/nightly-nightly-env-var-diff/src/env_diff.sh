#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <old.env> <new.env>"
  exit 1
fi

old_file=$1
new_file=$2

declare -A old new

parse_file() {
  local file=$1
  local -n arr=$2
  while IFS= read -r line || [[ -n $line ]]; do
    # Skip empty lines and comments
    [[ -z $line || $line =~ ^[[:space:]]*# ]] && continue
    if [[ $line =~ ^([^=]+)=(.*)$ ]]; then
      key=${BASH_REMATCH[1]}
      val=${BASH_REMATCH[2]}
      arr["$key"]="$val"
    fi
  done < "$file"
}

parse_file "$old_file" old
parse_file "$new_file" new

added=()
removed=()
modified=()

# Detect added and modified variables
for key in "${!new[@]}"; do
  if [[ -z ${old[$key]+_} ]]; then
    added+=("$key=${new[$key]}")
  elif [[ "${old[$key]}" != "${new[$key]}" ]]; then
    modified+=("$key: ${old[$key]} -> ${new[$key]}")
  fi
done

# Detect removed variables
for key in "${!old[@]}"; do
  if [[ -z ${new[$key]+_} ]]; then
    removed+=("$key=${old[$key]}")
  fi
done

output_section() {
  local title=$1
  shift
  local items=("$@")
  if [[ ${#items[@]} -gt 0 ]]; then
    echo "$title:"
    for i in "${items[@]}"; do
      echo "$i"
    done
    echo
  fi
}

output_section "Added" "${added[@]}"
output_section "Removed" "${removed[@]}"
output_section "Modified" "${modified[@]}"
