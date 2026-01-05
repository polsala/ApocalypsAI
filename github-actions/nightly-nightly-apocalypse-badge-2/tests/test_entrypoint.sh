#!/bin/sh
set -e

# Helper to run the entrypoint with given INPUT_CHANGED_FILES
run_entrypoint() {
  export INPUT_CHANGED_FILES="$1"
  export GITHUB_TOKEN=""
  # Ensure other env vars are unset for deterministic output
  unset GITHUB_REPOSITORY GITHUB_EVENT_PULL_REQUEST_NUMBER
  ./entrypoint.sh
}

# Test Small badge (3 files)
output=$(run_entrypoint "a.txt,b.txt,c.txt")
echo "$output" | grep "🛡️ Small"

# Test Medium badge (10 files)
files=$(seq -f "f%02g.txt" 1 10 | paste -sd "," -)
output=$(run_entrypoint "$files")
echo "$output" | grep "⚔️ Medium"

# Test Massive badge (25 files)
files=$(seq -f "f%02g.txt" 1 25 | paste -sd "," -)
output=$(run_entrypoint "$files")
echo "$output" | grep "☢️ Massive"

echo "All tests passed"
