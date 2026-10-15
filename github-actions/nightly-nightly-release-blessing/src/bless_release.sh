#!/bin/bash

# Mock rationale: In a real GitHub Action run, this script would be executed
# within the GitHub Actions environment. For standalone testing, we define
# the BLESSING_TYPE environment variable here if it's not already set.
# This allows the script to be tested deterministically without relying on
# the GitHub Actions runtime.

BLESSING_TYPE=${BLESSING_TYPE:-random} # Default to random if not set by action.yml

declare -a OMINOUS_BLESSINGS=(
  "May your code survive the digital dust storms and your servers withstand the solar flares."
  "The void watches your deployments. May its gaze be one of mild approval."
  "As the old world crumbles, may your commits stand as monuments to resilience."
  "Beware the silent bugs that crawl from the shadows. May your tests illuminate them."
  "The future is uncertain, but your pipelines, at least, are green. For now."
)

declare -a HOPEFUL_BLESSINGS=(
  "May this release bring forth new growth in the digital wasteland."
  "In the echoes of the past, may this code forge a brighter tomorrow."
  "May your innovations be beacons of hope in the encroaching darkness."
  "Let this deployment be a testament to collective survival and progress."
  "Through the static and the noise, may your signals always reach their destination."
)

declare -a SURVIVAL_TIPS=(
  "Always check your dependencies; they can turn on you faster than a mutated squirrel."
  "Keep your backups decentralized. You never know which data center will become a crater."
  "Hydrate your code regularly. Dehydration leads to unexpected crashes."
  "Learn to scavenge for resources. Open-source libraries are your best friends."
  "Maintain a strong communication network. Even in the apocalypse, collaboration is key."
  "Prioritize security. The digital raiders are always lurking."
  "Document everything. Future survivors will thank you (if they can read)."
  "Adaptability is survival. Be ready to refactor at a moment's notice."
  "Never trust a 'stable' branch. It's a lie."
  "Always have an escape plan for your data."
)

# Function to get a random element from an array
get_random_element() {
  local -n arr=$1 # nameref to array
  echo "${arr[$(( RANDOM % ${#arr[@]} ))]}"
}

BLESSING=""
case "$BLESSING_TYPE" in
  "ominous")
    BLESSING=$(get_random_element OMINOUS_BLESSINGS)
    ;;
  "hopeful")
    BLESSING=$(get_random_element HOPEFUL_BLESSINGS)
    ;;
  "random"|*)
    ALL_BLESSINGS=("${OMINOUS_BLESSINGS[@]}" "${HOPEFUL_BLESSINGS[@]}")
    BLESSING=$(get_random_element ALL_BLESSINGS)
    ;;
esac

SURVIVAL_TIP=$(get_random_element SURVIVAL_TIPS)

echo "--- Nightly Release Blessing ---"
echo ""
echo "$BLESSING"
echo ""
echo "--- Survival Tip of the Cycle ---"
echo "$SURVIVAL_TIP"
echo ""
echo "May your deployments be swift and your uptime eternal. (Or at least until the next cataclysm.)"
