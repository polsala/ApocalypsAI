#!/bin/bash

STATUS="$1"
EMOJIS=""

case "$STATUS" in
  "success")
    EMOJIS="✨🚀🎉"
    ;;
  "failure")
    EMOJIS="💥😭🔥"
    ;;
  "cancelled")
    EMOJIS="💨👻🛑"
    ;;
  "neutral")
    EMOJIS="☁️🤔⏳"
    ;;
  "skipped")
    EMOJIS="⏭️😴💤"
    ;;
  "timed_out")
    EMOJIS="⏳💀⏰"
    ;;
  "action_required")
    EMOJIS="🚨👀❓"
    ;;
  *)
    EMOJIS="❓🌀🤷"
    ;;
esac

echo "$EMOJIS"
