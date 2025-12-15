#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <directory> <size_limit_mb>"
  exit 1
}

if [[ $# -ne 2 ]]; then
  usage
fi

DIR=$1
LIMIT_MB=$2

if [[ ! -d "$DIR" ]]; then
  echo "Error: Directory not found: $DIR" >&2
  exit 1
fi

if ! [[ "$LIMIT_MB" =~ ^[0-9]+$ ]]; then
  echo "Error: Size limit must be an integer (MB)" >&2
  exit 1
fi

# Calculate size in bytes
SIZE_BYTES=$(du -sb "$DIR" | cut -f1)
LIMIT_BYTES=$((LIMIT_MB * 1024 * 1024))

# Avoid division by zero
if (( LIMIT_BYTES == 0 )); then
  echo "Error: Size limit must be greater than zero" >&2
  exit 1
fi

PERCENT=$((SIZE_BYTES * 100 / LIMIT_BYTES))

if (( PERCENT >= 80 )); then
  echo "⚠️ The wasteland is overflowing! (${PERCENT}% of ${LIMIT_MB}MB)"
else
  echo "✅ All is calm in the wasteland. (${PERCENT}% of ${LIMIT_MB}MB)"
fi
