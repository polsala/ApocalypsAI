#!/usr/bin/env bash
# nightly-commit-emoji-annotator
# Reads commit messages from stdin and prefixes each with an emoji based on conventional commit type.

while IFS= read -r line; do
  case "$line" in
    feat:* ) emoji="✨" ;;
    fix:* ) emoji="🐛" ;;
    docs:* ) emoji="📚" ;;
    chore:* ) emoji="🧹" ;;
    refactor:* ) emoji="♻️" ;;
    * ) emoji="🤔" ;;
  esac
  printf "%s %s\n" "$emoji" "$line"
done
