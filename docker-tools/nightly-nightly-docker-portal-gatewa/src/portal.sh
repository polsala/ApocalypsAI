#!/bin/sh

# portal.sh - prints a whimsical portal and destination

DESTINATIONS="\
The Neon Bazaar of 2099\
The Silent Library\
The Rusted Citadel\
The Whispering Wasteland\
The Clockwork Cathedral\
The Forgotten Oasis\
"

# If DESTINATION env var is set, use it; otherwise pick a random one
if [ -n "$DESTINATION" ]; then
  CHOICE="$DESTINATION"
else
  # Count lines
  COUNT=$(printf "%s\n" "$DESTINATIONS" | wc -l)
  # Generate a random index between 0 and COUNT-1
  INDEX=$(awk -v n=$COUNT 'BEGIN {srand(); print int(rand()*n)}')
  # Select the line (awk is 1‑based, so add 1)
  CHOICE=$(printf "%s\n" "$DESTINATIONS" | sed -n "$((INDEX+1))p")
fi

cat << "ART"
      .-.
     (   )
      '-'
     /| |\ 
    /_| |_|\
      | |
      | |
      |_| 
ART

echo "You have entered: $CHOICE"
