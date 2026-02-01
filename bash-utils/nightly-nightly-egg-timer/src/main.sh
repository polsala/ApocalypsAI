#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# nightly-egg-timer – convert duration strings to seconds
# ------------------------------------------------------------

show_egg=false
if [[ "${1:-}" == "--egg" ]]; then
  show_egg=true
  shift
fi

duration="${1:-}"
if [[ -z "$duration" ]]; then
  echo "Usage: $0 [--egg] <duration>"
  exit 1
fi

total=0
# Extract all <number><unit> pairs (h, m, s) and accumulate
while [[ $duration =~ ([0-9]+)([hms]) ]]; do
  value="${BASH_REMATCH[1]}"
  unit="${BASH_REMATCH[2]}"
  case $unit in
    h) ((total+=value*3600)) ;;
    m) ((total+=value*60))   ;;
    s) ((total+=value))      ;;
  esac
  # Remove the matched segment so the loop can find the next one
  duration="${duration/${BASH_REMATCH[0]}/}"
done

echo "$total"

if $show_egg; then
  cat <<'EOF'
   __
  /  \\
  \__/   *crack!*
EOF
fi
