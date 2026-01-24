#!/bin/bash

# nightly-chaos-monkey-cron
# Injects harmless chaos into your terminal sessions.

set -euo pipefail

CHAOS_MODE=${CHAOS_MODE:-random}
CHAOS_CHANCE=${CHAOS_CHANCE:-30}

# Random chance to activate
if (( RANDOM % 100 >= CHAOS_CHANCE )); then
  exit 0
fi

# Modes
modes=("typo" "emoji" "delay")
if [[ "$CHAOS_MODE" == "random" ]]; then
  mode=${modes[RANDOM % ${#modes[@]}]}
else
  mode="$CHAOS_MODE"
fi

case "$mode" in
  typo)
    echo -e "\nOops! Did I type that right? 😅"
    ;;
  emoji)
    emojis=("👾" "🤪" "👻" "👽" "🤖" "⚡" "💥")
    emoji=${emojis[RANDOM % ${#emojis[@]}]}
    echo -e "\nChaos Monkey says: $emoji"
    ;;
  delay)
    sleep_time=$((RANDOM % 3 + 1))
    echo -e "\n🐌 Slow mode activated for $sleep_time seconds..."
    sleep $sleep_time
    echo "Back to normal! ⏩"
    ;;
  *)
    echo "Unknown mode. No chaos today. 😿"
    ;;
esac
