#!/usr/bin/env bash
set -e

MESSAGE="$1"
# List of whimsical emojis
EMOJIS=("🚀" "✨" "🔥" "💥" "🌟" "🛸" "🤖" "🧩" "🎉" "⚡")
# Pick a random index
INDEX=$((RANDOM % ${#EMOJIS[@]}))
# Output the annotated message
echo "${EMOJIS[$INDEX]} $MESSAGE"
