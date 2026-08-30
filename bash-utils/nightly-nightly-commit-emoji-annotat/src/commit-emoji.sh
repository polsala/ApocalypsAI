#!/usr/bin/env bash
set -euo pipefail

# Default number of commits to display
NUM=10
REPO="."

while getopts ":n:h" opt; do
  case $opt in
    n) NUM=$OPTARG ;;
    h) echo "Usage: $0 [-n <num>] [repo_path]"; exit 0 ;;
    *) echo "Invalid option"; exit 1 ;;
  esac
done
shift $((OPTIND-1))
if [[ $# -gt 0 ]]; then
  REPO=$1
fi

# Mapping of keywords to emojis
declare -A EMOJI_MAP=(
  ["feat"]="🚀"
  ["feature"]="🚀"
  ["fix"]="🐛"
  ["bug"]="🐛"
  ["docs"]="📚"
  ["doc"]="📚"
  ["refactor"]="🔧"
  ["test"]="✅"
  ["chore"]="🧹"
)

git -C "$REPO" log -n "$NUM" --pretty=format:"%h %s" | while read -r hash subject; do
  emoji="❓"
  for key in "${!EMOJI_MAP[@]}"; do
    if grep -iq "$key" <<<"$subject"; then
      emoji="${EMOJI_MAP[$key]}"
      break
    fi
  done
  echo "$emoji $hash $subject"
done
