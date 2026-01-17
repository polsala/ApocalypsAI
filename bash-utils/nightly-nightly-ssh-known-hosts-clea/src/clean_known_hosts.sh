#!/usr/bin/env bash
set -euo pipefail

# Path to known_hosts file (default to user's SSH known_hosts)
KNOWN_HOSTS="${1:-$HOME/.ssh/known_hosts}"

# If the file does not exist, exit silently (nothing to clean)
if [[ ! -f "$KNOWN_HOSTS" ]]; then
  echo "File not found: $KNOWN_HOSTS"
  exit 0
fi

# Create a backup before making any changes
BACKUP="${KNOWN_HOSTS}.bak"
cp "$KNOWN_HOSTS" "$BACKUP"

# Separate comment lines and host lines
# Preserve comments exactly as they appear
comments=$(grep '^#' "$KNOWN_HOSTS" || true)
# Sort host lines and remove duplicates
hosts=$(grep -v '^#' "$KNOWN_HOSTS" | sort -u)

# Re‑assemble the file: comments first, then cleaned host entries
{
  if [[ -n "$comments" ]]; then
    printf "%s\n" "$comments"
  fi
  if [[ -n "$hosts" ]]; then
    printf "%s\n" "$hosts"
  fi
} > "$KNOWN_HOSTS"

echo "Cleaned known_hosts saved. Backup created at $BACKUP"
