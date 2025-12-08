#!/bin/bash

# Log fairy tale transformer - adds whimsy to logs
# Mock rationale: Uses ANSI colors and ASCII art for deterministic visual testing

while IFS= read -r line; do
  if [[ $line == *ERROR* ]]; then
    echo -e "🔥 DRAGON ATTACK! $line"
  elif [[ $line == *WARN* ]]; then
    echo -e "🧙‍♀️ MISCHIEVOUS GNOME DETECTED: $line"
  elif [[ $line == *INFO* ]]; then
    echo -e "🛷 ELF DELIVERY CONFIRMED: $line"
  else
    echo -e "✨ MYSTERIOUS WHISPER: $line"
  fi

done
