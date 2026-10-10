#!/usr/bin/env bash
set -euo pipefail

# Build the Go binary
go build -o tips ./src/main.go

# Expected tips (must match the Go source)
expected=(
    "Remember: water is life. Boil before you drink."
    "Scavenge wisely: the best tools are often hidden in plain sight."
    "Never trust a silent radio—static may be a warning."
    "A well‑kept fire can be a beacon and a shield."
    "Barter with humor; a laugh can be worth more than ammo."
    "Map the stars; they never move, even when the world does."
    "Keep a journal; future you will thank past you."
    "Stay low, stay quiet, stay alive."
)

# Run the binary and capture output
output=$(./tips)

# Check if output is one of the expected tips
for tip in "${expected[@]}"; do
    if [[ "$output" == "$tip" ]]; then
        echo "Tip matched: $output"
        exit 0
    fi
done

echo "Unexpected tip: $output"
exit 1
