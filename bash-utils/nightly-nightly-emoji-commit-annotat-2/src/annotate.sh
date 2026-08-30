#!/usr/bin/env bash

# nightly-emoji-commit-annotator
# Adds a random (or user‑specified) emoji to the most recent Git commit message.

set -euo pipefail

# List of whimsical emojis to choose from
EMOJIS=("😀" "🚀" "🌟" "🔥" "💡" "🧩" "🎉" "🛠️" "📦" "🧪" "⚡" "🪐" "🤖" "🦄" "🌈")

print_help() {
  cat <<'EOF'
Usage: emoji-commit [-e <emoji>] [-h]
  -e <emoji>   Specify an emoji to use instead of a random one.
  -h           Show this help message.
EOF
}

# Parse options
EMOJI=""
while getopts ":e:h" opt; do
  case $opt in
    e) EMOJI="$OPTARG" ;;
    h) print_help; exit 0 ;;
    \?) echo "Invalid option: -$OPTARG" >&2; print_help; exit 1 ;;
    :) echo "Option -$OPTARG requires an argument." >&2; print_help; exit 1 ;;
  esac
done
shift $((OPTIND -1))

# Ensure we are inside a Git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "Error: Not a Git repository." >&2
  exit 1
fi

# Ensure there is at least one commit
if ! git rev-parse HEAD > /dev/null 2>&1; then
  echo "Error: No commits found in this repository." >&2
  exit 1
fi

# Choose emoji if not supplied
if [[ -z "$EMOJI" ]]; then
  # Bash's $RANDOM gives a 0‑32767 value; use modulo to index array
  idx=$(( RANDOM % ${#EMOJIS[@]} ))
  EMOJI="${EMOJIS[$idx]}"
fi

# Retrieve current commit message
CURRENT_MSG=$(git log -1 --pretty=%B)

# Append emoji (separated by a space)
NEW_MSG="${CURRENT_MSG} ${EMOJI}"

# Amend the most recent commit without changing the author/date
git commit --amend -m "$NEW_MSG" --no-edit

echo "Commit message updated with emoji: $EMOJI"
