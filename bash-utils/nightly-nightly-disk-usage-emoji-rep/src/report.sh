#!/usr/bin/env bash
set -euo pipefail

# Determine target path
TARGET="${1:-.}"

# Get filesystem stats (portable output)
DF_OUTPUT=$(df -P "$TARGET" | tail -1)
# Parse fields: Size (2nd) and Used (3rd) in 1K‑blocks
FS_SIZE=$(echo "$DF_OUTPUT" | awk '{print $2}')
FS_USED=$(echo "$DF_OUTPUT" | awk '{print $3}')

# Compute usage percent (avoid division by zero)
if [[ "$FS_SIZE" -eq 0 ]]; then
  PCT=0
else
  PCT=$(( FS_USED * 100 / FS_SIZE ))
fi

# Choose emoji based on percentage
if (( PCT < 10 )); then
  EMOJI="🟢"
elif (( PCT <= 50 )); then
  EMOJI="🟡"
else
  EMOJI="🔴"
fi

# Human‑readable size of the target directory
DU_OUTPUT=$(du -sh "$TARGET" 2>/dev/null | awk '{print $1}')

echo "$EMOJI $DU_OUTPUT $TARGET"
