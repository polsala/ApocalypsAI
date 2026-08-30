#!/usr/bin/env bash
# nightly-dusty-disk-watcher
# Monitors a directory's size and warns with a random apocalypse‑themed quote if a threshold is exceeded.

set -euo pipefail

# Function to print usage information
usage() {
  echo "Usage: $0 <directory> <threshold_mb>"
  echo "  <directory>   Path to monitor"
  echo "  <threshold_mb> Size limit in megabytes"
  exit 2
}

# Ensure exactly two arguments are provided
if [[ $# -ne 2 ]]; then
  usage
fi

DIR="$1"
THRESHOLD_MB="$2"

# Validate that DIR exists and is a directory
if [[ ! -d "$DIR" ]]; then
  echo "Error: '$DIR' is not a directory or does not exist." >&2
  exit 2
fi

# Validate that THRESHOLD_MB is a positive integer
if ! [[ "$THRESHOLD_MB" =~ ^[0-9]+$ ]]; then
  echo "Error: threshold must be a positive integer (megabytes)." >&2
  exit 2
fi

# Helper to obtain directory size in kilobytes
# Allows mocking via MOCK_DU_OUTPUT for deterministic tests
get_dir_size_kb() {
  if [[ -n "${MOCK_DU_OUTPUT-}" ]]; then
    # MOCK_DU_OUTPUT should be a number representing kilobytes
    echo "$MOCK_DU_OUTPUT"
  else
    du -sk "$DIR" | cut -f1
  fi
}

SIZE_KB=$(get_dir_size_kb)
SIZE_MB=$((SIZE_KB / 1024))

if (( SIZE_MB > THRESHOLD_MB )); then
  # Array of whimsical apocalypse quotes
  QUOTES=(
    "The sands of time are running out…"
    "Your storage is as full as the vaults of the dead."
    "Even the wasteland has more space than this."
    "The end is near… for your free disk space."
    "Do you hear the distant rumble? It's the disk screaming."
  )
  # Pick a random quote
  RANDOM_INDEX=$((RANDOM % ${#QUOTES[@]}))
  SELECTED_QUOTE="${QUOTES[$RANDOM_INDEX]}"
  echo "⚠️  Disk usage warning for '$DIR'"
  echo "   Current size: ${SIZE_MB}MiB (threshold: ${THRESHOLD_MB}MiB)"
  echo "   ${SELECTED_QUOTE}"
  exit 1
else
  echo "✅  '$DIR' is within the safe limit (${SIZE_MB}MiB ≤ ${THRESHOLD_MB}MiB)."
  exit 0
fi
