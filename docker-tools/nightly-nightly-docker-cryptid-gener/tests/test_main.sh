#!/usr/bin/env bash
set -e

# Build the Docker image (quiet output)
docker build -t test-cryptid-gen . > /dev/null

# Run the container with a known seed
output=$(docker run --rm -e CRYPTID_SEED=0 test-cryptid-gen)

expected="Chupacabra: A blood‑sucking creature said to prey on livestock in the Americas."

if [[ "$output" == "$expected" ]]; then
  echo "PASS"
  exit 0
else
  echo "FAIL: expected '$expected' but got '$output'"
  exit 1
fi
