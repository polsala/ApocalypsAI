#!/usr/bin/env bash
set -euo pipefail

# List of emojis to cycle through
EMOJIS=("🚀" "✨" "🔥" "💡" "🎉")

# Determine input source: file argument or stdin
if [[ $# -gt 0 ]]; then
  INPUT_FILE="$1"
  exec 3<"$INPUT_FILE"
else
  exec 3<&0
fi

i=0
while IFS= read -r line <&3; do
  emoji="${EMOJIS[i % ${#EMOJIS[@]}]}"
  echo "$emoji $line"
  ((i++))
done
