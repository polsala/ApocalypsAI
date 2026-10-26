#!/usr/bin/env bash
# nightly-moon-phase-notifier
# Determines the moon phase for a given date (default: today) and prints an ASCII art.

# Reference new moon date (2000-01-06)
REF_DATE="2000-01-06"

# Get target date
if [[ -n "$MOON_DATE" ]]; then
  TARGET_DATE="$MOON_DATE"
else
  TARGET_DATE=$(date +%F)
fi

# Convert dates to seconds since epoch
ref_sec=$(date -d "$REF_DATE" +%s)
target_sec=$(date -d "$TARGET_DATE" +%s)

# Compute days elapsed
days=$(( (target_sec - ref_sec) / 86400 ))

# Lunar month length (average)
LUNAR=29.53

# Phase index (0-7)
phase_index=$(printf "%.0f" "$(awk "BEGIN {print ( (days % $LUNAR) / $LUNAR ) * 8 }")")
phase_index=$(( phase_index % 8 ))

case $phase_index in
  0) phase="New Moon"; art="   _..._   \n .'     '. \n|         |\n|         |\n '._____.' " ;;
  1) phase="Waxing Crescent"; art="   _..._   \n .'     '. \n|   )     |\n|         |\n '._____.' " ;;
  2) phase="First Quarter"; art="   _..._   \n .'     '. \n|   )   ( |\n|         |\n '._____.' " ;;
  3) phase="Waxing Gibbous"; art="   _..._   \n .'     '. \n|   )   ( |\n|   (     |\n '._____.' " ;;
  4) phase="Full Moon"; art="   _..._   \n .'*****'. \n|*******|\n|*******|\n '._____.' " ;;
  5) phase="Waning Gibbous"; art="   _..._   \n .'*****'. \n|     ( |\n|   (   |\n '._____.' " ;;
  6) phase="Last Quarter"; art="   _..._   \n .'     '. \n| (   )   |\n|         |\n '._____.' " ;;
  7) phase="Waning Crescent"; art="   _..._   \n .'     '. \n|     (   |\n|         |\n '._____.' " ;;
esac

printf "Moon phase on %s: %s\n%s\n" "$TARGET_DATE" "$phase" "$art"
