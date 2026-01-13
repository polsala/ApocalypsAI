#!/usr/bin/env bash
set -euo pipefail

# Ensure required env vars
: "${GITHUB_TOKEN:?}"
: "${PR_NUMBER:?}"
: "${REPO:?}"

# Determine quote index deterministically using PR_NUMBER
seed=$((PR_NUMBER))
a=1664525
c=1013904223
m=4294967296
rand=$(((seed * a + c) % m))
quote_file="${{ github.action_path }}/quotes.txt"
if [[ ! -f "$quote_file" ]]; then
  echo "Quotes file not found"
  exit 1
fi

total=$(wc -l < "$quote_file")
index=$(( (rand % total) + 1 ))
quote=$(sed -n "${index}p" "$quote_file")

# Escape double quotes in quote for JSON
escaped_quote=${quote//"/\"}
payload="{\"body\":\"$escaped_quote\"}"
url="https://api.github.com/repos/$REPO/issues/$PR_NUMBER/comments"
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" -d "$payload" "$url" >/dev/null

echo "Posted quote: $quote"

