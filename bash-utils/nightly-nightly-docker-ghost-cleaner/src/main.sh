#!/usr/bin/env bash
set -euo pipefail

# Find dangling images
dangling=$(docker images -f dangling=true -q)

if [[ -z "$dangling" ]]; then
  echo "🕸️ No ghosts found."
  exit 0
fi

# Remove them
removed=0
while read -r img; do
  docker rmi "$img" >/dev/null 2>&1 || true
  removed=$((removed + 1))
done <<< "$dangling"

echo "👻 Docker ghosts cleaned! ($removed images removed)"
