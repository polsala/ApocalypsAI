#!/usr/bin/env bash

# nightly-git-branch-pruner
# Lists (and optionally deletes) local Git branches that are merged into the current branch
# and whose most recent commit is older than a configurable number of days.

set -euo pipefail

# Default configuration
DAYS=30
DELETE=false

print_usage() {
  cat <<'EOF'
Usage: branch_pruner.sh [--days N] [-d]
  --days N   Consider only branches whose last commit is older than N days (default 30).
  -d        Delete the branches that match the criteria after listing them.
EOF
}

# Argument parsing
while [[ $# -gt 0 ]]; do
  case "$1" in
    --days)
      if [[ -z "${2:-}" ]]; then
        echo "Error: --days requires a numeric argument" >&2
        exit 1
      fi
      DAYS="$2"
      shift 2
      ;;
    -d|--delete)
      DELETE=true
      shift
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      print_usage
      exit 1
      ;;
  esac
done

# Validate DAYS is a positive integer
if ! [[ "$DAYS" =~ ^[0-9]+$ ]]; then
  echo "Error: --days must be a positive integer" >&2
  exit 1
fi

# Determine cutoff epoch time
CURRENT_EPOCH=$(date +%s)
CUTOFF=$((CURRENT_EPOCH - DAYS * 86400))

# Get current branch name
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)
if [[ -z "$CURRENT_BRANCH" ]]; then
  echo "Error: Not inside a Git repository" >&2
  exit 1
fi

# Find merged branches excluding the current one
MERGED_BRANCHES=$(git branch --merged "$CURRENT_BRANCH" | grep -v "^\*" | sed 's/^ *//')

if [[ -z "$MERGED_BRANCHES" ]]; then
  echo "No merged branches found."
  exit 0
fi

STALE_BRANCHES=()

while IFS= read -r branch; do
  # Skip empty lines (shouldn't happen)
  [[ -z "$branch" ]] && continue
  # Get timestamp of the most recent commit on the branch
  LAST_COMMIT_EPOCH=$(git log -1 --format=%ct "$branch" 2>/dev/null || echo 0)
  if (( LAST_COMMIT_EPOCH < CUTOFF )); then
    STALE_BRANCHES+=("$branch")
  fi
done <<< "$MERGED_BRANCHES"

if [[ ${#STALE_BRANCHES[@]} -eq 0 ]]; then
  echo "No stale merged branches older than $DAYS days."
  exit 0
fi

echo "Stale merged branches (older than $DAYS days):"
for b in "${STALE_BRANCHES[@]}"; do
  echo "  $b"
  if $DELETE; then
    # Attempt safe deletion; ignore errors for already-deleted branches
    git branch -d "$b" || true
  fi
done

if $DELETE; then
  echo "Deleted ${#STALE_BRANCHES[@]} branch(es)."
fi
