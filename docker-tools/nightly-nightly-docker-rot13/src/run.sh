#!/usr/bin/env bash
# ROT13 encoder
# If arguments are provided, process them; otherwise read from stdin
if [ $# -gt 0 ]; then
  echo "$*" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
else
  tr 'A-Za-z' 'N-ZA-Mn-za-m'
fi
