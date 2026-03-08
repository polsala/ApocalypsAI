#!/usr/bin/env bash

# nightly-disk-guardian
# Monitors root filesystem usage and prints whimsical alerts.

# Default threshold
THRESHOLD=${1:-80}

# Get usage percent without the % sign
USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')

# Function to print monster
print_monster() {
  cat <<'EOF'
      .-\"\"\"\"-.
     / -   -  \
    |  .-. .- |
    |  \o| |o (
    \     ^   /
     '.  )--.'
       '-...-'
EOF
  echo "🧟‍♂️  Disk usage is at ${USAGE}% – the monster awakens!"
}

# Function to print sun
print_sun() {
  cat <<'EOF'
    \   /  
     .-.   
  ‒ (   ) ‒
     `-’   
    /   \  
EOF
  echo "☀️  Disk usage is at ${USAGE}% – all clear."
}

if [[ "$USAGE" -ge "$THRESHOLD" ]]; then
  print_monster
  exit 1
else
  print_sun
  exit 0
fi
