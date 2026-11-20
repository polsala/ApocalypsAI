#!/usr/bin/env bash
# apocalypse quote generator

quotes=(
"Even the sun has given up."
"The last radio crackles with static."
"Water is a memory now."
"Shadows whisper the names of the dead."
"Hope is a relic buried under ash."
"Stars have forgotten to shine."
"The wind carries the scent of rust."
"Silence is the loudest scream."
"Tomorrow never came."
"Dreams are dust in the wind."
)

# Get random index
count=${#quotes[@]}
index=$((RANDOM % count))
echo "${quotes[$index]}"
