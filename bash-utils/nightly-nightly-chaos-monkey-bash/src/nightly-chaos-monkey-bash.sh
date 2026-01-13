#!/bin/bash

CHAOS_ENABLED=1
CHAOS_INTERVAL=30

chaos_monkey_disable() {
  CHAOS_ENABLED=0
  unset PROMPT_COMMAND
  echo "Chaos monkey pacified. Back to normalcy."
}

_chaos_prompt_hook() {
  if [[ $CHAOS_ENABLED -eq 1 && $(($RANDOM % 5)) -eq 0 ]]; then
    local emojis=("👾" "🌀" "👽" "🎭" "🎲" "🎪" "🛸" "👻")
    local emoji=${emojis[$RANDOM % ${#emojis[@]}]}
    PS1="${emoji} \w $ "
  fi

  if [[ $CHAOS_ENABLED -eq 1 && $(($RANDOM % 10)) -eq 0 ]]; then
    echo "⚠️  Fake alert: Low disk space (just kidding!)" >&2
  fi

  if [[ $CHAOS_ENABLED -eq 1 && $(($RANDOM % 8)) -eq 0 ]]; then
    sleep 0.5
  fi
}

PROMPT_COMMAND="_chaos_prompt_hook"

echo "👾 Chaos monkey activated. Type 'chaos_monkey_disable' to restore order."
