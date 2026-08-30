#!/usr/bin/env bash
set -euo pipefail

# Default to dry‑run; enable deletion with -d flag
delete=0
if [[ "${1:-}" == "-d" ]]; then
  delete=1
  shift
fi

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 [-d] <directory> <days>"
  exit 1
fi

dir=$1
days=$2

if [[ ! -d "$dir" ]]; then
  echo "Error: $dir is not a directory"
  exit 1
fi

if ! [[ "$days" =~ ^[0-9]+$ ]]; then
  echo "Error: days must be a non‑negative integer"
  exit 1
fi

if [[ $delete -eq 1 ]]; then
  echo "Deleting files older than $days days in $dir:"
  find "$dir" -type f -mtime +"$days" -print -delete
else
  echo "Dry run: files older than $days days in $dir:"
  find "$dir" -type f -mtime +"$days" -print
fi
