#!/usr/bin/env bash

set -euo pipefail

TARGET="${1:-.}"

# Ensure required commands are available
if ! command -v df >/dev/null; then
  echo "df command not found" >&2
  exit 1
fi
if ! command -v du >/dev/null; then
  echo "du command not found" >&2
  exit 1
fi

# Get usage percentage from df
# df output columns: Filesystem 1K-blocks Used Available Use% Mounted on
DF_OUTPUT=$(df -k "$TARGET" | tail -n +2)
USEPCT=$(echo "$DF_OUTPUT" | awk '{print $5}' | tr -d '%')

# Determine emoji based on thresholds
if (( USEPCT <= 50 )); then
  EMOJI="🟢"
elif (( USEPCT <= 80 )); then
  EMOJI="🟡"
else
  EMOJI="🔴"
fi

echo "Disk usage for $TARGET: $USEPCT% $EMOJI"
