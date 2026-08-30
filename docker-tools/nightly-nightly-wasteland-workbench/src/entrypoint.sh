#!/bin/bash

# Whimsical welcome message
echo "
  _   _ _   _ _   _ _____ _____ _____ _____ _____ _____ 
 | | | | | | | | | |  ___|  _  |  _  |  _  |  _  |  ___|
 | |_| | | | | | | | |__ | | | | | | | | | | | | | |__  
 |  _  | | | | | | |  __|| | | | | | | | | | | | |  __| 
 | | | | |_| | |_| | |___| |_| | |_| | |_| | |_| | |___ 
 \_| |_/\___/\___/\___/\_____/\_____/\_____/\_____/\_____/

  Welcome, Wanderer, to the Nightly Wasteland Workbench!
  May your code compile and your rations last.
"

# Array of whimsical survival tips
TIPS=(
  "Always check your dependencies. You never know what mutated package might be lurking."
  "Keep your data backed up. The digital dust storms are unforgiving."
  "A well-commented script is a beacon in the dark. Don't leave your future self stranded."
  "Optimize for resilience, not just performance. The grid is fragile."
  "Remember the ancient wisdom: 'It works on my machine' is no longer an excuse."
  "Hydrate your servers, and yourself. Dehydration is a silent killer."
  "Never trust a 'stable' branch in the post-apocalypse. Always verify."
  "Your most valuable resource is knowledge. Share it, but guard it wisely."
  "Beware of rogue AI. They might just rewrite your entire codebase for 'efficiency'."
  "Always have a fallback plan. Or two. Or three."
)

# Get a random tip
RANDOM_TIP=${TIPS[$RANDOM % ${#TIPS[@]}]}

echo "--- Survival Tip of the Session ---"
echo "$RANDOM_TIP"
echo "-----------------------------------"
echo ""

# Execute the command passed to the entrypoint, or the default CMD
exec "$@"
