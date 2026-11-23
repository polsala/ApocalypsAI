#!/usr/bin/env bash
set -e

# Expected quotes (must match the script's list)
expected=(
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

# Run the script and capture output
output=$(bash ../src/quote.sh)

# Verify the output is one of the expected quotes
found=false
for q in "${expected[@]}"; do
  if [[ "$output" == "$q" ]]; then
    found=true
    break
  fi
done

if [ "$found" = true ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: Unexpected output: $output"
  exit 1
fi
