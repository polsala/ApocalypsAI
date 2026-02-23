#!/bin/bash

MIN_DELAY=${INPUT_MIN_DELAY:-0}
MAX_DELAY=${INPUT_MAX_DELAY:-5}
FAILURE_CHANCE=${INPUT_FAILURE_CHANCE:-0} # 0-100
DRIFT_SEED=${INPUT_DRIFT_SEED:-$(date +%s%N)} # Use current time if no seed provided

# Ensure inputs are integers
MIN_DELAY=$(echo "$MIN_DELAY" | grep -oE '^[0-9]+$' || echo 0)
MAX_DELAY=$(echo "$MAX_DELAY" | grep -oE '^[0-9]+$' || echo 5)
FAILURE_CHANCE=$(echo "$FAILURE_CHANCE" | grep -oE '^[0-9]+$' || echo 0)
if (( FAILURE_CHANCE < 0 || FAILURE_CHANCE > 100 )); then
  FAILURE_CHANCE=0
fi

echo "--- Chrono-Drift Injector ---"
echo "Min Delay: ${MIN_DELAY}s, Max Delay: ${MAX_DELAY}s, Failure Chance: ${FAILURE_CHANCE}%"
echo "Drift Seed: ${DRIFT_SEED}"

# Use the seed for reproducible randomness
# Mock rationale: Using cksum provides a deterministic integer from a string seed,
# which is crucial for reproducible tests without relying on /dev/urandom or $RANDOM.
RANDOM_GEN=$(echo "$DRIFT_SEED" | cksum | awk '{print $1}')
echo "Deterministic random value from seed: ${RANDOM_GEN}"

# Calculate delay
DELAY_RANGE=$((MAX_DELAY - MIN_DELAY))
if (( DELAY_RANGE < 0 )); then DELAY_RANGE=0; fi

# Generate a random number between 0 and DELAY_RANGE (inclusive)
RANDOM_DELAY_OFFSET=$((RANDOM_GEN % (DELAY_RANGE + 1)))
ACTUAL_DELAY=$((MIN_DELAY + RANDOM_DELAY_OFFSET))

echo "Calculated delay: ${ACTUAL_DELAY}s"

# Simulate sleep for testing, otherwise actually sleep
if [[ -n "$MOCK_SLEEP" ]]; then
  echo "MOCK_SLEEP: Would have slept for ${ACTUAL_DELAY}s"
else
  sleep "$ACTUAL_DELAY"
fi

# Determine if failure should occur
# Generate a random number between 0 and 99 for failure check
RANDOM_FAILURE_CHECK=$(( (RANDOM_GEN / 100) % 100 )) # Use a different part of the seed-derived number
echo "Failure check random value (0-99): ${RANDOM_FAILURE_CHECK}"

if (( RANDOM_FAILURE_CHECK < FAILURE_CHANCE )); then
  echo "Injecting temporal anomaly: Workflow step failed due to Chrono-Drift!"
  exit 1
else
  echo "Temporal flow stable. Proceeding."
fi
