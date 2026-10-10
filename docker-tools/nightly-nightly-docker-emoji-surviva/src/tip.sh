#!/usr/bin/env bash

# -------------------------------------------------------------------
# Emoji Survival Tip Generator
# -------------------------------------------------------------------
# If the environment variable SEED is set, use it to pick a deterministic
# tip (useful for testing). Otherwise fall back to Bash's $RANDOM.
# -------------------------------------------------------------------

# Define an array of emojis (Unicode emoji characters)
EMOJIS=(
  "🛡️"  # shield
  "⚡"   # high voltage
  "💧"   # droplet
  "🔥"   # fire
  "🗡️"  # dagger
  "🧭"   # compass
  "🔧"   # wrench
  "📡"   # satellite antenna
  "🚰"   # potable water
  "🌾"   # sheaf of rice
)

# Corresponding survival tips (same order as EMOJIS)
TIPS=(
  "Keep a spare set of spare parts for your generator."
  "Store extra batteries in a cool, dry place."
  "Collect rainwater in clean containers before the storms hit."
  "Never leave a fire unattended; always have a bucket of water nearby."
  "Maintain a well‑sharpened blade for cutting wood and rope."
  "Carry a compass; GPS may be dead after a solar flare."
  "Carry a multi‑tool; you never know what will break."
  "Set up a low‑power radio antenna for emergency broadcasts."
  "Purify any water you find before drinking."
  "Plant fast‑growing crops to ensure a steady food supply."
)

# Determine the index to use
if [[ -n "$SEED" ]]; then
  # Use arithmetic modulo to stay within array bounds
  IDX=$(( SEED % ${#EMOJIS[@]} ))
else
  # Bash's $RANDOM gives 0‑32767; scale it down
  IDX=$(( RANDOM % ${#EMOJIS[@]} ))
fi

# Output the selected tip
printf "%s %s\n" "${EMOJIS[$IDX]}" "${TIPS[$IDX]}"
