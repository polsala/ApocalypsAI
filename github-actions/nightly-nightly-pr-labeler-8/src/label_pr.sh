#!/usr/bin/env bash
# label_pr.sh – determine PR labels based on changed files
# Usage: label_pr.sh "file1.txt,file2.md"

set -euo pipefail

changed="$1"
IFS=',' read -ra files <<< "$changed"

# Helper flags
all_docs=true
all_tests=true
has_config=false
has_code=false

for f in "${files[@]}"; do
  # Trim whitespace
  f=$(echo "$f" | xargs)
  # Docs detection
  if [[ ! "$f" =~ \.(md|txt)$ ]]; then
    all_docs=false
  fi
  # Test detection (common patterns)
  if [[ ! "$f" =~ (_test\.|_spec\.) ]]; then
    all_tests=false
  fi
  # Config detection (GitHub workflow or action files)
  if [[ "$f" =~ ^\.github/(workflows|actions)/.*\.yml$ ]]; then
    has_config=true
  fi
  # Anything else is considered code
  if [[ "$f" =~ \.(py|js|ts|go|rs|java|cpp|c|sh|rb|php|swift)$ ]]; then
    has_code=true
  fi
done

labels=()
if $all_docs; then
  labels+=("📚 docs-only")
fi
if $all_tests; then
  labels+=("🧪 test-only")
fi
if $has_config; then
  labels+=("⚙️ config-change")
fi
if $has_code; then
  labels+=("🚀 code-change")
fi

# If no specific category matched, fall back to a generic label
if [ ${#labels[@]} -eq 0 ]; then
  labels+=("🔧 miscellaneous-change")
fi

# Join labels with commas
joined=$(IFS=, ; echo "${labels[*]}")

# Export as GitHub Action output
echo "::set-output name=labels::$joined"
