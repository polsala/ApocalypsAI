#!/usr/bin/env bash
set -e

# Build the Docker image (quiet output)
docker build -t ghost-haiku . > /dev/null

# Run container with known input
output=$(echo -n "test" | docker run -i --rm ghost-haiku)

expected="Moonlight cracks the stone\nShadows dance on cracked glass\nTomorrow sings soft"

if [ "$output" = "$expected" ]; then
  echo "PASS"
  exit 0
else
  echo "FAIL"
  echo "Expected:"
  echo "$expected"
  echo "Got:"
  echo "$output"
  exit 1
fi
