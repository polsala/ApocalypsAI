#!/usr/bin/env sh
set -e

DOCKERFILE="${1:-Dockerfile}"

# Determine base image size (in MB)
BASE_IMAGE=$(grep -i '^FROM' "$DOCKERFILE" | head -n1 | awk '{print $2}')
case "$BASE_IMAGE" in
  alpine:3.18) size=5 ;;
  python:3.11-slim) size=30 ;;
  *) size=20 ;; # default size for unknown bases
esac

# Add size for RUN instructions (10 MB each)
RUN_COUNT=$(grep -i '^RUN' "$DOCKERFILE" | wc -l | tr -d ' ')
size=$((size + RUN_COUNT * 10))

# Add size for COPY or ADD instructions (1 MB each)
COPY_COUNT=$(grep -Ei '^(COPY|ADD)' "$DOCKERFILE" | wc -l | tr -d ' ')
size=$((size + COPY_COUNT * 1))

echo "${size}MB"
