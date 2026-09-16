#!/usr/bin/env bash
set -euo pipefail

DIR="${1:-$HOME/.ssh}"
if [[ ! -d "$DIR" ]]; then
  echo "Error: Directory $DIR does not exist" >&2
  exit 2
fi

weak_found=0

shopt -s nullglob
for key in "$DIR"/*; do
  # Only consider regular files (skip public .pub)
  if [[ -f "$key" && "$key" != *.pub ]]; then
    # Use ssh-keygen to get key size; fallback to mock if not available
    if command -v ssh-keygen >/dev/null 2>&1; then
      info=$(ssh-keygen -lf "$key" 2>/dev/null || true)
    else
      info=""
    fi
    # Expected format: "<bits> <fingerprint> <filename> (<type>)"
    bits=$(echo "$info" | awk '{print $1}')
    if [[ -z "$bits" ]]; then
      # Could not determine size; skip
      continue
    fi
    echo "Key: $key – $bits bits"
    if (( bits < 2048 )); then
      echo "⚠️ Weak key detected!"
      weak_found=1
    fi
  fi
done

if (( weak_found )); then
  exit 1
else
  exit 0
fi
