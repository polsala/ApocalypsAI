#!/bin/bash

# This script analyzes recent commit messages for sentiment and sets GitHub Action outputs.

COMMIT_COUNT=${1:-10} # Default to 10 if no argument is provided

# Define sentiment keywords (case-insensitive)
# Positive words
POSITIVE_WORDS=(
    "feat" "add" "new" "improve" "enhance" "fix" "resolve" "success" "happy" "joy"
    "delight" "celebrate" "yay" "woohoo" "good" "better" "optimistic" "stable"
)
# Negative words
NEGATIVE_WORDS=(
    "bug" "error" "fail" "broken" "issue" "problem" "stress" "frustrate" "ugh"
    "panic" "critical" "urgent" "bad" "worse" "regress" "broken"
)
# Neutral words (often present in commit types but not strong sentiment)
NEUTRAL_WORDS=(
    "chore" "docs" "refactor" "test" "update" "config" "style" "ci" "build" "perf"
)

# Function to get commit messages (mockable for tests)
get_commit_messages() {
    # Mock rationale: In a real scenario, this would use `git log`.
    # For testing, `git` command is mocked to provide deterministic output.
    # In a live GitHub Action, `actions/checkout` should run before this.
    git log -n "$COMMIT_COUNT" --pretty=format:%s
}

# Initialize counts
positive_score=0
negative_score=0
neutral_score=0
total_messages=0

# Get commit messages
commit_messages=$(get_commit_messages)

# Process each commit message
IFS=$'\n' # Set Internal Field Separator to newline to iterate over lines
for message in $commit_messages; do
    total_messages=$((total_messages + 1))
    lower_message=$(echo "$message" | tr '[:upper:]' '[:lower:]') # Convert to lowercase for case-insensitive matching

    is_positive=0
    is_negative=0

    # Check for positive words
    for word in "${POSITIVE_WORDS[@]}"; do
        if [[ "$lower_message" =~ (^|[[:space:]])"$word"($|[[:space:]]) ]]; then
            positive_score=$((positive_score + 1))
            is_positive=1
            break # Count only once per message for a category
        fi
    done

    # Check for negative words
    for word in "${NEGATIVE_WORDS[@]}"; do
        if [[ "$lower_message" =~ (^|[[:space:]])"$word"($|[[:space:]]) ]]; then
            negative_score=$((negative_score + 1))
            is_negative=1
            break # Count only once per message for a category
        fi
    done

    # Check for neutral words (only if not already positive or negative)
    if [[ $is_positive -eq 0 && $is_negative -eq 0 ]]; then
        for word in "${NEUTRAL_WORDS[@]}"; do
            if [[ "$lower_message" =~ (^|[[:space:]])"$word"($|[[:space:]]) ]]; then
                neutral_score=$((neutral_score + 1))
                break
            fi
        done
    fi
done
unset IFS # Restore default IFS

repo_mood="Neutral"
mood_summary="Analyzed $total_messages commit messages. "

if [[ $total_messages -eq 0 ]]; then
    repo_mood="Unknown"
    mood_summary="No commit messages found to analyze."
elif [[ $positive_score -gt $((negative_score * 2)) ]]; then
    repo_mood="Joyful"
    mood_summary+="The repository is feeling particularly cheerful and productive!"
elif [[ $negative_score -gt $((positive_score * 2)) ]]; then
    repo_mood="Stressed"
    mood_summary+="There might be some critical issues or frustrations brewing. Time for a break?"
elif [[ $positive_score -gt $negative_score ]]; then
    repo_mood="Optimistic"
    mood_summary+="A generally positive outlook, making good progress."
elif [[ $negative_score -gt $positive_score ]]; then
    repo_mood="Concerned"
    mood_summary+="Some challenges are present, but not overwhelming. Keep an eye out."
else
    repo_mood="Neutral"
    mood_summary+="A calm and steady pace, business as usual."
fi

mood_summary+=" (Positive: $positive_score, Negative: $negative_score, Neutral: $neutral_score)"

echo "::set-output name=repo-mood::$repo_mood"
echo "::set-output name=mood-summary::$mood_summary"

echo "Repo Mood: $repo_mood"
echo "Summary: $mood_summary"
