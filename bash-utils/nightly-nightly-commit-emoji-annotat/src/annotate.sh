#!/usr/bin/env bash

# nightly-commit-emoji-annotator
# Reads git commit history and prefixes each line with an emoji representing the commit type.
# If the environment variable GIT_LOG_MOCK is set, its value is used instead of calling git.

# Function to determine emoji based on commit message
get_emoji() {
    local msg="$1"
    shopt -s nocasematch
    case "$msg" in
        *feat*|*feature*) echo "✨" ;;
        *fix*) echo "🐛" ;;
        *docs*|*documentation*) echo "📚" ;;
        *refactor*) echo "🔧" ;;
        *test*) echo "✅" ;;
        *chore*) echo "🧹" ;;
        *) echo "🔖" ;;
    esac
    shopt -u nocasematch
}

# Retrieve git log (or mock)
if [[ -n "$GIT_LOG_MOCK" ]]; then
    LOG="$GIT_LOG_MOCK"
else
    # Use short hash and subject line only
    LOG=$(git log --pretty=format:"%h %s")
fi

# Process each line
while IFS= read -r line; do
    # Skip empty lines
    [[ -z "$line" ]] && continue
    # Split into hash and message
    hash=$(echo "$line" | awk '{print $1}')
    msg=$(echo "$line" | cut -d' ' -f2-)
    emoji=$(get_emoji "$msg")
    printf "%s %s %s\n" "$hash" "$emoji" "$msg"
done <<< "$LOG"
