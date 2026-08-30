#!/usr/bin/env sh
# Simple Docker image size estimator

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <Dockerfile>"
  exit 1
fi

DOCKERFILE="$1"

# Base image size table (in MB)
BASE_SIZES='\nalpine:3.18=5\nubuntu:22.04=70\ndebian:stable-slim=30\n'

# Extract the base image name from the first FROM line
BASE=$(awk '/^FROM /{print $2}' "$DOCKERFILE" | head -n1)
BASE_SIZE=0
for entry in $BASE_SIZES; do
  name=$(echo "$entry" | cut -d= -f1)
  size=$(echo "$entry" | cut -d= -f2)
  if [ "$name" = "$BASE" ]; then
    BASE_SIZE=$size
    break
  fi
done

# Count relevant Dockerfile instructions
RUN_COUNT=$(grep -i '^RUN ' "$DOCKERFILE" | wc -l | tr -d ' ')
COPY_COUNT=$(grep -iE '^(COPY|ADD) ' "$DOCKERFILE" | wc -l | tr -d ' ')

# Apply heuristics (10 MB per RUN, 1 MB per COPY/ADD)
RUN_SIZE=$((RUN_COUNT * 10))
COPY_SIZE=$((COPY_COUNT * 1))
TOTAL=$((BASE_SIZE + RUN_SIZE + COPY_SIZE))

echo "${TOTAL} MB"
