#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <old.env> <new.env>"
  exit 1
fi

old_file=$1
new_file=$2

declare -A old new

# Load old env
while IFS='=' read -r key value; do
  [[ -z "$key" || "$key" =~ ^# ]] && continue
  old["$key"]="$value"
done < "$old_file"

# Load new env
while IFS='=' read -r key value; do
  [[ -z "$key" || "$key" =~ ^# ]] && continue
  new["$key"]="$value"
done < "$new_file"

added=()
removed=()
changed=()
unchanged=()

# Determine added, changed, unchanged
for k in "${!new[@]}"; do
  if [[ -v old["$k"] ]]; then
    if [[ "${old[$k]}" == "${new[$k]}" ]]; then
      unchanged+=("$k")
    else
      changed+=("$k")
    fi
  else
    added+=("$k")
  fi
done

# Determine removed
for k in "${!old[@]}"; do
  if [[ ! -v new["$k"] ]]; then
    removed+=("$k")
  fi
done

print_section() {
  local title=$1
  shift
  local arr=("$@")
  if (( ${#arr[@]} )); then
    echo "$title:"
    for item in "${arr[@]}"; do
      echo "  $item"
    done
    echo
  fi
}

print_section "Added" "${added[@]}"
print_section "Removed" "${removed[@]}"
print_section "Changed" "${changed[@]}"
print_section "Unchanged" "${unchanged[@]}"

exit 0
