#!/usr/bin/env bash
set -e

# List of affirmations (one per line)
cat <<'EOF' > /tmp/affirmations.txt
The wasteland whispers: you are unstoppable.
Even the ruins bow to your resilience.
Radiation can't dim your inner glow.
Your footsteps echo hope across the dunes.
You turn scarcity into abundance.
EOF

# Read lines into an array
mapfile -t lines < /tmp/affirmations.txt
count=${#lines[@]}

if [ -n "$AFFIRM_INDEX" ]; then
  idx=$((AFFIRM_INDEX % count))
else
  idx=$((RANDOM % count))
fi

echo "${lines[$idx]}"
