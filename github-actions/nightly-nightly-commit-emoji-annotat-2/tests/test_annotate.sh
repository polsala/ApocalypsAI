#!/usr/bin/env bash
set -e

# Mock rationale: using a fixed list of emojis; randomness is acceptable because any output must match one of them.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="$SCRIPT_DIR/annotate.sh"
MESSAGE="Deploy new feature"
OUTPUT=$(bash "$SCRIPT" "$MESSAGE")

EXPECTED_EMOJIS=("🚀" "✨" "🔥" "💥" "🌟" "🛸" "🤖" "🧩" "🎉" "⚡")
FOUND=0
for EMOJI in "${EXPECTED_EMOJIS[@]}"; do
  if [[ "$OUTPUT" == "$EMOJI $MESSAGE" ]]; then
    FOUND=1
    break
  fi
done

if [[ $FOUND -eq 1 ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: Unexpected output -> $OUTPUT"
  exit 1
fi
