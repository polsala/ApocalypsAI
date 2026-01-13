#!/usr/bin/env sh

# Array of whimsical quotes
quotes=(
  "The stars whisper, \"Stay hydrated.\""
  "Even a cactus needs a hug sometimes."
  "When in doubt, reboot the universe."
)

# Determine index
if [ -n "$SEED" ]; then
  idx=$(( SEED % ${#quotes[@]} ))
else
  # $RANDOM is not available in POSIX sh on Alpine, use /dev/urandom fallback
  rand=$(dd if=/dev/urandom bs=2 count=1 2>/dev/null | od -An -tu2)
  idx=$(( rand % ${#quotes[@]} ))
fi

# Output the selected quote
echo "${quotes[$idx]}"
