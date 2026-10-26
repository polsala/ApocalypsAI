#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [-i] <known_hosts_file>"
  exit 1
}

inplace=false
while getopts ":i" opt; do
  case $opt in
    i) inplace=true ;;
    *) usage ;;
  esac
done
shift $((OPTIND-1))

[[ $# -eq 1 ]] || usage
file="$1"
[[ -f "$file" ]] || { echo "File not found: $file" >&2; exit 1; }

process() {
  awk '
    /^#/ {print; next}
    { if (!seen[$1]++) print }
  '
}

if $inplace; then
  tmp=$(mktemp)
  process < "$file" > "$tmp"
  mv "$tmp" "$file"
else
  process < "$file"
fi
