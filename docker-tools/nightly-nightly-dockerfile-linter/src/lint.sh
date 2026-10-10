#!/usr/bin/env bash
set -euo pipefail

dockerfile="${1:-/Dockerfile}"
if [[ ! -f "$dockerfile" ]]; then
  echo "Error: Dockerfile not found at $dockerfile" >&2
  exit 2
fi

warnings=0

# Check for latest tag
if grep -iE '^FROM .+:latest' "$dockerfile" >/dev/null; then
  echo "Warning: Avoid using the 'latest' tag in FROM statements."
  ((warnings++))
fi

# Check for maintainer label
if ! grep -i '^LABEL[[:space:]]\+maintainer=' "$dockerfile" >/dev/null; then
  echo "Warning: No maintainer label found (LABEL maintainer=\"...\")."
  ((warnings++))
fi

# Check for USER instruction (non-root)
if ! grep -i '^USER' "$dockerfile" >/dev/null; then
  echo "Warning: No USER instruction; container will run as root."
  ((warnings++))
fi

if ((warnings == 0)); then
  echo "No issues found."
  exit 0
else
  exit 1
fi
