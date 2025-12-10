#!/bin/sh
set -e

tmp=$(mktemp -d)

docker build -t cli-playpen .

# Test container runs and shows ASCII art
output=$(docker run --rm cli-playpen echo "TEST")
if [ $? -ne 0 ]; then
  echo "Container failed to run"
  exit 1
fi

if ! echo "$output" | grep -q "_____"; then
  echo "ASCII art missing from output"
  exit 1
fi

echo "Tests passed! 🎉"
