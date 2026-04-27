#!/usr/bin/env bash
# nightly-emoji-enhancer – prepend an appropriate emoji to a line of text
# ---------------------------------------------------------------
# Usage:
#   emoji-enhance "some message"
#   echo "some message" | emoji-enhance
# ---------------------------------------------------------------

# Function to select emoji based on keywords
select_emoji() {
    local text="$1"
    local lowered=$(echo "$text" | tr '[:upper:]' '[:lower:]')
    if [[ $lowered =~ (fix|bug) ]]; then
        echo "🛠️"
    elif [[ $lowered =~ (add|new|create) ]]; then
        echo "➕"
    elif [[ $lowered =~ (remove|delete|rm) ]]; then
        echo "➖"
    elif [[ $lowered =~ (update|upgrade|change) ]]; then
        echo "🔄"
    else
        echo "🎉"
    fi
}

# Retrieve input either from argument or STDIN
if [[ -n $1 ]]; then
    input="$*"
else
    # Read entire stdin (preserve newlines)
    input=$(cat)
fi

# Trim leading/trailing whitespace
input=$(echo "$input" | sed -e 's/^\s*//' -e 's/\s*$//')

# If input is empty, do nothing
if [[ -z $input ]]; then
    exit 0
fi

emoji=$(select_emoji "$input")

echo "$emoji $input"
