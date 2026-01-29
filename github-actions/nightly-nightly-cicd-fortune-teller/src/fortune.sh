#!/bin/bash

FORTUNE_TYPE=${1:-"blessing"}

BLESSINGS=(
  "May your merges be swift and your conflicts few."
  "The cosmic currents align for a flawless deployment."
  "Your code is blessed by the ancient ones; it shall run without error."
  "A gentle breeze of success guides your pipeline today."
  "The stars foretell a green build and happy users."
  "May your tests pass on the first try, and your bugs vanish into the void."
  "The spirits of the servers whisper 'well done' to your commit."
)

WARNINGS=(
  "Beware the rogue semicolon; it lurks in the shadows of your build."
  "The ancient scrolls speak of a dependency conflict. Proceed with caution."
  "A shadow of a race condition flickers. Double-check your concurrency."
  "The void gazes back... and it sees an unhandled exception."
  "A forgotten cache might bring unexpected woes. Clear it, just in case.""
  "The prophecy speaks of a 'works on my machine' scenario. Be vigilant."
  "A subtle off-by-one error could unravel the fabric of reality. Count carefully."
)

if [ "$FORTUNE_TYPE" == "warning" ]; then
  FORTUNE=$(printf "%s\n" "${WARNINGS[@]}" | shuf -n 1)
else
  FORTUNE=$(printf "%s\n" "${BLESSINGS[@]}" | shuf -n 1)
fi

echo "$FORTUNE"
