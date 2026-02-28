#!/usr/bin/env bash
set -euo pipefail

# Mapping for letters a‑z to regional indicator symbols
declare -A LETTER_MAP=(
  [a]=🇦 [b]=🇧 [c]=🇨 [d]=🇩 [e]=🇪 [f]=🇫 [g]=🇬 [h]=🇭 [i]=🇮 [j]=🇯
  [k]=🇰 [l]=🇱 [m]=🇲 [n]=🇳 [o]=🇴 [p]=🇵 [q]=🇶 [r]=🇷 [s]=🇸 [t]=🇹
  [u]=🇺 [v]=🇻 [w]=🇼 [x]=🇽 [y]=🇾 [z]=🇿
)

# Mapping for digits 0‑9 to keycap emojis
declare -A DIGIT_MAP=(
  [0]=0️⃣ [1]=1️⃣ [2]=2️⃣ [3]=3️⃣ [4]=4️⃣ [5]=5️⃣ [6]=6️⃣ [7]=7️⃣ [8]=8️⃣ [9]=9️⃣
)

SPACE_CHAR="␣"
MAP_FILE=".emoji_map"

encode() {
  local dir="$1"
  >"$dir/$MAP_FILE"
  shopt -s nullglob
  for path in "$dir"/*; do
    [[ -f "$path" ]] || continue
    [[ "$(basename "$path")" == "$MAP_FILE" ]] && continue
    local name="$(basename "$path")"
    local emoji_name=""
    local char
    for (( i=0; i<${#name}; i++ )); do
      char="${name:i:1}"
      lower="${char,,}"
      if [[ $lower =~ [a-z] ]]; then
        emoji_name+="${LETTER_MAP[$lower]}"
      elif [[ $char =~ [0-9] ]]; then
        emoji_name+="${DIGIT_MAP[$char]}"
      elif [[ $char == " " ]]; then
        emoji_name+="$SPACE_CHAR"
      else
        emoji_name+="$char"
      fi
    done
    mv -- "$path" "$dir/$emoji_name"
    echo "$name|$emoji_name" >>"$dir/$MAP_FILE"
  done
  shopt -u nullglob
}

decode() {
  local dir="$1"
  [[ -f "$dir/$MAP_FILE" ]] || { echo "No $MAP_FILE found in $dir"; exit 1; }
  while IFS='|' read -r original emoji; do
    if [[ -e "$dir/$emoji" ]]; then
      mv -- "$dir/$emoji" "$dir/$original"
    fi
  done <"$dir/$MAP_FILE"
  rm -f "$dir/$MAP_FILE"
}

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <encode|decode> <directory>"
  exit 1
fi

action="$1"
target="$2"

case "$action" in
  encode) encode "$target" ;;
  decode) decode "$target" ;;
  *) echo "Invalid action: $action"; exit 1 ;;
esac
