#!/usr/bin/env bash
EMOJIS=("😀" "😎" "🤖" "🌟" "🚀" "🦄")
RANDOM_INDEX=$((RANDOM % ${#EMOJIS[@]}))
echo "Good morning! Your mood emoji: ${EMOJIS[$RANDOM_INDEX]}"
