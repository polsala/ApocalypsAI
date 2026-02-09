#!/bin/bash

WISDOMS=(
  "Even in the deepest void, a single line of code can spark a new world. Keep building, wanderer!"
  "The wasteland tests our resolve, but every merged PR is a step closer to rebuilding. Stay strong!"
  "Remember, a bug today is a feature tomorrow... or at least a lesson learned. Embrace the chaos!"
  "Your code is a beacon in the digital dust storms. Let it shine, survivor!"
  "Don't let the rust get to your logic. Polish your commits, and your future will be bright!"
  "The ancient ones spoke of 'clean code'. Strive for it, and your legacy will endure."
  "Every commit is a footprint in the sands of time. Make them count, for the future depends on it."
  "When the servers hum, the wasteland thrives. Keep those machines purring!"
  "A well-documented function is a shelter from the storm. Build wisely."
  "The apocalypse may have taken much, but it left us with the power to create. Use it well!"
)

# Get a random index
RANDOM_INDEX=$(( RANDOM % ${#WISDOMS[@]} ))

# Print the random wisdom
echo "${WISDOMS[$RANDOM_INDEX]}"
