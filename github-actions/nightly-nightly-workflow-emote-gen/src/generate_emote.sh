#!/bin/bash

# This script generates a whimsical emote based on the provided workflow status.
# It's designed to be run as the entrypoint for a GitHub Action.

set -euo pipefail

# Get the status input from the environment variable set by GitHub Actions
STATUS="$INPUT_STATUS"

EMOTE=""
case "$STATUS" in
  "success")
    EMOTE="✨ Galactic Triumph! ✨"
    ;;
  "failure")
    EMOTE="💥 Cosmic Catastrophe! 💥"
    ;;
  "cancelled")
    EMOTE="💨 Vanished into the Aether 💨"
    ;;
  "skipped")
    EMOTE="😴 Hibernating in Hyperspace 😴"
    ;;
  *)
    EMOTE="❓ Unknown Cosmic Event ❓"
    ;;
esac

# Set the output variable 'emote' for the GitHub Action
echo "emote=$EMOTE" >> "$GITHUB_OUTPUT"
