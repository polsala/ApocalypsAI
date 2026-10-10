#!/usr/bin/env bash
set -euo pipefail

# Default threshold is 80% if not supplied
THRESHOLD="${1:-80}"

# Retrieve df output – allow injection via DF_OUTPUT for testing
if [[ -n "${DF_OUTPUT:-}" ]]; then
  DF_DATA="${DF_OUTPUT}"
else
  DF_DATA=$(df -h /)
fi

# Extract the line containing the root filesystem information
USAGE_LINE=$(echo "$DF_DATA" | tail -n +2 | head -n 1)
# The Use% column is typically the 5th field; strip the trailing % sign
USAGE_PCT=$(echo "$USAGE_LINE" | awk '{print $5}' | tr -d '%')

if [[ -z "$USAGE_PCT" ]]; then
  echo "Failed to parse disk usage."
  exit 2
fi

if (( USAGE_PCT > THRESHOLD )); then
  # Array of whimsical apocalypse‑themed warnings
  MESSAGES=(
    "⚠️ The void is swallowing your storage! ${USAGE_PCT}% used."
    "🔥 Your disk is on fire! ${USAGE_PCT}% used."
    "💀 Death approaches: ${USAGE_PCT}% occupied."
    "🌪️ A storm of bytes engulfs you: ${USAGE_PCT}% used."
  )
  # Pick a random message
  idx=$(( RANDOM % ${#MESSAGES[@]} ))
  echo "${MESSAGES[$idx]}"
  exit 1
else
  echo "✅ Disk usage is safe: ${USAGE_PCT}% (threshold ${THRESHOLD}%)."
  exit 0
fi
