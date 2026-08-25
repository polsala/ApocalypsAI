#!/bin/sh
# Apocalyptic Motivation Entrypoint
# Selects a motivational message either randomly or by index.

messages="Rise, wanderer! The sun may be a memory, but your spirit still burns.
Even in the wasteland, a single seed can spark a forest.
Radiation may glow, but your hope shines brighter.
When the world crumbles, build a castle of courage.
Remember: every night ends, and so does the zombie horde."

# Determine index
if [ -n "$MOTIVATION_INDEX" ]; then
  idx=$MOTIVATION_INDEX
else
  # Count lines in the messages variable
  line_count=$(printf "%s" "$messages" | wc -l)
  idx=$(shuf -i 0-$(($line_count - 1)) -n 1)
fi

# Extract the line (sed is 1‑based)
msg=$(printf "%s" "$messages" | sed -n "$((idx + 1))p")
printf "%s\n" "$msg"
