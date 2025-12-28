#!/usr/bin/env bash
set -euo pipefail

# Default: read from stdin
INPUT_FILE=""
WRITE_BACK=0

usage() {
  echo "Usage: $0 [-w] <commit_message_file>"
  echo "  -w   Write the modified message back to the file"
  exit 1
}

# Parse options
while getopts ":w" opt; do
  case $opt in
    w) WRITE_BACK=1 ;;
    *) usage ;;
  esac
done
shift $((OPTIND -1))

if [ $# -gt 0 ]; then
  INPUT_FILE="$1"
  if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: file not found: $INPUT_FILE" >&2
    exit 1
  fi
  MESSAGE=$(<"$INPUT_FILE")
else
  MESSAGE=$(cat)
fi

# Detect keyword
KEYWORD=$(echo "$MESSAGE" | grep -Eio '^(feat|fix|docs|style|refactor|test|chore)' | head -n1)

EMOJI=""
case "$KEYWORD" in
  feat) EMOJI="🎉" ;;
  fix) EMOJI="🐛" ;;
  docs) EMOJI="📚" ;;
  style) EMOJI="✨" ;;
  refactor) EMOJI="🔧" ;;
  test) EMOJI="✅" ;;
  chore) EMOJI="🔄" ;;
  *) EMOJI="" ;;
esac

if [ -n "$EMOJI" ]; then
  OUTPUT="$EMOJI $MESSAGE"
else
  OUTPUT="$MESSAGE"
fi

if [ $WRITE_BACK -eq 1 ]; then
  echo "$OUTPUT" > "$INPUT_FILE"
else
  echo "$OUTPUT"
fi
