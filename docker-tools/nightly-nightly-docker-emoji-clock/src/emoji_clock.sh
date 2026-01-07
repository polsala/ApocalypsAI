#!/usr/bin/env bash
# Emoji Clock: prints current time with a clock‑face emoji.
# If TIME_OVERRIDE is set (HH:MM), it uses that hour for the emoji.

if [[ -n "$TIME_OVERRIDE" ]]; then
  TIME_STR="$TIME_OVERRIDE"
else
  TIME_STR=$(date +%H:%M)
fi

HOUR=${TIME_STR%%:*}
# Strip leading zero to avoid octal interpretation
HOUR=${HOUR#0}
# Ensure decimal interpretation
HOUR=$((10#$HOUR))

HOUR12=$((HOUR % 12))

case $HOUR12 in
  0) EMOJI="🕛" ;;
  1) EMOJI="🕐" ;;
  2) EMOJI="🕑" ;;
  3) EMOJI="🕒" ;;
  4) EMOJI="🕓" ;;
  5) EMOJI="🕔" ;;
  6) EMOJI="🕕" ;;
  7) EMOJI="🕖" ;;
  8) EMOJI="🕗" ;;
  9) EMOJI="🕘" ;;
  10) EMOJI="🕙" ;;
  11) EMOJI="🕚" ;;
esac

echo "$EMOJI $TIME_STR"
