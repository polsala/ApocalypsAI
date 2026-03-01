#!/usr/bin/env bash

# nightly-emoji-encoder
# Convert input text to a sequence of emojis based on a fixed map.

# Declare associative array for mapping (requires Bash 4+)
declare -A EMOJI_MAP=(
  [a]="🍎" [b]="🐝" [c]="🌊" [d]="🍩" [e]="🍯" [f]="🍟" [g]="🍇" [h]="🍯" [i]="🍦" [j]="🕹️"
  [k]="🥝" [l]="🍋" [m]="🍈" [n]="🍜" [o]="🍊" [p]="🍍" [q]="❓" [r]="🌈" [s]="🍓" [t]="🌴"
  [u]="🍇" [v]="🎻" [w]="🌊" [x]="❌" [y]="🍋" [z]="🦓" [space]="🌟"
)

# Function to translate a single character
translate_char() {
  local ch="$1"
  if [[ "$ch" == " " ]]; then
    printf "%s" "${EMOJI_MAP[space]}"
    return
  fi
  local lower=$(echo "$ch" | tr 'A-Z' 'a-z')
  if [[ -n "${EMOJI_MAP[$lower]}" ]]; then
    printf "%s" "${EMOJI_MAP[$lower]}"
  else
    printf "%s" "$ch"
  fi
}

# Gather input: either arguments or stdin
if [[ $# -gt 0 ]]; then
  INPUT="$*"
else
  # Read all of stdin
  INPUT="$(cat)"
fi

# Iterate over each character
OUTPUT=""
while IFS= read -r -n1 char; do
  # Break on EOF (read returns non-zero when no more chars)
  if [[ -z "$char" && $? -ne 0 ]]; then
    break
  fi
  OUTPUT+="$(translate_char "$char")"
  # Reset IFS to default for next iteration
  IFS=$' \t\n'
  # If we hit a newline from stdin, treat it as end of input
  if [[ "$char" == $'\n' ]]; then
    break
  fi
done <<< "$INPUT"

printf "%s\n" "$OUTPUT"
