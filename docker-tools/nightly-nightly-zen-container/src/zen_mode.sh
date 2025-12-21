#!/bin/bash

AFFIRMATIONS=(
    "Breathe. Focus. Create."
    "The code flows like a calm river."
    "Embrace the silence, find your solution."
    "Every line is a step towards clarity."
    "You are capable of great things."
    "Let clarity guide your keystrokes."
    "Find peace in the patterns of your code."
)

# Pick a random affirmation
RANDOM_INDEX=$(( RANDOM % ${#AFFIRMATIONS[@]} ))
echo "Zen Mode: ${AFFIRMATIONS[$RANDOM_INDEX]}"
echo "For true auditory bliss, consider playing ambient sounds externally."
