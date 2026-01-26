#!/usr/bin/env bash
set -euo pipefail

# Path to the GitHub event payload (provided by the runner)
EVENT_PATH="${GITHUB_EVENT_PATH:-}" 
if [[ -z "$EVENT_PATH" || ! -f "$EVENT_PATH" ]]; then
  echo "::error::GITHUB_EVENT_PATH is not set or file does not exist"
  exit 1
fi

# Use a tiny Python snippet to parse JSON and compute labels
LABELS=$(python - <<'PY'
import json, sys, pathlib
event_path = pathlib.Path("$EVENT_PATH")
with event_path.open() as f:
    data = json.load(f)
files = [item.get("filename", "") for item in data.get("files", [])]
labels = set()
for fn in files:
    if fn.lower().endswith('.md'):
        labels.add('📚 docs‑drift')
    if fn.lower().endswith('.py'):
        labels.add('🐍 python‑whirl')
    if fn.lower().endswith('.test') or fn.lower().endswith('_test.py'):
        labels.add('🧪 test‑tornado')
# Sort for deterministic output
sorted_labels = sorted(labels)
print(' '.join(sorted_labels))
PY
)

if [[ -z "$LABELS" ]]; then
  echo "No matching file types found; no labels to add."
  exit 0
fi

echo "Labels to add: $LABELS"
# In a full implementation you would call the GitHub REST API here using $GITHUB_TOKEN
