#!/usr/bin/env bash\nset -euo pipefail\n\n# Ensure jq is available (GitHub Actions runners provide it)\nif ! command -v jq >/dev/null 2>&1; then\n  echo "jq is required but not installed"\n  exit 1\nfi\n\nTOKEN="${{GITHUB_TOKEN}}"\nISSUE="${{ISSUE_NUMBER}}"\nREPO="${{REPO}}"\nMAP_JSON="${{LABEL_EMOJI_MAP}}"\n\n# Fetch issue details to obtain labels\nISSUE_DATA=$(curl -s -H "Authorization: token ${TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/${REPO}/issues/${ISSUE}")\n\nLABELS=$(echo "$ISSUE_DATA" | jq -r '.labels[].name')\n\nEMOJI=""\nwhile IFS= read -r label; do\n  EMOJI=$(echo "$MAP_JSON" | jq -r --arg lbl "$label" '.[$lbl] // empty')\n  if [[ -n "$EMOJI" ]]; then\n    break\n  fi\ndone <<< "$LABELS"\n\nif [[ -z "$EMOJI" ]]; then\n  echo "No matching label found; no reaction added."\n  exit 0\nfi\n\n# Post the reaction\ncurl -s -X POST -H "Authorization: token ${TOKEN}" \
  -H "Accept: application/vnd.github.squirrel-girl-preview+json" \
  "https://api.github.com/repos/${REPO}/issues/${ISSUE}/reactions" \
  -d "{\"content\":\"${EMOJI}\"}" >/dev/null\n\necho "Added reaction ${EMOJI} to issue #${ISSUE}"\n
