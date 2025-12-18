#!/usr/bin/env bash
set -euo pipefail

QUOTE_FILE=\"quotes.txt\"

if [[ -f \"$QUOTE_FILE\" ]]; then
    mapfile -t QUOTES < \"$QUOTE_FILE\"
else
    QUOTES=(\"Believe you can and you're halfway there.\" \"The only limit to our realization of tomorrow is our doubts of today.\" \"Do not wait to strike till the iron is hot; but make it hot by striking.\")
fi

# Pick random
INDEX=$((RANDOM % ${#QUOTES[@]}))
echo \"${QUOTES[$INDEX]}\"
