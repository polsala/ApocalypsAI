#!/usr/bin/env bash
# Nightly Radiation Disk Monitor
# Checks root filesystem usage and reports a whimsical radiation level.

# Allow injection of a custom df command (useful for testing)
DF_CMD="${DF_CMD:-df}"

# Retrieve POSIX‑compatible df output for the root mount
output=$($DF_CMD -P / 2>/dev/null | tail -n +2 | head -n 1)
if [[ -z "$output" ]]; then
  echo "Error: unable to retrieve disk usage"
  exit 1
fi

# Expected df fields: Filesystem Size Used Avail Use% Mounted_on
usage_percent=$(echo "$output" | awk '{print $5}' | tr -d '%')
if ! [[ "$usage_percent" =~ ^[0-9]+$ ]]; then
  echo "Error: unexpected df output"
  exit 1
fi

if (( usage_percent <= 70 )); then
  level="Safe"
  emoji="🟢"
elif (( usage_percent <= 90 )); then
  level="Elevated"
  emoji="🟡"
else
  level="Critical"
  emoji="🔴"
fi

echo "Radiation level: $level $emoji (disk usage ${usage_percent}%)"
