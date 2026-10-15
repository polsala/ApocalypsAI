#!/usr/bin/env bash
set -euo pipefail

input="${1:-}"
if [[ -n "$input" ]]; then
  df_output=$(cat "$input")
else
  df_output=$(df -h --output=target,pcent | tail -n +2)
fi

while read -r mount pcent; do
  [[ -z "$mount" ]] && continue
  percent=${pcent%\%}
  used=$((percent / 10))
  free=$((10 - used))
  bar=$(printf '🟥%.0s' $(seq 1 $used))
  bar+=$(printf '🟩%.0s' $(seq 1 $free))
  echo "$mount $bar ($pcent)"
done <<< "$df_output"
