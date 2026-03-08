#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: Use a fixed list of whimsical survival tips
tips=("Remember to hydrate" "Check your shelter's structural integrity" "Never trust a silent wind" "Carry extra rations" "Map your surroundings daily")

# Determine index based on day of year
day_of_year=$(date +%j)  # 001-366
index=$(( (day_of_year - 1) % ${#tips[@]} ))
selected_tip="${tips[$index]}"

# Build JSON payload
payload=$(printf '{"title":"Daily Survival Tip","body":"%s"}' "$selected_tip")

# GitHub API endpoint
repo="${GITHUB_REPOSITORY}"
token="${INPUT_GITHUB_TOKEN}"
api_url="https://api.github.com/repos/${repo}/issues"

# Send request
curl -s -X POST -H "Authorization: token $token" -H "Accept: application/vnd.github+json" -d "$payload" "$api_url"
