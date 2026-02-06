#!/bin/bash

COMMIT_MESSAGE="$1"
COSMIC_LEVEL="$2"

STATUS="success"
SUGGESTION=""

# Conventional commit regex
CONVENTIONAL_REGEX="^(feat|fix|docs|chore|refactor|style|test|build|ci|perf|revert)(\(.+\))?: .+"

# Check for conventional commit
if [[ ! "$COMMIT_MESSAGE" =~ $CONVENTIONAL_REGEX ]]; then
  echo "::warning title=Cosmic Lint Warning::Commit message does not follow conventional commit format." >&2 # Send to stderr
  STATUS="warning"
fi

# Check for blandness and suggest cosmic wisdom
BLAND_KEYWORDS=("update files" "fix bug" "initial commit" "changes" "refactor code" "minor changes" "wip")
IS_BLAND=false
for keyword in "${BLAND_KEYWORDS[@]}"; do
  if [[ "$COMMIT_MESSAGE" =~ $keyword ]]; then
    IS_BLAND=true
    break
  fi
done

if $IS_BLAND || [[ ${#COMMIT_MESSAGE} -lt 20 ]]; then
  case "$COSMIC_LEVEL" in
    "stardust")
      EMOJIS=("✨" "🌌" "🌠" "💫" "🌟")
      WISDOMS=("Consider the cosmic implications of your changes." "May your commits shine bright like a supernova." "A small step for code, a giant leap for mankind." "The universe rewards clarity.")
      RANDOM_EMOJI=${EMOJIS[$RANDOM % ${#EMOJIS[@]}]}
      RANDOM_WISDOM=${WISDOMS[$RANDOM % ${#WISDOMS[@]}]}
      SUGGESTION="$RANDOM_EMOJI $RANDOM_WISDOM"
      ;;
    "nebula")
      EMOJIS=("🔭" "🪐" "🛰️" "🚀" "👽")
      WISDOMS=("Your commit is a star in the vast nebula of our codebase. Describe its luminosity!" "Even a black hole has a story. What's yours?" "The cosmos demands more detail, mortal." "Unveil the mysteries of this commit.")
      RANDOM_EMOJI=${EMOJIS[$RANDOM % ${#EMOJIS[@]}]}
      RANDOM_WISDOM=${WISDOMS[$RANDOM % ${#WISDOMS[@]}]}
      SUGGESTION="$RANDOM_EMOJI $RANDOM_WISDOM"
      STATUS="warning" # Nebula level makes blandness a warning
      ;;
    "blackhole")
      EMOJIS=("⚫" "🕳️" "💥" "☢️" "💀")
      WISDOMS=("This commit is a void. Fill it with meaning or be consumed!" "The cosmic council demands a more descriptive message. This is a black hole of information." "Your commit message lacks the gravitational pull of detail. Re-evaluate." "A commit without purpose is a cosmic anomaly.")
      RANDOM_EMOJI=${EMOJIS[$RANDOM % ${#EMOJIS[@]}]}
      RANDOM_WISDOM=${WISDOMS[$RANDOM % ${#WISDOMS[@]}]}
      SUGGESTION="$RANDOM_EMOJI $RANDOM_WISDOM"
      STATUS="failure" # Blackhole level makes blandness a failure
      ;;
    *)
      SUGGESTION="Unknown cosmic level, but your commit is still a bit bland. Try 'stardust'!"
      ;;
  esac
  echo "::notice title=Cosmic Suggestion::Your commit message could use more cosmic flair: $SUGGESTION" >&2 # Send to stderr
fi

echo "status=$STATUS"
echo "suggestion=$SUGGESTION"

# The action.yml will handle the exit code based on the 'status' output.
# The script itself doesn't need to exit with 1 for failure, as the action.yml will do it.
