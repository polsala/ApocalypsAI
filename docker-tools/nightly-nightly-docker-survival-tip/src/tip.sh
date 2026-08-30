#!/bin/sh
# nightly-docker-survival-tip script

tips="\
Always carry a rubber duck for debugging; it listens better than humans.\
When in doubt, add more coffee. It fuels both code and courage.\
A well‑placed meme can defuse even the most critical merge conflict.\
Never underestimate the power of a well‑timed break; it resets the apocalypse clock.\
If all else fails, blame the build server – it loves the attention."

# Convert the newline‑separated string into an array
IFS='\n' read -r -d '' -a tip_array <<EOF
$tips
EOF

# Determine index
if [ -n "$TIP_INDEX" ]; then
  idx=$TIP_INDEX
else
  # deterministic fallback using current epoch seconds
  idx=$(( $(date +%s) % ${#tip_array[@]} ))
fi

# Ensure index is within bounds
idx=$(( idx % ${#tip_array[@]} ))

echo "${tip_array[$idx]}"
