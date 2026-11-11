#!/usr/bin/env bash

# If an argument is provided, use it as the hour (01-12). Otherwise, get the current hour.
if [[ -n $1 ]]; then
  hour=$1
else
  hour=$(date +"%I")
fi

# Remove leading zero for case matching
hour=$(echo "$hour" | sed 's/^0//')

case $hour in
  1) emoji="🕐" ;;
  2) emoji="🕑" ;;
  3) emoji="🕒" ;;
  4) emoji="🕓" ;;
  5) emoji="🕔" ;;
  6) emoji="🕕" ;;
  7) emoji="🕖" ;;
  8) emoji="🕗" ;;
  9) emoji="🕘" ;;
  10) emoji="🕙" ;;
  11) emoji="🕚" ;;
  12|0) emoji="🕛" ;;
  *) echo "Invalid hour: $hour" >&2; exit 1 ;;
esac

echo "$emoji"
