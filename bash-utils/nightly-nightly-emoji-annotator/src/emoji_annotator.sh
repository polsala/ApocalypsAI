#!/usr/bin/env bash
# emoji_annotator.sh – Append an emoji based on detected keywords.
# Reads a line from stdin, determines an appropriate emoji, and prints the line with the emoji appended.

# Declare an associative array mapping lowercase keywords to emojis.
# Requires Bash 4+ for associative arrays.

declare -A map=(
  ["fix"]="🛠️"
  ["bug"]="🛠️"
  ["feat"]="🚀"
  ["feature"]="🚀"
  ["doc"]="📚"
  ["docs"]="📚"
  ["test"]="✅"
  ["tests"]="✅"
  ["refactor"]="♻️"
  ["chore"]="🧹"
)

# Default emoji when no keyword matches.
default_emoji="🙂"

# Read the entire stdin into a variable.
input=$(cat)

selected="$default_emoji"
# Split the input into words and look for the first matching keyword.
for word in $input; do
  lower=$(echo "$word" | tr '[:upper:]' '[:lower:]')
  if [[ -n "${map[$lower]}" ]]; then
    selected="${map[$lower]}"
    break
  fi
done

# Output the original line followed by a space and the chosen emoji.
echo "$input $selected"
