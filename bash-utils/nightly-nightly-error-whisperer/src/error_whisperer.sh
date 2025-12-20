#!/bin/bash

# Nightly Error Whisperer: Translates cryptic error messages into whimsical, less stressful suggestions.

# Function to whisper an error message
whisper_error() {
    local error_msg="$1"
    local whispered_msg=""

    # Convert to lowercase for case-insensitive matching
    local lower_msg=$(echo "$error_msg" | tr '[:upper:]' '[:lower:]')

    if [[ "$lower_msg" =~ "command not found" || "$lower_msg" =~ "no such command" ]]; then
        whispered_msg="Oops! It seems that command went on a coffee break. Did you spell it right, or is it hiding in your PATH?"
    elif [[ "$lower_msg" =~ "permission denied" || "$lower_msg" =~ "access denied" ]]; then
        whispered_msg="The digital bouncer says 'No entry!' Perhaps you need a magic 'sudo' spell or to check your access rights?"
    elif [[ "$lower_msg" =~ "no such file or directory" || "$lower_msg" =~ "file not found" ]]; then
        whispered_msg="The file you're looking for seems to have wandered off. Is it in the right folder, or did it change its name?"
    elif [[ "$lower_msg" =~ "syntax error" || "$lower_msg" =~ "parse error" ]]; then
        whispered_msg="Your code is speaking in riddles! A tiny typo might be causing a grand misunderstanding. Time for a quick proofread?"
    elif [[ "$lower_msg" =~ "connection refused" || "$lower_msg" =~ "host unreachable" ]]; then
        whispered_msg="The server isn't picking up the phone. Is it running, or is there a firewall dragon guarding the path?"
    elif [[ "$lower_msg" =~ "disk space" || "$lower_msg" =~ "no space left" ]]; then
        whispered_msg="Your digital attic is full! Time to declutter and make some space for new adventures."
    elif [[ "$lower_msg" =~ "memory allocation failed" || "$lower_msg" =~ "out of memory" ]]; then
        whispered_msg="Your computer's brain is feeling a bit overwhelmed. Maybe close a few tabs or give it a moment to rest?"
    else
        whispered_msg="The digital spirits are a bit muddled. While I ponder this mystery, perhaps a deep breath and a quick search will reveal its secrets?"
    fi

    echo "$whispered_msg"
}

# Main logic
if [ -t 0 ]; then # Check if stdin is a terminal (i.e., not piped input)
    if [ -n "$1" ]; then
        # If argument is provided, use it as the error message
        whisper_error "$1"
    else
        # If no argument and no pipe, prompt for input
        echo "Enter your cryptic error message (or pipe it in):"
        read -r input_error
        whisper_error "$input_error"
    fi
else
    # Read from stdin
    input_error=$(cat)
    whisper_error "$input_error"
fi
