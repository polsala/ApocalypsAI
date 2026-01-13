#!/usr/bin/env bash
# nightly-emoji-survival-tip
# A Bash utility that outputs a random survival tip with an emoji.
# Supports deterministic output via --seed.

set -euo pipefail

# Tips and emojis
TIPS=(
    \"Carry a multi-tool for unexpected repairs.\"
    \"Keep a small stash of high-energy snacks.\"
    \"Learn basic first-aid skills.\"
    \"Maintain a clean water source.\"
    \"Practice silent communication.\"
)

EMOJIS=(
    \"🛠️\"
    \"🍫\"
    \"🩹\"
    \"💧\"
    \"🤐\"
)

# Functions
usage() {
    echo \"Usage: $0 [--seed <int>] [-l]\"
    echo \"  --seed <int>  Provide a seed for deterministic tip selection.\"
    echo \"  -l            List all available tips.\"
    exit 1
}

# Parse arguments
SEED=\"\"
LIST=false

while [[ $# -gt 0 ]]; do
    case \"$1\" in
        --seed)
            shift
            SEED=\"$1\"
            ;;
        -l)
            LIST=true
            ;;
        -* )
            usage
            ;;
        *)
            usage
            ;;
    esac
    shift
done

if $LIST; then
    echo \"Available tips:\"
    for i in \"${!TIPS[@]}\"; do
        printf \"%d: %s\
\" \"$((i+1))\" \"${TIPS[$i]}\"
    done
    exit 0
fi

# Determine random number
if [[ -n \"$SEED\" ]]; then
    # Simple linear congruential generator
    RAND=$(( (SEED * 1103515245 + 12345) % 2147483648 ))
else
    RAND=$RANDOM
fi

TIP_INDEX=$(( RAND % ${#TIPS[@]} ))
EMOJI_INDEX=$(( RAND % ${#EMOJIS[@]} ))

echo \"🌟 Tip: ${TIPS[$TIP_INDEX]} ${EMOJIS[$EMOJI_INDEX]}\"

