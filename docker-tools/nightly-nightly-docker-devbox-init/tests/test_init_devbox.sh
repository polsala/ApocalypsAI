#!/bin/bash

set -e

# Mock rationale: Simulate devbox init without Docker to test file generation

LANGS=("python" "node" "go" "rust")

for lang in "${LANGS[@]}"; do
  echo "Testing $lang preset..."
  rm -rf .devbox
  ./src/init-devbox.sh "$lang"
  test -f .devbox/Dockerfile || { echo "Missing Dockerfile"; exit 1; }
  test -f .devbox/docker-compose.yml || { echo "Missing docker-compose.yml"; exit 1; }
  test -f .devbox/entrypoint.sh || { echo "Missing entrypoint.sh"; exit 1; }
  grep -q "LANG_PRESET=$lang" .devbox/docker-compose.yml || { echo "LANG_PRESET not set correctly"; exit 1; }
  echo "✓ $lang preset OK"
done

rm -rf .devbox

echo "All tests passed."
