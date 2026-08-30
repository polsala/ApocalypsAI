#!/usr/bin/env bash
set -euo pipefail

# Determine changed files
if [[ -n "${CHANGED_FILES:-}" ]]; then
  IFS=',' read -ra files <<< "$CHANGED_FILES"
else
  # Fallback to git diff (requires a checkout of the repo)
  if [[ -z "${GITHUB_SHA:-}" || -z "${GITHUB_BASE_SHA:-}" ]]; then
    echo "Error: GITHUB_SHA and GITHUB_BASE_SHA must be set when CHANGED_FILES is not provided." >&2
    exit 1
  fi
  mapfile -t files < <(git diff --name-only "$GITHUB_BASE_SHA" "$GITHUB_SHA")
fi

labels=()

for f in "${files[@]}"; do
  case "$f" in
    *.md)
      [[ " ${labels[*]} " != *" docs "* ]] && labels+=("docs")
      ;;
    *.js|*.ts|*.jsx|*.tsx)
      [[ " ${labels[*]} " != *" frontend "* ]] && labels+=("frontend")
      ;;
    *.py|*.go|*.rs)
      [[ " ${labels[*]} " != *" backend "* ]] && labels+=("backend")
      ;;
  esac
done

# Join labels with commas for the output
if [[ ${#labels[@]} -gt 0 ]]; then
  IFS=','; echo "${labels[*]}"
else
  echo ""
fi
